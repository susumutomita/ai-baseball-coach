import os

from flask import jsonify


def read_files(directory_path, file_extension):
    content = ""
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content += file.read() + "\n\n"
    return content


def error_response(message, status_code):
    return jsonify({"error": message}), status_code
