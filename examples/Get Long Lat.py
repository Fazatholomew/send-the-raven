from send_the_raven.geoaddress import Geocoder

addresses = [
    {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip": "12345"},
    {"street": "456 Oak Rd", "city": "Forest", "state": "VT", "zip": "67890"},
]
geocoder = Geocoder(addresses)
geocoder("nominatim", {"user_agent": "my_app"})

for address in geocoder.addresses:
    print(address.latitude, address.longitude)
