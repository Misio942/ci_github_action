# ci_github_action

Pequeña app en Python para practicar CI/CD con GitHub Actions.

Es una calculadora mínima expuesta a través de una API en Flask, con pruebas
unitarias y de integración, linting y dos pipelines: **CI** (lint + pruebas) y
**CD** (construir y publicar una imagen Docker).

## Estructura del proyecto

```
.
├── app/
│   ├── calculator.py     # add / subtract / multiply / divide
│   └── main.py           # API Flask (/health, /calculate)
├── tests/
│   ├── test_calculator.py
│   └── test_api.py
├── .github/workflows/
│   ├── ci.yml            # se ejecuta en push y PR: flake8 + pytest (py 3.10–3.12)
│   └── cd.yml            # se ejecuta en main y tags: build + push de imagen Docker
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── pytest.ini
```

## Ejecutar en local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# ejecutar la app
python -m app.main          # http://localhost:5000/health

# lint + pruebas (igual que CI)
flake8 app tests
pytest
```

## Probar la API

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"op": "add", "a": 2, "b": 3}'
```

## Pipelines

- **CI** (`.github/workflows/ci.yml`): se dispara en cada push y pull request a
  `main`. Instala dependencias, ejecuta `flake8` y luego `pytest` en Python
  3.10, 3.11 y 3.12.
- **CD** (`.github/workflows/cd.yml`): se dispara en los push a `main` y en los
  tags `v*`. Construye la imagen Docker y la publica en GHCR
  (`ghcr.io/<owner>/<repo>`). Usa el `GITHUB_TOKEN` integrado, no necesita
  secretos adicionales.

## Ideas para practicar

1. Abre un PR con una prueba que falle y observa cómo CI bloquea el merge.
2. Agrega una operación `power` (con pruebas) y haz que CI pase.
3. Publica un tag como `v0.1.0` y revisa la imagen en la pestaña Packages.
