from flask import Flask, request, render_template

POST_PATH = 'data/posts.json'

app = Flask(__name__)


@app.route('/')
def start_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
