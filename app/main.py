"""API mínima en Flask que expone la calculadora, para practicar CI/CD."""
from flask import Flask, jsonify, request

from app.calculator import dividir, multiplicar, restar, sumar

app = Flask(__name__)

OPERATIONS = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
}


@app.get("/health")
def health():
    """(liveness probe)."""
    return jsonify(status="ok"), 200


@app.post("/calculate")
def calculate():
    """Ejecuta una operación sobre dos números.

    Espera JSON: {"op": "sumar", "a": 1, "b": 2}
    """
    data = request.get_json(silent=True) or {}
    op = data.get("op")
    if op not in OPERATIONS:
        return jsonify(error=f"operación desconocida '{op}'"), 400

    try:
        a = float(data["a"])
        b = float(data["b"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="'a' y 'b' deben ser números"), 400

    try:
        result = OPERATIONS[op](a, b)
    except ZeroDivisionError as exc:
        return jsonify(error=str(exc)), 400

    return jsonify(op=op, a=a, b=b, result=result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
