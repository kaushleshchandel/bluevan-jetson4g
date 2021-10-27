#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
import numpy as np
import time
# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

from elements.yolo import OBJ_DETECTION

Object_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                'hair drier', 'toothbrush' ]

Object_colors = list(np.random.rand(80,3)*255)
Object_detector = OBJ_DETECTION('weights/yolov5s.pt', Object_classes)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=360,
    framerate=20,
    flip_method=2,
    cam='USB',
    camUSB=1,
):

    if cam == 'CSI':
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

    elif cam == 'USB':
        return ('v4l2src device=/dev/video{} ! '
                'video/x-raw, width=(int){}, height=(int){} ! '
                'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
                ).format(camUSB, capture_width, capture_height)

    elif cam == 'RTSP':

        return ('rtspsrc location={} latency={} ! '
            'rtph264depay ! h264parse ! omxh264dec ! '
            'nvvidconv ! '
            'video/x-raw, width=(int){}, height=(int){}, '
            'format=(string)BGRx ! '
            'videoconvert ! appsink'
            ).format('rtsp://jetson:jetson@10.0.2.203/live', 10, 320, 240)


        
def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('Person Detection Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('USB', size=(10, 1), font='Helvetica 14'),
               sg.Button('CSI', size=(10, 1), font='Any 14'),
               sg.Button('RTSP', size=(10, 1), font='Helvetica 14'), ],
              [sg.Button('Start', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Blue Van Demo',
                       layout, location=(800, 400))

    cameraSelect = 'USB'

    detection = False

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'CSI':
            cameraSelect = 'CSI'

        elif event == 'USB':
            cameraSelect = 'USB'

        elif event == 'RTSP':
            cameraSelect = 'RTSP'

        elif event == 'Start':
            detection = True

        elif event == 'Stop':
            detection = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
           # imgbytes = cv2.imencode('.png', img)[1].tobytes()
           # window['image'].update(data=imgbytes)


        if detection:

            try:
                cap
            except NameError:
                cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2, cam=cameraSelect), cv2.CAP_GSTREAMER)

            ret, frame = cap.read()
                # if video finished or no Video Input
            if not ret:
                break

          #  imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
          #  window['image'].update(data=imgbytes)

            # time when we finish processing for this frame
            new_frame_time = time.time()

            # fps will be number of frame processed in given time frame
            # since their will be most of time error of 0.001 second
            # we will be subtracting it to get more accurate result
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
        
            # converting the fps into integer
            fps = int(fps)
        
            # converting the fps to string so that we can display it on frame
            # by using putText function
            fps = str(fps)
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
                    frame = cv2.putText(frame, str(fps), (0, 0), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            #print(fps);
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()

            window['image'].update(data=imgbytes)

#            cv2.imshow("CSI Camera", frame)
            keyCode = cv2.waitKey(30)
            if keyCode == ord('q'):
                detection = False

    cap.release()
    cv2.destroyAllWindows()


main()