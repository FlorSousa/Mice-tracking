import os
import cv2 as cv
import numpy as np
from tqdm import tqdm
from helpers.helpers import *

if __name__ == '__main__':
    make_folder(path=os.path,folder="./logs")
    args = parser_args()
    cap = cv.VideoCapture(args.video)
    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))

    if (not cap.isOpened()):
        format_erro("opening video stream")

    ret, frame = cap.read()
    background_frame = frame

    if (not ret):
        format_erro("Error reanding video stream")

    window_name = 'Region of Interest Selection'
    cv.namedWindow(window_name, cv.WINDOW_KEEPRATIO)
    cv.resizeWindow(window_name, 1438, 896)
    rois = []

    while True:
        roi_actual = cv.selectROI(window_name, frame, False)
        if all(element == 0 for element in roi_actual):
            break
        rois.append(roi_actual)

    cv.destroyWindow(window_name)

    rois_counter = [0 for _ in range(len(rois))]

    if (args.save_video):
        save_video(filename=f"{args.video.split('/')[-1].split('.')[0]}_result.avi",
                   encode=cv.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                   frameWidth=frameWidth,
                   frameHeight=frameHeight,
                   frame_rate=args.frame_rate)
    

    # This work just for linux -> f"./logs/{args.video.split('/')[-1].split('.')[0]
    if(args.log_position):
        write_file(file_path=f"./logs/{args.video.split('/')[-1].split('.')[0]}_pos.csv",text='x,y\n')
    
    if(args.log_speed):
        write_file(file_path=f"./logs/{args.video.split('/')[-1].split('.')[0]}_speed.csv",text='time,speed\n')

    window_name = 'Tracker'
    cv.namedWindow(window_name, cv.WINDOW_KEEPRATIO) #Repetiton
    cv.resizeWindow(window_name, frameWidth, frameHeight) #Repetiton

    lower_white = np.array([100, 100, 100])
    upper_white = np.array([160, 160, 160])

    previous_pos = (0, 0)
    current_pos = (0, 0)

    rameIndex = 0
    traveledDistance = 0

    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=num_frames)