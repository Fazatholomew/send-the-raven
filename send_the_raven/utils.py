from random import getrandbits

def generate_id(extra_string=''):
    """
    Generate ID when not present.
    """
    return f"%010x{extra_string}" % getrandbits(60)
