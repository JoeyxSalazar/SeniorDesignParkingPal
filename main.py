import yaml
import torch
import cv2
import os
import time
import pyrebase
import matplotlib.pyplot as plt
#from spacedetection import CoordinatesGenerator
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import storage
#from models.experimental import attempt_load
#from utils.general import non_max_suppression, scale_coords
#from utils.plots import plot_one_box


def spacedetector():
    subprocess.run(['python', 'spacedetection.py'])

def ExtractCarCoords(modelresults):
    df = modelresults.pandas().xyxy[0]
    # Filter the dataframe to only include rows where the class is "car"
    df_cars = df[df['name'] == 'car']
    # Save the coordinates of the cars to a list
    car_coords = []
    for i in range(len(df_cars)):
        xmin, ymin, xmax, ymax = df_cars.iloc[i][['xmin', 'ymin', 'xmax', 'ymax']]
        car_coords.append((xmin, ymin, xmax, ymax))
    return car_coords

def ExtractParkingSpots():
    with open('coords.yaml','r') as f:
        data = yaml.safe_load(f)
    coordinates_dict = {}
    minmax = {}
    for item in data:
        id = item['id']
        coordinates = item['coordinates']
        coordinates_dict[id] = coordinates
        xmin = min([coord[0] for coord in coordinates_dict[id]])
        ymin = min([coord[1] for coord in coordinates_dict[id]])
        xmax = max([coord[0] for coord in coordinates_dict[id]])
        ymax = max([coord[1] for coord in coordinates_dict[id]])
        minmax[id] = [xmin, ymin, xmax, ymax]
    return minmax

def overlap_percentage(cars, spots):
    # Find coordinates of intersection rectangle
    x_overlap = max(0, min(cars[2], spots[2]) - max(cars[0], spots[0]))
    y_overlap = max(0, min(cars[3], spots[3]) - max(cars[1], spots[1]))

    # Calculate areas of rectangles and intersection
    cars_area = (cars[2] - cars[0]) * (cars[3] - cars[1])
    spots_area = (spots[2] - spots[0]) * (spots[3] - spots[1])
    overlap_area = x_overlap * y_overlap

    # Calculate percentage overlap
    if cars_area < spots_area:
        return overlap_area / cars_area * 100
    else:
        return overlap_area / spots_area * 100

def checkoccupany(cars, spots):
    bools = []
    percents = []
    x_labels = []
    for values in spots.values():
        is_occupied = False
        for car in cars:
            percents.append(overlap_percentage(car, values))
            if overlap_percentage(car, values) > 60:
                is_occupied = True
                cars.remove(car)
                break
        bools.append(is_occupied)
    print(percents)
    return bools

def updateFirebase(bools, img_path):
    #initialize pyrebase to store image
    config = {

    }
    firebase_storage = pyrebase.initialize_app(config)
    storage_pyre = firebase_storage.storage()
    # Get a Firestore client object
    img = "C:/Users/Joey/OneDrive - University of Miami/Seventh Semester/Senior Design/SeniorDesignParkingPal" + img_path
    # Get all documents in the collection
    # Reference the collection of spaces to update
    db = firestore.client()
    spaces_ref = db.collection('campuses').document('flYlS63HBdRvk8epjdoz').collection('lots').document('imUkfggDpQDuSjGFiHH8').collection('spaces')
    # Loop through the documents in the collection and update them
    i = 1
    print(bools)
    for space in spaces_ref.get():
        space_ref = spaces_ref.document(space.id)
        space_ref.update({
            'status': bools[i-1],
        })
        i+=1
    #upload photo to application
    if os.path.isfile(img_path):
        print('Attempting photo upload')
        storage_pyre.child("1.png").put(img_path)
    else:
        print('Error Uploading File')

def initializeFirebase():
    #Initialize Back End for boolean values
    cred = credentials.Certificate('parkingpal_admin.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': ''
    })


def RunProtocol():
    # Model
    print('Loading Model')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    initializeFirebase()
    while True:
        for x in range(1,8):
            #Setting up how to loop through each image
            image = 'photos/' + str(x) + '.png'
            #Perform object detection on image
            results = model(image)
            #List of car coordinates (xmin, ymin, xmax, ymax)
            car_coords = ExtractCarCoords(results) 
            #Dictionary of Parking Spots 0: [xmin, ymin, xmax, ymax]
            spots = ExtractParkingSpots()
            #Check which spots are available or taken
            available_spots = checkoccupany(car_coords, spots)
            #Update App
            updateFirebase(available_spots, image)
            #Wait for next image processing
            time.sleep(10)


if __name__ == '__main__':
    #Choose the spots that you would like to check
    while True:
        x = input('Would you like to choose your parking spots? Y/N : ')
        if x == 'Y':
            spacedetector()
            break
        elif x == 'N':
            break
        else:
            print('Please input valid entry')
    RunProtocol()
    


