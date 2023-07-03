import os
import cv2 as cv
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

    selection_roi_window = 'Region of Interest Selection'
    cv.namedWindow(selection_roi_window, cv.WINDOW_KEEPRATIO)
    cv.resizeWindow(selection_roi_window, 1438, 896)
    rois = []

    while True:
        roi_actual = cv.selectROI(selection_roi_window, frame, False)
        if all(element == 0 for element in roi_actual):
            break
        rois.append(roi_actual)

    cv.destroyWindow(selection_roi_window)

    rois_counter = [0 for _ in range(len(rois))]

    if (args.save_video):
        save_video(filename=f"{args.video.split('/')[-1].split('.')[0]}_result.avi",
                   encode=cv.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                   frameWidth=frameWidth,
                   frameHeight=frameHeight,
                   frame_rate=args.frame_rate)
    print(f"./logs/{args.video.split('/')[-1].split('.')[0]}_pos.csv")
    if(args.log_position):
        write_file(file_path=f"./logs/{args.video.split('/')[-1].split('.')[0]}_pos.csv",text='x,y\n')
    
    if(args.log_speed):
        write_file(file_path=f"./logs/{args.video.split('/')[-1].split('.')[0]}_speed.csv",text='time,speed\n')