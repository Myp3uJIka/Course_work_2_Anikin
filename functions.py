import json


def read_json(filename):  # функция для чтения json-файла
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def comments_in_posts(posts, comments):
    posts_list = read_json(posts)
    comments_list = read_json(comments)
    comments_count_list = {}
    for comment in comments_list:
        coincidence = False
        for key in comments_count_list.keys():
            if comment['post_id'] == key:
                comments_count_list[key] += 1
                coincidence = True
        if not coincidence:
            comments_count_list[comment['post_id']] = 1
    for post in posts_list:
        coincidence = False
        for comment, count in comments_count_list.items():
            if post['pk'] == comment:
                post['comments_count'] = count
                coincidence = True
        if not coincidence:
            post['comments_count'] = 0
    with open(posts, 'w', encoding='utf-8') as f:
        json.dump(posts_list, f, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    return





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


def search_user_post(posts, user_name):  # функция для поиска постов пользователя
    data = read_json(posts)
    result = []
    for post in data:
        if user_name.lower() in post['poster_name'].lower():
            result.append(post)
    return result

