from extractors.base import BaseExtractor
from utils.date_utils import format_entsoe_datetime
from utils.enums import LoadType


class LoadForecastExtractor(BaseExtractor):
    def extract(self, start, end, bidding_zone, load_type):
        if load_type == LoadType.FORECAST:
            process_type = "A01"
        elif load_type == LoadType.ACTUAL:
            process_type = "A16"
        else:
            raise ValueError("Invalid load type. Use FORECAST or ACTUAL.")

        params = {
            "securityToken": self.api_key,
            "documentType": "A65",
            "processType": process_type,
            "outBiddingZone_Domain": bidding_zone,
            "periodStart": format_entsoe_datetime(start),
            "periodEnd": format_entsoe_datetime(end),
        }

        return self.call_entsoe(params)
