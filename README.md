
# 📊 Simple Calculator Application

This project is a **web-based calculator application** built with:

- **Flask** for the backend API
- **HTML + CSS + JavaScript** frontend interface
- **Waitress** WSGI production server
- Tested with **unittest**, **pytest**, and **nose**

---

## 🚀 Features

✅ Web-based calculator UI (styled like a mobile calculator)  
✅ Supports addition `+`, subtraction `-`, multiplication `*`, division `/`, modulus `%`, parentheses `()`  
✅ Press `Close Calculator` button to shut down the server gracefully from the UI.

✅ Safe expression parsing with a regex filter, blocks dangerous Python code.

✅ Tested with:
- `pytest` in `pytest_calculator.py`
- `unittest` in `test_calculator.py`
- `nose` in `test_nose_calc.py`

---

## 📁 Project structure

```
.
├── main.py                 # Flask + Waitress server, Calculator logic
├── static/
│   └── index.html          # Calculator UI
├── test_calculator.py      # Unittest tests
├── pytest_calculator.py    # Pytest tests
├── test_nose_calc.py       # Nose tests
├── requirements.txt
├── README.md
```

---

## 🖥️ How to run

### 📦 Install dependencies
(Inside your Python virtual environment)

```bash
pip install -r requirements.txt
```

### 🏗️ Start the server

This will **run both unittest + pytest first**, and only start if they pass.

```bash
python main.py
```

- The server uses **Waitress** on `127.0.0.1:5000` in production mode.

---

## 🧑‍💻 The API

### `POST /calculate`

Accepts JSON payload:

```json
{
  "expression": "(2+3)*4"
}
```

Returns:

- `200 OK` with `{ "result": 20 }` if valid
- `400 Bad Request` if invalid (e.g. `2+*3`)
- Blocks unsafe operations like `__import__('os')`

### `POST /shutdown`

Gracefully shuts down the server (called by `Close Calculator` button).

---

## 🖱️ The UI (`static/index.html`)

- Styled with dark theme and circular buttons.
- Includes:
    - `AC` (clear)
    - Digits 0-9
    - `+`, `-`, `*`, `/`, `%`
    - `(` `)` for grouping
    - `=` to calculate
    - `Close Calculator` which stops the Flask server.

---

## ✅ Testing

### Pytest

```bash
pytest pytest_calculator.py
```

### Unittest

```bash
python test_calculator.py
```

### Nose

```bash
nose2 test_nose_calc
```

Each covers:

- `2+3` ➔ `5`
- `10-4` ➔ `6`
- `3*7` ➔ `21`
- `8/2` ➔ `4.0`
- `(2+3)*4` ➔ `20`
- Invalid expressions like `2+*3` return `400`
- Unsafe code like `__import__('os')` returns `400`

---

## ⚙️ Implementation highlights

### main.py

- `Calculator` class uses a **regex filter** to block unsafe code.

- Evaluates safely with:

```python
eval(expression, {"__builtins__": None}, {})
```

- `CalculatorAPI` serves:
  - `/` ➔ `index.html`
  - `/calculate` ➔ JSON API
  - `/shutdown` ➔ stops server

### static/index.html

- Makes `fetch('/calculate', ...)` to compute.
- Closes with `fetch('/shutdown', ...)` then tries `window.close()`.

---

## 🚀 To improve

✅ Run inside Docker  
 docker compose build --no-cache
