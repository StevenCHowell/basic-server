import time
from pathlib import Path

import PyPDF2
from celery import Celery
from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure Celery
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# Folder to store uploaded and processed files
# TODO: replace this with S3 storage or some alternative storage
UPLOAD_FOLDER = Path("uploads")
PROCESSED_FOLDER = Path("processed")
UPLOAD_FOLDER.mkdir(exist_ok=True)
PROCESSED_FOLDER.mkdir(exist_ok=True)


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
def process_pdf(self, fpath):
    self.update_state(state="PROCESSING", meta={"progress": 50})
    time.sleep(10)  # simulated processing time
    output_fpath = manipulate_pdf(fpath)
    self.update_state(state="COMPLETED", meta={"progress": 100})
    return {"processed_file": str(output_fpath)}


def manipulate_pdf(fpath):
    # dummy document processing function
    with open(fpath, "rb") as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        # dummy document processing function, TODO: replace with more useful function
        for page in reversed(reader.pages):  # reverse the page order
            page.rotate(180)  # rotate the page upside down
            writer.add_page(page)

        # save the new pdf file
        output_fpath = PROCESSED_FOLDER / Path(fpath).name
        with open(output_fpath, "wb") as output_file:
            writer.write(output_file)
    return output_fpath


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = process_pdf.AsyncResult(task_id)
    if task.state != "FAILURE":
        response = {
            "state": task.state,
            "progress": task.info.get("progress", 0),
        }
        if "processed_file" in task.info:
            response["processed_file"] = task.info["processed_file"]
    else:
        response = {
            "state": task.state,
            "progress": task.info.get("progress", 0),
            "error": str(task.info),
        }
    return jsonify(response)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_file(PROCESSED_FOLDER / filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
