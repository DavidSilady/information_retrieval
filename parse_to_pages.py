# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import xml.etree.ElementTree as ElementTree
import time


def parse_to_individual_pages():
    with open('resources/full_wiki.xml', encoding='utf8') as file:
        buffer = ''
        page_count = 0
        is_buffering = False
        for line in file:
            if '<page>' in line:
                is_buffering = True
            if is_buffering:
                buffer += line
            if '</page>' in line:
                is_buffering = False
                page_count += 1
                save_to_page_file(buffer, page_count)
                buffer = ''


def save_to_page_file(buffer, count):
    root = ElementTree.fromstring(buffer)
    title = root.find('title')
    print(f"{count:08d}: {title.text}")
    # file_name = re.sub('[*/:?\\"]', '-', title.text)

    with open(f"./pages/{count:08d}.xml", 'w', encoding='utf8') as input_file:
        input_file.write(buffer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.process_time()
    parse_to_individual_pages()
    end = time.process_time()
    print(end - start)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
