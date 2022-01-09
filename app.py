from flask import Flask, request, render_template
from werkzeug.utils import redirect

from functions import read_json, search_comments, get_post, search_content_post, search_user_post, comments_in_posts, \
    search_tags, get_post_with_tag, make_bookmark, delete_bookmark, add_comment

POSTS_PATH = 'data/posts.json'
COMMENTS_PATH = 'data/comments.json'
BOOKMARKS_PATH = 'data/bookmarks.json'

app = Flask(__name__)


@app.route('/')  # декоратор для стартовой страницы
def start_page():
    comments_in_posts(POSTS_PATH, COMMENTS_PATH)  # обновление информации о количестве постов
    posts = read_json(POSTS_PATH)
    bookmarks_count = len(read_json(BOOKMARKS_PATH))
    return render_template('index.html', posts=posts, bookmarks_count=bookmarks_count)


@app.route('/posts/<post_id>')  # вывод поста с комментариями
def get_comments(post_id):
    comments = search_comments(COMMENTS_PATH, int(post_id))  # получения списка комментариев к посту
    post = get_post(POSTS_PATH, int(post_id))  # получение данных указанной публикации
    return render_template('post.html', post=post, comments=comments, post_id=post_id)


@app.route('/search/', methods=['GET', 'POST'])  # вывод постов по совпадению с описанием
def find_posts():
    s = request.args.get('s')
    posts = []
    if s:
        posts = search_content_post(POSTS_PATH, s)  # получение списка совпадений
    posts_count = len(posts)  # получение количества сопадений
    return render_template('search.html', posts=posts, posts_count=posts_count)


@app.route('/users/<username>')  # вывод публикаций пользователя
def find_user_posts(username):
    posts = search_user_post(POSTS_PATH, username)  # получение списка постов
    return render_template('user-feed.html', posts=posts)


@app.route('/tag/<tagname>')  # поиск тегов
def find_tag(tagname):
    search_tags(POSTS_PATH)  # обновление информации о количестве тегов в публикациях
    posts = get_post_with_tag(POSTS_PATH, tagname)  # получение списка постов по совпадению с тегом
    return render_template('tag.html', posts=posts, tag_name=tagname)


@app.route('/bookmarks/')  # отображение закладок
def open_bookmarks():
    posts = read_json(BOOKMARKS_PATH)
    return render_template('bookmarks.html', posts=posts)


@app.route('/bookmarks/add/<post_id>')  # сохранение публикации в файле закладок
def save_bookmark(post_id):
    make_bookmark(POSTS_PATH, post_id, BOOKMARKS_PATH)
    return redirect('/', code=302)


@app.route('/bookmarks/remove/<post_id>')  # удаление публикации из файла закладок
def remove_bookmark(post_id):
    delete_bookmark(BOOKMARKS_PATH, post_id)
    return redirect('/', code=302)


@app.route('/posts/<post_id>/new_comment')  # вьюшка для добавления комментария к посту
def new_comment(post_id):
    name = request.args.get("commenter_name")
    comment = request.args.get("comment")
    add_comment(COMMENTS_PATH, post_id, name, comment)
    return redirect('/posts/{}'.format(post_id), code=302)


if __name__ == '__main__':
    app.run(debug=True)
