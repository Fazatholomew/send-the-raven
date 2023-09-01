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