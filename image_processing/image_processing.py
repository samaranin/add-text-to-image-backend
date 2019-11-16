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
                        footer='',
                        source_path='sources/test.jpg',
                        width=1080, height=1080,
                        header_font_path='fonts/Roboto-Regular.ttf',
                        text_width_header=30,  font_size_header=40,
                        footer_font_path='fonts/Roboto-Regular.ttf',
                        font_size_footer=30, text_width_footer=30,
                        save_folder='temp/',
                        top_padding=200,
                        bottom_padding=140):
    header_text = Header(
        text=header.upper(),
        font=Font(header_font_path, font_size_header),
        text_width=text_width_header,
        align='center',
        color='#ffffff'
    )

    para = Paragraph(
        text='',
        font=Font(footer_font_path, font_size_footer),
        text_width=text_width_footer,
        align='center',
        color='#ffffff'
    )

    linkback = Linkback(
        text='',
        font=Font(footer_font_path, font_size_footer),
        align='center',
        color='#ffffff',
        bottom_padding=20
    )

    content = Content(para, header_text, linkback, padding=top_padding)

    temp_save_path = get_save_file_name(save_folder)
    img = Image(content, width=width, height=height, fullpath=temp_save_path)

    img.draw_on_texture(source_path)

    header_text = Header(
        text='',
        font=Font(header_font_path, font_size_header),
        text_width=text_width_header,
        align='center',
        color='#ffffff'
    )

    para = Paragraph(
        text=footer,
        font=Font(footer_font_path, font_size_footer),
        text_width=text_width_footer,
        align='center',
        color='#ffffff'
    )

    content = Content(para, header_text, linkback, padding=bottom_padding)

    new_save_path = get_save_file_name(save_folder)
    img = Image(content, width=width, height=height, fullpath=new_save_path)

    img.draw_on_texture(temp_save_path)

    img = Img.open(new_save_path)
    img = img.crop((0, 0, width, height))

    final_save_path = get_save_file_name(save_folder)
    img.save(final_save_path)

    return final_save_path


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


def get_save_file_name(save_folder="temp/"):
    return save_folder + ''.join(str(datetime.datetime.now()).split()) + '.png'

