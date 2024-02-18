import connect4
import cv2
import mediapipe as mp
import time
import pyrealsense2 as rs
import numpy as np
import connect4_gui

cameraId = 0  # give a specific camera id connected to the computer
connect4game = connect4.connect4(7, 6)  # testing class connection
GUI = connect4_gui.Connect4GUI(connect4game)

slideWindowCounter = 0
pointUpCounter = 0
thumbUpCounter = 0
thumbDownCounter = 0
openPalmCounter = 0

cx = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

last_result = 0
enable_next = True


def rsOpen():  # open the realsense camera
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # depth stream
    # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # color stream
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)  # color stream
    # Start streaming
    pipeline.start(config)
    return pipeline


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print(result.gestures)
    global thumbDownCounter
    global thumbUpCounter
    global openPalmCounter
    global pointUpCounter
    global slideWindowCounter
    global last_result
    global enable_next

    for gesture in result.gestures:
        # checking for a certain case
        if [category.category_name for category in gesture] == ['Thumb_Up']:
            thumbUpCounter += 1
        elif [category.category_name for category in gesture] == ['Thumb_Down']:
            thumbDownCounter += 1
        elif [category.category_name for category in gesture] == ['Open_Palm']:
            openPalmCounter += 1
        elif [category.category_name for category in gesture] == ['Pointing_Up']:
            pointUpCounter += 1
            # GUI.pointting_up_track(cx-260)
            GUI.pointting_up_track(cx - 300)
            enable_next = True

        # window counter ++
        slideWindowCounter += 1

        # output
        if slideWindowCounter == 15:
            if thumbUpCounter > thumbDownCounter and thumbUpCounter > pointUpCounter and thumbUpCounter > openPalmCounter:
                print("Thumb_Up")
                if enable_next:
                    GUI.thumb_up_event()
                    enable_next = False
            elif thumbDownCounter > thumbUpCounter and thumbDownCounter > openPalmCounter and thumbDownCounter > pointUpCounter:
                print("Thumb_Down")
                if enable_next:
                    pass
            elif openPalmCounter > thumbDownCounter and openPalmCounter > thumbUpCounter and openPalmCounter > pointUpCounter:
                print("Open_Palm")
            elif pointUpCounter > thumbDownCounter and pointUpCounter > thumbUpCounter and pointUpCounter > openPalmCounter:
                print("Point_up")
                if last_result != 0:
                    last_result = 0


            else:
                print("None")

            # reset counter
            slideWindowCounter = 0
            thumbUpCounter = 0
            thumbDownCounter = 0
            openPalmCounter = 0
            pointUpCounter = 0
    # print([category.category_name for category in gesture]==['Thumb_Up'])


model_file = open('gesture_recognizer.task', "rb")
model_data = model_file.read()
model_file.close()
base_options = BaseOptions(model_asset_buffer=model_data)
# base_options = BaseOptions(model_asset_path='gesture_recognizer.task')
options = GestureRecognizerOptions(base_options=base_options, running_mode=VisionRunningMode.LIVE_STREAM,
                                   result_callback=print_result, num_hands=2)
recognizer = GestureRecognizer.create_from_options(options)


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=1, trackCon=1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist


# rsOpen()
pipeline = rsOpen()
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()

# start video stream
# capture = cv2.VideoCapture(cameraId)
# capture = color_frame
# capture = np.asanyarray(capture.get_data())

# cv2.namedWindow('capture', cv2.WINDOW_NORMAL)  # open a window to show
# pTime = 0
# cTime = 0
detector = handDetector()
timestamp = 0
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        # depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        # if not color_frame:
        #     continue
        frame = np.asanyarray(color_frame.get_data())

        if frame is not None:
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frameRGB)
            frame = detector.findHands(frame)
            lmlist = detector.findPosition(frame)
            if len(lmlist) != 0:
                print(lmlist[4])
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            timestamp += 1
            recognizer.recognize_async(mp_image, timestamp)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        if id == 8:
                            h, w, c = frame.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            # if id ==0:
                            # print(cx,cy)
                            print(cx)
                            cv2.circle(frame, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
                    mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        key = cv2.waitKey(1)
        GUI.draw_board()
        cv2.imshow('camera', frame)  # show the frame
        cv2.waitKey(1)

finally:
    pipeline.stop()
    cv2.destroyAllWindows()


