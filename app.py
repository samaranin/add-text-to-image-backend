from image_processing.image_processing import *
from flask import Flask, request, send_from_directory
from flask_cors import CORS


BACKGROUNDS_PATH_PREFIX = "sources/backgrounds/"
LABELS_PATH_PREFIX = "sources/labels/"
FONTS_PATH_PREFIX = "fonts/"

# backgrounds = get_list_of_files(backgrounds_path_prefix)
# labels = get_list_of_files(labels_path_prefix)
#
# background_file_path = backgrounds_path_prefix + backgrounds[1]
# label_file_path = labels_path_prefix + labels[1]
#
# width, height = get_image_size_by_name(backgrounds[1])
# header = "Визначення густини рідин ареометричним методом за допомогою торсійних ваг"
# paragraph = "Гаврилюк Ю. Ю., Нечипорук А. П."
#
# image_with_text = write_image_on_text(
#     header=header.encode('utf-8').decode('utf-8'),
#     paragraph=paragraph.encode('utf-8').decode('utf-8'), width=width, height=height,
#     source_path=background_file_path)
#
# joined_images = join_two_images(label_file_path, image_with_text)

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
    return {"data": send_from_directory('sources/backgrounds', path)}


@app.route("/sources/labels/<path:path>/")
def show_labels(path):
    return {"data": send_from_directory('sources/labels', path)}


@app.route("/temp/<path:path>/")
def finished_images(path):
    return {"data": send_from_directory('temp', path)}


@app.route("/api/join_images/", methods=['POST', 'GET'])
def join_image():
    error = None
    if request.method == 'POST':
        data = request.get_json(force=True)
        label_image = LABELS_PATH_PREFIX + validate_json(data, "image2", get_list_of_files(LABELS_PATH_PREFIX)[0])
        image1, image2 = (label_image, data["image1"]) if data["join"] == "left" else (data["image1"], label_image)
        image_path = join_two_images(image1, image2)
        return {"data": image_path}
    else:
        error = """Invalid request method. 
        Use POST request and next json format: 
        { "image1": "image_with_text", "image2": "label_image", "join": "left" or "right" }"""
    return {"data": error}


@app.route("/api/write_text/", methods=['POST', 'GET'])
def write_text():
    error = None
    if request.method == 'POST':
        data = request.get_json(force=True)

        header = validate_json(data, "header", ''),
        paragraph = validate_json(data, "paragraph", ''),
        footer = validate_json(data, "footer", ''),
        font_path = FONTS_PATH_PREFIX + validate_json(data, "font_name", get_list_of_files(FONTS_PATH_PREFIX)[0]),
        source_path = BACKGROUNDS_PATH_PREFIX + validate_json(data, "image", get_list_of_files(BACKGROUNDS_PATH_PREFIX)[0]),
        width = int(validate_json(data, "width", "960")),
        height = int(validate_json(data, "height", "960")),
        text_width_header = int(validate_json(data, "text_width_header", "30")),
        font_size_header = int(validate_json(data, "font_size_header", "40")),
        text_width_paragraph = int(validate_json(data, "text_width_paragraph", "30")),
        font_size_paragraph = int(validate_json(data, "font_size_paragraph", "30")),
        font_size_footer = int(validate_json(data, "font_size_footer", "30")),
        save_folder = "temp/"

        image_path = write_image_on_text(
            header=header.encode('utf-8').decode('utf-8'),
            paragraph=paragraph.encode('utf-8').decode('utf-8'),
            footer=footer,
            font_path=font_path,
            source_path=source_path,
            width=width, height=height,
            text_width_header=text_width_header, font_size_header=font_size_header,
            text_width_paragraph=text_width_paragraph, font_size_paragraph=font_size_paragraph,
            font_size_footer=font_size_footer,
            save_folder=save_folder)
        return {"data": image_path}
    else:
        error = """Invalid request method. 
        Use POST request and next json format: 
        { "image": "image_to_write_text", "header": "header", "paragraph": "paragraph", "footer": "footer",
          "font_name": "font_name", "width": "width", "height": "height", "text_width_header": "text_width_header",
          "font_size_header": "font_size_header", "text_width_paragraph": "text_width_paragraph", 
          "font_size_paragraph": "font_size_paragraph", "font_size_footer": "font_size_footer"}"""
    return {"data": error}


def validate_json(data, value, default=''):
    return default if value not in data else data[value]


if __name__ == "__main__":
    app.run(host='0.0.0.0')


