from send_the_raven.utils import generate_id, split_into_n_elements, clean_string


def test_generate_id():
    assert len(generate_id()) == 15
    assert generate_id() != generate_id()
    assert generate_id("sdfsdf") != generate_id()
    assert generate_id("sdfsdf") != generate_id("sdfsdf")

def test_split_into_n_elements():
    assert len(split_into_n_elements([1,2,3,4,5,6,7], 2)) == 4
    assert len(split_into_n_elements([1,2,3,4,5,6,7], 2)[0]) == 2
    assert len(split_into_n_elements([1,2,3,4,5,6,7], 2)[-1]) == 1
    assert len(split_into_n_elements([], 2)) == 0

def test_clean_string():
    assert '12 main st' == clean_string('12      main st      ')
    assert '1 2 main st' == clean_string('1  2   main   st   ')
    assert '12' == clean_string(12)