"""
Scanner de directoare care clasifică fișierele după conținut.

Parcurge recursiv un director și folosește analizorii din file_analyzer.py
pentru a clasifica fiecare fișier.
"""

from pathlib import Path

from lab6.file_analyzer import (
    FileType,
    AsciiAnalyzer,
    UnicodeAnalyzer,
    BinaryAnalyzer,
    BmpAnalyzer,
)


class DirectoryScanner:
    """Parcurge recursiv un director și clasifică fișierele găsite."""

    def __init__(self) -> None:
        """Inițializează scanner-ul cu toți analizorii disponibili."""
        # TODO: Creează instanțe pentru fiecare analyzer
        # Ordinea contează: BMP trebuie verificat înaintea Binary
        raise NotImplementedError("De implementat")

    # TODO: Implementează metoda scan
    def scan(self, root_dir: str) -> dict[FileType, list[str]]:
        """Parcurge recursiv directorul și clasifică fișierele.

        Args:
            root_dir: Calea absolută a directorului rădăcină.

        Returns:
            Dict unde cheile sunt FileType și valorile sunt liste
            cu căile absolute ale fișierelor de acel tip.

        Exemplu:
            {
                FileType.ASCII: ["/path/to/file.txt", "/path/to/doc.xml"],
                FileType.BMP: ["/path/to/image.bmp"],
                FileType.BINARY: ["/path/to/data.bin"],
                FileType.UNICODE: [],
                FileType.UNKNOWN: [],
            }
        """
        raise NotImplementedError("De implementat")

    def _classify_file(self, path: Path) -> FileType:
        """Clasifică un singur fișier folosind analizorii în ordine.

        Args:
            path: Calea fișierului de analizat.

        Returns:
            Tipul detectat sau FileType.UNKNOWN dacă niciun analyzer nu îl recunoaște.
        """
        # TODO: Citește conținutul fișierului și aplică analizorii în ordine
        raise NotImplementedError("De implementat")
