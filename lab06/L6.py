import os
import sys



class GenericFile:
    def __init__(self, path, freq):
        self.path = path
        self.freq = freq  # dictionar {byte_val: count}

    def get_path(self):
        return self.path

    def get_freq(self):
        return self.freq


class TextASCII(GenericFile):
    def __init__(self, path, freq):
        super().__init__(path, freq)


#UTF-16

class TextUNICODE(GenericFile):
    def __init__(self, path, freq):
        super().__init__(path, freq)


# Fisiere binare

class Binary(GenericFile):
    def __init__(self, path, freq):
        super().__init__(path, freq)



class XMLFile(TextASCII):
    def __init__(self, path, freq, first_tag):
        super().__init__(path, freq)
        self.first_tag = first_tag

    def get_first_tag(self):
        return self.first_tag


class BMP(Binary):
    def __init__(self, path, freq, width, height, bpp):
        super().__init__(path, freq)
        self.width = width
        self.height = height
        self.bpp = bpp

    def show_info(self):
        print(f"  BMP: {self.path} | {self.width}x{self.height} | {self.bpp} bpp")


# --- Functii ajutatoare ---

def calc_freq(content):
    freq = {}
    for b in content:
        freq[b] = freq.get(b, 0) + 1
    return freq


def is_ascii(freq, total):
    # caractere "text" ASCII: tab(9), newline(10), CR(13), spatiu-tilda(32-127)
    ascii_chars = set([9, 10, 13] + list(range(32, 128)))
    ascii_count = sum(freq.get(b, 0) for b in ascii_chars)
    return ascii_count / total > 0.95


def is_unicode_utf16(freq, total):
    # byte 0 apare in >30% din continut
    zero_count = freq.get(0, 0)
    return zero_count / total > 0.30


def is_bmp(content):
    # BMP incepe cu 'BM'
    return len(content) >= 54 and content[0] == 0x42 and content[1] == 0x4D


def parse_bmp(content):
    # width la offset 18, height la 22, bpp la 28 (little-endian, 4/4/2 bytes)
    width = int.from_bytes(content[18:22], 'little')
    height = int.from_bytes(content[22:26], 'little')
    bpp = int.from_bytes(content[28:30], 'little')
    return width, height, bpp


def is_xml(content):
    # XML ASCII incepe cu '<' sau cu BOM + '<'
    text = content[:100].lstrip()
    return text.startswith(b'<')


def get_first_xml_tag(content):
    text = content.decode('ascii', errors='ignore')
    start = text.find('<')
    end = text.find('>', start)
    if start != -1 and end != -1:
        return text[start:end + 1]
    return "?"


def classify(path, content):
    total = len(content)
    if total == 0:
        return None

    freq = calc_freq(content)

    # BMP check primul (e binar cu sematura specifica)
    if is_bmp(content):
        w, h, bpp = parse_bmp(content)
        return BMP(path, freq, w, h, bpp)

    if is_unicode_utf16(freq, total):
        return TextUNICODE(path, freq)

    if is_ascii(freq, total):
        if is_xml(content):
            tag = get_first_xml_tag(content)
            return XMLFile(path, freq, tag)
        return TextASCII(path, freq)

    return Binary(path, freq)


# --- Scanare recursiva director ---

def scan_dir(root_dir):
    ascii_files = []
    unicode_files = []
    bmp_files = []

    for root, subdirs, files in os.walk(root_dir):
        for fname in os.listdir(root):
            fpath = os.path.join(root, fname)
            if not os.path.isfile(fpath):
                continue

            f = open(fpath, 'rb')
            try:
                content = f.read()
            finally:
                f.close()

            obj = classify(fpath, content)

            if isinstance(obj, BMP):
                bmp_files.append(obj)
            elif isinstance(obj, XMLFile):
                ascii_files.append(obj)
            elif isinstance(obj, TextASCII):
                ascii_files.append(obj)
            elif isinstance(obj, TextUNICODE):
                unicode_files.append(obj)

    return ascii_files, unicode_files, bmp_files


def main():
    
    root_dir = input("Introduceti calea catre directorul de scanat: ")

    if not os.path.isdir(root_dir):
        print(f"Directorul '{root_dir}' nu exista.")
        sys.exit(1)

    ascii_files, unicode_files, bmp_files = scan_dir(root_dir)

    print("\n=== Fisiere XML ASCII ===")
    for f in ascii_files:
        if isinstance(f, XMLFile):
            print(f"  {f.get_path()} | primul tag: {f.get_first_tag()}")

    print("\n=== Fisiere UNICODE (UTF-16) ===")
    for f in unicode_files:
        print(f"  {f.get_path()}")

    print("\n=== Fisiere BMP ===")
    for f in bmp_files:
        f.show_info()


if __name__ == "__main__":
    main()