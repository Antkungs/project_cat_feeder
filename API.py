from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="projectcat"
)

if db.is_connected():
    print("Connected to MySQL!")


@app.route('/catinformation', methods=['GET'])
def get_catinformation():
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
            }
            results.append(converted_data)
        return jsonify(results)  # ส่งคืนในรูปแบบ JSON

    return jsonify({"error": "Invalid request"})  # ส่งคืนข้อความผิดพลาดในรูปแบบ JSON


@app.route('/eatinformation', methods=['GET'])
def get_eatinformation():
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
