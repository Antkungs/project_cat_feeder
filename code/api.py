import os
import socket
import cv2
import time
import mysql.connector
import requests
from flask import Flask, Response, request, jsonify,render_template
from flask_cors import CORS
from datetime import date, datetime, timedelta
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from gpiozero import OutputDevice,PWMOutputDevice,Button
from time import sleep
import hardwareSelect
import LineNotifi as line

app = Flask(__name__)
CORS(app)
frame2 = 0
haveEat = False
# Connect to MySQL
def connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="USERNAME",
            password="PASSWORD",
            database="projectcat"
        )
        if db.is_connected():
            print("Connected to MySQL!")
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def webcam():
    # Open webcam
    global frame2
    
    while True:
        frame = frame2
        # Process frame if needed
        # Example: Convert frame to grayscale
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        # Yield frame as byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        
@app.route('/webcamFeed')
def video_feed():
    return Response(webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
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

        #print(results)
        return render_template('setting.html', results=results)

    # Return an error message if the request method is not GET
    return jsonify({"error": "Invalid request"})



@app.route('/admin', methods=['GET'])
def admin():
    db = connect()  # Assuming this function connects to the database
    if request.method == 'GET':
        cursor = db.cursor()

        # Fetch tank data
        cursor.execute("SELECT * FROM tank")
        tank_data = cursor.fetchall()

        # Fetch all columns from catinformation table
        cursor.execute("SELECT * FROM catinformation")
        cat_data = cursor.fetchall()

        # Pass both tank and cat data to the template
        return render_template('admin.html', tanks=tank_data, cats=cat_data)



def handle_timedelta(obj):
    if isinstance(obj, timedelta):
        # Convert timedelta to total seconds
        total_seconds = int(obj.total_seconds())
        
        # Calculate hours and minutes
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Return the time in HH:MM format
        return f"{hours:02}:{minutes:02}"
    
    return obj


@app.route('/settingCat/<id>', methods=['GET'])
def settingCat(id):
    db = connect()  # Assuming connect() is a function that connects to the database
    if request.method == 'GET':
        cursor = db.cursor()

        # Fetch tank information
        cursor.execute("SELECT * FROM tank")
        tank_data = cursor.fetchall()
        if not tank_data:
            return jsonify({"error": "No tank data found"})

        # Prepare results for tank data
        tank_results = [{'id_tank': record[0], 'name_tank': record[1], 'notification_percen': record[2]} for record in tank_data]

        # Fetch cat information using the correct column 'id_cat'
        cursor.execute("SELECT * FROM catinformation WHERE id_cat = %s", (id,))
        cat_data = cursor.fetchall()

        # Fetch column names for the catinformation table
        column_names = [desc[0] for desc in cursor.description]

        # Prepare results for cat data including all columns and convert timedeltas
        cat_results = [dict((column, handle_timedelta(value)) for column, value in zip(column_names, cat)) for cat in cat_data]

        return jsonify({
            'tanks': tank_results,
            'cats': cat_results
        })
    
    return jsonify({"error": "Invalid request"})


@app.route('/getTank', methods=['GET'])
def getTank():
    db = connect()  # Assuming connect() is a function that connects to the database
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tank")
        data = cursor.fetchall()
        if data:
            results = [{'id_tank': record[0], 'name_tank': record[1], 'notification_percen': record[2]} for record in data]
            return jsonify(results)
        else:
            return jsonify({"error": "No data found"})

    return jsonify({"error": "Invalid request"})


@app.route('/getNameTank/<id_tank>', methods=['GET'])
def getNameTank(id_tank):
    db = connect()  # Assuming connect() is a function that connects to the database
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM tank WHERE id_tank = '{id_tank}'")
        data = cursor.fetchall()
        if data:
            results = [{ 'name_tank': record[1], 'notification_percen': record[2]} for record in data]
            return jsonify(results)
        else:
            return jsonify({"error": "No data found"})

    return jsonify({"error": "Invalid request"})


def checkTime(stime_1, etime_1, stime_2, etime_2, stime_3, etime_3):
    def parse_time(t):
        return datetime.strptime(t, '%H:%M')

    try:
        stime_1 = parse_time(stime_1)
        etime_1 = parse_time(etime_1)
        stime_2 = parse_time(stime_2)
        etime_2 = parse_time(etime_2)
        stime_3 = parse_time(stime_3)
        etime_3 = parse_time(etime_3)
    except ValueError:
        # Handle invalid time format
        return False, "Invalid time format. Please use HH:MM."

    # Check if start times are earlier than end times
    errors = []

    if stime_1 >= etime_1:
        errors.append("เริ่มมื้อ 1 ต้องน้อยกว่าเวลาที่จบมื้อ 1")
    if stime_2 >= etime_2:
        errors.append("เริ่มมื้อ 2 ต้องน้อยกว่าเวลาที่จบมื้อ 2")
    if stime_3 >= etime_3:
        errors.append("เริ่มมื้อ 3 ต้องน้อยกว่าเวลาที่จบมื้อ 3")
    
    if errors:
        return False, "\n".join(errors)
    
    return True, None

UPLOAD_FOLDER = r'/home/antkung/Desktop/project_cat_feeder/code/static/images'  # Adjust the path if needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/insertData/<id_cat>', methods=['POST'])
def insert_data(id_cat):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            name = request.form['name']
            food_quantity = request.form['food_quantity']
            stime_1 = request.form['stime_1']
            etime_1 = request.form['etime_1']
            stime_2 = request.form['stime_2']
            etime_2 = request.form['etime_2']
            stime_3 = request.form['stime_3']
            etime_3 = request.form['etime_3']
            tank = request.form['tank']
            
            # Time validation
            is_valid, error_message = checkTime(stime_1, etime_1, stime_2, etime_2, stime_3, etime_3)
            if not is_valid:
                return f"""
                <script>
                    alert('Error: {error_message}');
                    window.location.href = '/setting';
                </script>
                """
            
            # Database connection
            db = connect()
            cursor = db.cursor()
            
            # Get existing image URL
            cursor.execute("SELECT image_url FROM catinformation WHERE id_cat = %s", (id_cat,))
            existing_image = cursor.fetchone()
            old_image_url = existing_image[0] if existing_image else None
            
            # Handle file upload
            new_image_url = old_image_url  # Default to old image
            if 'file' in request.files and request.files['file'].filename != '':
                file = request.files['file']
                if allowed_file(file.filename):
                    filename = f"cat{id_cat}.jpg"  # Rename the file to cat{id_cat}.jpg
                    new_image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(new_image_url)
                    print(f"Image saved to {new_image_url}")  # Debugging output
            
            # Prepare SQL command
            sql = """
                UPDATE `catinformation` 
                SET `name_cat` = %s, `food_give` = %s, 
                    `time1_start` = %s, `time1_end` = %s, 
                    `time2_start` = %s, `time2_end` = %s, 
                    `time3_start` = %s, `time3_end` = %s, 
                    `id_tank` = %s, `image_url` = %s
                WHERE id_cat = %s
            """
            values = (name, food_quantity, stime_1, etime_1, stime_2, etime_2, stime_3, etime_3, tank, new_image_url, id_cat)
            
            # Execute SQL command
            cursor.execute(sql, values)
            db.commit()
            return """
            <script>
                alert('Update Successfully');
                window.location.href = '/';
            </script>
            """
        except Exception as e:
            if db.is_connected():
                db.rollback()
            print(f"Error occurred: {e}")  # Log error to console
            return f"""
            <script>
                alert('Error: {e}');
                window.location.href = '/setting';
            </script>
            """
            
@app.route('/insertLineFirstTime', methods=['POST'])
def insertLineFirstTime():
    if request.method == 'POST':
        token = request.form['token']
        db = connect()
        cursor = db.cursor()
        sql = "UPDATE `notification` SET `token` = %s WHERE 1"  # Fixed SQL syntax
        values = (token, )

        try:
            # ทำการ execute คำสั่ง SQL
            cursor.execute(sql, values)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            print("Scuess")
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในการ execute คำสั่ง SQL
            db.rollback()
            print(f"Error: {e}")

        
     
@app.route('/insertLine', methods=['POST'])
def insertLine():
    if request.method == 'POST':
        token = request.form['token']
        hour = request.form['hour']
        db = connect()
        cursor = db.cursor()
        sql = "UPDATE `notification` SET `token` = %s, `hour` = %s WHERE 1"  # Fixed SQL syntax
        values = (token, hour)

        try:
            # ทำการ execute คำสั่ง SQL
            cursor.execute(sql, values)
            # commit การเปลี่ยนแปลงในฐานข้อมูล
            db.commit()
            try:
                line.send_text_check(token,"\nเปิดการใช้งานการแจ้งเตือนเครื่องให้อาหารอัตโนมัติสำเร็จ")
            except Exception as e:
                print(e)
            return """
            <script>
                alert('Update Successfully');
                window.location.href = '/setting';
            </script>
            """
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในการ execute คำสั่ง SQL
            db.rollback()
            return f"""
            <script>
                alert('Error: {e}');
                window.location.href = '/setting';
            </script>
            """
        
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

@app.route('/setEatinformation', methods=['POST'])
def set_eatinformation():
    try:
        # Extract data from JSON body
        data = request.json  # รับข้อมูลจาก body ของ POST request
        id_cat = data.get('ID_Cat')
        food_give = data.get('food_give')
        food_eat = data.get('Food_eat')
        food_remaining = data.get('Food_remaining')
        timestamp = data.get('CurrentTime')

        # Validate parameters
        if not (id_cat and food_give is not None and food_eat is not None and food_remaining is not None and timestamp):
            return jsonify({"error": "Missing required parameters"}), 400

        # Connect to database
        db = connect()
        cursor = db.cursor()

        # Use parameterized query to prevent SQL injection
        query = """
        INSERT INTO eatinformation (ID_Cat, Food_give, Food_eat, Food_remaining, CurrentTime)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        Food_give = VALUES(Food_give),
        Food_eat = VALUES(Food_eat),
        Food_remaining = VALUES(Food_remaining),
        CurrentTime = VALUES(CurrentTime)
        """
        cursor.execute(query, (id_cat, food_give, food_eat, food_remaining, timestamp))
        db.commit()

        # Close database connection
        cursor.close()
        db.close()

        return jsonify({"message": "Record updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#การกินทั้งหมดในเดือนปัจจุบัน
@app.route('/get_cat_oneMonthInfoGrape/<cat_name>', methods=['GET'])
def get_cat_oneMonthInfoGrape(cat_name):
    try:
        db = connect()
        cursor = db.cursor()
        
        # Get cat ID
        cursor.execute("SELECT id_cat FROM catinformation WHERE name_cat = %s", (cat_name,))
        data = cursor.fetchone()
        
        if not data:
            return jsonify({"error": "Cat not found"}), 404
        
        cat_id = data[0]
        
        # Calculate date range for the current month
        current_month_start = date.today().replace(day=1)
        next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        # Fetch food consumption data
        cursor.execute("""
            SELECT DATE(CurrentTime) AS date, SUM(food_eat) AS total_food_eat
            FROM eatinformation
            WHERE id_cat = %s AND CurrentTime >= %s AND CurrentTime < %s
            GROUP BY DATE(CurrentTime)
            ORDER BY DATE(CurrentTime) ASC
        """, (cat_id, current_month_start, next_month_start))
        
        data = cursor.fetchall()
        results = []
        
        for record in data:
            formatted_date = record[0].strftime("%d %b %Y")
            cat_info = {
                'cat_name': cat_name,
                'date': formatted_date,
                'total_food_eat': record[1],
            }
            results.append(cat_info)
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/get_cat_allInfoGrape/<cat_name>', methods=['GET'])
def get_cat_allInfoGrape(cat_name):
    try:
        db = connect()
        cursor = db.cursor()
        
        # Get date range from query parameters
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        
        # Get cat ID
        cursor.execute("SELECT id_cat FROM catinformation WHERE name_cat = %s", (cat_name,))
        data = cursor.fetchone()
        
        if not data:
            return jsonify({"error": "Cat not found"}), 404
        
        cat_id = data[0]
        
        # Get food consumption data within the date range
        cursor.execute("""
            SELECT DATE(CurrentTime) AS date, SUM(food_eat) AS total_food_eat
            FROM eatinformation
            WHERE id_cat = %s AND DATE(CurrentTime) BETWEEN %s AND %s
            GROUP BY DATE(CurrentTime)
            ORDER BY DATE(CurrentTime) ASC
        """, (cat_id, start_date, end_date))
        
        data = cursor.fetchall()
        results = []
        
        for record in data:
            date_object = record[0]
            formatted_date = date_object.strftime("%d %b %Y")
            cat_info = {
                'cat_name': cat_name,
                'date': formatted_date,
                'total_food_eat': record[1],
            }
            results.append(cat_info)
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

#ข้อมูลการกิน ณ วันนี้
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


#ข้อมูลของแมว
@app.route('/catinformation', methods=['GET'])
def get_catinformation():
    try:
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
                    'time1_start': str(timedelta(seconds=x[4].total_seconds())),
                    'time1_end': str(timedelta(seconds=x[5].total_seconds())),    
                    'time2_start': str(timedelta(seconds=x[6].total_seconds())),
                    'time2_end': str(timedelta(seconds=x[7].total_seconds())),
                    'time3_start': str(timedelta(seconds=x[8].total_seconds())),
                    'time3_end': str(timedelta(seconds=x[9].total_seconds())),
                    'time1_status': x[10],
                    'time2_status': x[11],
                    'time3_status': x[12],
                    'img_path': x[13],
                }
                results.append(converted_data)
            return jsonify(results)  # ส่งคืนในรูปแบบ JSON

        return jsonify({"error": "Invalid request"})  # ส่งคืนข้อความผิดพลาดในรูปแบบ JSON
    except Exception as e:
        print(f"Error: {e}")

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


@app.route('/getPercenTank', methods=['GET'])
def getPercenTank():
    try:
        db = connect()
        cursor = db.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT hour FROM notification")
            hour_data = cursor.fetchall()
            hours = [item[0] for item in hour_data]

            cursor.execute("SELECT * FROM tank")
            tank_data = cursor.fetchall()

            if tank_data:
                tank_results = [
                    {'notification_percen': record[2]}
                    for record in tank_data
                ]
                return jsonify({
                    'hour': hours,
                    'tanks': tank_results
                })
            else:
                return jsonify({"error": "No tank data found"})

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return jsonify({"error": "Invalid request"}), 400

def update_status():
    db = connect()
    cursor = db.cursor()
    # อัปเดตค่าของ time1_status, time2_status, และ time3_status เป็น FALSE ทุกๆเที่ยงคืน
    cursor.execute("UPDATE catinformation SET time1_status = FALSE, time2_status = FALSE, time3_status = FALSE")
    db.commit()
    cursor.close()

def deleteData(select):
    db = connect()
    cursor = db.cursor()
    # อัปเดตค่าของ time1_status, time2_status, และ time3_status เป็น FALSE ทุกๆเที่ยงคืน
    cursor.execute(f"DELETE FROM catinformation WHERE id_cat = '{select}';")
    db.commit()
    cursor.close()
    updateID(select)

def updateID(select):
    db = connect()
    cursor = db.cursor()
    # อัปเดตค่าของ time1_status, time2_status, และ time3_status เป็น FALSE ทุกๆเที่ยงคืน
    cursor.execute(f"UPDATE catinformation SET id_cat = id_cat - 1 WHERE id_cat > '{select}';")
    db.commit()
    cursor.close()

def update_status():
    db = connect()
    cursor = db.cursor()
    # อัปเดตค่าของ time1_status, time2_status, และ time3_status เป็น FALSE ทุกๆเที่ยงคืน
    cursor.execute("UPDATE catinformation SET time1_status = FALSE, time2_status = FALSE, time3_status = FALSE")
    db.commit()
    cursor.close()

def resetStatusToFalse():
    """ Reset time statuses to FALSE """
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE catinformation SET time1_status = FALSE, time2_status = FALSE, time3_status = FALSE"
        )
        db.commit()
        print("Reset status fields successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()
        db.close()

@app.route('/resetStatusToFalse', methods=['GET'])
def reset_Status_False():
    """ Endpoint to manually trigger resetStatusToFalse """
    try:
        resetStatusToFalse()
        return jsonify({"message": "Status fields false reset successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def resetStatusToTrue():
    """ Reset time statuses to FALSE """
    db = connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE catinformation SET time1_status = TRUE, time2_status = TRUE, time3_status = TRUE"
        )
        db.commit()
        print("Reset status fields successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()
        db.close()

@app.route('/resetStatusToTrue', methods=['GET'])
def reset_Status_True():
    """ Endpoint to manually trigger resetStatusToTrue """
    try:
        resetStatusToTrue()
        return jsonify({"message": "Status fields true reset successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/switch1', methods=['GET'])
def switch1():
    try:
        hardwareSelect.switchOnPlace1()
        return jsonify({"message": "successfully"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/switch2', methods=['GET'])
def switch2():
    try:
        hardwareSelect.switchOnPlace2()
        return jsonify({"message": "successfully"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/switch3', methods=['GET'])
def switch3():
    try:
        servoFood()
        return jsonify({"message": "successfully"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/switch4', methods=['GET'])
def switch4():
    select_value =  request.args.get('select')
    range_value = request.args.get('value')
    # Process the values as needed
    print(f"Select: {select_value}, Value: {range_value}")
    hardwareSelect.loadRange(select_value,range_value)
    return jsonify({'status': 'success', 'select': select_value, 'value': range_value})

@app.route('/lineTest', methods=['GET'])
def lineTest():
    try:
        line.send_text("\ntest notification")
        return jsonify({"message": "successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cat_detection', methods=['POST'])
def add_cat_detection():
    data = request.get_json()
    
    # Check that required fields are provided
    if 'idcatfound' not in data or 'conf' not in data:
        return jsonify({"error": "Missing idcatfound or conf"}), 400

    idcatfound = data['idcatfound']
    conf = data['conf']
    detected_at = data.get('detected_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    print(f"Received data - detected_at: {detected_at}, idcatfound: {idcatfound}, conf: {conf}")  # Debugging output

    db = connect()
    cursor = db.cursor()
    
    # Define the SQL query
    query = """
    INSERT INTO `cat_detection` (`detected_at`, `idcatfound`, `conf`)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    conf = VALUES(conf), detected_at = VALUES(detected_at);
    """
    
    try:
        # Execute the query with the values in a tuple
        cursor.execute(query, (detected_at, idcatfound, conf))
        db.commit()

        # Check the number of rows affected
        affected_rows = cursor.rowcount
        print(f"Rows affected: {affected_rows}")  # Debugging output

        if affected_rows == 0:
            print("No new records were inserted or updated.")  # More debugging

        return jsonify({"message": "Cat detection saved successfully!"}), 200
    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"SQL Error: {str(e)}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500
    finally:
        # Close database connection
        cursor.close()
        db.close()


def detect():
    global frame2 , current_time , haveEat
    model = YOLO(r"/home/USER/Desktop/project_cat_feeder/code/model/catver0.2.pt") #model นับจำนวนแมว
    model2 = YOLO(r"/home/USER/Desktop/project_cat_feeder/code/model/best.pt") #model หาแมว
    cap = cv2.VideoCapture(0)
    current_time = time.time()
    updated_time = current_time + 5
    findCat1 = False
    
    skip_frame_count = 10 # Skip 10 frames, meaning every 6th frame will be processed
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result1 = model(frame,conf=0.6,classes=15) #classes = 15
        try:  
            print(f"กำลังกิน : {haveEat}")
            #ตีกรอบแมวธรรมดา
            for result in result1:
                boxes = result.boxes  # Bounding boxes for detected objects

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                    conf = box.conf[0]  # Confidence score
                    cls = int(box.cls[0])  # Class id
                    label = f"{model.names[cls]} {conf:.2f}"  # Class name and confidence score

                    # Draw the bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    current_time = time.time()
            #print(result1[0].boxes.conf)
            if(result1[0].boxes.cls.tolist().count(25) > 1): #เช็คแมวว่ามี > 1 ตัว
                print("เจอแมวมากกว่า 1 ตัว")
                findCat1 = False
                updated_time = None
            if(result1[0].boxes.cls.tolist().count(15) == 1):
                if not findCat1:
                    findCat1 = True  # Set flag that 1 cat has been detected
                    current_time = time.time()
                    updated_time = current_time + 1  # Set the time 2 seconds from now
                    # Check if the timer has passed 2 seconds after detecting 1 cat
                elif findCat1 and updated_time and current_time >= updated_time: #เช็คแมวว่ามี 1 ตัว
                    result2 = model2(frame) 
                    top_box = None  # เก็บ bounding box ที่มีค่า confidence สูงสุด
                    max_conf = 0  # ค่า confidence สูงสุดเริ่มต้นเป็น 0
                    top_label = ""  # ตัวแปรเพื่อเก็บ label ที่มีค่า confidence สูงสุด
                    top_class_id = None  # ตัวแปรเพื่อเก็บ class ID ที่มี confidence สูงสุด

                    for result in result2:
                        if hasattr(result, 'boxes'):  # ตรวจสอบว่ามี attribute 'boxes' หรือไม่
                            for box in result.boxes:
                                class_id = int(box.cls)  # Get the class ID
                                class_name = result.names[class_id]  # Get the class name from the model's 
                                confidence = box.conf.item()  # แปลง confidence เป็น float โดยใช้ .item()

                                # เช็คว่าค่า confidence สูงกว่าค่าที่บันทึกไว้หรือไม่
                            if confidence > max_conf:
                                max_conf = confidence
                                top_box = box
                                top_label = f"{class_name} {confidence:.2f}"
                                top_class_id = class_id
                    if confidence > 0.80:
                        # แสดงผลเฉพาะการตรวจจับที่มั่นใจที่สุด
                        print(f"Detected class ID: {top_class_id + 1}")  # +1 ถ้าคุณใช้ ID เริ่มต้นที่ 0
                        print(f"Detected class name: {top_label.split()[0]}")  # พิมพ์ชื่อ class
                        print(f"Confidence: {max_conf:.2f}") 
                        current_time = datetime.now()  # สร้างวัตถุ datetime
                        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        data = {
                            "idcatfound": class_id+1,
                            "conf": confidence,
                            "detected_at": formatted_time
                        }
                        requests.post("http://localhost:3000/api/cat_detection", json=data)
                        filename = "temp.jpg"  #ถ่ายภาพเพื่อเก็บสถานะไว้ส่งไปยังไลน์
                        cv2.imwrite(filename, frame)
                        #line.send_image("temp.jpg", model2.names[probs.top1])
                        jasonCatInformation = getTime(top_class_id + 1) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา
                        print(jasonCatInformation)
                        while haveEat:   
                                print(f"{top_class_id + 1} : {top_label.split()[0]} กำลังกิน :{haveEat}")
                                ret, frame = cap.read()
                                if not ret:          
                                    break
                                result1 = model(frame)
                                current_time = time.time() 
                                if(result1[0].boxes.cls.tolist().count(15) >= 1):
                                    play_loop_time = current_time + 5
                                elif(current_time > play_loop_time):
                                    #hardwareSelect.loadFoodEnd(jasonCatInformation)
                                    time.sleep(5)
                                    #hardwareSelect.throwAwayFood()
                                    print("สถานะ :  การกินเสร็จสิ้น")
                                    haveEat = False
                                    frame2 = frame
                        current_time = time.time()
                        updated_time = current_time + 5
                    else:
                        print("สถานะ :  เจอแมว 1 ตัว NOT SURE")
            else:
                findCat1 = False
                updated_time = None
                print("do noting")

        except Exception as e:
            print("ERROR")
        frame2 = frame
        #cv2.imshow("result",frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()
        
def servoFood():
    sleep(2)
    try:
        servo_pwm = PWMOutputDevice(12)
        servo_pwm.value = 0.05
        sleep(1)
        servo_pwm.value = 0.16
        sleep(1)
        servo_pwm.value = 0.05
        sleep(1)
        servo_pwm.value = 0.16
        sleep(3)
        servo_pwm.value = 0.05
        sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        servo_pwm.close()
        print("Servo Ending")

def getTime(select):
    try:
        global haveEat
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # Fetch data from API
            cat = next((c for c in cats if c['id_cat'] == select), None)  # Find the right cat by id

            if cat:
                jasonCatInformation = {
                    'idCat': cat['id_cat'],
                    'nameCat': cat['name_cat'],
                    'foodGive': cat['food_give'],
                    'idTank': cat['id_tank']
                }

                # Pre-parse meal times and statuses
                time_data = [
                    {'start': cat['time1_start'], 'end': cat['time1_end'], 'status': cat['time1_status']},
                    {'start': cat['time2_start'], 'end': cat['time2_end'], 'status': cat['time2_status']},
                    {'start': cat['time3_start'], 'end': cat['time3_end'], 'status': cat['time3_status']}
                ]

                current_time = datetime.now().time()  # Get current time
                print(f"ID : {jasonCatInformation['idCat']}\n"
                      f"Name : {jasonCatInformation['nameCat']}\n"
                      f"foodGive : {jasonCatInformation['foodGive']}\n"
                      f"idTank : {jasonCatInformation['idTank']}\n"
                      f"Current Time : {current_time}\n")

                # Loop through time data to check meal schedules
                for idx, data in enumerate(time_data):
                    start_time = datetime.strptime(data['start'], "%H:%M:%S").time()
                    end_time = datetime.strptime(data['end'], "%H:%M:%S").time()
                    status = data['status']

                    # Check if within the eating window and if not already eaten
                    if start_time <= current_time <= end_time and not status:
                        print("current_time pass")
                        
                        # Process food dispensing
                        jasonCatInformation = hardwareSelect.loadCell(jasonCatInformation)
                        
                        times = idx + 1
                        print(f"Processed ID {select} for time {times}")

                        # Update status to prevent reprocessing
                        update_status_url = f'http://localhost:3000/setstatus?id={select}&time={times}&status={True}'
                        requests.get(update_status_url)

                        # Notify Line
                        current_time_string = current_time.strftime("%H:%M:%S")
                        try:
                            line.sendCatEat(jasonCatInformation['nameCat'], current_time_string)
                        except Exception as e:
                            print("Line Error:", e)

                        haveEat = True
                        return jasonCatInformation
                    else:
                        print("not in time")

                return "nothing"
        else:
            print(f'Error: {response_cat.status_code} - {response_cat.text}')
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to an external server to get the local IP address
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error: {e}"

def mainapi():
    app.run(host="0.0.0.0", port=3000)

#mainapi()
