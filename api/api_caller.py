import requests
from dotenv import load_dotenv
import os

import xml.etree.ElementTree as ET

from utils.date_utils import format_entsoe_datetime


class Caller:

    def __init__(self):
        load_dotenv()
        self.url = "https://web-api.tp.entsoe.eu/api"
        self.api_key = os.getenv("API_KEY")

        self.defaults = {
            # equivalent to https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=03.07.2025+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)
            "bidding_zone": "10YNL----------L",
            "target_date": "2025-07-07"
        }

    def get_actual_load(self, start, end, bidding_zone=None):
        if bidding_zone is None:
            bidding_zone = self.defaults["bidding_zone"]
        params = {
            'securityToken': self.api_key,
            'documentType': 'A65',
            'processType': 'A16',
            'outBiddingZone_Domain': bidding_zone,
            'periodStart': format_entsoe_datetime(start),
            'periodEnd': format_entsoe_datetime(end),
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            print(f"✓ Retrieved data for {start}")
            return root
        except requests.HTTPError as e:
            print(f"⚠️  Skipping {start}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error on {start}: {e}")

