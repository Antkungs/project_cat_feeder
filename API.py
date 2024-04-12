from flask import Flask, request, jsonify
import mysql.connector
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to MySQL
def connect():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="projectcat"
    )

    if db.is_connected():
        print("Connected to MySQL!")
    return db


@app.route('/catinformation', methods=['GET'])
def get_catinformation():
    db = connect()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT * FROM catinformation")
        data = cursor.fetchall()
        results = []
        for x in data:
            converted_data = {
                'id_cat': x[0],  
                'name_cat': x[1],
                'food_give': x[2],
                'id_tank': x[3],
                'time1_start': str(datetime.timedelta(seconds=x[4].total_seconds())),
                'time1_end': str(datetime.timedelta(seconds=x[5].total_seconds())),    
                'time2_start': str(datetime.timedelta(seconds=x[6].total_seconds())),
                'time2_end': str(datetime.timedelta(seconds=x[7].total_seconds())),
                'time3_start': str(datetime.timedelta(seconds=x[8].total_seconds())),
                'time3_end': str(datetime.timedelta(seconds=x[9].total_seconds())),
                'time1_status': x[10],
                'time2_status': x[11],
                'time3_status': x[12],
            }
            results.append(converted_data)
        return jsonify(results)  # ส่งคืนในรูปแบบ JSON

    return jsonify({"error": "Invalid request"})  # ส่งคืนข้อความผิดพลาดในรูปแบบ JSON

@app.route('/setstatus', methods=['GET'])
def set_status():
    db = connect()
    catID = request.args.get('id')
    times = request.args.get('time')
    status = request.args.get('status')
    # ตรวจสอบค่า status เป็น boolean
    if status.lower() == 'true':
        status = True
    else:
        status = False
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM catinformation WHERE id_cat = '{catID}' ")
    row = cursor.fetchone()
    
    if row:
        update = f"time{times}_status"
        cursor.execute(f"UPDATE catinformation SET {update} = %s WHERE id_cat = %s", (status, catID))
        db.commit()
        cursor.close()
        return 'Status updated successfully', 200
    else:
        cursor.close()
        return 'Cat ID not found', 404

@app.route('/eatinformation', methods=['GET'])
def get_eatinformation():
    db = connect()
    catID = request.args.get('catID')
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')
    date= f"{year}-{month}-{day}"
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM  eatinformation WHERE ID_Cat = '{catID}' AND DATE(CurrentTime) = '{date}' ")
    data = cursor.fetchall()
    results = []
    for x in data:
        converted_data = {
                'ID_Cat': x[0],
                'Food_give': x[1],
                'Food_eat': x[2],
                'Food_remaining': x[3],
                'CurrentTime': x[4],
            }
        results.append(converted_data)
    return jsonify(results)

@app.route('/notification', methods=['GET'])
def get_notification():
    db = connect()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notification")
        data = cursor.fetchall()
        results = []
        for x in data:
            converted_data = {
                'token': x[0],  
                'hour': x[1],
            }
            results.append(converted_data)
        return jsonify(results)

    return jsonify({"error": "Invalid request"})

def update_status():
    db = connect()
    cursor = db.cursor()
    # อัปเดตค่าของ time1_status, time2_status, และ time3_status เป็น FALSE ทุกๆเที่ยงคืน
    cursor.execute("UPDATE catinformation SET time1_status = FALSE, time2_status = FALSE, time3_status = FALSE")
    db.commit()
    cursor.close()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
    
