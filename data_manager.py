import requests
from flight_search import FlightSearch
import os

tequila = FlightSearch()

TOKEN = os.environ.get("TOKEN")

sheety_headers = {
    "Authorization": f"Bearer {TOKEN}"
}

sheety_post_json_payload = {
    "price": {
        "city": "Los Angeles",
        "iataCode": "LAX",
        "lowestPrice": "100"
    },
}

sheety_endpoint = "https://api.sheety.co/4e3f4a222c8a662c8f843f40f235733e/flightDealsPythonDay39/prices"
sheety_endpoint_put = "https://api.sheety.co/4e3f4a222c8a662c8f843f40f235733e/flightDealsPythonDay39/prices/10"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.token = TOKEN
        self.headers = sheety_headers
        self.payload = sheety_post_json_payload
        self.endpoint = sheety_endpoint
        self.endpoint_put = sheety_endpoint_put

    def post_request(self):
        response = requests.post(url=self.endpoint, json=self.payload, headers=self.headers, verify=False)
        print(response.status_code)
        print(response.text)

    def get_request(self):
        response = requests.get(url=self.endpoint, headers=self.headers, verify=False)
        data = response.json()
        return data

    def get_list_of_spreadsheet_prices(self):
        response = requests.get(url=self.endpoint, headers=self.headers, verify=False)
        data = response.json()['prices']
        list_of_prices_in_spreadsheet = []
        for row in data:
            list_of_prices_in_spreadsheet.append(row['lowestPrice'])
        return list_of_prices_in_spreadsheet

