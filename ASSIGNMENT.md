# Lab 6 — Python POO — Identificator Tipuri Fișiere

## Descriere

Implementează un sistem orientat pe obiecte care parcurge recursiv un director și clasifică fișierele după **conținut** (nu după extensie), folosind analiza statistică a octeților.

## Structura proiectului

```
lab06/
  lab6/
    __init__.py
    file_analyzer.py     ← enum FileType + clase analyzer (stub)
    directory_scanner.py ← clasa DirectoryScanner (stub)
    main.py              ← entry point CLI
  tests/
    __init__.py
    test_lab6.py         ← teste complete
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

## Cerințe

### 1. `file_analyzer.py`

#### `FileType` (Enum)

```python
class FileType(Enum):
    ASCII = auto()
    UNICODE = auto()
    BINARY = auto()
    BMP = auto()
    UNKNOWN = auto()
```

#### `FileAnalyzer` (clasă abstractă)

```python
class FileAnalyzer(ABC):
    @abstractmethod
    def analyze(self, content: bytes) -> FileType: ...
```

#### `AsciiAnalyzer(FileAnalyzer)`

Detectează fișiere text ASCII/UTF-8:
- Octeții din setul `{9, 10, 13} ∪ {32..127}` reprezintă ≥85% din conținut
- Octeții "control" (`{0-8, 11, 12, 14-31}`) și `{128-255}` reprezintă ≤15%

```python
analyzer = AsciiAnalyzer()
assert analyzer.analyze(b"Hello World\n") == FileType.ASCII
```

#### `UnicodeAnalyzer(FileAnalyzer)`

Detectează fișiere UTF-16:
- Octetul `0x00` apare în ≥30% din conținut

```python
analyzer = UnicodeAnalyzer()
content = "Hello".encode("utf-16-le")  # fiecare char are octet nul
assert analyzer.analyze(content) == FileType.UNICODE
```

#### `BinaryAnalyzer(FileAnalyzer)`

Detectează fișiere binare:
- Nu este ASCII și nu este UNICODE
- Distribuție relativ uniformă a octeților

#### `BmpAnalyzer(FileAnalyzer)`

Detectează și parsează fișiere BMP:
- Magic bytes: primii 2 octeți = `0x42 0x4D` (ASCII: `BM`)

```python
analyzer = BmpAnalyzer()
assert analyzer.analyze(content) == FileType.BMP

info = analyzer.get_bmp_info(content)
# info = {'width': 100, 'height': 200, 'bits_per_pixel': 24}
```

**Structura header BMP:**

| Offset | Dimensiune | Descriere |
|--------|-----------|-----------|
| 0-1 | 2 bytes | Semnătură `BM` |
| 2-5 | 4 bytes | Dimensiunea fișierului (uint32 LE) |
| 6-9 | 4 bytes | Rezervat |
| 10-13 | 4 bytes | Offset date pixel (uint32 LE) |
| 14-17 | 4 bytes | Dimensiune DIB header = 40 (uint32 LE) |
| 18-21 | 4 bytes | Lățime în pixeli (int32 LE) |
| 22-25 | 4 bytes | Înălțime în pixeli (int32 LE) |
| 26-27 | 2 bytes | Planuri culoare = 1 (uint16 LE) |
| 28-29 | 2 bytes | Biți per pixel (uint16 LE) |

### 2. `directory_scanner.py`

#### `DirectoryScanner`

```python
scanner = DirectoryScanner()
rezultate = scanner.scan("/calea/catre/director")
# {
#     FileType.ASCII: ["/path/file.txt"],
#     FileType.BMP: ["/path/image.bmp"],
#     FileType.BINARY: ["/path/data.bin"],
#     FileType.UNICODE: [],
#     FileType.UNKNOWN: [],
# }
```

**Cerințe:**
- Parcurge recursiv directorul (inclusiv subdirectoare)
- Returnează căi **absolute**
- Sare peste directoare și fișiere inaccesibile (tratează excepțiile)
- Ordinea analizoarelor: BMP > ASCII > UNICODE > BINARY (BMP trebuie verificat primul)

### 3. `main.py` — Entry point CLI

```bash
uv run python -m lab6.main /calea/directorului
```

Afișează fișierele grupate pe tipuri, cu numărul de fișiere din fiecare categorie.

## Exemple de utilizare

### Rulare pe un director:
```bash
uv run python -m lab6.main /home/user/documente
```

**Output:**
```
Rezultate pentru directorul: /home/user/documente

=== ASCII (3 fișiere) ===
  /home/user/documente/readme.txt
  /home/user/documente/config.xml
  /home/user/documente/notes.csv

=== BMP (1 fișiere) ===
  /home/user/documente/imagine.bmp
```

### Testare manuală:
```python
from lab6.file_analyzer import AsciiAnalyzer, BmpAnalyzer, FileType

# ASCII
a = AsciiAnalyzer()
print(a.analyze(b"Hello\n"))  # FileType.ASCII

# BMP
b = BmpAnalyzer()
with open("imagine.bmp", "rb") as f:
    content = f.read()
print(b.analyze(content))           # FileType.BMP
print(b.get_bmp_info(content))      # {'width': 800, 'height': 600, 'bits_per_pixel': 24}
```

## Tabel evaluare

| Cerință | Punctaj |
|---------|---------|
| `AsciiAnalyzer.analyze()` corect | 15p |
| `UnicodeAnalyzer.analyze()` corect | 15p |
| `BmpAnalyzer.analyze()` — magic bytes | 10p |
| `BmpAnalyzer.get_bmp_info()` — width/height/bpp | 20p |
| `BinaryAnalyzer.analyze()` corect | 10p |
| `DirectoryScanner.scan()` — clasificare corectă | 20p |
| `DirectoryScanner.scan()` — recursivitate | 10p |
| **Total** | **100p** |

## Resurse

- [struct — Python docs](https://docs.python.org/3/library/struct.html)
- [abc — Python docs](https://docs.python.org/3/library/abc.html)
- [pathlib — Python docs](https://docs.python.org/3/library/pathlib.html)
- [Specificație format BMP](https://en.wikipedia.org/wiki/BMP_file_format)
