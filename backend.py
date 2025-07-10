# import time

# import PyPDF2
from celery import Celery
from flask import Flask, jsonify, request, send_file
from Pathlib import Path
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure Celery
app.config["CELERY_BROCKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# Folder to store uploaded and processed files
# TODO: replace this with S3 storage
UPLOAD_FOLDER = Path("uploads")
ANNOTATED_FOLDER = Path("annotated")
UPLOAD_FOLDER.mkdir(exist_ok=True)
ANNOTATED_FOLDER.mkdir(exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    # confirm input includes "file" data field
    if "file" not in request.files:
        return jsonify({"error": "No file input field"})

    # confirm the input actually includes a data file
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    fname = secure_filename(file.filename)
    path_fname = UPLOAD_FOLDER / fname
    file.save(path_fname)
    task = process_pdf.apply_async(args=[str(path_fname)])
    return jsonify({"task_id": task.id})


@celery.task(bind=True)
def process_pdf(self, file_path):
    NotImplemented


def annotate_pdf(file_path):
    NotImplemented


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    NotImplemented


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_file(ANNOTATED_FOLDER / filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
