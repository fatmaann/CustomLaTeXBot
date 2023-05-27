import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def make_users_profile(user_id):
    user_data = {
        'send': 0,
        'make': 0,
        'change': 0,
        'get_info': 0,
        'format_json': '',
        'format_name': '',
        'format_tex': '',
        'curr_chapter': 0,
        'amount_chapter': 0,
        'pre_doc_info': '',
    }
    r.hmset(str(user_id), user_data)
    r.expire(str(user_id), 43200)


def make_pre_doc_info(user_id):
    pass


def clear_users_profile(user_id):
    if check_new_user(user_id):
        r.delete(str(user_id))


def check_new_user(user_id):
    return r.exists(str(user_id)) == 1


def usage_time_update(user_id):
    r.expire(str(user_id), 43200)


def list_all_keys():
    keys = r.keys()
    keys = [key.decode() for key in keys]
    return keys


# Getter
def get_user_proc_send_json(user_id):
    tmp = r.hget(str(user_id), 'send')
    return int(tmp) if tmp is not None else None


def get_user_proc_make_json(user_id):
    tmp = r.hget(str(user_id), 'make')
    return int(tmp) if tmp is not None else None


def get_user_proc_change_json(user_id):
    tmp = r.hget(str(user_id), 'change')
    return int(tmp) if tmp is not None else None


def get_user_proc_get_info_json(user_id):
    tmp = r.hget(str(user_id), 'get_info')
    return int(tmp) if tmp is not None else None


def get_users_info_dict(user_id):
    tmp = r.hget(str(user_id), 'format_json')
    return json.loads(tmp) if tmp is not None else None


def get_users_json_name(user_id):
    tmp = r.hget(str(user_id), 'format_name')
    return tmp.decode() if tmp is not None else None


def get_subchapter_amount(user_id, chapter_name):
    tmp_dict = get_users_info_dict(user_id)
    return tmp_dict[chapter_name][1]


def get_users_curr_chapter(user_id):
    tmp = r.hget(str(user_id), 'curr_chapter')
    return int(tmp) if tmp is not None else None


def get_users_tex_dict(user_id):
    tmp = r.hget(str(user_id), 'format_tex')
    return json.loads(tmp) if tmp is not None else None


def get_users_amount_chapters(user_id):
    tmp = r.hget(str(user_id), 'amount_chapter')
    return int(tmp) if tmp is not None else None


def get_users_doc_info_dict(user_id):
    tmp = r.hget(str(user_id), 'pre_doc_info')
    return json.loads(tmp) if tmp is not None else None


# Processes
def proc_on(user_id, proc):
    usage_time_update(user_id)
    r.hset(str(user_id), proc, 1)


def proc_off(user_id, proc):
    usage_time_update(user_id)
    r.hset(str(user_id), proc, 0)


# Definition
def define_json_format(user_id, format_dict):
    usage_time_update(user_id)
    serialized_dict = json.dumps(format_dict)
    r.hset(str(user_id), "format_json", serialized_dict)


def define_json_name(user_id, format_name):
    usage_time_update(user_id)
    r.hset(str(user_id), "format_name", format_name)


def define_curr_chapter(user_id, curr_chapter):
    usage_time_update(user_id)
    r.hset(str(user_id), "curr_chapter", curr_chapter)


def define_amount_chapters(user_id):
    usage_time_update(user_id)
    tmp_dict = get_users_tex_dict(user_id)
    r.hset(str(user_id), "amount_chapter", len(tmp_dict.keys()))


def define_format_tex_dict(user_id, format_dict):
    usage_time_update(user_id)
    tmp_prev_dict = get_users_info_dict(user_id)
    for chapter in tmp_prev_dict.keys():
        if chapter != 'Титульный лист':
            format_dict[f'title {chapter}'] = {"text": chapter}
            if tmp_prev_dict[chapter][1] != 0:
                for subchapter in tmp_prev_dict[chapter][2]:
                    format_dict[f'subtitle {chapter} ({subchapter})'] = {
                        "text": ""}
                    format_dict[f'text {chapter} ({subchapter})'] = {"text": ""}
            else:
                format_dict[f'text {chapter}'] = {"text": ""}
            format_dict[f'new_page {chapter}'] = {}
    format_dict.popitem()
    serialized_dict = json.dumps(format_dict)
    r.hset(str(user_id), "format_tex", serialized_dict)


def define_doc_info_dict(user_id, doc_info):
    usage_time_update(user_id)
    r.hset(str(user_id), "amount_chapter", len(doc_info.keys()))
    serialized_dict = json.dumps(doc_info)
    r.hset(str(user_id), "pre_doc_info", serialized_dict)


def define_fill_chapter(user_id, text):
    usage_time_update(user_id)
    tmp_dict = get_users_tex_dict(user_id)
    chapter = list(tmp_dict.keys())[get_users_curr_chapter(user_id)]
    tmp_dict[chapter]['text'] = text
    serialized_dict = json.dumps(tmp_dict)
    r.hset(str(user_id), "format_tex", serialized_dict)


def define_fill_info_chapter(user_id, text):
    usage_time_update(user_id)
    tmp_dict = get_users_doc_info_dict(user_id)
    chapter = list(tmp_dict.keys())[get_users_curr_chapter(user_id) - 1]
    tmp_dict[chapter]['text'] = text
    serialized_dict = json.dumps(tmp_dict)
    r.hset(str(user_id), "pre_doc_info", serialized_dict)


def define_more_info_chapter(user_id, chapter, text):
    usage_time_update(user_id)
    tmp_dict = get_users_doc_info_dict(user_id)
    tmp_dict[chapter] = text
    serialized_dict = json.dumps(tmp_dict)
    r.hset(str(user_id), "pre_doc_info", serialized_dict)


# Checking processes
def check_proc_send_json(user_id):
    usage_time_update(user_id)
    tmp_proc = get_user_proc_send_json(user_id)
    return tmp_proc == 1


def check_proc_make_json(user_id):
    usage_time_update(user_id)
    tmp_proc = get_user_proc_make_json(user_id)
    return tmp_proc == 1


def check_proc_change_json(user_id):
    usage_time_update(user_id)
    tmp_proc = get_user_proc_change_json(user_id)
    return tmp_proc == 1


def check_proc_get_info_json(user_id):
    usage_time_update(user_id)
    tmp_proc = get_user_proc_get_info_json(user_id)
    return tmp_proc == 1


# Changing parts of a format
def get_real_chapter(user_id, chapter_name):
    tmp_dict = get_users_info_dict(user_id)
    for chap in tmp_dict.keys():
        if chapter_name in chap:
            return chap
    return chapter_name


def add_json_subchapter(user_id, bad_chapter_name):
    usage_time_update(user_id)
    chapter_name = get_real_chapter(user_id, bad_chapter_name)
    tmp_dict = get_users_info_dict(user_id)
    tmp_dict[chapter_name][1] += 1
    tmp_dict[chapter_name][2].append(
        f"Под глава {tmp_dict[chapter_name][1]}")
    serialized_dict = json.dumps(tmp_dict)
    r.hset(str(user_id), "format_json", serialized_dict)


def remove_json_subchapter(user_id, bad_chapter_name):
    usage_time_update(user_id)
    chapter_name = get_real_chapter(user_id, bad_chapter_name)
    tmp_dict = get_users_info_dict(user_id)
    tmp_dict[chapter_name][1] -= 1
    del tmp_dict[chapter_name][2][-1]
    serialized_dict = json.dumps(tmp_dict)
    r.hset(str(user_id), "format_json", serialized_dict)
