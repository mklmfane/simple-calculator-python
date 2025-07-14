import unittest
from simple_calculator.main import app

class CalculatorTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_addition(self):
        response = self.client.post('/calculate', json={'expression': '2+3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 5)

    def test_subtraction(self):
        response = self.client.post('/calculate', json={'expression': '10-4'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 6)

    def test_multiplication(self):
        response = self.client.post('/calculate', json={'expression': '3*7'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 21)

    def test_division(self):
        response = self.client.post('/calculate', json={'expression': '8/2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 4.0)

    def test_parentheses(self):
        response = self.client.post('/calculate', json={'expression': '(2+3)*4'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 20)

    def test_invalid_expression(self):
        response = self.client.post('/calculate', json={'expression': '2+*3'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid expression', response.get_json()['error'])

    def test_unsafe_code(self):
        response = self.client.post('/calculate', json={'expression': '__import__("os").system("ls")'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid characters', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
