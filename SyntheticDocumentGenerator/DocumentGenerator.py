import matplotlib.pyplot as plt
import numpy as np
import json
import random
import os

DOCUMENT_OUTPUT_PATH = 'data/synthetic/'
DOCUMENT_LABELS_OUTPUT_PATH = 'data/synthetic/labels/'
TITLE_FONT_SIZE = 32
SUBTITLE_FONT_SIZE = 16

def generate_synthetic_document(min_x=600, min_y=800, max_x =1000, max_y=1600, min_margin=5, max_margin =20, amount=10,
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
                start_y = j * section_height + margin[1] + TITLE_FONT_SIZE
                end_y = (j + 1) * section_height 

                draw_title(image, 
                           x0=margin[0], y0= j * section_height + margin[1], 
                           x1= random.randint(30,img_size[0]), y1= j * section_height +TITLE_FONT_SIZE,
                           color=debug_title_color)
            else:
                start_y = j * section_height + margin[1]
                end_y = (j + 1) * section_height 

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
                        x1= random.randint(start_x + 1,end_x), y1=start_y +SUBTITLE_FONT_SIZE,
                        color=debug_subtitle_color)
                else:        
                     image[start_y:end_y, start_x:end_x, :] = section_color
                 

        save_image(image, str(i))

def draw_title(image, x0, y0, x1, y1=TITLE_FONT_SIZE, color = (230, 40, 15)):
    image[y0:y1, x0:x1, :] = color

def save_image(image, filename):
    fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100), dpi=100)
    ax.imshow(image)
    ax.axis('off')
    plt.savefig(DOCUMENT_OUTPUT_PATH + filename + '.png', bbox_inches='tight', pad_inches=0)
    plt.close()

if __name__ == '__main__':
    generate_synthetic_document()    