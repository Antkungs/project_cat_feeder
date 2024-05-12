from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from flask import render_template
from datetime import datetime

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

@app.route('/', methods=['GET'])
def webApp():
    db = connect()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT name_cat FROM catinformation")
        data = cursor.fetchall()
        results = [x[0] for x in data]
        
        return render_template('cat.html', cat_names=results)  # Correct indentation
    # Return an error message if the request method is not GET
    return jsonify({"error": "Invalid request"})

@app.route('/setting', methods=['GET'])
def setting():
    db = connect()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT id_cat , name_cat FROM catinformation")
        data = cursor.fetchall()
        results = []
        for cat in data:
            results.append({'id_cat': cat[0], 'name_cat': cat[1]})

        print(results)
        return render_template('setting.html', results=results)

    # Return an error message if the request method is not GET
    return jsonify({"error": "Invalid request"})


@app.route('/getTank', methods=['GET'])
def getTank():
    db = connect()  # Assuming connect() is a function that connects to the database
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tank")
        data = cursor.fetchall()
        if data:
            results = [{'id_tank': record[0], 'name_tank': record[1], 'persens': record[2]} for record in data]
            return jsonify(results)
        else:
            return jsonify({"error": "No data found"})

    return jsonify({"error": "Invalid request"})


@app.route('/insertData/<id_cat>', methods=['POST'])
def insert_data(id_cat):
    if request.method == 'POST':
        # ดึงข้อมูลจากฟอร์ม
        name = request.form['name']
        food_quantity = request.form['food_quantity']
        stime_1 = request.form['stime_1']
        etime_1 = request.form['etime_1']
        stime_2 = request.form['stime_2']
        etime_2 = request.form['etime_2']
        stime_3 = request.form['stime_3']
        etime_3 = request.form['etime_3']
        tank = request.form['tank']
        
        db = connect()
        cursor = db.cursor()
        sql = "UPDATE `catinformation` SET `name_cat` = %s, `food_give` = %s, `time1_start` = %s, `time1_end` = %s, `time2_start` = %s, `time2_end` = %s, `time3_start` = %s, `time3_end` = %s, `id_tank` = %s WHERE id_cat = %s"
        values = (name, food_quantity, stime_1, etime_1, stime_2, etime_2, stime_3, etime_3, tank, id_cat)
        
        try:
            # ทำการ execute คำสั่ง SQL
            cursor.execute(sql, values)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            return """
            <script>
                alert('Update Successfully');
                window.location.href = '/';
            </script>
            """
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในการ execute คำสั่ง SQL
            db.rollback()
            return f'Error: {e}'
        
@app.route('/insertLine', methods=['POST'])
def insertLine():
    if request.method == 'POST':
        token = request.form['token']

        db = connect()
        cursor = db.cursor()
        sql = "UPDATE `notification` SET `token` = %s WHERE 1"
        values = (token,)

        try:
            # ทำการ execute คำสั่ง SQL
            cursor.execute(sql, values)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            return """
            <script>
                alert('Update Successfully');
                window.location.href = '/';
            </script>
            """
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในการ execute คำสั่ง SQL
            db.rollback()
            return f'Error: {e}'
        
@app.route('/insertTank', methods=['POST'])
def insertTank():
    if request.method == 'POST':
        Tank1 = request.form['Tank1']
        percenTank1 = request.form['percenTank1']
        Tank2 = request.form['Tank2']
        percenTank2 = request.form['percenTank2']

        db = connect()
        cursor = db.cursor()
        sql1 = "UPDATE `tank` SET `name_tank` = %s , `notification_percen` = %s WHERE id_tank = 1"
        values1 = (Tank1,percenTank1)
        sql2 = "UPDATE `tank` SET `name_tank` = %s , `notification_percen` = %s WHERE id_tank = 2"
        values2 = (Tank2,percenTank2)

        try:
            # ทำการ execute คำสั่ง SQL
            cursor.execute(sql1, values1)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            cursor.execute(sql2, values2)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            return """
            <script>
                alert('Update Successfully');
                window.location.href = '/';
            </script>
            """
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในการ execute คำสั่ง SQL
            db.rollback()
            return f'Error: {e}'



@app.route('/get_cat_infogrape/<cat_name>', methods=['GET'])
def get_cat_infogrape(cat_name):
    db = connect()
    cursor = db.cursor()
    cursor.execute(f"SELECT id_cat FROM catinformation WHERE name_cat = '{cat_name}'")
    data = cursor.fetchone()
    if data:
        cat_id = data[0]
        cursor.execute(f"SELECT DATE(CurrentTime), SUM(food_eat) FROM eatinformation WHERE id_cat = '{cat_id}' GROUP BY DATE(CurrentTime) ORDER BY CurrentTime ASC")
        data = cursor.fetchall()
        results = []
        for record in data:
            # 
            original_date = record[0]
            original_date_string = original_date.strftime("%a, %d %b %Y %H:%M:%S")
            date_object = datetime.strptime(original_date_string, "%a, %d %b %Y %H:%M:%S")
            formatted_date = date_object.strftime("%d %b %Y")
            cat_info = {
                'cat_name': cat_name,
                'date': formatted_date,
                'total_food_eat': record[1],
            }
            results.append(cat_info)
        return jsonify(results)
    else:
        return jsonify({"error": "Cat not found"})

    
@app.route('/get_cat_info/<cat_name>', methods=['GET'])
def get_cat_info(cat_name):
    db = connect()
    cursor = db.cursor()
    cursor.execute(f"SELECT id_cat FROM catinformation WHERE name_cat = '{cat_name}'")
    data = cursor.fetchone()
    if data:
        cat_id = data[0]
        today_date = datetime.today().date()
        cursor.execute(f"SELECT * FROM eatinformation WHERE id_cat = '{cat_id}' AND DATE(CurrentTime) = '{today_date}' ORDER BY CurrentTime ASC")
        data = cursor.fetchall()
        results = []
        for record in data:
            # 
            cat_info = {
                'cat_name': cat_name,
                'id_cat': record[0],
                'food_give': record[1],
                'food_eat': record[2],
                'food_remaining': record[3],
                'CurrentTime': record[4].strftime('%H:%M:%S')
            }
            results.append(cat_info)
        return jsonify(results)
    else:
        return jsonify({"error": "Cat not found"})



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
    
