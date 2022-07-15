import time
import numpy as np
import cv2
from flask import Flask, render_template, Response, stream_with_context, request


time.sleep(0.1)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)
app = Flask('__name__')

def video_stream():
    while True:
        ret, frame = cap.read()
        if not ret:
            break;
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')

while True:
     ret, frame = cap.read()
     flipped = cv2.flip(frame, flipCode = -1)
     frame1 = cv2.resize(flipped, (640, 480))
     font = cv2.FONT_HERSHEY_SIMPLEX

     gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
     boxes, weights = hog.detectMultiScale(frame1, winStride=(8,8) )
     boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
     for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame1, (xA, yA), (xB, yB),(0, 255, 0), 2)
        
        b=len(boxes)
        cv2.putText(frame1,"peoplecount:"+str(b),(20,50),0,2,(255,0,0),3)
     img = cv2.resize(frame1,(640,480))
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     if key == ord("q"):
        break

@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
