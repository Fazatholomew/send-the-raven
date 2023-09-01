from send_the_raven.utils import generate_id
def test_generate_id():
  assert len(generate_id()) == 15
  assert generate_id() != generate_id()
  assert generate_id('sdfsdf') != generate_id()
  assert generate_id('sdfsdf') != generate_id('sdfsdf')
