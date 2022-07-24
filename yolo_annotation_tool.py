import os
import cv2
import subprocess
import threading
import csv
from recognize_objects import recognize_objects


import configparser
parser = configparser.ConfigParser()
parser.read('config.ini')

data_folder = parser['Settings']['data_folder']
annotation_index = parser['Settings']['annotation_index']
label_file = parser['Settings']['label_file']
output_folder = parser['Settings']['output_folder']

data_folder = data_folder
annotation_index = int(annotation_index)

all_labels = []

ob = recognize_objects("./models/yolov3.weights", "./models/yolov3.cfg","./models/coco.names")

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255),
			(255, 100, 0), (255, 255, 100), (0, 255, 100), (50, 255, 255), (50, 0, 255), (255, 50, 255),
			(255, 50, 0), (255, 255, 50), (100, 255, 0), (100, 255, 255), (0, 100, 255), (255, 100, 255),
			(255, 0, 100), (255, 255, 150), (50, 255, 50), (150, 255, 255), (0, 50, 255), (255, 150, 255)
			]  


def get_all_images(dir):
	list_of_images = []
	for x in os.listdir(dir):
	    if x.endswith(".png") or x.endswith(".jpeg")  or x.endswith(".jpg") :
	        list_of_images.append(str(dir)+str(x))
	return list_of_images

def get_one_image(list_of_images, annotation_index):
	return cv2.imread(list_of_images[annotation_index])

def show_image(frame):
	cv2.imshow("Annotation Tool", frame)
	cv2.waitKey(0)

def list_of_labels():
	if all_labels == []:
		with open(label_file, mode ='r')as file:
			# reading the CSV file
			csvFile = csv.reader(file)
			# displaying the contents of the CSV file
			for lines in csvFile:
				lines = str(lines)
				lines = lines.replace("['", "")
				lines = lines.replace("']", "")
				all_labels.append(lines)

	return all_labels

def get_label():
	ind= 1
	labels = ""
	with open(label_file, mode ='r')as file:
		# reading the CSV file
		csvFile = csv.reader(file)
		# displaying the contents of the CSV file
		for lines in csvFile:
			lines = str(lines)
			lines = lines.replace("['", "")
			lines = lines.replace("']", "")
			labels = labels + " \"" + str(ind) + "\" \" " + str(lines) + "\""
			ind = ind + 1

	return(os.popen("zenity --list  --height 500 --title=\"Labels\" --column=\"Index\" --column=\"Label\""+labels).read())


def pre_annotate(frame, all_labels):
	ob_results = ob.process_frame(frame, all_labels, False)
	return ob_results


def convert_list_to_str(lst):
    return str(lst).translate(None, '[],\'')

def convert_boxes_to_yolo(yolo_boxes, frame):
	yolo_label = []
	for name, box in yolo_boxes:
		x = box[0][0]
		y = box[0][1]
		w = box[1][0] - box[0][0]
		h = box[1][1] - box[0][1]

		print( frame.shape)
		xc = float((x + w/2.0) / frame.shape[1])
		yc = float((y + h/2.0) / frame.shape[0])
		wc = float(w / frame.shape[1])
		hc = float(h / frame.shape[0])

		yolo_label.append(' '.join([str(all_labels.index(name)), str(xc), str(yc), str(wc), str(hc)]))
	return (yolo_label)

def save_annotation(frame, labels):
	output_dir = output_folder
	cv2.imwrite(output_dir+str(annotation_index)+".jpg", frame)
	file=open(output_dir+str(annotation_index)+".txt",'w')
	for items in labels:
	    file.writelines(items+'\n')
	file.close()

	print("Annotations saved as: ", labels)

	parser.set('Settings', 'annotation_index', str(annotation_index))
	fp=open('config.ini','w')
	parser.write(fp)
	fp.close()


is_clicked = 0
last_click = 0
start_point = []
stop_point = []

temp_point = []
mouse_point = [0,0]

current_label = 'person'
def get_mouse_click(event, x, y, flags, param):
	global is_clicked, last_click
	global start_point, stop_point, temp_point, mouse_point

	if event == cv2.EVENT_LBUTTONDOWN:
		is_clicked = 1
		if is_clicked != last_click:
			start_point = [x,y]
			last_click = is_clicked
			return start_point
	if event == cv2.EVENT_LBUTTONUP:
		is_clicked = 0
		if is_clicked != last_click:
			stop_point = [x,y]
			last_click = is_clicked
			return stop_point

	if start_point:
		temp_point = [x,y]

	mouse_point = [x,y]


