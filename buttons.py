def cut_long_chapter_name(chapter_name):
    if len(chapter_name) > 21:
        return chapter_name[5:22]
    return chapter_name


def choose_change_part_buttons(users_dict, format_name):
    buttons_list, i = [], 1
    for part in users_dict.keys():
        if users_dict[part][0]:
            part = cut_long_chapter_name(part)
            buttons_list.append([str(i), f'choose_{part}'])
            i += 1
    buttons_list.append(['Назад', f'making_{format_name}'])
    return buttons_list


def choose_classifier_buttons():
    buttons = [[1, f'classifier_01', 2, f'classifier_02', 3, f'classifier_03'],
               [4, f'classifier_04', 5, f'classifier_05', 6, f'classifier_06'],
               [7, f'classifier_07', 8, f'classifier_08', 9, f'classifier_09'],
               [10, f'classifier_10', 11, f'classifier_11']]
    return buttons


def choose_sub_classifier_buttons(amount):
    buttons_list, tmp, i = [], [], 1
    while i < amount + 1:
        tmp += [f'{i}', f'subclass_{str(i).zfill(2)}']
        if i % 3 == 0:
            buttons_list.append(tmp)
            tmp = []
        i += 1
    buttons_list.append(tmp) if len(tmp) != 0 else None
    return buttons_list


def change_chapter_buttons(chapter_name):
    chapter_name = cut_long_chapter_name(chapter_name)
    return [['Добавить под главу', f'add_ch_{chapter_name}',
             'Убрать под главу', f'rem_ch_{chapter_name}'],
            ['Сохранить', f'change_json']]


def start_buttons():
    return [['Заполнить', 'make_json', 'Загрузить', 'get_json']]


def make_json_buttons():
    return [['1', 'making_рук-опер_json', '2', 'making_рук-прог_json', '3',
             'making_тех-зад_json'],
            ['4', 'making_пояс-зап_json', '5', 'making_прог-ми_json', '6',
             'making_тек-прог_json'],
            ['Назад', 'main_menu']]


def change_curr_json_buttons(format_name):
    return [['Изменить', 'change_json', 'Создать',
             f'start_make_json.{format_name}'],
            ['Назад', 'make_json']]


def send_json_buttons():
    return [['Отправить', 'wait_get_json', 'Позже', 'main_menu']]


def send_json_again_buttons():
    return [['Пере отправить', 'wait_get_json', 'Позже', 'main_menu']]


def make_pdf_buttons():
    return [['Да', 'make_pdf', 'Отмена', 'main_menu']]


def stop_buttons():
    return [['Отмена', 'main_menu']]
