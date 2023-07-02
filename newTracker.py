import cv2 as cv
from helpers.helpers import *

if __name__ == '__main__':
    args = parser_args()
    cap = cv.VideoCapture(args.video)
    frameWidth = int(cap.get(3)) 
    frameHeight = int(cap.get(4))

    if (not cap.isOpened()):
        format_erro("opening video stream")
        
    ret, frame = cap.read()
    background_frame = frame
    
    if(not ret):
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