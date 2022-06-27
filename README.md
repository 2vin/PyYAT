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

