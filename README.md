
## Car Accident Detection (under construction 🏗️)
In this mini-project, tools such as YOLO, Torch, Roboflow (from Ultralytics), and the CUDA API will be used to train a neural network for object detection, specifically for detecting types of vehicle accidents. The final product consists of a small app that allows identifying the type of accident through a video or image to automate the process of determining how much money the insurance company should compensate the affected parties.


## RoboFlow, YOLO and CUDA <image src="https://cdn.icon-icons.com/icons2/2699/PNG/512/nvidia_logo_icon_169902.png"  width="25">

Using<a href="https://universe.roboflow.com/" title="Title"> RoboFlow</a>, different bounding boxes were created for image detection, with six labels: Motorcycle, Vehicle, Minor, Moderate, Severe, and Total Loss. These labels are used to recognize the various variables that may exist in motor vehicle accidents. The advantage of this tool lies in its high compatibility with Meta's system for AI-based object detection, which simplifies the process of manually defining the coordinates of the bounding boxes and their respective labels.

This results in a file format that YOLO can quickly process for a large set of images. For this initial training, 320 images were used, including Data Augmentation. The training took 50 seconds, running on an RTX 4070 Ti with 12 GB of V-RAM

## Model 👁️

For the model, a function is created that takes the following arguments: the path to the `data.yaml` file, the number of epochs, the image size, and the batch size. The model used is `yolo11n.pt`, a pre-trained model from Ultralytics for object detection. In the end, the function will return the best model in this way:
```
def  modelo_detection(dataset,epochs,imgsz,batch):
	model  = YOLO('yolo11n.pt')
	results  = model.train(data=dataset, epochs=epochs, imgsz=imgsz,batch=batch)
	best_model  = YOLO("/path_to/best/model/best.pt")
	return  best_model
```


##  Video detection 📽️

For our app, a video detector is required, so a function is created that takes two parameters: the path to the video to be evaluated and the path to the best-performing model. This function will create a pop-up window that displays the video along with its respective bounding box and the label of the type of accident shown in the video. For this section, the OpenCV tool is used.

##  Image detection 🖼️

Similarly to video detection, this function takes the path of the model and the path of the image, with the modification that in this case, it outputs both the label and the image with its respective detection, like this:

```
def  imagen_detect(path,model):
	res  =  model.predict(path,imgsz=640)
	imagen  =  res[0].plot()
	labels  =  res[0].names
	predicted_labels  = []
	for  result  in  res:
		for  pred  in  result.boxes:
			label_index  =  int(pred.cls)
			label  =  labels[label_index]
			predicted_labels.append(label)
	return  imagen,predicted_labels

```
##  Test 🧪

To test each of the functions created, a test notebook is set up to correct any errors in the functions and to verify that the output of each function is as expected.

## Coming soon🚧
Main app to sumarize all functions, Docker Container, StreamLit local App, and improve model addin more images