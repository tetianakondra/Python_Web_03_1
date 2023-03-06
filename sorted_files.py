import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
import os


parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Folder with trash", required=True)
parser.add_argument("--output", "-o", help="sorted folder", default="sorted")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_path = Path(os.path.join(output, ext))
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, Path(os.path.join(new_path, el.name)))
            except OSError as error:
                logging.error(error)


def delete_files(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            os.remove(el)


def delete_folders(path: Path) -> None:

    while len(list(path.iterdir())) > 0:

        for sorted_elem in path.iterdir():

            if len(list(sorted_elem.iterdir())) == 0:
                Path(sorted_elem).rmdir()
                
            else:

                delete_folders(sorted_elem)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    folders.append(source)
    grabs_folder(source)
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    want_to_delete = input("Trash was sorted. Do you want to delete trash folder? y/n ")
    
    if want_to_delete.lower() == "y":
        threads_rm = []
        threads_rm_folders = []
        for folder in folders:
            th_rm = Thread(target=delete_files, args=(folder,))
            th_rm.start()
            threads_rm.append(th_rm)
        
        [th_rm.join() for th_rm in threads_rm]

        delete_folders(source)
        source.rmdir()

    print("Trash folder was deleted")



