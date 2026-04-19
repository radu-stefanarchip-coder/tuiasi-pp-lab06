"""
Entry point pentru scanner-ul de directoare.

Utilizare:
    uv run python -m lab6.main /calea/catre/director
"""

import sys
from lab6.directory_scanner import DirectoryScanner
from lab6.file_analyzer import FileType


def main() -> None:
    """Parsează argumentele CLI și afișează clasificarea fișierelor."""
    if len(sys.argv) < 2:
        print("Utilizare: python -m lab6.main <director>")
        sys.exit(1)

    root_dir = sys.argv[1]
    scanner = DirectoryScanner()
    rezultate = scanner.scan(root_dir)

    print(f"\nRezultate pentru directorul: {root_dir}\n")

    for tip, fisiere in rezultate.items():
        if fisiere:
            print(f"=== {tip.name} ({len(fisiere)} fișiere) ===")
            for cale in fisiere:
                print(f"  {cale}")
            print()


if __name__ == "__main__":
    main()
