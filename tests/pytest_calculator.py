import pytest
from simple_calculator.main import app

@pytest.fixture
def client():
    return app.test_client()

def test_addition(client):
    response = client.post('/calculate', json={'expression': '2+3'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 5

def test_subtraction(client):
    response = client.post('/calculate', json={'expression': '10-4'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 6

def test_multiplication(client):
    response = client.post('/calculate', json={'expression': '3*7'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 21

def test_division(client):
    response = client.post('/calculate', json={'expression': '8/2'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 4.0

def test_parentheses(client):
    response = client.post('/calculate', json={'expression': '(2+3)*4'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 20

def test_invalid_expression(client):
    response = client.post('/calculate', json={'expression': '2+*3'})
    assert response.status_code == 400
    assert 'Invalid expression' in response.get_json()['error']

def test_unsafe_code(client):
    response = client.post('/calculate', json={'expression': '__import__("os").system("ls")'})
    assert response.status_code == 400
    assert 'Invalid characters' in response.get_json()['error']
