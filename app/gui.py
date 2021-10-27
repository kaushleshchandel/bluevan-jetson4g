#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
import numpy as np
from elements.yolo import OBJ_DETECTION
import os

#------------------------------------
# Get Object Classess
#------------------------------------
def get_object_classes():
    Object_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                    'hair drier', 'toothbrush' ]
    return Object_classes

Object_colors = list(np.random.rand(80,3)*255)
Object_detector = OBJ_DETECTION('weights/yolov5s.pt', get_object_classes())
#------------------------------------
# Get List of available Camera
#------------------------------------
def get_camera_list():
    all_camera_idx_available = []
    for camera_idx in range(5):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            print(f'Camera index available: {camera_idx}')
            all_camera_idx_available.append(camera_idx)
            cap.release()
    return all_camera_idx_available


#------------------------------------
# Load the AI models
#------------------------------------
def get_model_list(filePath):
    print(os.getcwd())
    with open(filePath) as f:
        model_selection = f.readlines()
    f.close()
    return model_selection

logsList = ["Initializing"]

#------------------------------------
# Add to the logList
#------------------------------------
def add_log(modelWindow, logMessage):
    logsList.append(logMessage)
    window.Element('-LISTLOG-').update(values=logsList)


#------------------------------------
# Define the window layoutf
#------------------------------------
def get_layout():
 
    model_selection = get_model_list(filePath=os.getcwd() + '/modelList.txt')
    layout = [[sg.Image(filename='', key='final', size=(320,240))],
            
            [sg.T("Select Camera          "), 
            sg.Radio('USB  0', "RADIO1", default=False, key="-INUSB0-"),
            sg.Radio('USB  1', "RADIO1", default=False, key="-INUSB1-"),
            sg.Radio('File', "RADIO1", default=False, key="-INFILE-"),
            sg.Radio('CSI ', "RADIO1", default=True, key="-INCSI-"),
            sg.Radio('RTSP ', "RADIO1", default=False, key="-INRTSP-")
            ],

            [sg.T("Select detection model"), sg.Combo(model_selection, size=(20, 5), enable_events=True, key='-COMBO-')],
            [sg.T("Select Sensitivity        "), sg.Slider(orientation ='horizontal', key='stSlider', range=(1,10), )],
            [sg.Button('Start', size=(10, 1), font='Helvetica 14', key='-ss-'),
            sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ],
            [sg.Listbox(logsList, size=(108, 30), key="-LISTLOG-")],
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
# Main Function
#------------------------------------
        
def main():

    connectedCameras = get_camera_list()
    #Define & create the window
    screenWidth = 600
    screenHeight = 1024
    window = sg.Window('Blue Van Demo',get_layout(), location=(0, 0), size=(screenWidth,screenHeight))

    #Set Default variables
    cameraSelect = 'CSI'
    detection = False
    usbCamID = 1

    # Run the loop endlessly
    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return
        elif event == '-ss-' and detection == False:
            if values["-INCSI-"] == True:
                logsList.append('Camera Selected CSI')
                window.Element('-LISTLOG-').update(values=logsList)
                cameraSelect = 'CSI'
            if values["-INUSB0-"] == True:
                logsList.append('Camera Selected USB0')
                window.Element('-LISTLOG-').update(values=logsList)
                cameraSelect = 'USB'
                usbCamID = 0
            if values["-INUSB1-"] == True:
                logsList.append('Camera Selected USB1')
                window.Element('-LISTLOG-').update(values=logsList)
                cameraSelect = 'USB'
                usbCamID = 1
            if values["-INRTSP-"] == True:
                logsList.append('Camera Selected RTSP')
                window.Element('-LISTLOG-').update(values=logsList)
                cameraSelect = 'RTSP'
            cap = cv2.VideoCapture(gstreamer_pipeline(camUSBID=usbCamID, flip_method=2, sourceCamera=cameraSelect), cv2.CAP_GSTREAMER)
            detection = True
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
            logsList.append('Stop Camera')
            window.Element('-LISTLOG-').update(values=logsList)

        if detection:

            try:
                cap
            except NameError:
                cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2, cam=cameraSelect), cv2.CAP_GSTREAMER)

            ret, frame = cap.read()
          #  imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
          #  window['image'].update(data=imgbytes)
            Object_classes = get_object_classes()
            if ret:
                # detection process
                objs = Object_detector.detect(frame)

                # plotting
                for obj in objs:
                    # print(obj)
                    label = obj['label']
                    score = obj['score']
                    [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                    color = Object_colors[Object_classes.index(label)]
                    frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                    frame = cv2.putText(frame, f'{label} ({str(score*100)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)

            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['final'].update(data=imgbytes)

#            cv2.imshow("CSI Camera", frame)
            keyCode = cv2.waitKey(30)
            if keyCode == ord('q'):
                detection = False


# Finally release the CV2
    cap.release()
    cv2.destroyAllWindows()

#------------------------------------
# Call main function
#------------------------------------
main()