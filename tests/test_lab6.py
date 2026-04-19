"""
Teste pentru Lab 6 — Identificator tipuri fișiere prin POO.

Testele acoperă:
- Fiecare analyzer cu bytes hardcoded
- DirectoryScanner cu fișiere temporare (pytest tmp_path)
"""

import struct
import pytest

from lab6.file_analyzer import (
    FileType,
    AsciiAnalyzer,
    UnicodeAnalyzer,
    BinaryAnalyzer,
    BmpAnalyzer,
)
from lab6.directory_scanner import DirectoryScanner


class TestFileAnalyzers:
    """Teste pentru analizatorii individuali."""

    # ── AsciiAnalyzer ──────────────────────────────────────────────────────────

    def test_ascii_text_simplu(self) -> None:
        """Text ASCII pur este recunoscut corect."""
        analyzer = AsciiAnalyzer()
        content = b"Hello World\n"
        assert analyzer.analyze(content) == FileType.ASCII

    def test_ascii_text_mai_lung(self) -> None:
        """Text ASCII mai lung este recunoscut corect."""
        analyzer = AsciiAnalyzer()
        content = b"Acesta este un text simplu.\nCu mai multe linii.\nSi punctuatie!"
        assert analyzer.analyze(content) == FileType.ASCII

    def test_ascii_nu_detecteaza_binar(self) -> None:
        """Datele binare NU sunt detectate ca ASCII."""
        analyzer = AsciiAnalyzer()
        # Bytes distribuiți uniform pe 0..255 nu sunt ASCII
        content = bytes(range(256)) * 10
        assert analyzer.analyze(content) != FileType.ASCII

    # ── UnicodeAnalyzer ────────────────────────────────────────────────────────

    def test_unicode_cu_multi_zerouri(self) -> None:
        """Conținut cu ≥30% octeți zero este detectat ca UNICODE."""
        analyzer = UnicodeAnalyzer()
        # UTF-16 little-endian: 'AB' = 0x41 0x00 0x42 0x00 → 50% zerouri
        content = "AB".encode("utf-16-le")
        assert analyzer.analyze(content) == FileType.UNICODE

    def test_unicode_text_utf16(self) -> None:
        """Text UTF-16 real este detectat ca UNICODE."""
        analyzer = UnicodeAnalyzer()
        # Caractere ASCII în UTF-16-LE: fiecare are octet nul
        content = "Hello World".encode("utf-16-le")
        assert analyzer.analyze(content) == FileType.UNICODE

    def test_unicode_nu_detecteaza_ascii(self) -> None:
        """Text ASCII pur NU este detectat ca UNICODE."""
        analyzer = UnicodeAnalyzer()
        content = b"Hello World\n"
        assert analyzer.analyze(content) != FileType.UNICODE

    # ── BmpAnalyzer ────────────────────────────────────────────────────────────

    def _create_bmp_bytes(
        self,
        width: int = 10,
        height: int = 10,
        bpp: int = 24,
    ) -> bytes:
        """Creează un header BMP minimal valid."""
        # Header BMP (14 bytes) + BITMAPINFOHEADER (40 bytes)
        pixel_data_offset = 54
        row_size = ((bpp * width + 31) // 32) * 4
        pixel_data_size = row_size * abs(height)
        file_size = pixel_data_offset + pixel_data_size

        header = struct.pack(
            "<2sIHHI",       # semnătură, file_size, rezervat×2, offset pixel data
            b"BM",
            file_size,
            0, 0,
            pixel_data_offset,
        )
        dib_header = struct.pack(
            "<IiiHHIIiiII",  # BITMAPINFOHEADER
            40,              # dimensiune header
            width,
            height,
            1,               # planuri culoare
            bpp,
            0,               # compresie (BI_RGB)
            pixel_data_size,
            2835, 2835,      # rezoluție
            0, 0,
        )
        pixel_data = b"\x00" * pixel_data_size
        return header + dib_header + pixel_data

    def test_bmp_detecteaza_fisier_bmp(self) -> None:
        """Fișier cu header 'BM' este detectat ca BMP."""
        analyzer = BmpAnalyzer()
        content = self._create_bmp_bytes(width=5, height=5, bpp=24)
        assert analyzer.analyze(content) == FileType.BMP

    def test_bmp_magic_bytes(self) -> None:
        """Magic bytes 0x42 0x4D = 'BM' sunt detectate."""
        analyzer = BmpAnalyzer()
        # Header minim: doar magic bytes + padding
        content = bytes([0x42, 0x4D]) + b"\x00" * 52
        assert analyzer.analyze(content) == FileType.BMP

    def test_bmp_nu_detecteaza_alta_semnatura(self) -> None:
        """Fișier fără magic bytes BMP NU este detectat ca BMP."""
        analyzer = BmpAnalyzer()
        content = b"PNG\r\n" + b"\x00" * 50
        assert analyzer.analyze(content) != FileType.BMP

    def test_bmp_get_info_width_height(self) -> None:
        """get_bmp_info extrage corect width și height."""
        analyzer = BmpAnalyzer()
        content = self._create_bmp_bytes(width=100, height=200, bpp=24)
        info = analyzer.get_bmp_info(content)
        assert info["width"] == 100
        assert info["height"] == 200

    def test_bmp_get_info_bpp(self) -> None:
        """get_bmp_info extrage corect bits_per_pixel."""
        analyzer = BmpAnalyzer()
        content = self._create_bmp_bytes(width=10, height=10, bpp=32)
        info = analyzer.get_bmp_info(content)
        assert info["bits_per_pixel"] == 32

    def test_bmp_get_info_returneaza_dict(self) -> None:
        """get_bmp_info returnează un dict cu cheile corecte."""
        analyzer = BmpAnalyzer()
        content = self._create_bmp_bytes()
        info = analyzer.get_bmp_info(content)
        assert isinstance(info, dict)
        assert "width" in info
        assert "height" in info
        assert "bits_per_pixel" in info

    def test_bmp_get_info_eroare_date_insuficiente(self) -> None:
        """get_bmp_info aruncă ValueError pentru date insuficiente."""
        analyzer = BmpAnalyzer()
        with pytest.raises(ValueError):
            analyzer.get_bmp_info(b"BM\x00\x00")  # prea scurt


class TestDirectoryScanner:
    """Teste pentru DirectoryScanner cu fișiere temporare."""

    def test_scan_fisier_ascii(self, tmp_path) -> None:
        """Fișierul text ASCII este clasificat corect."""
        # Creare fișier ASCII
        fisier = tmp_path / "document.txt"
        fisier.write_text("Acesta este un text simplu.\nCu mai multe linii.\n", encoding="ascii")

        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        ascii_files = rezultate.get(FileType.ASCII, [])
        assert str(fisier) in ascii_files

    def test_scan_fisier_bmp(self, tmp_path) -> None:
        """Fișierul BMP este clasificat corect."""
        # Creare fișier BMP minimal
        bmp_analyzer = BmpAnalyzer()
        # Construim BMP manual
        width, height, bpp = 2, 2, 24
        pixel_data_offset = 54
        row_size = ((bpp * width + 31) // 32) * 4
        pixel_data_size = row_size * height
        file_size = pixel_data_offset + pixel_data_size

        header = struct.pack("<2sIHHI", b"BM", file_size, 0, 0, pixel_data_offset)
        dib = struct.pack("<IiiHHIIiiII", 40, width, height, 1, bpp, 0, pixel_data_size, 0, 0, 0, 0)
        content = header + dib + b"\x00" * pixel_data_size

        fisier = tmp_path / "imagine.bmp"
        fisier.write_bytes(content)

        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        bmp_files = rezultate.get(FileType.BMP, [])
        assert str(fisier) in bmp_files

    def test_scan_director_gol(self, tmp_path) -> None:
        """Director gol returnează dict cu liste goale."""
        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        assert isinstance(rezultate, dict)
        # Toate listele sunt goale sau nu există
        total_fisiere = sum(len(v) for v in rezultate.values())
        assert total_fisiere == 0

    def test_scan_mai_multe_fisiere(self, tmp_path) -> None:
        """Scanner clasifică corect mai multe fișiere simultan."""
        # Fișier ASCII
        (tmp_path / "text.txt").write_text("Hello world\n", encoding="ascii")
        # Alt fișier ASCII
        (tmp_path / "doc.txt").write_text("Alt document text\n", encoding="ascii")

        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        ascii_files = rezultate.get(FileType.ASCII, [])
        assert len(ascii_files) == 2

    def test_scan_recursiv(self, tmp_path) -> None:
        """Scanner-ul parcurge subdirectoarele recursiv."""
        # Creare subdirector
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "fisier.txt").write_text("Conținut ASCII\n", encoding="ascii")

        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        ascii_files = rezultate.get(FileType.ASCII, [])
        assert len(ascii_files) >= 1
        # Fișierul din subdir este inclus
        cai = [str(f) for f in ascii_files]
        assert any("subdir" in c for c in cai)

    def test_scan_returneaza_cai_absolute(self, tmp_path) -> None:
        """Căile returnate sunt absolute."""
        (tmp_path / "test.txt").write_text("Text simplu\n", encoding="ascii")

        scanner = DirectoryScanner()
        rezultate = scanner.scan(str(tmp_path))

        for tip, fisiere in rezultate.items():
            for cale in fisiere:
                assert cale.startswith("/"), f"Calea '{cale}' nu este absolută"
