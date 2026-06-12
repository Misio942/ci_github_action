# ci_github_action

App en Python para CI/CD con GitHub Actions.

Es una calculadora mínima expuesta a través de una API en Flask, con pruebas
unitarias y de integración, linting y un pipeline único (`ci-cd.yml`) que separa
las fases de **CI** (lint + pruebas) y **CD** (construir y publicar la imagen
Docker en GHCR), con entornos distintos para QA y producción.

## Estructura del proyecto

```
.
├── app/
│   ├── calculator.py        # sumar / restar / multiplicar / dividir
│   └── main.py              # API Flask (/health, /calculate)
├── tests/
│   ├── test_calculator.py
│   └── test_api.py
├── .github/workflows/
│   └── ci-cd.yml            # pipeline único: jobs ci, cd-qa y cd-prod
├── Dockerfile
├── requirements.txt         # dependencias de runtime (producción)
├── requirements-dev.txt     # runtime + test/lint (incluye al anterior con -r)
└── pytest.ini
```

## Arquitectura del pipeline

El workflow `ci-cd.yml` se dispara con `push` a `main`, `pull_request` a `main`
y tags `v*`. Está compuesto por tres jobs: uno de integración (`ci`) y dos de
entrega (`cd-qa` y `cd-prod`) que dependen del primero y se seleccionan según el
tipo de tag.

### Jobs

| Job       | Cuándo corre                                  | Qué hace |
|-----------|-----------------------------------------------|----------|
| `ci`      | Siempre (push, PR y tags)                     | Instala dependencias, corre `flake8` y `pytest` sobre una matriz de Python. Actúa como gate: si falla, no se construye nada. |
| `cd-qa`   | Solo en tags `v*` que contienen `-rc`         | Construye la imagen y la publica en GHCR con el tag del release candidate más el tag móvil `qa`. **No** mueve `latest`. |
| `cd-prod` | Solo en tags `v*` que **no** contienen `-rc`  | Construye la imagen y la publica en GHCR con el tag de versión y mueve `latest`. |

### Decisiones de diseño

- **`needs: ci`** en ambos jobs de CD: ninguna imagen se publica si las pruebas
  o el lint fallan.
- **Separación QA / Prod por convención de tags**: un tag `-rc` va a QA, un tag
  limpio va a producción. Así se practica un flujo de promoción real
  (`v1.2.0-rc1` → validar → `v1.2.0`).
- **`latest` solo lo controla producción** (`flavor: latest=true` en `cd-prod`,
  `latest=false` en `cd-qa`) para que `latest` nunca apunte a un candidato.
- **Autenticación con `GITHUB_TOKEN`**: usa el token integrado y el permiso
  `packages: write`, sin necesidad de secretos adicionales.

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
  -d '{"op": "sumar", "a": 2, "b": 3}'
```
