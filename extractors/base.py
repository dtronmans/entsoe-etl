import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from utils.cacher import Cacher


class BaseExtractor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.url = "https://web-api.tp.entsoe.eu/api"
        self.cacher = Cacher()

    def call_entsoe(self, params):
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
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
