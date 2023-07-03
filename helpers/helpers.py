import argparse
import cv2 as cv
from os import mkdir

#incomplete
def format_erro(mensagem):
    print(f"Error: {mensagem}")
    exit()
    
def parser_args():
    parser = argparse.ArgumentParser(
        description='Tracks mice.'
    )

    parser.add_argument(
        'video', type=str,
        help='Path to the video file to be processed.'
    )

    parser.add_argument(
        'frame_rate', type=int,
        help='Frame rate of the video file to be processed.'
    )

    parser.add_argument(
        '--draw-axis', action='store_true',
        help='Draw both PCA axis.'
    )

    parser.add_argument(
        '--save-video', action='store_true',
        help='Create a video file with the analysis result.'
    )

    parser.add_argument(
        '--color-mask', action='store_true',
        help='Draw a colored mask over the detection.'
    )

    parser.add_argument(
        '--log-position', action='store_true',
        help='Logs the position of the center of mass to file.'
    )

    parser.add_argument(
        '--log-speed', action='store_true',
        help='Logs the speed of the center of mass to file.'
    )
    
    return parser.parse_args()

def save_video(filename,frameWidth,frameHeight,frame_rate, encode=cv.VideoWriter_fourcc('M', 'J', 'P', 'G')):
        try:
            cv.VideoWriter(filename,encode,frame_rate, (frameWidth, frameHeight))
            return True
        except:
             return False
        
def make_folder(path,folder):
    if (not path.exists(folder)):
            mkdir(folder)

def write_file(file_path,text,mode="w"):
    with open(file_path, mode) as log_file:
            log_file.write(f'{text}')