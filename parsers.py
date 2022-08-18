import requests
import lxml.html
import os
import random

from os.path import expanduser

HOME_DIR = expanduser("~")
PARSER_FILE_PATH = f'{HOME_DIR}/._amalgama_files'


def parse_name(url):
    try:
        api = requests.get(url)
    except Exception as ex:
        return f'{ex}, не удалось получить данные с url'
    tree = lxml.html.document_fromstring(api.text)
    name = tree.xpath(
        '/html/body/div[7]/div[3]/div[2]/div[3]/div[1]/h2[1]/text()')
    return name


def parse(url):
    try:
        api = requests.get(url)
    except Exception as ex:
        return f'{ex}, не удалось получить данные с url'
    tree = lxml.html.document_fromstring(api.text)
    text_original = tree.xpath(
        '//*[@id="click_area"]/div//*[@class="original"]/text()')
    text_translate = tree.xpath(
        '//*[@id="click_area"]/div//*[@class="translate"]/text()')

    os.chdir(HOME_DIR)

    if not os.path.isdir("._amalgama_files"):
        os.mkdir("._amalgama_files")

    os.chdir(PARSER_FILE_PATH)

    with open(
         "text.txt", "w", newline='', encoding='utf-8') as txt_file:
        for i in range(len(text_original)):
            txt_file.write(text_original[i])
            txt_file.write(text_translate[i])
    try:
        os.rename("text.txt", f"{parse_name(url)}.txt")
    except Exception as e:
        os.rename(
            "text.txt", f"{parse_name(url)}.{random.randint(0, 100)}.txt")
        return f'{e}'

    txt_file.close()
    # 2. Некоторые песни без перехода на новую строку


def main():
    link = 'Вставьте ссылку на песню с сайта amalgama-lab.com'
    parse(link)
    parse_name(link)


if __name__ == "__main__":
    main()