def draw_boxes(frame, yolo_boxes, frame_orig):

	global is_clicked
	global start_point, stop_point, temp_point,mouse_point

	global annotation_index

	global current_label

	cv2.namedWindow(winname = "Image Annotations")
	cv2.setMouseCallback("Image Annotations", get_mouse_click)

	keep_running = 1

	while keep_running != 0:

		for name,boxes in yolo_boxes:
			cv2.rectangle(frame, (boxes[0][0],boxes[0][1]) , (boxes[1][0],boxes[1][1]), colors[list_of_labels().index(name)], 2)
			cv2.putText(frame, str(name), (boxes[0][0],boxes[0][1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[list_of_labels().index(name)], 1, cv2.LINE_AA)

		frame_temp = frame.copy()

		cv2.imshow("Image Annotations", frame)

		ch = cv2.waitKey(3)

		
		if mouse_point[0] > 0 and mouse_point[0] < frame_temp.shape[1] and mouse_point[1] > 0 and mouse_point[1] < frame_temp.shape[0]:
			cv2.line(frame_temp, (mouse_point[0], 0), (mouse_point[0], frame_temp.shape[0]), (0,255,255), 1)
			cv2.line(frame_temp, (0, mouse_point[1]), (frame_temp.shape[1], mouse_point[1]), (0,255,255), 1)

			cv2.rectangle(frame, (0,0), (150,15), (0, 0, 0), -1)
			cv2.putText(frame_temp, str(current_label), (5,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)

			cv2.imshow("Image Annotations", frame_temp)
			ch = cv2.waitKey(10)

		if start_point and temp_point:
			# print(start_point, temp_point)
			cv2.rectangle(frame_temp, (start_point[0],start_point[1]) , (temp_point[0], temp_point[1]), (255, 0, 0), 2)
			cv2.imshow("Image Annotations", frame_temp)
			ch = cv2.waitKey(10)

		if start_point and stop_point:
			# If there is atleast 10 pixels of distance movement
			if abs(start_point[0] - stop_point[0]) > 10:
				cv2.rectangle(frame, (start_point[0],start_point[1]), (stop_point[0], stop_point[1]), (255, 0, 255), 2)

				yolo_boxes.append([current_label, [(start_point[0],start_point[1]),(stop_point[0], stop_point[1])]])

			# Reset points for next box
			start_point =[]
			stop_point =[]
			temp_point = []
			

		if ch == ord('s'):
			print("Saved")
			annotation_index = annotation_index+1

			yolo_labels = convert_boxes_to_yolo(yolo_boxes, frame)

			save_annotation(frame_orig, yolo_labels)

			print(yolo_labels)
			break

		elif ch == ord('r'):
			print("Reset")
			break

		elif ch == ord('p'):
			print("Previous Frame")
			# if annotation_index > 0:
			# 	annotation_index = annotation_index-1
			break

		elif ch == ord('x'):
			print("Skip Frame")
			if annotation_index > 0:
				annotation_index = annotation_index+1
			break

		elif ch == ord('l'):
			all_labels = list_of_labels()
			current_label = all_labels[int(get_label())-1]
			print("Label: ", current_label)

		elif ch == 27: # ESC to exit
			keep_running = 0
			print("Exit")	
			exit()

	cv2.destroyAllWindows()


# Code starts from here
list_of_images = get_all_images(data_folder)

for im in range(len(list_of_images)):
	frame = get_one_image(list_of_images, annotation_index)
	frame_orig = frame.copy()

	scale_percent = 70.0
	width = int(frame.shape[1] * scale_percent / 100)
	height = int(frame.shape[0] * scale_percent / 100)

	# dsize
	dsize = (width, height)

	# resize image
	frame = cv2.resize(frame, dsize)

	yolo_boxes = pre_annotate(frame,['person', 'car', 'cat', 'dog', 'cow', 'traffic light'])#list_of_labels())

	# show_image(frame)
	draw_boxes(frame, yolo_boxes, frame_orig)
