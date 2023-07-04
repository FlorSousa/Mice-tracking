import os
import cv2 as cv
import numpy as np
import platform
from tqdm import tqdm
from helpers.helpers import *

def roi_selection(capture):
    if (not capture.isOpened()):
        format_erro("opening video stream")

    ret, frame = capture.read()

    if (not ret):
        format_erro("Error reanding video stream")

    window_name = 'Region of Interest Selection'
    make_window(window_name=window_name,ratio=cv.WINDOW_KEEPRATIO,width=frameWidth,height=frameHeight)

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
    
    if(args.log_position):
        log_path = "./logs/{}_pos.csv".format(args.video.split('\\')[-1].split('.')[0]) if platform.system() == "Windows" else f"./logs/{args.video.split('/')[-1].split('.')[0]}_pos.csv"
        write_file(file_path=log_path,text='x,y\n')
    
    if(args.log_speed):
        log_path = ("./logs/{}_speed.csv".format(args.video.split('\\')[-1].split('.')[0])) if platform.system() == "Windows" else (f"./logs/{args.video.split('/')[-1].split('.')[0]}_speed.csv")
        write_file(file_path=log_path,text='time,speed\n')
    
    return {"rois_counter":rois_counter,"background_frame":frame}

if __name__ == '__main__':
    make_folder(path=os.path,folder="./logs")
    args = parser_args()
    cap = cv.VideoCapture(args.video)
    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    selection = roi_selection(capture=cap)

    window_name = 'Tracker'
    make_window(window_name=window_name,ratio=cv.WINDOW_KEEPRATIO,width=frameWidth,height=frameHeight)

    lower_white = np.array([100, 100, 100])
    upper_white = np.array([160, 160, 160])

    previous_pos = (0, 0)
    current_pos = (0, 0)

    rameIndex = 0
    traveledDistance = 0

    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=num_frames)

    while(cap.isOpened()):
        ret, frame = cap.read()
        pbar.update(1)
        