import json


def read_json(filename):  # функция для чтения json-файла
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def find_comments(comments, post_id):  # функция для поиска комментариев к посту по номеру публикации
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
