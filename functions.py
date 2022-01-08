import json


def read_json(filename):  # функция для чтения json-файла
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def search_comments(comments, post_id):  # функция для поиска комментариев к посту по номеру публикации
    data = read_json(comments)
    result = []
    for comment in data:
        if comment['post_id'] == post_id:
            result.append(comment)
    return result


def get_post(posts, pk):  # функция для поиска поста но номеру публикации
    data = read_json(posts)
    result = {}
    for post in data:
        if post['pk'] == pk:
            result = post
    return result


def search_content_post(posts, key):  # функция для поска постов по фрагменту описания
    data = read_json(posts)
    result = []
    for post in data:
        if len(result) != 10:  # ограничение на количество постов в результате (не больше 10 шт.)
            if key.lower() in post['content'].lower():
                result.append(post)
    return result


def search_user_post(posts, user_name):
    data = read_json(posts)
    result = []
    for post in data:
        if user_name.lower() in post['poster_name'].lower():
            result.append(post)
    return result

