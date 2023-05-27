def mess_starting():
    return f'👋 Добро пожаловать в наш бот Telegram!\n\nНаш бот разработан, ' \
           f'чтобы помочь вам легко создавать PDF-документы. Просто следуйте ' \
           f'инструкциям, и наш бот будет помогать вам на каждом этапе ' \
           f'пути.\n\nУдачного создания документа! 📄'


def mess_main_menu():
    return f'<b>Выберете вариант создания PDF файла:</b>\n\n' \
           f'<b>Заполнить шаблон</b>: вам будет предложено выбрать ' \
           f'и заполнить шаблон, ' \
           f'на основе которого создастся итоговый файл.\n\n' \
           f'<b>Загрузить документ</b>: если у вас есть ' \
           f'свой заполненный документ в виде JSON файла, ' \
           f'система извлечет соответствующие данные и сгенерирует PDF.\n'


def mess_send_json():
    help_mess = f'<a href="https://github.com/fatmaann/CustomLaTeXBot">инструкциям</a>'
    return f'<b>Создание файла:</b>\n\nЧтобы отправить свой собственный' \
           f'формат документа в формате JSON, следуйте {help_mess}.' \
           f'\n\nРуководство ' \
           f'расскажет вам, как правильно структурировать файл <b>JSON</b> ' \
           f'для создания документа.\n\nОбязательно внимательно следуйте ' \
           f'инструкциям в руководстве, чтобы избежать ошибок в процессе.'


def mess_make_json():
    return f'<b>Выберите один из форматов:</b>\n' \
           f'\n1) Руководство оператора\n' \
           f'2) Руководство программиста\n' \
           f'3) Техническое задание\n' \
           f'4) Пояснительная записка\n' \
           f'5) Программа и методика испытаний\n' \
           f'6) Текст программы'


def mess_doc_classifier():
    return f'<b>Укажите раздел классификатора для документа:</b>\n\n' \
           f'1) Встроенное программное обеспечение\n' \
           f'2) Системное программное обеспечение\n' \
           f'3) Средства обеспечения информационной безопасности\n' \
           f'4) Средства разработки программного обеспечения\n' \
           f'5) Прикладное программное обеспечение\n' \
           f'6) Офисные приложения\n' \
           f'7) Лингвистическое программное обеспечение\n' \
           f'8) Промышленное программное обеспечение\n' \
           f'9) Средства управления процессами организации\n' \
           f'10) Средства обработки и визуализации массивов данных\n' \
           f'11) Средства анализа данных'


def mess_doc_sub_classifier(text):
    return f'<b>Укажите подкласс классификатора документа:</b>\n\n{text}'


def mess_start_make_json():
    help_mess = f'<a href="https://github.com/fatmaann/CustomLaTeXBot">руководство</a>'
    return f'<b>Заполнение шаблона:</b>\n\n' \
           f'В следующем опросе мы соберем от вас необходимую информацию ' \
           f'для создания PDF-документа.\n\nПрежде чем начать, ' \
           f'настоятельно рекомендуется прочитать {help_mess} по заполнению ' \
           f'документов [вставьте ссылку здесь].\n\n<b>Просим Вас быть ' \
           f'внимательными на протяжении всего опроса.</b>\n\n' \
           f'Для остановки процесса вызовите команду "/main_menu".'


def mess_wait_get_json():
    return f'Ожидаю файл формата <b>".json"</b>\n\n' \
           f'*для отмены отправки нажмите кнопку ниже'


def mess_choose_info_json(users_dict):
    explain_text = '<b>Структура документа:</b>\n\n'
    quest_explain_text = '\n\nЕсли в начале строки стоит ✅, вы можете ' \
                         'настроить (добавить или удалить) под главы в этой ' \
                         'главе. Главы со знаком ❌ не являются гибкими с ' \
                         'точки зрения количества под глав.\n\n' \
                         'Выберите главы, которые вы ' \
                         'хотите изменить в документе, нажав соответствующие ' \
                         'кнопки ниже. Иначе можете сразу создать документ по' \
                         ' выбранному формату.'
    tmp_string = []
    for part in users_dict.keys():
        if users_dict[part][0]:
            tmp_string.append('✅ ' + part)
        else:
            tmp_string.append('❌ ' + part)
    return explain_text + '\n'.join(tmp_string) + quest_explain_text


