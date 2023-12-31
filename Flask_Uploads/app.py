from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'  # Set the destination folder for uploaded photos

configure_uploads(app, photos)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        file_url = photos.url(filename)
        return f'File uploaded successfully. URL: {file_url}'

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
