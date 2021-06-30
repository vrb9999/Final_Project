from flask import Flask, render_template, Response, request, redirect, url_for
from flask import Flask, request, jsonify, render_template
from textsummarizer import *
#from summary import *
from subprocess import call
from werkzeug.utils import secure_filename
import os
import cv2
import pytesseract
import pyttsx3


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "images/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("basic.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    if request.method == 'POST':
        if request.form.get('myid') == "1":
            if request.files:
                if request.files['file'].filename != "":
                    print(1)
                    file = request.files['file']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        print(filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        text = pytesseract.image_to_string(img)
                        print(text)


        elif request.form.get('myid') == "2":
            return "Hello"
            # class CallPy(object):
            #     def __init__(self, path = "C:/Users/Vinay Biradar/PycharmProjects/TEXT_EXTRACTION/summary.py"):
            #         self.path = path
            #
            #     def call_python_file(self):
            #         call(["Python3","{}".format(self.path)])



        else:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()

    # return redirect(url_for('home1'))
    return render_template('ab.html', text=text)
    # return redirect(f"/user",text)


if __name__ == '__main__':
    app.debug = True
    app.run()
