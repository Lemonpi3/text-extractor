import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg

from PIL import Image

import numpy as np
import markdown
import json
import random
import os

DOCUMENT_OUTPUT_PATH = 'data/synthetic/'
DOCUMENT_LABELS_OUTPUT_PATH = 'data/synthetic/labels/'
FONT_SIZE = 3
TITLE_FONT_SIZE = 3
SUBTITLE_FONT_SIZE = 3
PH_TITLE = "this is a title text*"
PH_SUBTITLE = "this is a subtitle text*"
PH_PARAGRAPH = """
Brookesia thieli, commonly known as Domergue's leaf chameleon, is a species of lizard in the chameleon family, Chamaeleonidae.
The species is endemic to eastern Madagascar. It was first described in 1969 by Édouard-Raoul Brygoo and Charles Antoine Domergue. 
This B. thieli lizard was photographed on a leaf in Andasibe, Madagascar.
"""
SECTION_TEXT_HEIGHT = 100
TITLE_TEXT_HEIGHT = 100
SUBTITLE_TEXT_HEIGHT = 100

def generate_synthetic_document(min_x=600, min_y=800, max_x =1000, max_y=1600, min_margin=0, max_margin =1, amount=10,
                                max_vertical_sections=5, max_horizontal_sections=5):

    debug_section_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    debug_title_color = (100, 40, 15)
    debug_subtitle_color = (130, 140, 15)

    for i in range(amount):

        img_size = (random.randint(min_x, max_x), random.randint(min_y, max_y))
        image = np.ones((img_size[1], img_size[0], 3), dtype=np.uint8) * 255
        
        margin = (random.randint(min_margin, max_margin) , random.randint(min_margin, max_margin))
        vertical_sections = random.randint(1, max_vertical_sections)
        section_height = img_size[1] // vertical_sections
        
        for j in range(vertical_sections):
            has_title = random.choice([True, False])
            if has_title:
                start_y = j * section_height + margin[1] // 2 + TITLE_FONT_SIZE
                end_y = (j + 1) * section_height - margin[1] // 2

                draw_title(image, 
                           x0=margin[0], y0= j * section_height + margin[1], 
                           x1= img_size[0], y1= j * section_height + TITLE_FONT_SIZE,
                           text=PH_TITLE, color=debug_title_color, text_height=TITLE_TEXT_HEIGHT // vertical_sections )
            else:
                start_y = j * section_height + margin[1] // 2
                end_y = (j + 1) * section_height - margin[1] // 2

            horizontal_sections = random.randint(1, max_horizontal_sections)
            section_width = img_size[0] // horizontal_sections

            for k in range(horizontal_sections):
                has_sub_title = random.choice([True, False])
                section_color = random.choice(debug_section_colors)
                start_x = k * section_width + margin[0] // 2
                end_x = (k + 1) * section_width - margin[0] // 2
                
                if has_sub_title:
                    image[start_y + SUBTITLE_FONT_SIZE:end_y, start_x:end_x, :] = section_color
                    draw_title(image, 
                        x0=start_x, y0= start_y, 
                        x1= end_x, y1=start_y +SUBTITLE_FONT_SIZE,
                        text=PH_SUBTITLE, color=debug_subtitle_color, text_height=SUBTITLE_TEXT_HEIGHT // vertical_sections)
                else:    
                    text_image = draw_text_section(start_x, start_y, end_x, end_y, text= PH_PARAGRAPH, font_size=FONT_SIZE, text_height= SECTION_TEXT_HEIGHT // vertical_sections)
                    image[start_y:end_y, start_x:end_x, :] = text_image
                 

        save_image(image, str(i))


def draw_title(image, x0, y0, x1, y1=TITLE_FONT_SIZE, text = '', color = (230, 40, 15), text_height=100, bold=True):
    image[y0:y1, x0:x1, :] =  draw_text_section(x0, y0, x1, y1, text= text, font_size=y1, text_height=text_height, bold=bold)



def draw_text_section(min_x, min_y, max_x, max_y, text, font_size, color=(0, 0, 0), bold=False, text_height=100):
    html_text = text #PH having trouble with matplotlib to recognize markdown

    aspect_ratio = (max_x - min_x) / (max_y - min_y)
    # Set a fixed text height
    text_height = 10

    # Calculate the text width based on the aspect ratio
    text_width = int(aspect_ratio * text_height)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=((max_x - min_x)/1000,  (max_y - min_y)/1000), dpi=1000)

    # Add a rectangle to represent the bounding box without an outline
    rect = Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, linewidth=0, edgecolor='none', facecolor='none')
    ax.add_patch(rect)

    # Set axis limits based on the bounding box
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Set the text properties
    text_properties = {'verticalalignment': 'top', 'horizontalalignment': 'left', 'fontsize': font_size, 'color': color}
    if bold:
        text_properties['weight'] = 'bold'

    ax.text(min_x, max_y, html_text, **text_properties,ha='left', wrap=True)

    ax.axis('off')

    # Draw the figure on a canvas
    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    # Extract the image array from the canvas
    text_image = np.array(canvas.renderer.buffer_rgba())

    plt.close(fig)

    target_shape = (max_y - min_y, max_x - min_x)
    if text_image.shape[:2] != target_shape:
        text_image = resize_image(text_image, target_shape)

    return text_image[:, :, :3]

def resize_image(image, target_shape):
    image = image[:, :, :3]

    text_image = Image.fromarray(image)
    text_image = text_image.resize(target_shape[::-1], Image.LANCZOS)
    text_image = np.array(text_image)
    return text_image

def save_image(image, filename):
    dpi = 100
    fig, ax = plt.subplots(figsize=(image.shape[1] / dpi, image.shape[0] / dpi), dpi=dpi)
    ax.imshow(image)
    plt.axis('off')
    plt.savefig(DOCUMENT_OUTPUT_PATH + filename + '.png', bbox_inches='tight', pad_inches=0)
    plt.close()

if __name__ == '__main__':
    generate_synthetic_document()    