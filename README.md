<a href="https://linkedin.com/in/2vin"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></img></a>
<a href="https://connect.vin"><img src="https://img.shields.io/badge/website-FF6A00?style=for-the-badge&logo=About.me&logoColor=white"></img></a>

# PyYAT
Semi-Automatic Yolo Annotation Tool In Python

Using this tool, we can annotate bounding boxes for image annotation in YOLO format. 
It uses YOLOv3-608 weights to pre-annotate the bounding boxes in images. It reduces time and efforts in annotating large datasets by upto 90%.

## About the repository
* 'yolo_annotation_tool.py' : Main file to load images one-by-one from the dataset, and then annotate them.
* 'recognize_objects.py' : Object recognition class for pre-annotating images before manual annotation process.
* 'config.ini' : Edit data folder, output folder and label file path according to your preference. 'annotation_index' is automatically updated based on index of the last saved annotated image.
* 'labels.csv' : List of all the classes to be annotated.
* '/models' : It contains YOLOv3-608 weights (to be downloaded), cfg and coco.names files.
* '/data' : Sample of input images to be annotated
* '/output' : Sample of output files after annotation.

## Usage:
```
python yolo_annotation_tool.py
```
## Key buttons:
* 'S' : Save annotations
* 'L' : Change current class of labeling
* 'Esc' :  Exit the code

## Input images

<table>
  <tr>
    <td>Image 1</td>
     <td>Image 2</td>
     <td>Image 3</td>
  </tr>
  <tr>
    <td><img src="https://github.com/2vin/PyYAT/blob/master/data/1.jpg" width=320 height=240></td>
    <td><img src="https://github.com/2vin/PyYAT/blob/master/data/2.jpg" width=320 height=240></td>
    <td><img src="https://github.com/2vin/PyYAT/blob/master/data/3.jpeg" width=320 height=240></td>
  </tr>
 </table>


## Output images (Pre-annotation)

<table>
  <tr>
    <td>Image 1</td>
     <td>Image 2</td>
     <td>Image 3</td>
  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/38634222/175885476-e8b33fb0-f2be-4a4e-b1fc-ae493e03e85b.png" width=320 height=240></td>
    <td><img src="https://user-images.githubusercontent.com/38634222/175885461-93b0fafe-e135-4a76-9b6a-416de9a4513a.png" width=320 height=240></td>
    <td><img src="https://user-images.githubusercontent.com/38634222/175885482-baf10681-6ef5-45b5-873d-c4304e8fea73.png" width=320 height=240></td>
  </tr>
 </table>

