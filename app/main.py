"""Minimal Flask API exposing the calculator, used to practice CI/CD."""
from flask import Flask, jsonify, request

from app.calculator import add, divide, multiply, subtract

app = Flask(__name__)

OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


@app.get("/health")
def health():
    """Liveness probe."""
    return jsonify(status="ok"), 200


@app.post("/calculate")
def calculate():
    """Run an operation on two numbers.

    Expects JSON: {"op": "add", "a": 1, "b": 2}
    """
    data = request.get_json(silent=True) or {}
    op = data.get("op")
    if op not in OPERATIONS:
        return jsonify(error=f"unknown op '{op}'"), 400

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="'a' and 'b' must be numbers"), 400

    try:
        result = OPERATIONS[op](a, b)
    except ZeroDivisionError as exc:
        return jsonify(error=str(exc)), 400

    return jsonify(op=op, a=a, b=b, result=result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
