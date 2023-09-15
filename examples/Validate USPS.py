from send_the_raven.validator import Validator

addresses = [
    {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip": "12345"},
    {"street": "456 Oak Rd", "city": "Forest", "state": "VT", "zip": "67890"},
]
validator = Validator(addresses, usps_id="MY_ID")
valid_addresses = validator()
for addr in valid_addresses:
    print(addr.street, addr.city, addr.state, addr.zip_code)
