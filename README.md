# SeniorDesignParkingPal
This is a Python Microservice that utilizes Yolov5 to determine whether or not cars occupy parking spaces. This is used to communicate with a firestore database for a mobile application to use.

1.)
  Using an ESP-32 module, images of a parking lot are sent to my onedrive account, where they will be processed by this Python Microservice.
  ![DEBO_CAM_ESP32_001-3490802814](https://user-images.githubusercontent.com/74478647/234034604-15dbe973-1adf-4f5e-9239-dab37d54ba51.png)

  
2.)
  This Python Microservice allows the user to outline which parking spots they would like to track. Once the user has outlined their spots, they should enter 'q' to quit. If a mistake is made, the user can enter 'r' for reset. The coordinates of the spots are then saved to a .yaml file. The microservice then performs object detection using YOLOv5's model to find cars. Once the cars are found, the program determines how much the cars overlap with the parking spots. If a car occupies more than 60% of a parking spot, the spot is marked 'True' and 'Occupied' on Firestore. The image is also sent to Firestore.
   ![ChoosingSpotas](https://user-images.githubusercontent.com/74478647/234034729-56f36847-62f9-488e-a6b5-3dfcc0d38a47.png)
   ![CarDetSquares](https://user-images.githubusercontent.com/74478647/234034843-0cff7cde-51d9-42cf-89b4-9e826ce2e284.png)
   ![image](https://user-images.githubusercontent.com/74478647/234036610-bc9ba9bb-510d-4a28-a7f6-a4144331537d.png)


  
 3.)
  Fire store contains the necessary containers and data for our mobile application to pull from. 
  
4.)
  Once the data is in Firestore, our mobile Swift application uses the data and images to display to a user for convenience. 
  ![image](https://user-images.githubusercontent.com/74478647/234034100-37d39f18-3c1c-4d85-8e0d-0405c9a15095.png)

  
Overview:
  This project as a whole can help businesses, universities, and other public lots manage their parking occupany and allow visitors easy accessibility. Today, many garages rely on LiDAR systems for every single space, but our solution can track multiple spots per one camera module. If we were to utilize a bird's eye view of a large lot, we could accurately track and display available spots to the public. 
  ![SeniorDiagram drawio](https://user-images.githubusercontent.com/74478647/234034956-3568f1d3-b2fa-4138-b9a5-7c734c009b2c.png)

