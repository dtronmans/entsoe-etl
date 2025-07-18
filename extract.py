from zoneinfo import ZoneInfo

import requests
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
import os
import pickle

def format_entsoe_datetime(dt):
    return dt.strftime('%Y%m%d%H%M')


def extract_actual_load(api_key, bidding_zone='10YFR-RTE------C', target_date=None, cache_file="cached_actual_load.pkl"):
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            print("Loading from cache...")
            return pickle.load(f)

    print("Fetching from ENTSO-E API...")
    url = "https://web-api.tp.entsoe.eu/api"
    data_per_day = []

    if target_date is None:
        start_date = datetime.utcnow().date() - timedelta(days=2)
    else:
        start_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    for i in range(5):
        date = start_date - timedelta(days=i)
        local_tz = ZoneInfo("Europe/Paris")  # or make this dynamic based on bidding zone

        local_start = datetime.combine(date, datetime.min.time(), tzinfo=local_tz)
        local_end = local_start + timedelta(days=1)

        start = local_start.astimezone(timezone.utc)
        end = local_end.astimezone(timezone.utc)

        params = {
            'securityToken': api_key,
            'documentType': 'A65',
            'processType': 'A16',
            'outBiddingZone_Domain': bidding_zone,
            'periodStart': format_entsoe_datetime(start),
            'periodEnd': format_entsoe_datetime(end),
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            data_per_day.append((date, root))
            print(f"✓ Retrieved data for {date}")
        except requests.HTTPError as e:
            print(f"⚠️  Skipping {date}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error on {date}: {e}")

    if data_per_day:
        with open(cache_file, "wb") as f:
            pickle.dump(data_per_day, f)
        print(f"✅ Saved {len(data_per_day)} days to cache.")
    else:
        print("❗ No data fetched. Check API key or parameters.")

    return data_per_day