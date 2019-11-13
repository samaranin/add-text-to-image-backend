from nider.models import Header
from nider.models import Paragraph
from nider.models import Linkback
from nider.models import Content
from nider.models import Image

from nider.core import Font

from PIL import Image as Img

import datetime

from os import listdir
from os.path import isfile, join


def write_image_on_text(header='',
                        paragraph='',
                        footer='',
                        font_path='fonts/Roboto-Regular.ttf',
                        source_path='sources/test.jpg',
                        width=1080, height=1080,
                        text_width_header=30,  font_size_header=40,
                        text_width_paragraph=30,  font_size_paragraph=30,
                        font_size_footer=30,
                        save_folder='temp/'):
    header = Header(
        text=header.upper(),
        font=Font(font_path, font_size_header),
        text_width=text_width_header,
        align='center',
        color='#ffffff'
    )

    para = Paragraph(
        text=paragraph,
        font=Font(font_path, font_size_paragraph),
        text_width=text_width_paragraph,
        align='center',
        color='#ffffff'
    )

    linkback = Linkback(
        text=footer,
        font=Font(font_path, font_size_footer),
        align='center',
        color='#ffffff'
    )

    content = Content(para, header, linkback, padding=60)

    save_path = save_folder + ''.join(str(datetime.datetime.now()).split()) + '.png'
    img = Image(content, width=width, height=height, fullpath=save_path)

    img.draw_on_texture(source_path)

    return save_path


def join_two_images(im1_path, im2_path, save_folder='temp/'):
    images = [Img.open(x) for x in [im1_path, im2_path]]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Img.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset, 0))
      x_offset += im.size[0]

    save_path = save_folder + ''.join(str(datetime.datetime.now()).split()) + '.png'
    new_im.save(save_path)

    return save_path


def get_list_of_files(my_path="temp/"):
    files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return sorted(files, key=lambda x: str(x[0]).lower())