[+] Building 51.5s (10/11)
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 413B                                                                                     0.0s
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 1.71kB                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                2.4s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 180B                                                                                  0.0s
 => [internal] load build context                                                                                 22.4s
 => => transferring context: 19.90MB                                                                              22.3s
 => [builder 1/4] FROM docker.io/library/python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a15ae  6.9s
 => => resolve docker.io/library/python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a15ae2fbd2e8f  0.0s
 => => sha256:0fe95cb712c4580a50adcc8e7f597abfcde47afc75c02bf8b116ab73b307fb8f 251B / 251B                         0.4s
 => => sha256:29fc64be73415f7dc67858b8564d51e731d96f3d9f5466a479aadd08f62fbaa2 12.58MB / 12.58MB                   3.1s
 => => sha256:e76888448fef0806c49e7438c5ea222b2883da9e1a3e7a8f8fe207f9eade79e3 3.51MB / 3.51MB                     2.3s
 => => sha256:3da95a905ed546f99c4564407923a681757d89651a388ec3f1f5e9bf5ed0b39d 28.23MB / 28.23MB                   4.7s
 => => extracting sha256:3da95a905ed546f99c4564407923a681757d89651a388ec3f1f5e9bf5ed0b39d                          0.6s
 => => extracting sha256:e76888448fef0806c49e7438c5ea222b2883da9e1a3e7a8f8fe207f9eade79e3                          0.3s
 => => extracting sha256:29fc64be73415f7dc67858b8564d51e731d96f3d9f5466a479aadd08f62fbaa2                          0.8s
 => => extracting sha256:0fe95cb712c4580a50adcc8e7f597abfcde47afc75c02bf8b116ab73b307fb8f                          0.0s
 => [builder 2/4] WORKDIR /app                                                                                     0.3s
 => [builder 3/4] COPY . .                                                                                         2.6s
 => [builder 4/4] RUN rm -rf dist build src/*.egg-info &&     python -m venv /opt/venv &&     /opt/venv/bin/pip   19.5s
 => [final 3/4] COPY --from=builder /app /app                                                                      0.4s
 => [final 4/4] RUN python -m venv /opt/venv &&     /opt/venv/bin/pip install --upgrade pip &&     /opt/venv/bin/  2.9s


docker compose up -d
[+] Running 2/2
 ✔ Network simple-calculator_default  Created                                                                      0.0s
 ✔ Container simple-calculator-app-1  Started                                                                      0.5s

### Report SAST scanning by using bandit
 docker build --target sast -t my-app-sast .
[+] Building 16.5s (10/10) FINISHED                                                                docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 1.71kB                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                1.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 180B                                                                                  0.0s
 => CACHED [sast 1/5] FROM docker.io/library/python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a  0.0s
 => => resolve docker.io/library/python:3.13-slim@sha256:6544e0e002b40ae0f59bc3618b07c1e48064c4faed3a15ae2fbd2e8f  0.0s
 => [internal] load build context                                                                                  0.3s
 => => transferring context: 351.41kB                                                                              0.3s
 => [sast 2/5] WORKDIR /scan                                                                                       0.0s
 => [sast 3/5] COPY . /scan                                                                                        0.6s
 => [sast 4/5] RUN python -m venv /opt/venv &&     /opt/venv/bin/pip install --upgrade pip &&     /opt/venv/bin/  10.7s
 => [sast 5/5] RUN /opt/venv/bin/bandit -r /scan -f json -o /scan/bandit-report.json --exit-zero &&     /opt/venv  0.7s
 => exporting to image                                                                                             3.6s
 => => exporting layers                                                                                            2.1s
 => => exporting manifest sha256:7c69bb944558bbd94f568dfb0c74996870c55a0d0acf53394f9e49d2eeb6c0e3                  0.0s
 => => exporting config sha256:fcc0bf1c68a160969344b70b02c69a912b9dac4e3a52f2723d72fcdbac902e47                    0.0s
 => => exporting attestation manifest sha256:e4c3048267a10b30472169720b7530e6fc5d0a7591c56729dc564b20435fe31a      0.0s
 => => exporting manifest list sha256:dcd8c6c5ccbeb77627edf9d58ef595bdc467cb892ff69b396c7821c497dc8dea             0.0s
 => => naming to docker.io/library/my-app-sast:latest                                                              0.0s
 => => unpacking to docker.io/library/my-app-sast:latest                                                           1.3s

docker run --rm my-app-sast
 docker run --rm my-app-sast
Run started:2025-07-14 20:03:16.031798

Test results:
>> Issue: [B404:blacklist] Consider possible security implications associated with the subprocess module.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_imports.html#b404-import-subprocess
   Location: /scan/src/simple_calculator/main.py:4:0
3       import re
4       import subprocess
5       import sys

--------------------------------------------------
>> Issue: [B307:blacklist] Use of possibly insecure function - consider using safer ast.literal_eval.
   Severity: Medium   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_calls.html#b307-eval
   Location: /scan/src/simple_calculator/main.py:21:21
20              try:
21                  result = eval(expression, {"__builtins__": None}, {})
22              except Exception as e:

---

## 📜 License

MIT License - free to use and modify.
