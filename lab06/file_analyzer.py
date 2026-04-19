"""
Analizor de fișiere după conținut (nu după extensie).

Clasifică fișierele în tipuri: ASCII, UNICODE (UTF-16), BINAR, BMP.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto


class FileType(Enum):
    """Tipurile posibile de fișiere detectate."""

    ASCII = auto()
    UNICODE = auto()
    BINARY = auto()
    BMP = auto()
    UNKNOWN = auto()


class FileAnalyzer(ABC):
    """Clasă abstractă pentru analizarea conținutului unui fișier."""

    @abstractmethod
    def analyze(self, content: bytes) -> FileType:
        """Analizează conținutul și returnează tipul detectat.

        Args:
            content: Conținutul brut al fișierului ca bytes.

        Returns:
            Tipul de fișier detectat.
        """
        ...


class AsciiAnalyzer(FileAnalyzer):
    """Detectează fișierele ASCII/UTF-8.

    Criterii:
    - Octeții din {9, 10, 13, 32..127} au frecvență mare (≥85% din total)
    - Octeții din {0-8, 11, 12, 14-31, 128-255} au frecvență mică (≤15% din total)
    """

    # TODO: Implementează metoda analyze
    def analyze(self, content: bytes) -> FileType:
        """Returnează ASCII dacă fișierul este text ASCII/UTF-8, altfel UNKNOWN.

        Args:
            content: Conținutul fișierului.

        Returns:
            FileType.ASCII sau FileType.UNKNOWN.
        """
        raise NotImplementedError("De implementat")


class UnicodeAnalyzer(FileAnalyzer):
    """Detectează fișierele Unicode/UTF-16.

    Criterii:
    - Octetul 0x00 apare în ≥30% din conținut
    """

    # TODO: Implementează metoda analyze
    def analyze(self, content: bytes) -> FileType:
        """Returnează UNICODE dacă fișierul este UTF-16, altfel UNKNOWN.

        Args:
            content: Conținutul fișierului.

        Returns:
            FileType.UNICODE sau FileType.UNKNOWN.
        """
        raise NotImplementedError("De implementat")


class BinaryAnalyzer(FileAnalyzer):
    """Detectează fișierele binare.

    Criterii:
    - Distribuție relativ uniformă a octeților pe intervalul {0..255}
    - Niciun interval nu depășește pragul pentru ASCII sau UNICODE
    """

    # TODO: Implementează metoda analyze
    def analyze(self, content: bytes) -> FileType:
        """Returnează BINARY dacă fișierul este binar, altfel UNKNOWN.

        Args:
            content: Conținutul fișierului.

        Returns:
            FileType.BINARY sau FileType.UNKNOWN.
        """
        raise NotImplementedError("De implementat")


class BmpAnalyzer(FileAnalyzer):
    """Detectează și parsează fișierele BMP.

    Criterii:
    - Magic bytes: primii 2 octeți sunt 0x42 0x4D ('BM')
    """

    # TODO: Implementează metoda analyze
    def analyze(self, content: bytes) -> FileType:
        """Returnează BMP dacă fișierul are header BMP valid, altfel UNKNOWN.

        Args:
            content: Conținutul fișierului.

        Returns:
            FileType.BMP sau FileType.UNKNOWN.
        """
        raise NotImplementedError("De implementat")

    # TODO: Implementează metoda get_bmp_info
    def get_bmp_info(self, content: bytes) -> dict:
        """Extrage informații din header-ul BMP.

        Structura header BMP (little-endian):
        - Offset 0-1:  Semnătură 'BM'
        - Offset 2-5:  Dimensiunea totală a fișierului (uint32)
        - Offset 6-9:  Rezervat
        - Offset 10-13: Offset date pixel (uint32)
        - Offset 14-17: Dimensiunea DIB header (uint32) = 40 pentru BITMAPINFOHEADER
        - Offset 18-21: Lățimea imaginii în pixeli (int32)
        - Offset 22-25: Înălțimea imaginii în pixeli (int32)
        - Offset 26-27: Numărul de planuri de culoare (uint16) = 1
        - Offset 28-29: Biți per pixel (uint16)

        Args:
            content: Conținutul fișierului BMP.

        Returns:
            Dict cu cheile: 'width', 'height', 'bits_per_pixel'.

        Raises:
            ValueError: Dacă fișierul nu este BMP valid sau este prea scurt.
        """
        raise NotImplementedError("De implementat")
