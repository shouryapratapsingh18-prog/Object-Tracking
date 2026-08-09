import cv2
import os
import sys
import time

#Define GOTURN model paths
PROTOTXT = "goturn.prototxt"
CAFFEMODEL = "goturn.caffemodel"

def validate_goturn_model():
    if not os.path.exists(PROTOTXT) or not os.path.exists(CAFFEMODEL):
        print("\n GOTURN model files not found")
        print("Expected Files")
        print(f"    -{os.path.abspath(PROTOTXT)}")
        print(f"    -{os.path.abspath(CAFFEMODEL)}")
        print("Please place them in  paths shown above.\n")
        sys.exit(1)

def main():
    validate_goturn_model()

    # Create GOTURN tracker
    try:
        tracker = cv2.TrackerGOTURN_create()
    except AttributeError:
        tracker = cv2.legacy.TrackerGOTURN_create()

    #Open Webcame
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcame")
        return

    #Read the first frame
    ret , frame = cap.read()
    if not ret:
        print("Failed to read from webcam")
        return

    #Let user Select ROI
    bbox = cv2.selectROI("Select Object to track" , frame , fromCenter = False  , showCrosshair = True)
    cv2.destroyAllWindows()

    #Initialize Tracker
    tracker.init(frame,bbox) #Initializes the tracking algorithm with the first frame and the initial bounding box

    while True: #Starts an infinite loop to continuously read and process video frames one by one in real-time.
        ret,frame = cap.read()
        if not ret:
            break

        #Track object
        start = time.time() #Captures the current timestamp (in seconds) right before tracking begins.
        success , bbox = tracker.update(frame)
        end = time.time() #Captures the timestamp immediately after tracking completes.

        if success:
            x, y, w, h = map(int, bbox)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"GOTURN: {1000 * (end - start):.1f} ms" #eates a formatted text string displaying the tracking latency per frame in milliseconds ($\text{ms}$).
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        else:
            cv2.putText(frame, "Tracking Lost", (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        cv2.imshow("GOTURN Tracker" , frame)

        key = cv2.waitKey(1) #Pauses execution for 1 millisecond to display the frame and listens for any key pressed on your keyboard.
        if key == 27:# ESC key  to exit
            break
    cap.release()
    cv2.destroyALLWindows()

if __name__ == "__main__":
    main()
