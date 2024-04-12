import os
from flask import Flask, abort, request, jsonify, url_for, render_template
from werkzeug.utils import secure_filename
import config
import eq_solver as eqs

config.showImgFlag = False
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/evalEq', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'Record not found') 
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        abort(400, 'No selected file') 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filePath = os.path.join(config.upload, filename)
        file.save(filePath)
        todoCount = request.form.get('todoCount')
        fontSize = request.form.get('fontSize')

        fileName = eqs.writeAnswerToPDF(filePath, int(fontSize), int(todoCount))
        respBody = {
            'pdf': url_for('static', filename=f'out/{fileName}.pdf')
        }
        return jsonify(respBody)
    
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
