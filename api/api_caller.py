from utils.cacher import Cacher
import xml.etree.ElementTree as ET
import requests
from functools import wraps
import os
from dotenv import load_dotenv

from utils.date_utils import format_entsoe_datetime  # make sure this exists


class Caller:
    def __init__(self):
        load_dotenv()
        self.url = "https://web-api.tp.entsoe.eu/api"
        self.api_key = os.getenv("API_KEY")
        self.cacher = Cacher()

        self.defaults = {
            "bidding_zone": "10YNL----------L",
            "target_date": "2025-07-07"
        }

    @staticmethod
    def entsoe_api_call(api_method):
        @wraps(api_method)
        def wrapper(self, *args, **kwargs):
            params = api_method(self, *args, **kwargs)
            if self.cacher.does_cache_exist(params):
                print("✓ Loaded from cache")
                return self.cacher.load_from_cache(params)

            print("Fetching from ENTSO-E API...")
            try:
                response = requests.get(self.url, params=params)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                self.cacher.save_to_cache(params, root)
                print(f"✓ Retrieved and cached data for {params.get('periodStart', 'unknown')}")
                return root
            except requests.HTTPError as e:
                print(f"⚠️  HTTP error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

        return wrapper

    @entsoe_api_call
    def get_load(self, load_type, start, end, bidding_zone=None):
        # equivalent to https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=03.07.2025+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)
        if bidding_zone is None:
            bidding_zone = self.defaults["bidding_zone"]

        if load_type == "forecast":
            process_type = 'A01'
        elif load_type == "actual":
            process_type = 'A16'
        else:
            raise Exception("Not correct type of load")

        return {
            'securityToken': self.api_key,
            'documentType': 'A65',
            'processType': process_type,
            'outBiddingZone_Domain': bidding_zone,
            'periodStart': format_entsoe_datetime(start),
            'periodEnd': format_entsoe_datetime(end),
        }
