from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Create object for Google Spreadsheet
sheety = DataManager()

# Requests all the data in our spreadsheet.
sheety_data = sheety.get_request()['prices']

# Call function to return list of prices in spreadsheet
spreadsheet_prices = sheety.get_list_of_spreadsheet_prices()

# Create object for Tequila API.
flight_search = FlightSearch()

# Call function to return Tequila prices it found for today.
tequila_flight_info = flight_search.get_search_itineraries(sheety_data)
# print(tequila_flight_info)

# Call function to print out if it found a cheaper flight.
cities_with_low_fare = flight_search.check_if_price_is_lower(prices_from_tequila=tequila_flight_info, prices_from_spreadsheet=spreadsheet_prices)
print(cities_with_low_fare)

# Create object for Notification Manager.
notification_manager = NotificationManager(cities_with_low_fare)

# Sending email for each deal.
notification_manager.send_email()