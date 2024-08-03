
# Напишите код, который запускается из командной строки и получает на вход путь до директории на ПК.
# Соберите информацию о содержимом в виде объектов namedtuple.
# Каждый объект хранит:
# ○ имя файла без расширения или название каталога,
# ○ расширение, если это файл,
# ○ флаг каталога,
# ○ название родительского каталога.
# В процессе сбора сохраните данные в текстовый файл используя
# логирование.

from collections import namedtuple
import logging
import os
import argparse

logging.basicConfig(filename='parser.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

Obj = namedtuple('Obj', ['name', 'expansion', 'is_directory', 'parent_catalog'], defaults=None)


def traverse_directory(directory_path):
    dir_counter = 1
    file_counter = 1
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if not os.path.islink(file_path):
                obj = Obj(file.split('.')[:-1], os.path.splitext(file)[1][1:], False,
                          os.path.dirname(file_path).split('\\')[-1])
                logger.info(f'Added information about file № {file_counter}: {obj}')
                file_counter += 1
        for directory in enumerate(dirnames):
            dir_path = os.path.join(dirpath, directory[1])
            obj = Obj(directory[1], None, True, os.path.dirname(dir_path).split('\\')[-1])
            logger.info(f'Added information about catalog № {dir_counter}: {obj}')
            dir_counter += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Directory Parser')
    parser.add_argument('path', metavar='directory', type=str,
                        nargs=1, help='Enter the path to the directory on the PC')
    args = parser.parse_args()
    path = os.path.abspath(args.path[0])
    print(traverse_directory(path))