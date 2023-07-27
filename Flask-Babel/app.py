from flask import Flask
from flask_babel import Babel, get_locale

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def locale_selector():
    return 'en'


@app.route('/')
def index():
    return f'<h1>Locale: {get_locale()}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
