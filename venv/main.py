import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
from collections import Counter

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://realtime-database-54879-default-rtdb.firebaseio.com/",
    'storageBucket': "realtime-database-54879.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []
encodeListUnknown = []  # List to store unknown face encodings

# Set the threshold and tolerance it add more accuracy on face recognition
threshold = 0.7
tolerance = 0.6

while True:
    success, img = cap.read()

    if not success:
        # Handle camera read failure
        print("Failed to capture frame from the camera.")
        break

    imgS = cv2.resize(img, None, fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        # Initialize lists for storing recognized and unrecognized face IDs
        recognizedIds = []
        unrecognizedIds = []

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=tolerance)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex] and faceDis[matchIndex] < threshold:
                # Known face detected
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                recognizedIds.append(studentIds[matchIndex])
            else:
                # Unknown face detected
                unrecognizedIds.append(len(encodeListUnknown))
                encodeListUnknown.append(encodeFace)

        if recognizedIds:
            # Identify the most common recognized ID
            mostCommonId = Counter(recognizedIds).most_common(1)[0][0]

            if id != mostCommonId:
                id = mostCommonId
                counter = 1
                modeType = 1

        if unrecognizedIds:
            # Set modeType to 4 for unknown person
            modeType = 4

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Registered/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                if studentInfo is not None:
                    try:
                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                        print(secondsElapsed)
                        # 24 hours = 86400 seconds 1 attendance per day
                        if secondsElapsed > 1000:
                            ref = db.reference(f'Registered/{id}')
                            studentInfo['total_attendance'] += 1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    except ValueError:
                        print("Invalid date and time format: ", studentInfo['last_attendance_time'])
                        datetimeObject = datetime.min  # Set to the minimum datetime value as a default
                else:
                    print("Student information not found for the given ID.")

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    if studentInfo is not None:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        if 'role' in studentInfo:
                            cv2.putText(imgBackground, str(studentInfo['role']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                        (255, 255, 255), 1)
                        else:
                            cv2.putText(imgBackground, "Unknown", (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                        (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (50, 50, 50), 1)

                        resizedImgStudent = cv2.resize(imgStudent, (216, 216))
                        imgBackground[175:175 + 216, 909:909 + 216] = resizedImgStudent
                    else:
                        # Handle case when studentInfo is None
                        print("Student information not found for the given ID.")

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = None
                    imgStudent = None
                    imgBackground[55:55 + 640, 162:162 + 480] = 0

        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)
