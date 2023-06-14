import os
import pytest
import sys
from main import copy_files_with_english_chars


@pytest.fixture
def setup_target_directory():
    target_directory = 'directory'
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    return target_directory


def test_non_english_chars_direct(setup_target_directory, capsys):
    target_directory = setup_target_directory

    temp_file = 'tempnonenglish.txt'
    with open(temp_file, 'w') as f:
        f.write('НеАнглийскийТекст')

    # Запускаем функцию
    copy_files_with_english_chars(files=[temp_file], target_directory=target_directory)

    # Получаем вывод в консоль
    stdout_capture = capsys.readouterr().out

    # Проверяем, что файл не был скопирован и что в консоль выведена нужная информация
    assert not os.path.exists(os.path.join(target_directory,
                                           'directory/tempnonenglish.txt')) and "Файл 'tempnonenglish.txt' не содержит английских символов." in stdout_capture


def test_english_chars_direct(setup_target_directory):
    target_directory = setup_target_directory

    temp_file = 'tempenglish.txt'
    with open(temp_file, 'w') as f:
        f.write('EnglishText')

    # Тестируем функцию
    copy_files_with_english_chars(files=[temp_file], target_directory=target_directory)

    # Проверяем, что файл был скопирован
    assert os.path.exists('directory/tempenglish.txt')
    # Проверяем, что скопированный файл тот, который нужен
    copied_file = 'directory/tempenglish.txt'
    with open(copied_file, 'r') as f:
        content = f.read()
        assert content == 'EnglishText'


def test_mixed_chars(setup_target_directory):
    target_directory = setup_target_directory

    temp_file = 'tempmixed.txt'
    with open(temp_file, 'w') as f:
        f.write('EnglishТекст')

    # Запускаем функцию
    copy_files_with_english_chars(files=[temp_file], target_directory=target_directory)

    # Проверяем, что файл был скопирован
    assert os.path.exists('directory/tempmixed.txt')
    # Проверяем, что скопированный файл тот, который нужен
    copied_file = 'directory/tempmixed.txt'
    with open(copied_file, 'r') as f:
        content = f.read()
        assert content == 'EnglishТекст'


def test_multiple_files(setup_target_directory, capsys):
    target_directory = setup_target_directory

    temp_file1 = 'temp1.txt'
    with open(temp_file1, 'w') as f:
        f.write('English Text')

    temp_file2 = 'temp2.txt'
    with open(temp_file2, 'w') as f:
        f.write('НеАнглийскийТекст')

    temp_file3 = 'temp3.txt'
    with open(temp_file3, 'w') as f:
        f.write('Mixed Text')

    # Запускаем функцию
    copy_files_with_english_chars(files=[temp_file1, temp_file2, temp_file3], target_directory=target_directory)

    # Получаем вывод в консоль
    stdout_capture = capsys.readouterr().out

    # Проверяем, что только файлы 1 и 3 были скопированы
    assert os.path.exists(
        'directory/temp1.txt')
    assert os.path.exists(
        'directory/temp3.txt')
    # Проверяем, что файл 2 не был скопирован и что в консоль выведена нужная информация
    assert not os.path.exists(
        'directory/temp2.txt') and "Файл 'temp2.txt' не содержит английских символов." in stdout_capture


def test_copy_files_with_nonexistent_file(setup_target_directory, capsys):
    target_directory = setup_target_directory

    # Запускаем функцию с несуществующим файлом
    copy_files_with_english_chars(files=['nonexisted.txt'], target_directory=target_directory)

    # Получаем вывод в консоль
    stdout_capture = capsys.readouterr().out

    # Проверяем что вывелось то, что нужно
    assert "Указанный файл не существует." in stdout_capture or "Указанный путь не является файлом." in stdout_capture


def test_directory_as_file(setup_target_directory, capsys):
    target_directory = setup_target_directory

    temp_directory = "dir_instead_of_file"
    os.mkdir(temp_directory)

    # Запускаем функцию с директорией вместо файла
    copy_files_with_english_chars(files=[temp_directory], target_directory=target_directory)

    # Получаем вывод в консоль
    stdout_capture = capsys.readouterr().out

    # Проверяем что вывелось то, что нужно
    assert "Указанный путь не является файлом." in stdout_capture


def test_invalid_target_directory(setup_target_directory, capsys):
    target_directory = setup_target_directory

    # Тестируем функцию с некорректной директорией
    copy_files_with_english_chars(['temp1.txt'], target_directory + '/nonexisted')

    # Получаем вывод в консоль
    stdout_capture = capsys.readouterr().out

    # Проверяем что вывелось то, что нужно
    assert "Указанная директория не существует." in stdout_capture or "Указанный путь не является директорией." in stdout_capture


# Тесты для ввода данных через командную строку

@pytest.mark.parametrize('file_arg', ['/Users/aliya/PycharmProjects/pythonProject/tempenglish.txt'])
def test_from_command_line(file_arg, monkeypatch):
    target_directory = 'directory'

    monkeypatch.setattr(sys, 'argv', ['', f"file={file_arg}"])
    # Тестируем функцию
    copy_files_with_english_chars(files=[file_arg], target_directory=target_directory)

    # Проверяем что файл скопировался
    assert os.path.exists(os.path.join(target_directory, 'tempenglish.txt'))


@pytest.mark.parametrize('file_env', ['/Users/aliya/PycharmProjects/pythonProject/tempenglish.txt'])
def test_from_environment(file_env, monkeypatch, mocker):
    target_directory = 'directory'

    monkeypatch.setattr(sys, 'argv', [])
    mocker.patch.dict(os.environ, {'FILE': file_env})
    # Тестируем функцию
    copy_files_with_english_chars(files=[file_env], target_directory=target_directory)

    # Проверяем что файл скопировался
    assert os.path.exists(os.path.join(target_directory, 'tempenglish.txt'))
