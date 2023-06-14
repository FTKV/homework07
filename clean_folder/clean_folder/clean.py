import pathlib
import re
import shutil
import sys

ARCHIVE_LABEL = "archives"

CATEGORY_EXTS = {
    ARCHIVE_LABEL: ('ZIP', 'GZ', 'TAR'),
    "audio": ('MP3', 'OGG', 'WAV', 'AMR', 'FLAC', 'CUE'),
    "documents": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX', 'DJV', 'DJVU'),
    "images": ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP', 'TIF', 'TIFF'),
    "video": ('AVI', 'MP4', 'MOV', 'MKV'),
    "unknown files": ()
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


def define_data(path):
    defined_files = {}
    key_unknown_files = get_key_unknown_files(CATEGORY_EXTS)
    for key in CATEGORY_EXTS:
        defined_files[key] = []

    for i in path.glob("**/*"):
        if i.is_file():
            for key in defined_files:
                if i.suffix.removeprefix(".").upper() in CATEGORY_EXTS[key] or key == key_unknown_files:
                    defined_files[key].append(i)
                    break

    return defined_files

def get_key_unknown_files(CATEGORY_EXTS):
    key_unknown_files = ""
    for key in CATEGORY_EXTS:
        if CATEGORY_EXTS[key] == ():
            key_unknown_files = key
            break

    return key_unknown_files

def normalize(string):
    trans_map = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans_map[ord(c)] = l
        trans_map[ord(c.upper())] = l.upper()

    string = string.translate(trans_map)

    return re.sub("\W", "_", string)

def normalize_data(path):
    for i in path.glob("**/*"):
        i.rename(i.parent.joinpath(normalize(i.name.removesuffix(i.suffix)) + i.suffix))

def print_data(defined_files):
    key_unknown_files = get_key_unknown_files(CATEGORY_EXTS)
    exts_known = set()
    exts_unknown = set()
    for key in defined_files:
        if len(defined_files[key]) > 0:
            print(f"Files from '{key}' category:")
            for i in defined_files[key]:
                print(" " * 8 + f"{i.name}")
                ext = i.suffix.removeprefix(".").upper()
                if key != key_unknown_files:
                    exts_known.add(ext)
                elif key == key_unknown_files and ext != "":
                    exts_unknown.add(ext)
        else:
            continue
        print("\n")

    print(f"Known file extensions:\n{exts_known}\n")
    print(f"Unknown file extensions:\n{exts_unknown}\n")

def rm_empty_dirs(path):
    for i in path.iterdir():
        if i.is_dir():
            rm_empty_dirs(i)
            try:
                i.rmdir()
            except OSError:
                continue

def sort_data(path, defined_files):
    key_unknown_files = get_key_unknown_files(CATEGORY_EXTS)
    for key in defined_files:
        if len(defined_files[key]) > 0:
            if key == key_unknown_files:
                for i in defined_files[key]:
                    i.replace(path.joinpath(i.name))
            else:
                subpath = path.joinpath(key)
                subpath.mkdir()
                for i in defined_files[key]:
                    i.replace(subpath.joinpath(i.name))

def unpack_archives(defined_files):
    for i in defined_files[ARCHIVE_LABEL]:
        shutil.unpack_archive(i.absolute(), i.parent.joinpath(i.name.removesuffix(i.suffix)))

def main():
    sysargv = sys.argv
    if len(sysargv) > 1:
        source = sysargv[1]        
    else:
        print("The path to folder should be passed as argument after script name")
        return
    path = pathlib.Path(source)
    if not path.is_dir():
        print("The argument is path to file or folder doesn't exist")
        return
    normalize_data(path)
    defined_files = define_data(path)
    sort_data(path, defined_files)
    rm_empty_dirs(path)
    defined_files = define_data(path)
    print_data(defined_files)
    unpack_archives(defined_files)

if __name__ == "__main__":
    main()