# FSDA Multi-Language Gateway — Architecture A (Embedded)

Access the MATLAB **FSDA** toolbox from **Python, R, and Julia** — without MCR, without a server, and without writing a wrapper for every function.

R and Julia connect through an **embedded Python interpreter** (`reticulate` / `PyCall`), which talks to a **shared MATLAB Engine session**. One generic MATLAB dispatcher (`FSDAEngine.m`) handles every FSDA function by name, so adding a new function requires zero new code.

```
R (reticulate)   ┐
Julia (PyCall)    ├──► Embedded Python ──► fsda_gateway.py ──► Shared MATLAB Engine ──► FSDAEngine.m
Python (direct)  ┘                                              ('FSDA_Shared')
```

## Prerequisites

- MATLAB, with the **FSDA toolbox** installed via Add-On Manager
- Python 3.12
- R, with `reticulate`, `httr`, `jsonlite`
- Julia, with `PyCall`

## Folder Structure

```
fsda-multilang/
├── venv/                                  (created by setup, not committed)
├── src/
│   └── gateways/
│       ├── fsda_gateway.py                Python gateway class (FSDA)
│       └── matlab_engine/
│           └── FSDAEngine.m               Generic MATLAB dispatcher
├── tests/
│   └── test_python.py                     Direct Python test
├── embedded/
│   ├── r/
│   │   └── fsda_embedded.R                R test (via reticulate)
│   └── julia/
│       └── fsda_embedded.jl               Julia test (via PyCall)
└── start_shared_engine.m                  Shares the MATLAB session
```

> **Rule of thumb: every command below is run from the project root** (`fsda-multilang/`), never from a subfolder. All paths in the code are root-relative — running from elsewhere will fail to resolve them.

## Setup

### 1. Check your MATLAB version

In the MATLAB Command Window:

```matlab
version
```

Note the release (e.g. `R2025b`). You'll need the matching short version number below (R2025b → `25.2`, R2026a → `26.1`, etc.).

### 2. Create the Python virtual environment

From the project root:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python dependencies — version-matched to MATLAB

```cmd
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install matlabengine==25.2.* numpy pandas
```

Replace `25.2` with your own MATLAB's short version number from Step 1. Installing `matlabengine` without pinning the version will often pull a release that doesn't match your MATLAB installation and fails to build.

Confirm:

```cmd
venv\Scripts\python.exe -c "import matlab.engine; import numpy; import pandas; print('ALL OK')"
```

### 4. Install R packages

In an R console:

```r
install.packages(c("reticulate", "httr", "jsonlite"))
```

### 5. Install Julia packages

Open a Julia REPL **from the project root** (or `cd` to it first), then:

```julia
using Pkg
ENV["PYTHON"] = joinpath(pwd(), "venv", "Scripts", "python.exe")
Pkg.build("PyCall")
```

### 6. Share the MATLAB engine session

In MATLAB, from the project root:

```matlab
run('start_shared_engine.m')
```

Confirm it worked:

```matlab
matlab.engine.isEngineShared
```

This should return `1`. **Keep this MATLAB window open** — R and Julia both connect to this same running session, not a new one.

## Usage

With the MATLAB window still open and the engine shared, run each of these **from the project root**:

```cmd
python tests\test_python.py
Rscript embedded\r\fsda_embedded.R
julia embedded\julia\fsda_embedded.jl
```

Each should print the same result for the `zscoreFS` test:

```
[[-0.674, -0.674, -0.674], [0.0, 0.0, 0.0], [0.674, 0.674, 0.674]]
```

## How It Works

- **`FSDAEngine.m`** — a MATLAB handle class with one method, `execute(funcName, varargin)`. It uses `str2func` to resolve any FSDA function by name and forwards all arguments — no per-function code needed.
- **`fsda_gateway.py`** — a Python class (`FSDA`) that connects to MATLAB (either a new session or the shared one) and calls `execute()` via `feval`. This is the single gateway every language ultimately goes through.
- **R and Julia** don't reimplement any MATLAB logic. `reticulate` and `PyCall` simply embed a Python interpreter inside the R / Julia process and import `fsda_gateway.py` directly.
- **The shared engine** (`matlab.engine.shareEngine('FSDA_Shared')`) ensures only one MATLAB session exists no matter how many languages connect — avoiding wasted license seats and inconsistent state.

## Troubleshooting

| Problem | Fix |
|---|---|
| `matlabengine` build fails with a version mismatch error | Re-check `version` in MATLAB and install the exact matching `matlabengine==<version>.*` |
| `NameError: name '__file__' is not defined` (from R/Julia) | Already handled in `fsda_gateway.py` via `os.getcwd()` — make sure you're running from the project root |
| `matlab.engine.EngineError: MATLAB session 'FSDA_Shared' cannot be found` | Run `start_shared_engine.m` again in MATLAB and keep that window open |
| `numpy [NOT FOUND]` when running R's `py_config()` | Packages were installed into a different Python than the one `reticulate`/`PyCall` is pointed at — reinstall using the venv's `python.exe` directly |
| `PyCall not properly installed` | Set `ENV["PYTHON"]` to the venv's `python.exe` **before** `Pkg.build("PyCall")`, then rebuild |
