import cv2

tracker_type = 'mil'
tracker = cv2.legacy.TrackerMIL_create()


#Load video from file or webcame 
Video = cv2.VideoCapture(0) #use 0 for webcam ore replace with "video.mp4"

#Read the first frame
ret , frame = Video.read()
if not ret:
    print("failed to read video")
    exit()

#Select the bounding box (ROI) for the object to track
bbox = cv2.selectROI("Select object" , frame , fromCenter = False, showCrosshair = True)
cv2.destroyWindow("Select object")

#Initialize the tracker with the first frame and selected bounding box
tracker.init(frame ,bbox)

while True:
    ret , frame = Video.read()
    if not ret:
        break
    #Update Tracker
    success , bbox = tracker.update(frame)

    #Draw bounding box
    if success:
        x,y,w,h = [int(v) for v in bbox] #Converting Coordinates to integers
        cv2.rectangle(frame ,(x,y) , (x+w , y+h),(0,255,0),2,1) #Drawing the bouding box
        cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2) #Drawing the "Tracking" test
    else:
        cv2.putText(frame , "Lost" , (50,80) , cv2.FONT_HERSHEY_SIMPLEX , 0.6 , (0,255,0),2)


    #Dispaly result
    cv2.imshow("Object Tracking" , frame)

    #Exit with Esc
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break

Video.realease()
cv2.destroyAllWindows()