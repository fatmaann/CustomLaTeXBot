import os

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiogram.utils.exceptions import BotBlocked

import buttons
import database
import files_manager
import texts
from tex.json_reader import make_con_doc, make_def_doc
from configure.env import config

bot = Bot(token=config["token"])
dp = Dispatcher(bot)


def simply_inline_kb(butt_list, row=2):
    markup_inline = types.InlineKeyboardMarkup(row_width=row)
    for but_type in butt_list:
        if row != 1:
            tmp_kb = []
            item1 = types.InlineKeyboardButton(text=but_type[0],
                                               callback_data=but_type[1])
            tmp_kb.append(item1)
            if len(but_type) >= 4:
                item2 = types.InlineKeyboardButton(text=but_type[2],
                                                   callback_data=but_type[3])
                tmp_kb.append(item2)
            if len(but_type) >= 6:
                item3 = types.InlineKeyboardButton(text=but_type[4],
                                                   callback_data=but_type[5])
                tmp_kb.append(item3)
            markup_inline.add(*tmp_kb)
        else:
            item1 = types.InlineKeyboardButton(text=but_type[0],
                                               callback_data=but_type[1])
            markup_inline.add(item1)
    return markup_inline


async def selection_inline_kb(call, text, butt_list, row=3, command=False):
    markup_inline = types.InlineKeyboardMarkup(row_width=row)
    for i in range(len(butt_list) - 1):
        item1 = types.InlineKeyboardButton(text=butt_list[i][0],
                                           callback_data=butt_list[i][1])
        item2 = types.InlineKeyboardButton(text=butt_list[i][2],
                                           callback_data=butt_list[i][3])
        item3 = types.InlineKeyboardButton(text=butt_list[i][4],
                                           callback_data=butt_list[i][5])
        markup_inline.add(item1, item2, item3)
    item_last = types.InlineKeyboardButton(text=butt_list[-1][0],
                                           callback_data=butt_list[-1][1])
    markup_inline.add(item_last)
    if command:
        await bot.send_message(call.from_user.id, text,
                               reply_markup=markup_inline,
                               parse_mode='html')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=markup_inline,
                                    parse_mode='html')


def choose_part_inline_kb(butt_list, row):
    markup_inline, parts = types.InlineKeyboardMarkup(
        row_width=len(butt_list) - 1), []
    for but_type in butt_list:
        item = types.InlineKeyboardButton(text=but_type[0],
                                          callback_data=but_type[1])
        parts.append(item)
    markup_inline.add(*parts)
    return markup_inline


async def send_mess(message, text, butt_list=None, row=2, change=False):
    if butt_list is None:
        butt_list = list()
    if not change:
        markup_inline = simply_inline_kb(butt_list, row)
    else:
        markup_inline = choose_part_inline_kb(butt_list, row)
    await bot.send_message(chat_id=message.chat.id,
                           text=text,
                           reply_markup=markup_inline,
                           parse_mode='html')


async def edit_mess(call, text, butt_list, row=2, change=False):
    if not change:
        markup_inline = simply_inline_kb(butt_list, row)
    else:
        markup_inline = choose_part_inline_kb(butt_list, row)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=markup_inline,
                                parse_mode='html')


async def send_finish_pdf(message):
    pdf_path = os.path.join(
        files_manager.get_user_folder_path(message.from_user.id), 'pdf_files',
        f'{message.from_user.id}.pdf')
    with open(pdf_path, 'rb') as f:
        await bot.send_document(message.from_user.id, document=f)


async def start_make_fill_json(call):
    database.proc_on(call.from_user.id, 'make')
    database.define_curr_chapter(call.from_user.id, 0)
    database.define_amount_chapters(call.from_user.id)
    await edit_mess(call, texts.mess_start_make_json(), [])
    await ask_tex_question_mess(call.message, call.from_user.id,
                                database.get_users_curr_chapter(
                                    call.from_user.id))


