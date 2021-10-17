import time
import re
import xml.etree.ElementTree as ElementTree
import json


def clean_sentences(sentence_tuples):
    entries = []
    for sentence_tuple in sentence_tuples:
        original = sentence_tuple[0]
        print(f'Origin: {original}')
        processed = re.sub(r'(\'\'\'?)|(^\s)|(<.+?>)|(</.+?>)', '', original)
        processed = re.sub(r'(\[\[[^]]*\|)|(]])|(\[\[)', '', processed)
        print(f'Clear: {processed}')
        entries.append({
            "original": original,
            "processed": processed,
        })
    return entries


def parse_text_to_sentences(text):
    text = re.sub(r'(<ref.+?/>)|(<ref.+?</ref>)|(<!--.+?-->)', '', text)
    sentences = re.findall(r'((\s|^)\'*[A-Z].+?(\(([^()])*\))?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(\S*[A-Z].+?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(\S*[A-Z].+?(\(.+?\))?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(?![a-z])*', text)
    entries = clean_sentences(sentences)
    return entries


def parse_page(page_string):
    text = parse_text_from_xml(page_string)
    entries = parse_text_to_sentences(text)
    return entries


def parse_text_from_xml(xml_string):
    root = ElementTree.fromstring(xml_string)
    text_element = root.find('revision/text')
    return text_element.text


def main():
    entries = []

    for i in range(100):
        # with open(f'./pages/00000099.xml', encoding='utf8') as file:
        with open(f'./pages/{(i+1):08d}.xml', encoding='utf8') as file:
            # print(f'Page: {i+1}')
            file_string = file.read()
            entries += parse_page(file_string)

    with open('./result.json', 'w', encoding='utf8') as fp:
        json.dump(entries, fp)


if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print(end - start)
