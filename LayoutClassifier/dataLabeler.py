import tkinter as tk
from PIL import Image, ImageTk
import os
import fitz
import json

class ImageLabelingApp:
    def __init__(self, root, data_folder):
        self.root = root
        self.data_folder = data_folder
        self.file_list = [file for file in os.listdir(data_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]
        self.current_file_index = 0
        self.current_page = 0
        self.total_pages = 0

        self.label_var = tk.StringVar()
        self.label_var.set("")
        self.bbox_start = None
        self.bbox_end = None
        self.bboxes = []
        self.labels = ["Title", "Subtitle", "Paragraph", "Table", "Other"]
        self.color_map = {
            "Title": "red",
            "Subtitle": "blue",
            "Paragraph": "green",
            "Table": "orange",
            "Other": "purple"
        }

        self.create_widgets()
        

    def create_widgets(self):
        # Label selection buttons
        self.label_buttons = []
        
        for i, label in enumerate(self.labels):
            button = tk.Button(self.root, text=label, command=lambda i=i: self.set_label(i + 1))
            button.pack(side="left")
            self.label_buttons.append(button)

        # Canvas for drawing bounding boxes
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        # Navigation buttons
        self.prev_page_button = tk.Button(self.root, text="Previous Page", command=self.prev_page)
        self.prev_page_button.pack(side="left")

        self.next_page_button = tk.Button(self.root, text="Next Page", command=self.next_page)
        self.next_page_button.pack(side="right")

        # Buttons
        self.next_file_button = tk.Button(self.root, text="Next File", command=self.next_file)
        self.next_file_button.pack()

        self.clear_page_button = tk.Button(self.root, text="Clear Labels for Page", command=self.clear_page_labels)
        self.clear_page_button.pack()

        # Load the first file (image or PDF)
        self.load_file()

        # Mouse bindings for bounding box drawing
        self.canvas.bind("<ButtonPress-1>", self.on_bounding_box_start)
        self.canvas.bind("<B1-Motion>", self.on_bounding_box_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_bounding_box_end)

    def load_file(self):
        current_file = self.file_list[self.current_file_index]
        file_path = os.path.join(self.data_folder, current_file)

        if current_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Load image
            self.image = Image.open(file_path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

            # Draw existing bounding boxes
            for bbox_info in self.bboxes:
                label_id, bbox_coords = bbox_info
                x1, y1, x2, y2 = bbox_coords
                color = self.color_map.get(self.labels[int(label_id) - 1], '')
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.labels[int(label_id) - 1], fill="red")

                # Draw the filled rectangle below the bottom right corner with the class color
                text_x = max(x1, x2) - 100
                text_y = max(y1, y2)
                text_width = 100  
                text_height = 20 
                self.canvas.create_rectangle(text_x, text_y, text_x + text_width, text_y + text_height, fill=color)

                # Draw the text label below the filled rectangle
                text_label = self.labels[int(label_id) - 1]
                self.canvas.create_text(text_x + text_width // 2, text_y + (text_height/2), text=text_label, fill="black")

        elif current_file.lower().endswith('.pdf'):
            # Load PDF
            pdf_doc = fitz.open(file_path)
            self.total_pages = pdf_doc.page_count
            self.load_pdf_page()

    def load_pdf_page(self):
        pdf_doc = fitz.open(os.path.join(self.data_folder, self.file_list[self.current_file_index]))
        pdf_page = pdf_doc[self.current_page]
        pix = pdf_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Draw existing bounding boxes
        for bbox_info in self.bboxes:
            label_id, bbox_coords = bbox_info
            x1, y1, x2, y2 = bbox_coords
            color = self.color_map.get(self.labels[int(label_id) - 1], '')
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.labels[int(label_id) - 1], fill="red")

            # Draw the filled rectangle below the bottom right corner with the class color
            text_x = max(x1, x2) - 100
            text_y = max(y1, y2)
            text_width = 100 
            text_height = 20 
            self.canvas.create_rectangle(text_x, text_y, text_x + text_width, text_y + text_height, fill=color)

            # Draw the text label below the filled rectangle
            text_label = self.labels[int(label_id) - 1]
            self.canvas.create_text(text_x + text_width // 2, text_y + (text_height/2), text=text_label, fill="black")

    def set_label(self, label_id):
        self.label_var.set(label_id)

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.save_bounding_boxes()
            self.current_page += 1
            self.clear_canvas()
            self.clear_page_labels()
            self.load_pdf_page()
            self.bboxes = []

    def prev_page(self):
        if self.current_page > 0:
            self.save_bounding_boxes()
            self.current_page -= 1
            self.clear_canvas()
            self.clear_page_labels()
            self.load_pdf_page()
            self.bboxes = []

    def next_file(self):
        self.save_bounding_boxes()
        self.current_file_index += 1
        self.current_page = 0

        if self.current_file_index < len(self.file_list):
            self.label_var.set("")
            self.bbox_start = None
            self.bbox_end = None
            self.clear_canvas()
            self.clear_page_labels()
            self.load_file()
        else:
            self.label_var.set("Labeling Complete!")

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_page_labels(self):
        self.bbox_start = None
        self.bbox_end = None
        self.bboxes = []
        self.clear_canvas()
        self.load_file()

    def save_bounding_boxes(self):
        label_id = self.label_var.get()
        if label_id and self.bbox_start and self.bbox_end:
            bbox_coords = (self.bbox_start[0], self.bbox_start[1], self.bbox_end[0], self.bbox_end[1])
            self.bboxes.append((label_id, bbox_coords))
            self.save_to_json()

    def save_to_json(self):
        current_file = self.file_list[self.current_file_index]
        json_file_name = os.path.splitext(current_file)[0] + "_labels.json"
        json_file_path = os.path.join("ocrPipeline/trainingLabels", json_file_name)

        label_id = self.label_var.get()
        if label_id and self.bbox_start and self.bbox_end:
            bbox_coords = (self.bbox_start[0], self.bbox_start[1], self.bbox_end[0], self.bbox_end[1])
            self.bboxes.append((label_id, bbox_coords))

        json_data = []
        for bbox_info in self.bboxes:
            label_id, bbox_coords = bbox_info
            label_text = self.labels[int(label_id) - 1]
            color = self.color_map.get(label_text, "black")
            json_data.append({
                "fileName": current_file,
                "page": self.current_page + 1,
                "textPos": [
                    {"label": label_text, "boxCoords": bbox_coords, "color": color}
                ]
            })

        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)


    def on_bounding_box_start(self, event):
        self.bbox_start = (event.x, event.y)

    def on_bounding_box_drag(self, event):
        if self.bbox_start:
            self.bbox_end = (event.x, event.y)
            self.clear_canvas()
            self.load_pdf_page()

            # Draw existing bounding boxes
            for bbox_info in self.bboxes:
                label_id, bbox_coords = bbox_info
                x1, y1, x2, y2 = bbox_coords
                color = self.color_map.get(self.labels[int(label_id) - 1], 'black')
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=color)
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.labels[int(label_id) - 1], fill="red")

            label_id = self.label_var.get()
            color = self.color_map.get(self.labels[int(label_id) - 1], 'black')

            # Draw the current bounding box
            self.canvas.create_rectangle(self.bbox_start[0], self.bbox_start[1], self.bbox_end[0], self.bbox_end[1], outline=color)

            # Draw the filled rectangle below the bottom right corner with the class color
            text_x = max(self.bbox_start[0], self.bbox_end[0]) - 100
            text_y = max(self.bbox_start[1], self.bbox_end[1])
            text_width = 100 
            text_height = 20 
            self.canvas.create_rectangle(text_x, text_y, text_x + text_width, text_y + text_height, fill=color)

            # Draw the text label below the filled rectangle
            try: 
               text_label = self.labels[int(label_id) - 1]
            except:
               text_label = "" 
            self.canvas.create_text(text_x + text_width // 2, text_y + text_height, text=text_label, fill="black")

    def on_bounding_box_end(self, event):
        if self.bbox_start:
            self.bbox_end = (event.x, event.y)
            label_id = self.label_var.get()
            if label_id:
                bbox_coords = (self.bbox_start[0], self.bbox_start[1], self.bbox_end[0], self.bbox_end[1])
                self.bboxes.append((label_id, bbox_coords))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingApp(root, "data/")
    root.mainloop()