async def ask_tex_question_mess(message, user_id, curr_chapter_num):
    tmp_dict, mess_text = database.get_users_tex_dict(user_id), ''
    amount_chapter = database.get_users_amount_chapters(user_id)
    if curr_chapter_num < amount_chapter:
        chapter = list(tmp_dict.keys())[curr_chapter_num]
        if 'question' in tmp_dict[chapter]:
            mess_text = f'Напишите {tmp_dict[chapter]["question"]}:'
        elif chapter.split()[0] in ["new_page", "title", "skip_numbering",
                                    "table"]:
            database.define_curr_chapter(user_id, curr_chapter_num + 1)
            await ask_tex_question_mess(message, user_id, curr_chapter_num + 1)
            return 0
        else:
            mess_text = texts.mess_fill_chapter(chapter)
        await send_mess(message, mess_text)
    else:
        database.proc_off(user_id, 'make')
        await send_mess(message, texts.mess_finish_tex(),
                        buttons.make_pdf_buttons())


async def ask_doc_info_question_mess(message, user_id, curr_chapter_num):
    tmp_dict, mess_text = database.get_users_doc_info_dict(user_id), ''
    amount_chapter = database.get_users_amount_chapters(user_id)
    if curr_chapter_num < amount_chapter:
        chapter = list(tmp_dict.keys())[curr_chapter_num]
        mess_text = texts.mess_fill_info_chapter(tmp_dict[chapter])
        database.define_curr_chapter(user_id, curr_chapter_num + 1)
        await send_mess(message, mess_text)
    else:
        database.proc_off(user_id, 'get_info')
        await send_mess(message, texts.mess_doc_classifier(),
                        buttons.choose_classifier_buttons(), 3)


async def make_default_finish_pdf(call):
    users_folder = str(call.from_user.id)
    users_pdf_folder = os.path.join(users_folder, 'pdf_files')
    files_manager.make_user_folder(users_pdf_folder)
    try:
        make_def_doc(str(call.from_user.id),
                     database.get_users_tex_dict(call.from_user.id),
                     database.get_users_doc_info_dict(call.from_user.id),
                     files_manager.get_user_folder_path(
                         call.from_user.id))
        await edit_mess(call, texts.mess_finish_pdf(), [])
        pdf_path = os.path.join(
            files_manager.get_user_folder_path(call.from_user.id), 'pdf_files',
            f'{call.from_user.id}.pdf')
        with open(pdf_path, 'rb') as f:
            await bot.send_document(call.from_user.id, document=f)
    except Exception as e:
        await edit_mess(call, f"{texts.mess_pdf_error(e, True)}", [])
        await welcome_func(call.message)
    database.clear_users_profile(call.from_user.id)
    files_manager.delete_user_folder(call.from_user.id)


@dp.message_handler(commands=['start'])
async def welcome_func(message):
    database.clear_users_profile(message.from_user.id)
    await send_mess(message, texts.mess_starting(), [])
    await send_mess(message, texts.mess_main_menu(), buttons.start_buttons())


@dp.message_handler(commands=['main_menu'])
async def welcome_func(message):
    database.clear_users_profile(message.from_user.id)
    await send_mess(message, texts.mess_main_menu(), buttons.start_buttons())


@dp.message_handler(commands=['help'])
async def help_func(message):
    await send_mess(message, texts.mess_com_help(), [])


@dp.message_handler(commands=['choose_format'])
async def help_func(message):
    database.make_users_profile(message.from_user.id)
    await selection_inline_kb(message, texts.mess_make_json(),
                              buttons.make_json_buttons(), 3, True)


@dp.message_handler(commands=['send_file'])
async def help_func(message):
    database.clear_users_profile(message.from_user.id)
    await send_mess(message, texts.mess_send_json(),
                    buttons.send_json_buttons())


