import cv2

#Define the tracker 
tracker_type = 'moose'
tracker = cv2.legacy.TrackerMOSSE_create()

#Load video from file or webcame
video = cv2.VideoCapture(0) #Use 0 for webcam or replace with "Video.mp4"

#Read the first frame
ret, frame = video.read()
if not ret:
    print("Failed to read video")
    exit()

#Select the bouding box (ROI) for the object to track
bbox  = cv2.selectROI("Select object",frame , fromCenter = False , showCrosshair= True)
cv2.destroyWindow("Select object")

#Initialize the tracker with first frame and selected bounding box
tracker.init(frame , bbox)

while True:
    ret , frame = video.read()
    if not ret:
        break

    #Update Tracker
    success , bbox = tracker.update(frame)

    #Draw Bouding Box
    if success:
        x,y,w,h = [int(v) for v in bbox]
        cv2.rectangle(frame , (x,y), (x+w , y+h) , (0,255,0),2,1)
        cv2.putText(frame , "Tracking " , (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    else:
        cv2.putText(frame , "Lost" , (50,80) , cv2.FONT_HERSHEY_SIMPLEX , 0.6 , (0,0,255) , 2)


    #Display result
    cv2.imshow("Object Tracking" , frame)

    #Exit with ESC
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
