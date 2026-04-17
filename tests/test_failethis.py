def test_failThisTest():
    assert "Sun" == "sun"

def add_ints(a, b):
    return a+b

def mul_ints(a, b):
    return a*b

def performOperation(operation, val1, val2):
    if operation == 'add':
        return add_ints(val1, val2)
    elif operation == 'mul':
        return mul_ints(val1, val2)

def test_add():
    assert performOperation('add', 10, 11) == 21    

def test_mul():
    assert performOperation('mul', 10, 11) == 110