@dp.callback_query_handler()
async def vote_callback(call: types.CallbackQuery):
    if call.data == 'main_menu':
        database.clear_users_profile(call.from_user.id)
        await edit_mess(call, texts.mess_main_menu(), buttons.start_buttons())

    elif call.data == 'make_json':
        database.make_users_profile(call.from_user.id)
        await selection_inline_kb(call, texts.mess_make_json(),
                                  buttons.make_json_buttons())

    elif call.data == 'get_json':
        await edit_mess(call, texts.mess_send_json(),
                        buttons.send_json_buttons())

    elif call.data == 'wait_get_json':
        database.proc_on(call.from_user.id, 'send')
        await edit_mess(call, texts.mess_wait_get_json(),
                        buttons.stop_buttons(), 1)

    elif call.data.split('_')[0] == 'making' and database.check_new_user(
            call.from_user.id):
        if database.get_users_json_name(call.from_user.id) == '':
            database.define_json_name(call.from_user.id,
                                      call.data.split('_')[1])
            database.define_json_format(call.from_user.id,
                                        files_manager.read_chosen_json_file(
                                            call.data.split('_')[1]))
        await edit_mess(call, texts.mess_choose_info_json(
            database.get_users_info_dict(call.from_user.id)),
                        buttons.change_curr_json_buttons(
                            database.get_users_json_name(call.from_user.id)))

    elif call.data == 'change_json' and database.check_new_user(
            call.from_user.id):
        if not database.check_proc_change_json(call.from_user.id):
            database.proc_on(call.from_user.id, 'change')
            await edit_mess(call, texts.mess_change_parts_json(
                database.get_users_info_dict(call.from_user.id)),
                            buttons.choose_change_part_buttons(
                                database.get_users_info_dict(call.from_user.id),
                                database.get_users_json_name(
                                    call.from_user.id)), 1,
                            True)
        else:
            await edit_mess(call, texts.mess_change_parts_json(
                database.get_users_info_dict(call.from_user.id)),
                            buttons.choose_change_part_buttons(
                                database.get_users_info_dict(call.from_user.id),
                                database.get_users_json_name(
                                    call.from_user.id)), 1,
                            True)

    elif call.data.split('_')[0] == 'choose' and database.check_new_user(
            call.from_user.id):
        await edit_mess(call, texts.mess_change_chapter(
            database.get_users_info_dict(call.from_user.id),
            database.get_real_chapter(call.from_user.id,
                                      call.data.split('_')[1])),
                        buttons.change_chapter_buttons(
                            database.get_real_chapter(call.from_user.id,
                                                      call.data.split('_')[1])))

    elif call.data.split('_')[0] == 'add' and database.check_new_user(
            call.from_user.id):
        database.add_json_subchapter(call.from_user.id, call.data.split('_')[2])
        await edit_mess(call, texts.mess_change_chapter(
            database.get_users_info_dict(call.from_user.id),
            database.get_real_chapter(call.from_user.id,
                                      call.data.split('_')[2])),
                        buttons.change_chapter_buttons(call.data.split('_')[2]))

    elif call.data.split('_')[0] == 'rem' and database.check_new_user(
            call.from_user.id):
        if database.get_subchapter_amount(call.from_user.id,
                                          database.get_real_chapter(
                                              call.from_user.id,
                                              call.data.split('_')[2])) != 0:
            database.remove_json_subchapter(call.from_user.id,
                                            call.data.split('_')[2])
            await edit_mess(call, texts.mess_change_chapter(
                database.get_users_info_dict(call.from_user.id),
                database.get_real_chapter(call.from_user.id,
                                          call.data.split('_')[2])),
                            buttons.change_chapter_buttons(
                                call.data.split('_')[2]))
    elif call.data.split('.')[0] == 'start_make_json' and \
            database.check_new_user(call.from_user.id):
        database.define_format_tex_dict(call.from_user.id,
                                        files_manager.read_tex_json_file(
                                            call.data.split('.')[1]))
        database.define_doc_info_dict(call.from_user.id,
                                      files_manager.read_info_json_file(
                                          'doc_pre_info'))
        database.proc_off(call.from_user.id, 'change')
        database.proc_on(call.from_user.id, 'get_info')
        await edit_mess(call, texts.mess_start_make_json(), [])
        await ask_doc_info_question_mess(call.message, call.from_user.id,
                                         database.get_users_curr_chapter(
                                             call.from_user.id))
    elif call.data.split('_')[0] == 'classifier' and \
            database.check_new_user(call.from_user.id):
        database.define_more_info_chapter(call.from_user.id, 'project_code',
                                          call.data.split('_')[1])
        tmp_info = files_manager.get_value_from_classifier_json(
            call.data.split('_')[1])
        await edit_mess(call, texts.mess_doc_sub_classifier(tmp_info[1]),
                        buttons.choose_sub_classifier_buttons(tmp_info[0]), 3)

    elif call.data.split('_')[0] == 'subclass' and \
            database.check_new_user(call.from_user.id):
        database.define_more_info_chapter(call.from_user.id,
                                          'project_class_code',
                                          call.data.split('_')[1])
        database.define_more_info_chapter(call.from_user.id,
                                          'format_short_name',
                                          files_manager.get_format_short_name(
                                              database.get_users_json_name(
                                                  call.from_user.id)))
        await start_make_fill_json(call)

    elif call.data == 'make_pdf' and database.check_new_user(
            call.from_user.id):
        await edit_mess(call, texts.mess_wait_pdf(), [])
        await make_default_finish_pdf(call)
        return 0
    else:
        await edit_mess(call, texts.mess_time_error() + texts.mess_main_menu(),
                        buttons.start_buttons())
    await bot.answer_callback_query(call.id)


