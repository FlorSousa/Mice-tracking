import os
import cv2 as cv
import numpy as np
from tqdm import tqdm
from utils import *

def analyzer():
    pass

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
        write_file(file_path=get_path(args,"position"),text='x,y\n')
    
    if(args.log_speed):
        write_file(file_path=get_path(args,"speed") ,text='time,speed\n')
    
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
    frameIndex = 0
    previous_pos = (0, 0)
    current_pos = (0, 0)

    rameIndex = 0
    traveledDistance = 0

    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=num_frames)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if(not ret):
            format_erro("reading video stream")
            pbar.close()
            exit()
        sub_frame = cv.absdiff(frame, selection["background_frame"])

        filtered_frame = cv.inRange(sub_frame, lower_white, upper_white)
        
        kernel3 = cv.getStructuringElement(
            cv.MORPH_ELLIPSE,
            (3, 3),
            (-1, -1)
        )

        kernel20 = cv.getStructuringElement(
            cv.MORPH_ELLIPSE,
            (20, 20),
            (-1, -1)
        )

        mask = apply_morphological_filter(actual_frame=frame,background_frame=selection["background_frame"],lower_white=lower_white,upper_white=upper_white)
        returns = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        contours = returns[1] if len(returns) == 3 else returns[0]
        
        if(len(contours) != 0):
            # find the biggest countour by the area
            contour = max(contours, key = cv.contourArea)
            cv.drawContours(frame, [contour], 0, (255, 0, 255), 2)

            # Find the orientation of each shape
            current_pos = getOrientation(contour, frame, args.draw_axis)["center"]

        speed = np.sqrt(
            (previous_pos[0] - current_pos[0])**2 + 
            (previous_pos[1] - current_pos[1])**2
        )

        traveledDistance += speed
        previous_pos = current_pos
        if(args.log_speed and current_pos[0] > 50 and current_pos[1] > 50):     
                write_file(file_path = get_path(args,"speed"),text = f'{frameIndex * (1/float(args.frame_rate)):.3f},{speed:.3f}\n',mode="a")

        rois = selection["rois_counter"]
        if  rois is not None:
            for index, roi in enumerate(rois):
                x, y, w, h = roi

                

        pbar.update(1)