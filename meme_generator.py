import textwrap
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops, ImageSequence
import pyvips
import imageio
from os import system, mkdir
import shutil


class Memegen:
    """FOR SMALL GIF, IMAGES
    EATS ~1000 mb ram, when advice_slow ~100 mb ram
    WORKING FAST AND EATS A LOT OF RAM"""
    def advice_fast(path, bottom_text, top_text="", font_path='./fonts/impact/impact.ttf', font_size=9,
               stroke_width=3, url=False, RESULT_FILENAME="temp", watermark=None, rt_bytes=False, can_resize=True):
        if url:
            p = requests.get(path)
            path = BytesIO(p.content)
        # грузим фото
        im = Image.open(path)
        image_width_old, image_height_old = im.size
        if image_height_old < 500:
            image_width = image_width_old * 2
            image_height = image_height_old * 2
        else:
            image_width = image_width_old
            image_height = image_height_old
        # грузим шрифт (хихи грузин)
        fontSize = int(image_height * font_size) // 100
        fontSize2 = int(image_height * font_size) // 100
        font = ImageFont.truetype(font=font_path, size=fontSize)
        font2 = ImageFont.truetype(font=font_path, size=fontSize)

        # делаем текст CAPSLOCK
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()

        # первоначальный перенос текста
        char_width, char_height = font.getsize('A')
        chars_per_line = image_width // char_width
        top_lines = textwrap.wrap(top_text, width=chars_per_line)

        char_width2, char_height2 = font2.getsize('A')
        chars_per_line2 = image_width // char_width2
        bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line2)

        # если многа текста
        ammount_top = len(top_lines)
        ammount_bottom = len(bottom_lines)
        if char_height * ammount_top > image_height // 2.5:
            while char_height * ammount_top > image_height // 2.5:
                fontSize = fontSize - 1
                font = ImageFont.truetype(font=font_path, size=fontSize)
                char_width, char_height = font.getsize('A')
                chars_per_line = image_width // char_width
                top_lines = textwrap.wrap(top_text, width=chars_per_line)
                ammount_top = len(top_lines)
        if char_height2 * ammount_bottom > image_height // 2.5:
            while char_height2 * ammount_bottom > image_height // 2.5:
                fontSize2 = fontSize2 - 1
                font2 = ImageFont.truetype(font=font_path, size=fontSize2)
                char_width2, char_height2 = font2.getsize('A')
                chars_per_line2 = image_width // char_width2
                bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line2)
                ammount_bottom = len(bottom_lines)

        #делаем текст канвас для ускорения генерации гиф
        text_canvas = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(text_canvas)
        if top_text != None:
            # ебашим верх строку
            y = char_height2 // 2
            for line in top_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                d.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
                y += line_height
        if bottom_text != None:
            # ебашим нижнюю строку
            y = image_height - char_height2 * len(bottom_lines) - char_height2 // 2
            for line in bottom_lines:
                line_width, line_height = font2.getsize(line)
                x = (image_width - line_width) / 2
                d.text((x, y), line, fill='white', font=font2, stroke_width=stroke_width, stroke_fill='black')
                y += line_height
        frames_ammount = 0
        frames = []
        need_resize = False
        # Нужно ли ресайзить
        if image_height_old < 500 or image_width_old < 500:
            if can_resize:
                need_resize = True
        # Вставляем текст канвас в каждый кадр
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert('RGBA')
            frames_ammount += 1

            if need_resize == True:
                frame = frame.resize((image_width, image_height), Image.NEAREST)

            frame.paste(text_canvas, (0, 0), text_canvas)
            frames.append(frame)
            del frame
        del text_canvas
        del im
        # сохраняем кал
        if frames_ammount > 1:
            if rt_bytes:
                byte_io = BytesIO()
                frames[0].save(byte_io, format="GIF", save_all=True, quality=95, append_images=frames[1:])
                contents = byte_io.getvalue()
                return contents
            else:
                frames[0].save(RESULT_FILENAME + ".gif", format="GIF", save_all=True, quality=95,
                               append_images=frames[1:])
                return "successful"
        else:
            if rt_bytes:
                byte_io = BytesIO()
                frames[0].save(byte_io, format="PNG", quality=90)
                contents = byte_io.getvalue()
                return contents
            else:
                frames[0].save(RESULT_FILENAME + ".png", quality=90)
                return "successful"
            return "successful"
    """FOR BIG GIFS, IMAGES
    EATS ~100 mb ram, when advice_fast ~1000 mb ram
    AND THIS METHOD WORK SLOWLY"""
    def advice_slow(path, bottom_text, top_text="", font_path='./fonts/impact/impact.ttf', font_size=9,
               stroke_width=3, url=False, RESULT_FILENAME="temp", TEMP_FOLDER="temp", watermark=None, gt_bytes=False, can_resize=True):
        options = ""
        if url:
            path = requests.get(path).content
            try:
                image = pyvips.Image.new_from_buffer(path, options="n=-1")
                options = "n=-1"
            except:
                image = pyvips.Image.new_from_buffer(path, "")
                options = "n=-1"
            path = BytesIO(path)
        elif gt_bytes:
            path = BytesIO(path)
            try:
                image = pyvips.Image.new_from_buffer(path, options="n=-1")
                options = "n=-1"
            except:
                image = pyvips.Image.new_from_buffer(path, "")
        else:
            try:
                image = pyvips.Image.new_from_file(path, access="sequential", n=-1)
                options = "n=-1"
            except:
                image = pyvips.Image.new_from_file(path, access="sequential")
        loader = image.get("vips-loader").split("_")[0]
        image.get("vips-loader")
        print(loader)
        #options = ""
        #if loader == "gifload" or loader == "webpload":
            # an animated format -- make a thumbnail of all frames
            #options = "n=-1"
        # грузим фото
        im = Image.open(path)
        image_width_old, image_height_old = im.size
        print(image_height_old)
        if image_height_old < 500 or image_width_old < 500:
            image_width = image_width_old * 2
            image_height = image_height_old * 2
        else:
            image_width = image_width_old
            image_height = image_height_old
        # грузим шрифт (хихи грузин)
        fontSize = int(image_height * font_size) // 100
        fontSize2 = int(image_height * font_size) // 100
        font = ImageFont.truetype(font=font_path, size=fontSize)
        font2 = ImageFont.truetype(font=font_path, size=fontSize)

        # делаем текст CAPSLOCK
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()

        # первоначальный перенос текста
        char_width, char_height = font.getsize('A')
        chars_per_line = image_width // char_width
        top_lines = textwrap.wrap(top_text, width=chars_per_line)

        char_width2, char_height2 = font2.getsize('A')
        chars_per_line2 = image_width // char_width2
        bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line2)

        # если многа текста
        ammount_top = len(top_lines)
        ammount_bottom = len(bottom_lines)
        if char_height * ammount_top > image_height // 2.5:
            while char_height * ammount_top > image_height // 2.5:
                fontSize = fontSize - 1
                font = ImageFont.truetype(font=font_path, size=fontSize)
                char_width, char_height = font.getsize('A')
                chars_per_line = image_width // char_width
                top_lines = textwrap.wrap(top_text, width=chars_per_line)
                ammount_top = len(top_lines)
        if char_height2 * ammount_bottom > image_height // 2.5:
            while char_height2 * ammount_bottom > image_height // 2.5:
                fontSize2 = fontSize2 - 1
                font2 = ImageFont.truetype(font=font_path, size=fontSize2)
                char_width2, char_height2 = font2.getsize('A')
                chars_per_line2 = image_width // char_width2
                bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line2)
                ammount_bottom = len(bottom_lines)

        #делаем текст канвас для ускорения генерации гиф
        text_canvas = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(text_canvas)
        if top_text != None:
            # ебашим верх строку
            y = char_height2 // 2
            for line in top_lines:
                line_width, line_height = font.getsize(line)
                x = (image_width - line_width) / 2
                d.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
                y += line_height
        if bottom_text != None:
            # ебашим нижнюю строку
            y = image_height - char_height2 * len(bottom_lines) - char_height2 // 2
            for line in bottom_lines:
                line_width, line_height = font2.getsize(line)
                x = (image_width - line_width) / 2
                d.text((x, y), line, fill='white', font=font2, stroke_width=stroke_width, stroke_fill='black')
                y += line_height

        byte_io = BytesIO()
        text_canvas.save(byte_io, format="PNG", quality=90)
        text_image = pyvips.Image.new_from_buffer(byte_io.getvalue(), "")
        del im
        del text_canvas
        if options != "n=-1":
            save_file = RESULT_FILENAME
        else:
            prefix = "GIF"
            save_file = RESULT_FILENAME + "." + prefix
        print(save_file)
        need_resize = False
        if image_width_old < 500 or image_height_old < 500:
            if can_resize:
                need_resize = True
        print(image.get("format"))
        if options == "n=-1":
            print(image.get_fields())
            page_height = image.get("page-height")
            n_pages = image.height // page_height
            print(n_pages)
            # cut into pages
            pages = [image.crop(0, p * page_height, image.width, page_height)
                     for p in range(n_pages)]
            dur = image.get("delay")
            print(image.get("filename"))
            del image
            print("кроп")
            if need_resize == True:
                pages = [page.resize(2, kernel = "linear")
                         for page in pages]
            print("кроп ок")
            print("запись")
            path_to_save = f"{TEMP_FOLDER}/"
            try:
                mkdir(path_to_save)
            except OSError:
                print("folder is exist already!")
            imageprefix = 1
            path_to_save = path_to_save + "image"
            print(path_to_save)
            for page in pages:
                frame = page.composite(text_image, "over", x=0, y=0)
                aboba = str(path_to_save) + str(imageprefix) + ".jpg"
                frame.write_to_file(aboba)
                imageprefix += 1
            fps = 1000 / dur[0]
            print(system(f"ffmpeg -f image2 -framerate {fps} -y -i {path_to_save}%d.jpg {RESULT_FILENAME}.gif"))
            #with imageio.get_writer(save_file, format=prefix, fps = 1000 / dur[0]) as writer:
                #for page in pages:
                    #frame = page.composite(text_image, "over", x=0, y=0)
                    #writer.append_data(imageio.imread(frame.write_to_buffer('.png', Q=95)))
                    #del frame
                    #del page
            #system(f"rm -rf {path_to_save}")
            #shutil.rmtree(f'/{TEMP_FOLDER}/{RESULT_FILENAME}', ignore_errors=True)
            #system(f"rd /s /q *.{path_to_save}")
            print("запись ок")
        else:
            if need_resize == True:
                image = image.resize(2, kernel = "linear")
            print("тхере")
            image = image.composite(text_image, "over", x=0, y=0)
            image.write_to_file(save_file  + "." + "png")

    if __name__ == '__main__':
        top_text = input(">top_text: ")
        bottom_text = input(">bottom_text: ")
        path = input(">path: ")
        advice_slow(path, bottom_text=bottom_text, top_text=top_text,
             url=False, watermark=None, TEMP_FOLDER="./convert/temp")
        