@dp.message_handler(content_types=['document'])
async def handle_document(message):
    if database.check_proc_send_json(message.from_user.id):
        if message.document.mime_type == 'application/json':
            users_folder = str(message.from_user.id)
            users_json_folder = os.path.join(users_folder, 'json_files')
            users_pdf_folder = os.path.join(users_folder, 'pdf_files')
            files_manager.make_user_folder(users_json_folder)
            files_manager.make_user_folder(users_pdf_folder)
            file_name = f'{message.from_user.id}.json'
            file_path = os.path.join(users_json_folder, file_name)
            await message.document.download(
                destination=os.path.join('users', file_path))
            try:
                if files_manager.validate_json_file(file_path):
                    try:
                        make_con_doc(str(message.from_user.id), file_name,
                                     files_manager.get_user_folder_path(
                                         message.from_user.id))
                        await send_mess(message, texts.mess_finish_pdf())
                        await send_finish_pdf(message)
                    except Exception as e:
                        await send_mess(message, f"{texts.mess_pdf_error(e)}",
                                        buttons.send_json_again_buttons())
                        database.proc_off(message.from_user.id,
                                          'send')
            except Exception as e:
                error_message = f"{texts.mess_json_error()}{e}"
                await send_mess(message, error_message,
                                buttons.send_json_again_buttons())
                database.proc_off(message.from_user.id, 'send')
            files_manager.delete_user_folder(message.from_user.id)
        else:
            await get_problem_mes(message)
    else:
        await get_problem_mes(message)


@dp.message_handler(content_types=['text'])
async def handle_document(message):
    if database.check_proc_make_json(message.from_user.id):
        database.define_fill_chapter(message.from_user.id, message.text)
        database.define_curr_chapter(message.from_user.id,
                                     database.get_users_curr_chapter(
                                         message.from_user.id) + 1)
        await ask_tex_question_mess(message, message.from_user.id,
                                    database.get_users_curr_chapter(
                                        message.from_user.id))
    elif database.check_proc_get_info_json(message.from_user.id):
        database.define_fill_info_chapter(message.from_user.id, message.text)
        database.define_curr_chapter(message.from_user.id,
                                     database.get_users_curr_chapter(
                                         message.from_user.id))
        await ask_doc_info_question_mess(message, message.from_user.id,
                                         database.get_users_curr_chapter(
                                             message.from_user.id))
    else:
        await get_problem_mes(message)


@dp.message_handler(content_types=['voice', 'video', 'video_note',
                                   'pinned_message', 'animation',
                                   'sticker', 'photo', 'contact',
                                   'location', 'poll', 'dice'])
async def get_problem_mes(message):
    await send_mess(message, texts.mess_chat_error())


@dp.errors_handler(exception=BotBlocked)
async def error_get_blocked(update: types.Update, exception: BotBlocked):
    return True


async def on_startup(dp):
    webhook_url = config['url']
    await bot.set_webhook(webhook_url)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path="/",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="localhost",
        port=5000,
    )
