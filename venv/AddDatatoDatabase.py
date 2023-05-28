
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
 
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://realtime-database-54879-default-rtdb.firebaseio.com/"
})
 
ref = db.reference('Registered')
 
data = {
    "ABAYAN SHAWN LESNAR":
        {
            "name": "SHAWN ABAYAN",
            "major": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
        
    "ESMERALDA REX EMMANUELLE":
        {
            "name": "REX  ESMERALDA",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "LAROGA MHARLECK C":
        {
            "name": "MHARLECK LAROGA",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "PRESILDA RAIZA":
        {
            "name": "RAIZA PRESILDA",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "RABIN ELA":
       {
            "name": "ELA RABIN",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "REGAMA JANINE":
        {
            "name": "JANINE REGAMA",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "TUQUERO CARELL JOHN T":
        {
            "name": "JOHN TUQUERO ",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
     "ZERJECKO MISFITS S":
        {
            "name": "MISFITS ZERJECKO",
            "role": "BSIT",
            "starting_year": 2019,
            "total_attendance": 0,
            "standing": "Registered",
            "year": 4,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
        
    "Prof1":
        {
            "name": "Sample Professor1",
            "role": "Professor",
            "starting_year": 2015,
            "total_attendance": 1,
            "standing": "Registered",
            "year": 0,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
    "Prof2":
        {
            "name": "Sample Professor2",
            "role": "Professor",
            "starting_year": 2015,
            "total_attendance": 1,
            "standing": "Registered",
            "year": 0,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },
    "Prof3":
        {
            "name": "Sample Professor3",
            "role": "Professor",
            "starting_year": 2015,
            "total_attendance": 1,
            "standing": "Registered",
            "year": 0,
            "last_attendance_time": "2023-05-29 00:00:00"
            
        },        
    
}

 
for key, value in data.items():
    ref.child(key).set(value)