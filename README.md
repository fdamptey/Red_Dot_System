# PROJECT TOPIC: A PYTHON CODE TO DEMONSTRATE DIGITAL RED DOT SYSTEM IN GENERAL RADIOGRAPHY

# Overview
The project was to demonstrate Red Dot System in general radiography practice where a radiographer/technologist places a red dot on an x-ray image (radiograph) with acute abnormal finding, and writes a brief comment to describe  the abnormality. This practice assists doctors and other healthcare givers to diagnose diseases on x-rays and initiate interventions in acute situations when a radiologist/specialist is not readily available to write a report or give diagnoses. If it is correctly done, it also saves radiologists time by focusing on problem images and areas on the image when writing their reports. 
The aim of this project is to write a python program to make the system digital. 

# How The Program Will Run
The code combines digital image processing and GUI. When the program is executed, a frame/window with a canvass and widgets containing buttons and a text box is created, allowing the user to upload an X-ray image, which is displayed in the Tkinter canvass. The user can place a small solid red ellipse on the image, use arrows to point to the observed acute abnormality, and write a comment of the observation in a text box which is present below gthe lower right side of the image. The annotated image and text comment is then saved as a png file.

# Key Functions
Define the class RedDotSystem containing several methods that define the behaviour of GUI, and initialize using __init__. 
Frame/Window setup: Tkinter to set up the frame, create buttons, and define the canvas for displaying an image.
Widget features include upload image, place red dot, draw arrows, save project and a textbox for the comment, which allow image upload, placement of solid red dots, drawing of arrows, writing of comments in a text box and saving the resultant image.
Digital image processing: PIL used to process digital image.
Image resizing and centering: Math module for image resizing and centering on canvass using aspect ratio. 
os module: For file handling.
Saving project: Annotated image with comments is saved as a PNG file by clicking on save annotated file function on canvass.

# Installations/Resources
Python VSCode
Tkinter
PIL
Math
os

# Acknowledgement
I want to thank Professor Zhou for his help and support with this project. This is my first big Python project, and his positive feedback has made me feel confident. I'm especially grateful for his kind words and encouragement, which is motivating me to do my best in my field.
