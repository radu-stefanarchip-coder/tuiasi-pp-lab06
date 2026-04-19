# Lab 6 — Python POO — Identificator Tipuri Fișiere

Template GitHub Classroom pentru laboratorul 6 de Programare Python.

## Conținut

- **`lab6/file_analyzer.py`** — `FileType` enum + clase analyzer abstracte (stub de implementat)
- **`lab6/directory_scanner.py`** — `DirectoryScanner` care parcurge directoare (stub)
- **`lab6/main.py`** — Entry point CLI
- **`tests/test_lab6.py`** — Suite de teste (nu modifica)

## Cum se rulează

```bash
# Rulare teste
uv run pytest

# Rulare cu output detaliat
uv run pytest -v

# Rulare pe un director
uv run python -m lab6.main /calea/catre/director
```

## Cum se instalează dependențele

```bash
uv sync
```

## Cerințe

- Python >= 3.11
- uv (package manager)
