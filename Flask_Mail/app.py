from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'shegiyan.samvel@mail.ru'
app.config['MAIL_PASSWORD'] = 'WanrSdVZqvbcwCcSVp2J'
app.config['MAIL_DEFAULT_SENDER'] = ('Samo', 'shegiyan.samvel@mail.ru')
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRES_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


# mail = Mail()
# mail.init_app(app)

@app.route('/')
def index():
    msg = Message('Hello man', recipients=['armine.gyulazyan@gmail.com', 'shegiyansam@gmail.com'])
    # msg.body = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the ' \
    #            'industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and ' \
    #            'scrambled it to make a type specimen book.'

    with app.open_resource('cat.jpeg') as cat:
        msg.attach('cat.jpeg', 'image/jpeg', cat.read())

    # msg = Message(
    #     subject='',
    #     recipients=[],
    #     body='',
    #     html='',
    #     sender='',
    #     cc=[],
    #     bcc=[],
    #     attachments=[],
    #     reply_to=[],
    #     date='date',
    #     charset='',
    #     extra_headers={'': ''},
    #     mail_options=[],
    #     rcpt_options=[]
    # )

    mail.send(msg)

    return 'Message has been sent!!'


if __name__ == '__main__':
    app.run()
