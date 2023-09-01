from send_the_raven.address import Address

def test_id_creation():
   """
   Test that when ID is not present, should be created correctly.
   """
   address = Address()
   assert address.id is not None

def test_no_id_creation():
   """
   Test that when ID is present, it should be preserved.
   """
   address = Address(id='testest')
   assert address.id == 'testest'

def test_generate_full_address():
    """
    Test that full address is generated correctly.
    """
    address = Address(id='testest')
    assert address.generate_full_address() == ''
    address = Address(street='12 main st', city='boston')
    assert address.generate_full_address() == '12 main st, boston'
    address = Address(street='12 main st', state='ma')
    assert address.generate_full_address() == '12 main st, ma'