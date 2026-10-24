from flask import Flask, render_template, request, abort, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join
#from werkzeug.datastructures import  FileStorage
import errno
import os
from datetime import datetime
from pyresparser import ResumeParser

app = Flask(__name__, template_folder='template')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file11():
   if request.method == 'POST':
      #f = request.files['file']
      files = request.files.getlist("file")
      mydir = os.path.join(
        os.getcwd(), 'resume', 
        datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
      resp = []
      for f in files:
        fname = secure_filename(f.filename)
        if not fname:
          continue  # submitted with no file chosen
        os.makedirs(mydir, mode=0o777, exist_ok=True)
        fpp = os.path.join(mydir, fname)
        f.save(fpp)
        resp.append(ResumeParser(fpp).get_extracted_data())
      return resp
   else:
      return render_template('upload.html')

@app.route('/storage', defaults={'req_path': ''})
@app.route('/storage/<path:req_path>')
def dir_listing(req_path):
    # Serve only from the upload folder; safe_join returns None for ../ or absolute paths.
    BASE_DIR = os.path.join(os.getcwd(), 'resume')
    abs_path = safe_join(BASE_DIR, req_path)
    if abs_path is None or not os.path.exists(abs_path):
        return abort(404)
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = []
    with os.scandir(abs_path) as it:
        for entry in sorted(it, key=lambda e: e.name):
            files.append({ 'name': entry.name,
                           'path': '/'.join(filter(None, [req_path, entry.name])),
                           'size': entry.stat().st_size if entry.is_file() else None })
    return render_template('files.html', files=files)