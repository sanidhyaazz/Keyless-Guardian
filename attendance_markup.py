from pymongo import MongoClient
from datetime import date, datetime


def make_attendance(uid):                      #accessing database

    uri = "mongodb+srv://happybirthday:KIEc69RJmDFmCFu5@galaxycluster.ivlxj.mongodb.net/"

    dateToday = str(date.today().strftime("%d-%m-%Y"))
    now = datetime.now()

    try:
        client = MongoClient(uri)      #initializing mongodb client connection
        database = client["labserver"]                      #accessing database
        member_data = database["member_detail"]
        memDetail = member_data.find_one({"uid": uid},{"_id":0,"name":1})

        attendance = database[dateToday]            #create collection with the name of date(YYYY-MM-DD) if it doesn't exist or access it if it exists

        if(memDetail):
            attendance.insert_one({"uid": uid, "name": memDetail["name"], "time": f"{now.strftime('%H:%M:%S')}", "Validity": "AUTHORIZED"})
            return memDetail["name"]
        else:
            attendance.insert_one({"uid": uid, "time": f"{now.strftime('%H:%M:%S')}", "Validity": "UNAUTHORIZED"})


        client.close()
        return "0"

    except:
        return "Error"