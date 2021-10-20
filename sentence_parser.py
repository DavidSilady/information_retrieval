import time
import re
import xml.etree.ElementTree as ElementTree
import json
import csv


def is_dict_pair_valid(dict_pair):
    # If the starting letter differs, the pair is not valid
    if not dict_pair['base'][0] == dict_pair['form'][0]:
        return False
    # If the number of words differ, the pair is not valid
    if not len(dict_pair['base'].split(' ')) == len(dict_pair['form'].split(' ')):
        return False
    return True


def extract_link_to_dict(sentence):
    dict_results = []
    results = re.findall(r'\[\[[A-Za-z0-9.]+?\|.+?]]', sentence)
    if results:
        for result in results:
            dict_result = {
                'base': re.findall(r'\[\[(.+?)\|', result)[0],
                'form': re.findall(r'\|(.+?)]]', result)[0],
                'postfix': ''
            }
            if is_dict_pair_valid(dict_result):
                dict_results.append(dict_result)
    if not results:
        results = re.findall(r'\[\[[A-Za-z0-9.]+?]][a-z]+?\s', sentence)
        if results:
            for result in results:
                dict_result = {
                    'base': re.findall(r'\[\[(.+?)]]', result)[0],
                    'postfix': re.findall(r'\[\[.+?]](.*)\s', result)[0]
                }
                dict_result['form'] = dict_result['base'] + dict_result['postfix']
                dict_results.append(dict_result)

    if results:
        print(dict_results)
    save_to_terms_dictionary(dict_results)
    return dict_results


def save_to_terms_dictionary(dict_terms):
    csv_columns = ['base', 'form', 'postfix']
    csv_file = "./term_dictionary.csv"
    try:
        with open(csv_file, 'a', encoding='utf8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns, lineterminator='\n')
            # writer.writeheader()
            for data in dict_terms:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def clean_sentences(sentence_tuples):
    entries = []
    for sentence_tuple in sentence_tuples:
        original = sentence_tuple[0]
        # print(f'Origin: {original}')
        processed = re.sub(r'(\'\'\'?)|(^\s)|(<.+?>)|(</.+?>)', '', original)
        extract_link_to_dict(processed)
        processed = re.sub(r'(\[\[[^]]*\|)|(]])|(\[\[)', '', processed)
        # print(f'Clear: {processed}')
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
