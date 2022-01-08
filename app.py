from flask import Flask, request, render_template
from functions import find_comments, get_post

POSTS_PATH = 'data/posts.json'
COMMENTS_PATH = 'data/comments.json'

app = Flask(__name__)


@app.route('/')  # декоратор для стартовой страницы
def start_page():
    return render_template('index.html')


@app.route('/posts/<post_id>')  # вывод поста с комментариями
def get_comments(post_id):
    comments = find_comments(COMMENTS_PATH, int(post_id))  # получения списка комментариев к посту
    post = get_post(POSTS_PATH, int(post_id))  # получение данных указанной публикации
    len_comments = len(comments)  # вычесление количества комментариев для шаблона
    return render_template('post.html', post=post, comments=comments, len_comments=len_comments)


if __name__ == '__main__':
    app.run(debug=True)
