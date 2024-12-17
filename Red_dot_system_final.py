import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math

class RedDotSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Dot System")

        # Canvas setup
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Buttons for functionality
        self.upload_button = tk.Button(root, text="Upload X-ray Image", command=self.upload_image)
        self.upload_button.pack(side=tk.LEFT)

        self.red_dot_button = tk.Button(root, text="Place Red Dot", command=self.enable_red_dot_mode)
        self.red_dot_button.pack(side=tk.LEFT)

        self.arrow_button = tk.Button(root, text="Draw Arrow", command=self.enable_arrow_mode)
        self.arrow_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(root, text="Save Annotated Image", command=self.save_project)
        self.save_button.pack(side=tk.LEFT)

        # Text box for pathology comments
        self.text_box = tk.Text(root, height=2, width=70)  # Increased length
        self.text_box.pack(side=tk.RIGHT)

        # Image and drawing setup
        self.original_image = None
        self.display_image = None
        self.annotated_image = None
        self.photo_image = None
        self.image_position = (0, 0)
        self.image_scale = 1.0
        self.current_mode = None
        self.temp_arrow = None  # Used for temporary arrow drawing

        # Annotations storage
        self.annotations = {"red_dots": [], "arrows": []}

        # Canvas event bindings
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.arrow_draw)
        self.canvas.bind("<ButtonRelease-1>", self.arrow_end)

    def upload_image(self):
        """Upload and display the X-ray image."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            try:
                # Load the original image
                self.original_image = Image.open(file_path)

                # Resize and center the image
                self.display_image = self.resize_and_center_image(self.original_image)
                self.annotated_image = self.original_image.copy()  # Start with a copy for annotations

                # Calculate the image scaling factor
                self.image_scale = self.display_image.width / self.original_image.width
                self.image_position = self.calculate_center_position(self.display_image)

                # Display the image
                self.display_image_on_canvas()

            except Exception as e:
                messagebox.showerror("Error", f"Unable to load image: {e}")

    def calculate_center_position(self, image):
        """Calculate the top-left position to center the image on the canvas."""
        x_position = (self.canvas_width - image.width) // 2
        y_position = (self.canvas_height - image.height) // 2
        return x_position, y_position

    def resize_and_center_image(self, image):
        """Resize the image to fit the canvas while maintaining aspect ratio."""
        img_width, img_height = image.size
        canvas_ratio = self.canvas_width / self.canvas_height
        img_ratio = img_width / img_height

        if img_ratio > canvas_ratio:
            new_width = self.canvas_width
            new_height = int(self.canvas_width / img_ratio)
        else:
            new_height = self.canvas_height
            new_width = int(self.canvas_height * img_ratio)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def display_image_on_canvas(self):
        """Display the image on the canvas."""
        try:
            self.photo_image = ImageTk.PhotoImage(self.display_image)
            self.canvas.delete("all")  # Clear the canvas before drawing
            self.canvas.create_image(self.image_position[0], self.image_position[1], image=self.photo_image, anchor=tk.NW)
            self.draw_annotations()

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {e}")

    def draw_annotations(self):
        """Draw red dots and arrows on the image."""
        for dot in self.annotations["red_dots"]:
            x, y, r = dot
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")

        for arrow in self.annotations["arrows"]:
            self.canvas.create_line(arrow[0], arrow[1], arrow[2], arrow[3], arrow=tk.LAST, fill="red", width=3)

    def enable_red_dot_mode(self):
        """Enable red dot placement mode"""
        self.current_mode = "red_dot"

    def enable_arrow_mode(self):
        """Enable arrow drawing mode"""
        self.current_mode = "arrow"
        self.temp_arrow = [0, 0, 0, 0]

    def canvas_click(self, event):
        """Handle mouse click events on the canvas."""
        if self.current_mode == "red_dot":
            self.place_red_dot(event)
        elif self.current_mode == "arrow":
            self.temp_arrow = [event.x, event.y, event.x, event.y]  # Start arrow

    def place_red_dot(self, event):
        """Place a red dot at the clicked position."""
        red_dot_radius = 18.9  # 1cm radius in pixels
        
        # Add the red dot to annotations
        self.annotations["red_dots"].append((event.x, event.y, red_dot_radius))
        self.display_image_on_canvas()
            
    def arrow_draw(self, event):
        """Draw the arrow dynamically as the mouse moves."""
        if self.current_mode == "arrow" and self.temp_arrow:
            self.temp_arrow[2], self.temp_arrow[3] = event.x, event.y
            self.display_image_on_canvas()

    def arrow_end(self, event):
        """Finalize the arrow once the mouse button is released."""
        if self.current_mode == "arrow" and self.temp_arrow:
            self.temp_arrow[2], self.temp_arrow[3] = event.x, event.y
            self.annotations["arrows"].append(tuple(self.temp_arrow))
            self.temp_arrow = None
            self.display_image_on_canvas()

    def save_project(self):
        """Save the annotated image with the same name as the original file."""
        if self.annotated_image and self.original_image:
            # Define the target folder
            target_folder = "reddot/Annotated_images"
            os.makedirs(target_folder, exist_ok=True)

            # Use the same filename as the original image
            original_filename = os.path.basename(self.original_image.filename)
            annotated_filename = os.path.splitext(original_filename)[0] + "_annotated.png"
            file_path = os.path.join(target_folder, annotated_filename)

            try:
                # Save the annotated image
                self.save_annotated_image(file_path)
                messagebox.showinfo("Saved", f"Annotated image saved as:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving annotated image: {e}")
        else:
            messagebox.showerror("Error", "No image to save or no original image loaded.")

    def save_annotated_image(self, file_path):
        """Save the image with red dots, arrows, arrowheads, and text."""
        image = self.annotated_image.copy()
        draw = ImageDraw.Draw(image)

        # Draw white background for text box in the lower right corner
        text = self.text_box.get("1.0", tk.END).strip()
        font = ImageFont.truetype("arial.ttf", 20)
        text_box_width = 400
        text_box_height = 40
        text_x = image.width - text_box_width - 10
        text_y = image.height - text_box_height

        draw.rectangle((text_x, text_y, text_x + text_box_width, text_y + text_box_height), fill="white")
        draw.text((text_x + 10, text_y + 10), text, font=font, fill="black")

        # Transform coordinates based on the scaling factor and image position
        scale_factor = self.image_scale
        offset_x, offset_y = self.image_position

        # Draw red dots
        for dot in self.annotations["red_dots"]:
            x, y, r = dot
            # Transform the canvas coordinates to image coordinates
            img_x = (x - offset_x) / scale_factor
            img_y = (y - offset_y) / scale_factor
            img_r = r / scale_factor
            draw.ellipse((img_x - img_r, img_y - img_r, img_x + img_r, img_y + img_r), fill="red")

        # Draw arrows with arrowheads
        for arrow in self.annotations["arrows"]:
            x1, y1, x2, y2 = arrow
            # Transform the canvas coordinates to image coordinates
            img_x1 = (x1 - offset_x) / scale_factor
            img_y1 = (y1 - offset_y) / scale_factor
            img_x2 = (x2 - offset_x) / scale_factor
            img_y2 = (y2 - offset_y) / scale_factor
            draw.line((img_x1, img_y1, img_x2, img_y2), fill="red", width=3)
            self.draw_arrow_head(draw, (img_x1, img_y1, img_x2, img_y2))

            # Save the image
            image.save(file_path, "PNG")

    def draw_arrow_head(self, draw, arrow):
        """Draw an arrowhead for the given arrow."""
        x1, y1, x2, y2 = arrow
        arrow_length = 15
        arrow_angle = 20
        
        line_angle = math.atan2(y2 - y1, x2 - x1)
        left_angle = line_angle + math.radians(arrow_angle)
        left_x = x2 - arrow_length * math.cos(left_angle)
        left_y = y2 - arrow_length * math.sin(left_angle)

        right_angle = line_angle - math.radians(arrow_angle)
        right_x = x2 - arrow_length * math.cos(right_angle)
        right_y = y2 - arrow_length * math.sin(right_angle)

        draw.polygon([(x2, y2), (left_x, left_y), (right_x, right_y)], fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedDotSystem(root)
    root.mainloop()