import os
from datetime import datetime, timedelta
import requests

# Creating variable for tomorrow's date.
now = datetime.now()
delta_1_day = timedelta(days=1.0)
tomorrow = now + delta_1_day
date_tomorrow = tomorrow.strftime('%d/%m/%Y')
# print(date_tomorrow)

# Creating variable for date 6 months from now.
delta_180_days = timedelta(days=180.0)
days_180 = now + delta_180_days
date_180_days = days_180.strftime('%d/%m/%Y')
# print(date_180_days)

# Tequila credentials
tequila_username = "jsanagustin828"
tequila_api_key = os.environ.get("TEQUILA_API_KEY")
tequila_endpoint = "https://api.tequila.kiwi.com/v2/search"

# Tequila Headers
tequila_headers = {
    "apikey": tequila_api_key,
}


# Tequila Get Payload
# tequila_get_payload = {
#     'fly_from': fly_from,
#     'date_from': date_tomorrow,
#     'date_to': date_180_days,
#     'limit': 5,
# }

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = tequila_api_key
        self.username = tequila_username
        self.endpoint = tequila_endpoint
        self.header_dict = tequila_headers
        self.payload_dict = {}

    def get_search_itineraries(self, sheet_data):
        flight_deal_info = []
        for num in sheet_data:
            # print(f"We are iterating through: {num['iataCode']}")
            self.payload_dict = {
                'fly_from': 'LAX',
                'fly_to': num['iataCode'],
                'date_from': date_tomorrow,
                'date_to': date_180_days,
                'curr': 'USD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 28,
                'limit': 5,
            }
            response = requests.get(url=self.endpoint, params=self.payload_dict, headers=self.header_dict, verify=False)
            # print(f"The response code for searching itineraries is: {response.status_code}")
            data = response.json()

            # Checking if there was any valid data for the tequila get request. It might return no data.
            if len(data['data']) > 0:
                # print(f"All of the data printed: {data}")
                # print(f"This is the entire data from tequila: {data['data'][0]['flyFrom']}")

                # I'm pulling out the key values to get location from, to and flight price.
                location_from = data['data'][0]['flyFrom']
                # print(f"location from: {location_from}")
                location_to = data['data'][0]['flyTo']
                city_from = data['data'][0]['cityFrom']
                city_to = data['data'][0]['cityTo']
                flight_price = data['data'][0]['price']
                # print(f"The flight price from {location_from} to {location_to} is ${flight_price}.")

                # I'm adding the location to and flight price to a dictionary.
                flight_deal_dict = {
                    'location_from': location_from,
                    'location_to': location_to,
                    'city_from': city_from,
                    'city_to': city_to,
                    'flight_price': flight_price,
                }

                flight_deal_info.append(flight_deal_dict)
            else:
                print(f"No data for this iteration")

            # print(f"Here is the dictionary to compare for the new function: {flight_deal_info}")

            # This will just break, so we don't have sit through the for loop.
            # if response.status_code == 200:
            #     break
        return flight_deal_info

    def check_if_price_is_lower(self, prices_from_spreadsheet, prices_from_tequila):
        city_prices_to_email = [tequila_flight_info for tequila_flight_info, price_spreadsheet
                                in zip(prices_from_tequila, prices_from_spreadsheet)
                                if tequila_flight_info['flight_price'] < price_spreadsheet]
        # for tequila_flight_info in prices_from_tequila:
        #     for price_spreadsheet in prices_from_spreadsheet:
        #         if tequila_flight_info['flight_price'] < price_spreadsheet:
                    # print(f"Tequila founder a cheaper flight for {city} that costs ${tequila_flight_info}")
                    # city_prices_to_email[city] = tequila_flight_info
                    # break
        return city_prices_to_email

