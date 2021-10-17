import time
import re
import xml.etree.ElementTree as ElementTree


def clean_sentences(sentences):
    for sentence_tuple in sentences:
        sentence = sentence_tuple[0]
        # print(sentence)
        remove_markdown_pattern = r'(\'\'\'?)'
        sentence = re.sub(remove_markdown_pattern, '', sentence)
        remove_link_pattern = r'(\[\[[^\]]*\|)|(\]\])|(\[\[)'
        sentence = re.sub(remove_link_pattern, '', sentence)
        print(sentence)


def parse_text_to_sentences(text):
    print(text)
    sentences = re.findall(r'(\S*[A-Z].+?(\(([^()])*\))?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(\S*[A-Z].+?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(\S*[A-Z].+?(\(.+?\))?[.!?])(?=\s+\S*[A-Z]|$)', text)
    # sentences = re.findall(r'(?![a-z])*', text)
    clean_sentences(sentences)
    return sentences


def parse_page(page_string):
    text = parse_text_from_xml(page_string)
    sentences = parse_text_to_sentences(text)
    print(sentences)


def parse_text_from_xml(xml_string):
    root = ElementTree.fromstring(xml_string)
    text_element = root.find('revision/text')
    return text_element.text


def main():
    # for i in range(100):
    with open(f'./pages/00000099.xml', encoding='utf8') as file:
        # print(f'Page: {i+1}')
        file_string = file.read()
        parse_page(file_string)


if __name__ == '__main__':
    start = time.process_time()
    main()
    end = time.process_time()
    print(end - start)
