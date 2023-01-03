import cv2
import numpy as np
import csv

class recognize_objects:
	def __init__(self, yolo_model_weights, yolo_model_cfg, coco_names):
		self.weights = yolo_model_weights
		self.cfg = yolo_model_cfg
		self.coco = coco_names

		self.classes = open(self.coco).read().strip().split('\n')
		np.random.seed(42)
		self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')


		self.net = cv2.dnn.readNetFromDarknet(self.cfg, self.weights)
		self.ln = self.net.getLayerNames()
		
		if cv2.__version__ == '4.6.0':
           	    self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]
        	else:
            	    self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

	def process_frame(self, frame, all_labels, show = True):

		frame_copy = frame.copy()

		(H, W) = frame.shape[:2]

		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
		self.net.setInput(blob)
		layerOutputs = self.net.forward(self.ln)

		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]
				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > 0.5:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")
					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))
					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

		# ensure at least one detection exists
		results = []
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box -coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in self.colors[classIDs[i]]]
				cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(self.classes[classIDs[i]], confidences[i])
				cv2.putText(frame_copy, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

				if self.classes[classIDs[i]] in all_labels:
					results.append([self.classes[classIDs[i]],[(x, y), (x + w, y + h)]])

		if show:
			# show the output image
			cv2.imshow("Objects", frame_copy)
		else:
			if len(idxs) > 0:
				print("Objects detected in this frame:\n")
				for i in idxs.flatten():
				    if cv2.__version__ == '4.6.0':
                    		        i = i
                		    else:
                    			i = i[0]
				    print(self.classes[classIDs[i]])
				print("\n###################################\n")

		# If it is person, cat, dog detected
		return results


