from send_the_raven.address import Address, Addresses, compare

# Create Address instance manually
addr1 = Address(street="12 Main St", city="Boston", state="MA")
addr2 = Address(street="12 Main Street", city="Boston", state="massachusetts")
assert addr1 == addr2

# Smartly filling Zip Code to import USPS Validation
print(f"Zipcode: {addr1.zip_code}")
addr1.fill_in_zipcode()
print(f"Zipcode: {addr1.zip_code}")

addr2.fill_in_state()
assert addr2.state == "MA"

# Extract address from 1 string
many_address = Addresses(
    [
        {"full_address": "12 park st, lawrence"},
        {"full_address": "12 park street, lawrence"},
    ]
)

many_address.normalize()

print(compare(many_address[0], many_address[1]))
