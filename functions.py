import json


def read_json(filename):  # функция для чтения json-файла
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def comments_in_posts(posts, comments):  # функция для добавления количества комментариев к посту
    posts_list = read_json(posts)
    comments_list = read_json(comments)
    comments_count_list = {}  # словарь пост/количество комментариев
    for comment in comments_list:  # перебор комментариев
        coincidence = False  # переменная для указания совпадения комментария и публикации
        for key in comments_count_list.keys():
            if comment['post_id'] == key:
                comments_count_list[key] += 1  # увеличение значения количества комментариев на 1 при наличии
                # совпадения в списке комментариев
                coincidence = True
        if not coincidence:
            comments_count_list[comment['post_id']] = 1  # создание новой записи в словаре списка комментариев при
            # несовпадении комментария и существующих записей в словаре
    for post in posts_list:  # добавление новой записи (количество комментариев) в список словарей с публикациями
        coincidence = False
        for comment, count in comments_count_list.items():
            if post['pk'] == comment:
                post['comments_count'] = count
                coincidence = True
        if not coincidence:
            post['comments_count'] = 0  # нулевое значение при отсутствии комментариев к публикации
    with open(posts, 'w', encoding='utf-8') as f:  # запись в файл
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


def search_tags(posts):  # функция для извлечения списка тегов и добавления их к посту
    data = read_json(posts)
    for post in data:
        tags_list = set()  # создание множества (без повторения одинаковых значений)
        words = post['content'].split()  # создание словаря из слов в описании поста для дальнейшей обработки
        for teg in words:
            if teg.startswith('#'):
                tags_list.add(teg[1:])  # добавление в множество совпадений по словам начинающимся с '#'
        tags = list(tags_list)  # создание списка для дальнейшей сортировки по алфавиту
        tags.sort()  # сортировка списка
        post['tags'] = tags  # создание записи к посту со всеми тегами
    with open(posts, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


def get_post_with_tag(posts, tag_name):  # получение списка постов по совпадению с тегом
    data = read_json(posts)
    result = []
    for post in data:
        if post['tags']:  # проверка: пустой ли список тэгов
            if tag_name in post['tags']:
                result.append(post)  # добавление постов с совпадением в финальный список
    return result


def make_bookmark(posts, post_id, bookmarks):  # функция для добавления поста в закладки
    bookmarks_dic = read_json(bookmarks)
    data = read_json(posts)
    coincidence = False  # переменная-маркер для проверки наличия поста в закладках перед добавлением
    if bookmarks_dic:
        for post in bookmarks_dic:
            if post['pk'] == int(post_id):
                coincidence = True
    if not coincidence:  # цикл в случае отсутствия указанного post_id в закладках
        for post in data:
            if int(post_id) == post['pk']:
                bookmarks_dic.append(post)  # добавление поста в закладки
    with open(bookmarks, 'w', encoding='utf-8') as f:  # запись в файл bookmarks обновлённой информации
        json.dump(bookmarks_dic, f, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))


def delete_bookmark(bookmarks, post_id):  # функция для удаления поста из закладок
    bookmarks_dic = read_json(bookmarks)
    for post in bookmarks_dic:
        if post['pk'] == int(post_id):
            bookmarks_dic.remove(post)
    with open(bookmarks, 'w', encoding='utf-8') as f:
        json.dump(bookmarks_dic, f, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
