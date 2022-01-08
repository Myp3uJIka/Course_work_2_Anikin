from flask import Flask, request, render_template
from functions import read_json, search_comments, get_post, search_content_post, search_user_post, comments_in_posts

POSTS_PATH = 'data/posts.json'
COMMENTS_PATH = 'data/comments.json'

app = Flask(__name__)


@app.route('/')  # декоратор для стартовой страницы
def start_page():
    comments_in_posts(POSTS_PATH, COMMENTS_PATH)
    posts = read_json(POSTS_PATH)
    return render_template('index.html', posts=posts)


@app.route('/posts/<post_id>')  # вывод поста с комментариями
def get_comments(post_id):
    comments = search_comments(COMMENTS_PATH, int(post_id))  # получения списка комментариев к посту
    post = get_post(POSTS_PATH, int(post_id))  # получение данных указанной публикации
    len_comments = len(comments)  # вычесление количества комментариев для шаблона
    return render_template('post.html', post=post, comments=comments, len_comments=len_comments)


@app.route('/search/')  # вывод постов по совпадению с описанием
def find_posts():
    s = request.args.get('s')
    posts = search_content_post(POSTS_PATH, s)  # получение списка совпадений
    posts_count = len(posts)  # получение количества сопадений
    return render_template('search.html', posts=posts, posts_count=posts_count)


@app.route('/users/<username>')  # вывод публикаций пользователя
def find_user_posts(username):
    posts = search_user_post(POSTS_PATH, username)  # получение списка постов
    return render_template('user-feed.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
