import os
import json
import shutil

base_path = os.path.join('users')


def get_json_formats_path(users_format):
    data_json_formats = {
        'рук-опер': ['Operators manual'],
        'рук-прог': ['Programmers Guide'],
        'тех-зад': ['Technical task'],
        'пояс-зап': ['Explanatory note'],
        'прог-ми': ['Test program and methodology'],
        'тек-прог': ['Program text']
    }
    return data_json_formats[users_format]


def get_format_short_name(users_format):
    data_short_name_json_formats = {
        'рук-опер': '34',
        'рук-прог': '33',
        'тех-зад': 'ТЗ',
        'пояс-зап': '81',
        'прог-ми': '51',
        'тек-прог': '12'
    }
    return data_short_name_json_formats[users_format]


def get_user_folder_path(user_id):
    return os.path.join(base_path, f'{user_id}')


def make_user_folder(user_folder):
    user_folder = os.path.join(base_path, user_folder)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)


def delete_user_folder(folder_name):
    path = os.path.join(base_path, str(folder_name))
    shutil.rmtree(path)


def validate_json_file(file_path):
    file_path = os.path.join(base_path, file_path)
    if not file_path.endswith(".json"):
        raise ValueError(f"Подан файл не JSON формата.")
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            json.load(f)
            return True
        except json.JSONDecodeError as e:
            error_message = f"{e.msg} at line " f"{e.lineno} column " \
                            f"{e.colno}\n\n{e.lineno}: " \
                            f"{e.doc.splitlines()[e.lineno - 1]}"
            raise ValueError(error_message)


def read_chosen_json_file(users_format):
    format_path = get_json_formats_path(users_format)
    file_path = os.path.join(base_path, 'default', format_path[0],
                             format_path[0] + '.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        users_dict = json.load(f)
    return users_dict


def read_tex_json_file(users_format):
    format_path = get_json_formats_path(users_format)
    file_path = os.path.join(base_path, 'default', format_path[0],
                             format_path[0] + ' tex.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        users_dict = json.load(f)
    return users_dict


def read_info_json_file(file_name):
    file_path = os.path.join(base_path, 'default', 'doc_info',
                             f'{file_name}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        users_dict = json.load(f)
    return users_dict


def get_value_from_classifier_json(key):
    file_path = os.path.join(base_path, 'default', 'doc_info',
                             f'classifier_info.json')
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         data = json.loads(line)
    #         print(data)
    #         if key in data:
    #             return data[key]
    with open(file_path, 'r', encoding='utf-8') as f:
        users_dict = json.load(f)
    return users_dict[key]
