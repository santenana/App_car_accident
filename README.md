﻿
  

## Car Accident Detection (under construction 🏗️)

In this mini-project, tools such as YOLO, Torch, Roboflow (from Ultralytics), and the CUDA API will be used to train a neural network for object detection, specifically for detecting types of vehicle accidents. The final product consists of a small app that allows identifying the type of accident through a video or image to automate the process of determining how much money the insurance company should compensate the affected parties.

  
  

## RoboFlow, YOLO and CUDA <image src="https://cdn.icon-icons.com/icons2/2699/PNG/512/nvidia_logo_icon_169902.png"  width="25">

  

Using<a  href="https://universe.roboflow.com/"  title="Title"> RoboFlow</a>, different bounding boxes were created for image detection, with six labels: Motorcycle, Vehicle, Minor, Moderate, Severe, and Total Loss. These labels are used to recognize the various variables that may exist in motor vehicle accidents. The advantage of this tool lies in its high compatibility with Meta's system for AI-based object detection, which simplifies the process of manually defining the coordinates of the bounding boxes and their respective labels.

  

This results in a file format that YOLO can quickly process for a large set of images. For this initial training, 320 images were used, including Data Augmentation. The training took 50 seconds, running on an RTX 4070 Ti with 12 GB of V-RAM

  

## Model 👁️

  

For the model, a function is created that takes the following arguments: the path to the `data.yaml` file, the number of epochs, the image size, and the batch size. The model used is `yolo11n.pt`, a pre-trained model from Ultralytics for object detection. In the end, the function will return the best model in this way:

```

def modelo_detection(dataset,epochs,imgsz,batch):
	model = YOLO('yolo11n.pt')
	results = model.train(data=dataset, epochs=epochs,imgsz=imgsz,batch=batch)
	best_model = YOLO("/path_to/best/model/best.pt")
return best_model

```

  
  

## Video detection 📽️

  

For our app, a video detector is required, so a function is created that takes two parameters: the path to the video to be evaluated and the path to the best-performing model. This function will create a window in streamlit which show the predicted label with a bounding box, that displays the video along with its respective bounding box and the label of the type of accident shown in the video. For this section, the OpenCV tool is used.

```
def  Video(video_path, best_model):
	video  =  cv2.VideoCapture(video_path)
	labels  =  best_model.model.names
	all_predicted_labels  = []
	frame_placeholder  =  st.empty()
	while  video.isOpened():
		ret, frame  =  video.read()
		if  not  ret:
			break
		res  =  best_model.predict(frame, imgsz=640)
		predicted_labels  = []
		for  result  in  res:
			for  pred  in  result.boxes:
				label_index  =  int(pred.cls)
				label  =  labels[label_index]
				predicted_labels.append(label)
		all_predicted_labels.append(predicted_labels)
		annotated_frame  =  res[0].plot()
		annotated_frame_rgb  =  cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
		frame_placeholder.image(annotated_frame_rgb, channels="RGB")
		sleep(1/60)
	video.release()
	cv2.destroyAllWindows()
	f_label  = [item  for  sublist  in  all_predicted_labels  for  item  in  sublist]
	label_counts  =  Counter(f_label)
	return  label_counts
```

  

## Image detection 🖼️

  
Similarly to video detection, this function takes the path of the model and the path of the image, with the modification that in this case, it outputs both the label and the image with its respective detection, like this:

  ```

def  imagen_detect(path):
	image_array  =  read_image_file(path)
	res  =  model.predict(image_array,imgsz=640)
	imagen  =  res[0].plot()
	labels  =  res[0].names
	predicted_labels  = []
	for  result  in  res:
		for  pred  in  result.boxes:
			label_index  =  int(pred.cls)
			label  =  labels[label_index]
			predicted_labels.append(label)
	return (imagen,predicted_labels)
  

```
  

## App With Streamlit 👑

An app is created in Streamlit, which will support the previous functions and use the model to make predictions, as well as for uploading image and video files. This application will also record the affected person's ID and generate a report with the severity of the accident they have suffered.

## How to Use it

For now, the application is in beta and only works by downloading the repository and installing a container in Docker. Later, it will be moved to a web or mobile application for greater user convenience.

To use it, step 0 is to have Docker installed on your computer, then you should follow these instructions.

```

git clone https://github.com/santenana/App_car_accident.git
cd .\App_car_accident\
docker build -t caraccident_app .
docker run -p 8501:8501 caraccident_app
```
Then, in your browser, go to http://localhost:8501/ in your local browser to view the application and there you go, your own crash Detection.

![reisa-uzawa-reisa](https://github.com/user-attachments/assets/006ee6d2-95cc-499a-8c01-d09dbb45f40c)
