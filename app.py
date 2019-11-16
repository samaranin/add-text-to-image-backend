from image_processing.image_processing import *
from flask import Flask, request, send_from_directory, send_file
from flask_cors import CORS
from PIL import Image
import os
import shutil


BACKGROUNDS_PATH_PREFIX = "sources/backgrounds/"
LABELS_PATH_PREFIX = "sources/labels/"
FONTS_PATH_PREFIX = "fonts/"

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route("/")
def hello():
    return "Web server to write text on image for NUWEE library"


@app.route("/api/fonts/")
def fonts():
    return {"data": get_list_of_files(FONTS_PATH_PREFIX)}


@app.route("/api/backgrounds/")
def backgrounds():
    return {"data": get_list_of_files(BACKGROUNDS_PATH_PREFIX)}


@app.route("/api/labels/")
def labels():
    return {"data": get_list_of_files(LABELS_PATH_PREFIX)}


@app.route("/sources/backgrounds/<path:path>/")
def show_background(path):
    return send_from_directory('sources/backgrounds', path)


@app.route("/sources/labels/<path:path>/")
def show_labels(path):
    return send_from_directory('sources/labels', path)


@app.route("/temp/<path:path>/")
def finished_images(path):
    return send_file("temp/"+path, as_attachment=True)


@app.route("/api/join_images/", methods=['POST', 'GET'])
def join_image():
    error = None
    if request.method == 'POST':
        data = request.get_json(force=True)
        label_image = LABELS_PATH_PREFIX + validate_json(data, "label_image", get_list_of_files(LABELS_PATH_PREFIX)[0])
        image1, image2 = (label_image, data["text_image"]) if data["join"] == "left" else (data["text_image"], label_image)
        image_path = join_two_images(image1, image2)
        return {"data": image_path}
    else:
        error = """Invalid request method. 
        Use POST request and next json format: 
        { "text_image": "image_with_text", "label_image": "label_image", "join": "left" or "right" }"""
    return {"data": error}


@app.route("/api/write_text/", methods=['POST', 'GET'])
def write_text():
    error = None
    if request.method == 'POST':
        data = request.get_json(force=True)

        header = validate_json(data, "header", '')
        footer = validate_json(data, "footer", '')

        source_path = BACKGROUNDS_PATH_PREFIX + validate_json(data, "background_image",
                                                              get_list_of_files(BACKGROUNDS_PATH_PREFIX)[0])

        width = int(validate_json(data, "width", "960"))
        height = int(validate_json(data, "height", "960"))

        header_font_path = FONTS_PATH_PREFIX + validate_json(data, "header_font_name",
                                                             get_list_of_files(FONTS_PATH_PREFIX)[0])
        text_width_header = int(validate_json(data, "text_width_header", "30"))
        font_size_header = int(validate_json(data, "font_size_header", "40"))

        footer_font_path = FONTS_PATH_PREFIX + validate_json(data, "footer_font_name",
                                                             get_list_of_files(FONTS_PATH_PREFIX)[0])
        text_width_footer = int(validate_json(data, "font_width_footer", "30"))
        font_size_footer = int(validate_json(data, "font_size_footer", "30"))

        top_padding = int(validate_json(data, "top_padding", "200"))
        bottom_padding = int(validate_json(data, "bottom_padding", "60"))

        save_folder = "temp/"

        image_path = write_image_on_text(
            header=header.encode('utf-8').decode('utf-8'),
            footer=footer,
            source_path=source_path,
            width=width, height=height,
            header_font_path=header_font_path,
            text_width_header=text_width_header, font_size_header=font_size_header,
            footer_font_path=footer_font_path,
            font_size_footer=font_size_footer,
            text_width_footer=text_width_footer,
            save_folder=save_folder,
            top_padding=top_padding,
            bottom_padding=bottom_padding)
        return {"data": image_path}
    else:
        error = """Invalid request method. 
        Use POST request and next json format: 
        { "background_image": "image_to_write_text", "header": "header", "paragraph": "paragraph", "footer": "footer",
          "font_name": "font_name", "width": "width", "height": "height", "header_font_name": "header_font_name", 
          "text_width_header": "text_width_header", "font_size_header": "font_size_header", 
          "footer_font_name": "footer_font_name", "font_size_footer": "font_size_footer", 
          "text_width_footer": "text_width_footer", "top_padding": "top_padding", "bottom_padding": "bottom_padding"}"""
    return {"data": error}


@app.route("/api/get_image_size/", methods=['POST', 'GET'])
def get_image_size():
    error = None
    if request.method == 'POST':
        data = request.get_json(force=True)
        image_path = LABELS_PATH_PREFIX if data["image_type"] == "label" else BACKGROUNDS_PATH_PREFIX
        image_path += data["image_name"]
        img = Image.open(image_path)
        width, height = img.size
        img.close()
        return {"width": width, "height": height}
    else:
        error = """Invalid request method. 
            Use POST request and next json format: 
            { "image_type": "background or label", "image_name": "image_name" }"""
    return {"data": error}


@app.route("/api/remove_temp_files/")
def remove_temp_files():
    for root, dirs, files in os.walk('temp/'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return {"data": "success"}


def validate_json(data, value, default=''):
    return str(default) if value not in data else str(data[value])


if __name__ == "__main__":
    app.run(host='0.0.0.0')


