import os
import sys
import shutil

def copy_files_with_english_chars(files, target_directory):
    if target_directory is None:
        target_directory = os.getenv('TARGET_DIRECTORY', None)
        if target_directory is None:
            target_directory = input("Введите директорию для копирования файлов: ")

    if not os.path.exists(target_directory):
        print("Указанная директория не существует.")
        return

    if not os.path.isdir(target_directory):
        print("Указанный путь не является директорией.")
        return
    for file in files:
        if not os.path.exists(file):
            print("Указанный файл не существует.")
            return

        if not os.path.isfile(file):
            print("Указанный путь не является файлом.")
            return

        filename = os.path.basename(file)

        flag = False
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            for c in content:
                if c.isalpha() and c.isascii() and ord(c) < 127:
                    flag = True

            if flag:
                shutil.copy(file, target_directory)
                print(f"Файл '{filename}' скопирован в '{target_directory}'.")
            else:
                print(f"Файл '{filename}' не содержит английских символов.")


if __name__ == '__main__':
    # Получение параметров напрямую из кода Python
    copy_files_with_english_chars(files=["/Users/aliya/PycharmProjects/pythonProject/myDir.txt"], target_directory=
    None)

    # Получение параметров из командной строки
    if len(sys.argv) > 1:
        file_arg = None
        for arg in sys.argv[1:]:
            if arg.startswith("file="):
                file_arg = arg.split("=")[1]
        if file_arg is not None:
            copy_files_with_english_chars(files=[file_arg], target_directory=None)

    # Получение параметров из переменного окружения
    file_env = os.getenv('FILE', None)
    if file_env is not None:
        copy_files_with_english_chars(files=[file_env], target_directory=None)
