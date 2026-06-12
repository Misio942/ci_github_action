"""Pruebas unitarias del módulo de la calculadora."""
import pytest

from app.calculator import dividir, multiplicar, restar, sumar


def test_sumar():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0


def test_restar():
    assert restar(5, 3) == 2
    assert restar(0, 4) == -4


def test_multiplicar():
    assert multiplicar(4, 3) == 12
    assert multiplicar(-2, 3) == -6


def test_dividir():
    assert dividir(10, 2) == 5
    assert dividir(9, 3) == 3


def test_dividir_entre_cero():
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)