def mess_change_info_json():
    return f'<b>Настраиваемые главы:</b>\n\n'


def mess_change_parts_json(users_dict):
    tmp_change_string, i = [], 1
    for part in users_dict.keys():
        if users_dict[part][0]:
            tmp_change_string.append(f'{i}) ' + part)
            i += 1
    explain_text = '\n\nℹ️ <i>Выберите главу, которую хотите изменить и ' \
                   'нажмите ' \
                   'соответствующую кнопку ниже, чтобы получить доступ к ' \
                   'настройкам. На странице настроек вы можете добавлять или ' \
                   'удалять под главы в соответствии с вашими ' \
                   'требованиями.\n\nНе торопитесь, чтобы просмотреть ' \
                   'и настроить под главы в соответствии с потребностями ' \
                   'вашего документа.</i>'
    return mess_change_info_json() + '\n'.join(
        tmp_change_string) + explain_text


def mess_change_chapter(users_dict, chapter_name):
    chapter_info = f'<b>{chapter_name}:\n\n</b>'
    if users_dict[chapter_name][1] == 0:
        return chapter_info + '*в данной главе пока нет под глав'
    return chapter_info + '\n'.join(users_dict[chapter_name][2])


def mess_fill_chapter(chapter_name):
    if chapter_name.split()[0] == 'text':
        return f"Напишите <b>текст</b> для части:\n" \
               f"`{' '.join(chapter_name.split()[1:])}`"
    return f"Напишите <b>название</b> для части:\n" \
           f"`{' '.join(chapter_name.split()[1:])}`"


def mess_fill_info_chapter(chapter_dict):
    text = [f'<b>Введите {chapter_dict["quest"]}:</b>']
    if 'comm' in chapter_dict.keys():
        text.append(f'\n\n{chapter_dict["comm"]}')
    return ''.join(text)


def mess_finish_tex():
    return f'<b>Пожалуйста, проверьте ваши входные данные</b>.\n' \
           f'Если все верно, нажмите кнопку ниже, чтобы создать файл.\n\n' \
           f'В противном случае нажмите <b>"Отмена"</b>.'


def mess_wait_pdf():
    return f'<b>Заполненный шаблон обрабатывается и создается PDF-файл.</b>\n' \
           f'Пожалуйста, немного подождите, это может занять ' \
           f'<b>несколько секунд</b>.'


def mess_finish_pdf():
    return f'Ваш файл успешно создан.\n' \
           f'Вы можете скачать файл в сообщении ниже.'


def mess_latex_pdf():
    Overleaf = f'<a href="https://www.overleaf.com">Overleaf</a>'
    ShareLaTeX = f'<a href="https://www.sharelatex.com">ShareLaTeX</a>'
    return f'Ваш <b>LaTeX</b> файл успешно создан.\n' \
           f'Вы можете скачать файл в сообщении ниже.\n\n' \
           f'Сервисы для компиляции его в <b>PDF</b>:\n' \
           f'· {Overleaf}\n' \
           f'· {ShareLaTeX}\n'


def mess_json_error():
    return f'<b>JSON-файл содержит ошибку:</b>\n\n'


def mess_pdf_error(error, default=False):
    tmp = error
    if default:
        return f'<b>Ошибка при создании PDF-файла.\n\n' \
               f'Проверьте данные указанные при опросе</b>\n\n'
    else:
        return f'<b>Ошибка при создании PDF-файла.\n\n' \
               f'Проверьте данные указанные в JSON-файле</b>\n\n'


def mess_tex_error(error, default=False):
    tmp = error
    if default:
        return f'<b>Ошибка при создании LaTeX-файла.\n\n' \
               f'Проверьте данные указанные при опросе</b>\n\n'
    else:
        return f'<b>Ошибка при создании LaTeX-файла.\n\n' \
               f'Проверьте данные указанные в JSON-файле</b>\n\n'


def mess_photo_error(error=''):
    return f'В фото есть ошибка...{error}'


def mess_chat_error():
    return f'Извините, я не могу вас понять.\n' \
           f'Напиши мне ещё раз, используя кнопки или команды.'


def mess_time_error():
    return f'<b>📍 Извините, Вас не было слишком долго.</b>\n\n'


def mess_com_help():
    return f"Я вам помогу, но позже\n\n/start\n/main_menu"
