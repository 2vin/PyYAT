import os
import cv2
import subprocess
import threading
import csv
from recognize_objects import recognize_objects


data_folder = "./data/"
annotation_index = 0

ob = recognize_objects("./models/yolov3.weights", "./models/yolov3.cfg","./models/coco.names")

def get_all_images(dir):
	list_of_images = []
	for x in os.listdir(dir):
	    if x.endswith(".png"):
	        list_of_images.append(str(dir)+str(x))

	return list_of_images

def get_one_image(list_of_images, annotation_index):
	return cv2.imread(list_of_images[annotation_index])

def show_image(frame):
	cv2.imshow("Annotation Tool", frame)
	cv2.waitKey(0)

def list_of_labels():
	all_labels = []
	with open('labels.csv', mode ='r')as file:
		# reading the CSV file
		csvFile = csv.reader(file)
		# displaying the contents of the CSV file
		for lines in csvFile:
			all_labels.append(lines)

	return all_labels

def get_label():
	labels = ""
	with open('labels.csv', mode ='r')as file:
		# reading the CSV file
		csvFile = csv.reader(file)
		# displaying the contents of the CSV file
		for lines in csvFile:
			# print(lines)
			labels = labels + " \"" + lines[0] + "\" \" " + lines[1] + "\""

	return(os.popen("zenity --list  --height 500 --title=\"Labels\" --column=\"Index\" --column=\"Label\""+labels).read())


def pre_annotate(frame):
	ob_results = ob.process_frame(frame, False)
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

		xc = (x + w/2.0) / frame.shape[1]
		yc = (y + h/2.0) / frame.shape[0]
		wc = w / frame.shape[1]
		hc = h / frame.shape[0]

		yolo_label.append(' '.join([str(name), str(xc), str(yc), str(wc), str(hc)]))
	return (yolo_label)

def save_annotation(frame, labels):
	output_dir = "./output/"
	cv2.imwrite(output_dir+"_temp.jpg", frame)
	file=open(output_dir+"_temp.txt",'w')
	for items in labels:
	    file.writelines(items+'\n')
	file.close()


is_clicked = 0
last_click = 0
start_point = []
stop_point = []

temp_point = []
mouse_point = [0,0]

current_label = None
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
			cv2.rectangle(frame, (boxes[0][0],boxes[0][1]) , (boxes[1][0],boxes[1][1]), (255, 255, 0), 2)

		frame_temp = frame.copy()

		cv2.imshow("Image Annotations", frame)

		ch = cv2.waitKey(3)

		
		if mouse_point[0] > 0 and mouse_point[0] < frame_temp.shape[1] and mouse_point[1] > 0 and mouse_point[1] < frame_temp.shape[0]:
			cv2.line(frame_temp, (mouse_point[0], 0), (mouse_point[0], frame_temp.shape[0]), (0,255,255), 1)
			cv2.line(frame_temp, (0, mouse_point[1]), (frame_temp.shape[1], mouse_point[1]), (0,255,255), 1)
			
			cv2.putText(frame_temp, str(current_label), (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

			cv2.imshow("Image Annotations", frame_temp)
			ch = cv2.waitKey(10)

		if start_point and temp_point:
			print(start_point, temp_point)
			cv2.rectangle(frame_temp, (start_point[0],start_point[1]) , (temp_point[0], temp_point[1]), (255, 0, 0), 2)
			cv2.imshow("Image Annotations", frame_temp)
			ch = cv2.waitKey(10)

		if start_point and stop_point:
			print(start_point, stop_point)
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
			if annotation_index > 0:
				annotation_index = annotation_index-1
			break

		elif ch == ord('l'):
			all_labels = list_of_labels()
			current_label = all_labels[int(get_label())-1][1]
			print("Label: ", current_label)

		elif ch == 27: # ESC to exit
			keep_running = 0
			print("Exit")	
			exit()

	cv2.destroyAllWindows()

list_of_images = get_all_images(data_folder)

for im in range(len(list_of_images)):
	frame = get_one_image(list_of_images, annotation_index)
	frame_orig = frame.copy()

	yolo_boxes = pre_annotate(frame)
	# show_image(frame)
	draw_boxes(frame, yolo_boxes, frame_orig)