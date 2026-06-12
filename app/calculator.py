"""Módulo de calculadora pequeña para practicar CI/CD."""


def sumar(a: float, b: float) -> float:
    """Devuelve la suma de dos números."""
    return a + b


def restar(a: float, b: float) -> float:
    """Devuelve la resta de dos números."""
    return a - b


def multiplicar(a: float, b: float) -> float:
    """Devuelve el producto de dos números."""
    return a * b


def dividir(a: float, b: float) -> float:
    """Devuelve el cociente de dos números.

    Lanza:
        ZeroDivisionError: si b es 0.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero")
    return a / b
