from flask import Flask, render_template, send_file, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pathlib
import os
import cal_operations

ALLOWED_EXTENSIONS = {'csv'}
#UPLOAD_FOLDER = pathlib.Path.cwd().joinpath('definitions')
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'secret'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'File uploaded successfully at {filepath}/{filename}')
        return redirect(request.url)

    return redirect(request.url)


@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/downloadxls", methods=['GET'])
def get_cal_xl():
    exec('cal_operations')
    return send_file(
        'output/CALENDAR.xlsx',
        mimetype="xlsx",
        as_attachment=True)


@app.route("/get_pdf", methods=['GET'])
def get_pdf():
    return send_file(
        'bkp/AutoCal_Doc.pdf',
        mimetype="pdf",
        as_attachment=True)


@app.route("/get_sample_cal", methods=['GET'])
def get_sample_cal():
    return send_file(
        'bkp/calendar_data.csv',
        mimetype="csv",
        as_attachment=True)


@app.route("/get_sample_hol", methods=['GET'])
def get_sample_hol():
    return send_file(
        'bkp/HolidayList.csv',
        mimetype="csv",
        as_attachment=True)


@app.route("/upload-holidays", methods=['GET', 'POST'])
def upload_holidays():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename != "HolidayList.csv":
            flash('File Name is not correct!')
            return redirect(request.url)
        else:
            get_upload_file(file)

    return render_template('uploadholiday.html')


@app.route("/upload-calendar", methods=["GET", "POST"])
def upload_calendar():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename != "calendar_data.csv":
            flash('File Name is not correct!')
            return redirect(request.url)
        else:
            get_upload_file(file)

    return render_template('uploadcalendar.html')


@app.route("/get-info", methods=["GET"])
def get_info():
    return render_template('get_info.html')


if __name__ == "__main__":
    app.run(debug=True)

