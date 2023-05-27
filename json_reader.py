import json
from tex.convert_doc_class import ConLatexDocument
from tex.default_doc_class import DefLatexDocument
import os

convert_func_dict = {
    'numeration_style': "make_numeration_style",
    'center_page_title': 'center_page_title',
    'title': 'make_title',
    'subtitle': 'make_subtitle',
    'subsubtitle': 'make_subsubtitle',
    'paragraph': 'add_paragraph',
    'table': 'make_table',
    'numeration': 'make_numeration_style',
    'text': 'add_text',
    'number_of_pages': 'add_number_of_pages',
    'new_page': 'make_new_page',
    'skip_numbering': 'skip_numbering'
}

def_func_dict = {
    'approved': 'add_approved_text',
    'center_page_title': 'center_page_title',
    'title': 'make_title',
    'subtitle': 'make_subtitle',
    'subsubtitle': 'make_subsubtitle',
    'table': 'make_table',
    'text': 'add_text',
    'image': 'add_image',
    'new_page': 'make_new_page',
    'skip_numbering': 'skip_numbering'
}


def make_con_doc(user_id, file_name, user_folder):
    json_path = os.path.join(f'{user_folder}', 'json_files', f'{file_name}')
    with open(json_path, "r", encoding='utf-8') as file:
        our_doc = json.load(file)
    doc_settings = our_doc['doc_sett']
    doc = ConLatexDocument(doc_settings)
    doc_data = our_doc['doc_data']
    for key, val in doc_data.items():
        func = convert_func_dict[key.split()[0]]
        if not val:
            eval(f'doc.{func}()')
        else:
            eval(f'doc.{func}({val})')
    doc.gen_doc(user_id, user_folder)


def make_def_doc(user_id, users_dict, doc_settings, user_folder):
    doc = DefLatexDocument()
    doc.make_pre_title(doc_settings)
    for our_doc in [users_dict]:
        for key, val in our_doc.items():
            func = def_func_dict[key.split()[0]]
            if not val:
                eval(f'doc.{func}()')
            else:
                eval(f'doc.{func}({val})')
    doc.gen_doc(user_id, user_folder)
