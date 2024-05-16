import smtplib
import os

# Email Settings
my_email = "jsapythontest828@gmail.com"
MY_PASSWORD = os.environ.get("MY_PASSWORD")
to_email = "pythonjsatest828@yahoo.com"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_deals):
        self.my_email = my_email
        self.my_password = MY_PASSWORD
        self.to_email = to_email
        self.flight_deals = flight_deals

    def send_email(self):
        for city in self.flight_deals:
            # print(city)
            # print(f"{city['city_to']}-{city['location_to']}")
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.my_password)
                connection.sendmail(from_addr=self.my_email,
                                    to_addrs=self.to_email,
                                    msg=f"Subject:Cheap flight from {city['location_from']} to {city['location_to']}"
                                        f"\n\nLow Price Alert! Only {city['flight_price']} to fly from {city['city_from']}-{city['location_from']}"
                                        f"to {city['city_to']}-{city['location_to']}"
                                    )
