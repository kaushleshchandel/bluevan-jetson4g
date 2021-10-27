#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
import numpy as np
from elements.yolo import OBJ_DETECTION
import os

#Set Default values
logsList = ["Initializing"]
cameraSelect = 'CSI'
detection = False
usbCamID = 1

#------------------------------------
# Log Defaults / Last used parameters
#------------------------------------
def get_settings():
    logsList.append("Loding default values")


#------------------------------------
# Log events in window
#------------------------------------
def add_log(log_string, log_type='default'):
    logsList.append(log_string)

#------------------------------------
# List all the connected Cameras
#------------------------------------

def get_camera_list():
    camera_idx_available = []
    for camera_idx in range(5):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            print(f'Camera index available: {camera_idx}')
            add_log(f'Camera index available: {camera_idx}')
            camera_idx_available.append(camera_idx)
            cap.release()
    return camera_idx_available


#------------------------------------
# Load model list
#------------------------------------
def get_models():
    model_selection = ['Select Model']
    print(os.getcwd())
    with open(os.getcwd() + '\jetson.app\modelList.txt') as f:
        model_selection = f.readlines()
    f.close()
    return model_selection

def get_layout(modelList):
    layout = [[sg.Image(filename='', key='raw', size=(320,240)), sg.Image(filename='', key='final', size=(320,240))],
            
            [sg.T("Select Camera          "), 
            sg.Radio('USB  0', "RADIO1", default=False, key="-INUSB0-"),
            sg.Radio('USB  1', "RADIO1", default=False, key="-INUSB1-"),
            sg.Radio('File', "RADIO1", default=False, key="-INFILE-"),
            sg.Radio('CSI ', "RADIO1", default=True, key="-INCSI-"),
            sg.Radio('RTSP ', "RADIO1", default=False, key="-INRTSP-")
            ],

            [sg.T("Select detection model"), sg.Combo(modelList, size=(50, 5), enable_events=True, key='-COMBO-')],
            [sg.T("Select Sensitivity        "), sg.Slider(orientation ='horizontal', key='stSlider', range=(1,10), )],
            [sg.Button('Start', size=(10, 1), font='Helvetica 14', key='-ss-'),
            sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ],
            [sg.Listbox(logsList, size=(108, 30))],
            [sg.Button('Clear Logs', size=(10, 1), font='Helvetica 14', key='-slogclear-'), sg.Checkbox('Application', default=True), sg.Checkbox('Debug', default=True), sg.Checkbox('Motion Events', default=True) ],
            ]
    return layout
#------------------------------------
#Function to create gstreamer pipeline
#------------------------------------
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=20,
    flip_method=2,
    sourceCamera='USB',
    camUSBID=1,
):

    if sourceCamera == 'CSI':
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

    elif sourceCamera == 'USB':
        return ('v4l2src device=/dev/video{} ! '
                'video/x-raw, width=(int){}, height=(int){} ! '
                'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
                ).format(camUSBID, capture_width, capture_height)

    elif sourceCamera == 'RTSP':
        return ('rtspsrc location={} latency={} ! '
            'rtph264depay ! h264parse ! omxh264dec ! '
            'nvvidconv ! '
            'video/x-raw, width=(int){}, height=(int){}, '
            'format=(string)BGRx ! '
            'videoconvert ! appsink'
            ).format('rtsp://jetson:jetson@10.0.2.203/live', 10, 320, 240)

#------------------------------------
# Process User Input
#------------------------------------
def process_user_input():
    if(1==1):
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return
        elif event == '-ss-' and detection == False:
            if values["-INCSI-"] == True:
                cameraSelect = 'CSI'
            if values["-INUSB0-"] == True:
                cameraSelect = 'USB'
                usbCamID = 0
            if values["-INUSB1-"] == True:
                cameraSelect = 'USB'
                usbCamID = 1
            if values["-INRTSP-"] == True:
                cameraSelect = 'RTSP'
            try:    
                cap = cv2.VideoCapture(gstreamer_pipeline(camUSBID=usbCamID, flip_method=2, sourceCamera=cameraSelect), cv2.CAP_GSTREAMER)
                detection = True
            except:
                print("Error opening Video capture")    
            window['-ss-'].Update('Stop')
        elif event == '-ss-'and detection == True:
            detection = False

            #Clear the frame
            #img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            # imgbytes = cv2.imencode('.png', img)[1].tobytes()
            # window['image'].update(data=imgbytes)

            # Release the Capture object and CV2
            cap.release()
            cv2.destroyAllWindows()
            window['-ss-'].Update('Start')



#------------------------------------
# Read Camera Image
#------------------------------------
def read_camera():
    print('Read Camera')

#------------------------------------
# Display Camera Image
#------------------------------------
def display_camera():
    print('Display Camera')

#------------------------------------
# Main Function
#------------------------------------
def main():
    list_of_cameras = get_camera_list()
    list_of_models = get_models()
    settings = get_settings()
    window_layout = get_layout(list_of_models)

    window = sg.Window('Blue Van Demo',window_layout, location=(0, 0), size=(800,1024))

    # Run the loop endlessly
    while True:
       # process_user_input()
        
        if detection:
            
            # This is where we read the camera
            
            try: cap
            except NameError: c = None

            if(c) is None:
                print("CAP undefined")
            else:
                ret, frame = cap.read()

            #This is where we do motion detection and boulding boxes, etc    


            # This is where we Show the frame on screen
            try: cv2
            except NameError: cv = None
            
            if(cv) is None:
                print("CV2 undefined")
            else:
                cv2.imshow("Camera", frame)
            
# Finally release the CV2
cv=0
try: cv2
except NameError: cv = None
            
if(cv) is None:
    print("CV2 undefined")
else:
    cv2.destroyAllWindows()

c=0
try: cap
except NameError: c = None
            
if(c) is None:
    print("Cap undefined")
else:
    cap.release()
     
#------------------------------------
# Call main function
#------------------------------------
main()