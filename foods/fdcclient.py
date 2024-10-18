import requests
import os


class FdcClient:
    base_url = "https://api.nal.usda.gov/fdc/v1"

    def __init__(self, apikey):
        self.key = apikey

    def get_food(self, fdc_ids: list[int], format: str = "abridged", nutrients: list[str] = None):
        if nutrients == None:
            params = {"fdcIds": fdc_ids, "format": format, "api_key": self.key}
        else:
            params = {
                "fdcIds": fdc_ids,
                "format": format,
                "nutrients": nutrients,
                "api_key": self.key,
            }

        try:
            response = requests.get(f"{self.base_url}/foods", params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        return response


def get_fdc_client():
    return FdcClient(apikey=os.environ.get("FDC_API_KEY"))
