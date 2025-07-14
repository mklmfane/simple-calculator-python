from flask import Flask, request, jsonify
from http import HTTPStatus
import re
import subprocess
import sys

app = Flask(__name__, static_folder="static")

class Calculator:
    SAFE_PATTERN = re.compile(r"[0-9+\-*/().% ]+")

    @classmethod
    def evaluate(cls, expression: str):
        if not expression:
            return {"error": "Missing expression"}, HTTPStatus.BAD_REQUEST

        if not cls.SAFE_PATTERN.fullmatch(expression):
            return {"error": "Invalid characters in expression"}, HTTPStatus.BAD_REQUEST

        try:
            result = eval(expression, {"__builtins__": None}, {})
        except Exception as e:
            return {"error": f"Invalid expression: {str(e)}"}, HTTPStatus.BAD_REQUEST

        return {"result": result}, HTTPStatus.OK


class CalculatorAPI:
    @staticmethod
    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    @staticmethod
    @app.route('/calculate', methods=['POST'])
    def calculate():
        data = request.get_json(silent=True)
        if not data:
            return jsonify(error="Missing JSON payload"), HTTPStatus.BAD_REQUEST

        expression = data.get("expression")
        response, status = Calculator.evaluate(expression)
        return jsonify(response), status

    @staticmethod
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            return jsonify(error="Not running with the Werkzeug Server"), HTTPStatus.INTERNAL_SERVER_ERROR
        shutdown_func()
        return jsonify(message="Calculator server has been shut down. You can close this tab."), HTTPStatus.OK


if __name__ == '__main__':
    print("🔍 Running unittest tests in test_calculator.py...")
    result_unittest = subprocess.run([sys.executable, "test_calculator.py"])
    if result_unittest.returncode != 0:
        print("❌ Unittest tests failed. Fix the issues before running the server.")
        sys.exit(1)

    print("✅ Unittest tests passed.")

    print("🔍 Running pytest tests in pytest_calculator.py...")
    result_pytest = subprocess.run([sys.executable, "-m", "pytest", "pytest_calculator.py"])
    if result_pytest.returncode != 0:
        print("❌ Pytest tests failed. Fix the issues before running the server.")
        sys.exit(1)

    print("✅ All pytest tests passed. Starting production server ...")