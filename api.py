import cv2 , time ,mysql.connector , Time
import requests
from flask import Flask, Response, request, jsonify,render_template
from flask_cors import CORS
from datetime import date, datetime, timedelta
import LineNotifi as line
import hardwareSelect
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


app = Flask(__name__)
CORS(app)
frame2 = 0
haveEat = False
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
            line.send_text(token, "\nเปิดการใช้งานการแจ้งเตือนเครื่องให้อาหารอัตโนมัติสำเร็จ")
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

#insert การกิน
@app.route('/setEatinformation', methods=['GET'])
def set_eatinformation():
    try:
        # Extract data from query parameters
        id_cat = request.args.get('ID_Cat')
        food_give = request.args.get('food_give')
        food_eat = request.args.get('Food_eat')
        food_remaining = request.args.get('Food_remaining')
        timestamp = request.args.get('CurrentTime')

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

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500
        
#การกินทั้งหมดในเดือนปัจจุบัน
@app.route('/get_cat_oneMonthInfoGrape/<cat_name>', methods=['GET'])
def get_cat_oneMonthInfoGrape(cat_name):
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT id_cat FROM catinformation WHERE name_cat = %s", (cat_name,))
    data = cursor.fetchone()
    if data:
        cat_id = data[0]
        current_month_start = date.today().replace(day=1)
        next_month_start = (current_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        cursor.execute("""
            SELECT DATE(CurrentTime), SUM(food_eat) 
            FROM eatinformation 
            WHERE id_cat = %s AND CurrentTime >= %s AND CurrentTime < %s
            GROUP BY DATE(CurrentTime) 
            ORDER BY CurrentTime ASC
        """, (cat_id, current_month_start, next_month_start))
        data = cursor.fetchall()
        results = []
        for record in data:
            original_date = record[0]
            formatted_date = original_date.strftime("%d %b %Y")
            cat_info = {
                'cat_name': cat_name,
                'date': formatted_date,
                'total_food_eat': record[1],
            }
            results.append(cat_info)
        return jsonify(results)
    else:
        return jsonify({"error": "Cat not found"})
    
#การกินทั้งหมด
@app.route('/get_cat_allInfoGrape/<cat_name>', methods=['GET'])
def get_cat_allInfoGrape(cat_name):
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


def detect():
    global frame2 , current_time , haveEat
    model = YOLO("model/countCat.pt")
    model2 = YOLO("model/classification.pt") #model หาแมว
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result1 = model(frame,conf=0.6)
        result2 = model2(frame) 
        try:  
            print(haveEat)
            #ตีกรอบแมวธรรมดา
            for r in result1:
                annotator = Annotator(frame)    
                boxes = r.boxes
                for box in boxes:        
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)]) 
            frame = annotator.result() 

            current_time = time.time()
            #print(result1[0].boxes.conf)
            if(result1[0].boxes.cls.tolist().count(0) > 1): #เช็คแมวว่ามี > 1 ตัว
                print("เจอแมวมากกว่า 1 ตัว")
                updated_time = current_time + 5
                
            elif(result1[0].boxes.cls.tolist().count(0) == 1 and current_time >= updated_time): #เช็คแมวว่ามี 1 ตัว
                for result in result2:
                    probs = result.probs  # Probs object for classification outputs
                    print(probs.top1+1)
                    if(probs.top1conf > 0.7): #id classification
                        filename = "temp.jpg"  #ถ่ายภาพเพื่อเก็บสถานะไว้ส่งไปยังไลน์
                        cv2.imwrite(filename, frame)
                        #line.send_image("temp.jpg", model2.names[probs.top1])
                        getTime(probs.top1 + 1) #เรียกใช้ API เพื่อดึงข้อมูลแมวตัวนั้นๆ และเช็คเวลา
                        while haveEat:   
                            print(probs.top1+1)
                            print(model2.names[probs.top1])
                            ret, frame = cap.read()
                            if not ret:
                                break
                            result1 = model(frame)
                            current_time = time.time() 
                            if(result1[0].boxes.cls.tolist().count(0) >= 1):
                                play_loop_time = current_time + 5
                            elif(current_time > play_loop_time):
                                haveEat = False
                            frame2 = frame
                            #hardwareSelect.throwAwayFood()
                        current_time = time.time()
                        updated_time = current_time + 5
                    else:
                        print("NOT SURE")
            else:
                print("do noting")

        except Exception as e:
            #updated_time = current_time + 5
            print("ERROR")

        #current_time = time.time()
        #updated_time = current_time + 2
        frame2 = frame

        #cv2.imshow("result",frame)
        if cv2.waitKey(10) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()
        
def getTime(select):
    try:
        global haveEat
        time_data = []
        response_cat = requests.get('http://localhost:3000/catinformation')
        if response_cat.status_code == 200:
            cats = response_cat.json()  # รับข้อมูลทั้งหมดจาก API
            for cat in cats:  # loop เช็ค
                #เช็คไอดีให้ตรงกับค่าที่ส่งมา
                if cat['id_cat'] == select:
                    
                    id_cat = cat['id_cat']
                    name = cat['name_cat']# ดึงชื่อแมว

                    food_give = cat['food_give']#อาหารที่จะให้(กรัม)
                    id_tank = cat['id_tank']#ไอดี tank (Servo select)
                    #เวลามื้อที่ 1,2,3 และ สถานะการกิน
                    time_data = [
                        #มื้อที่ 1
                        {'start': datetime.strptime(cat['time1_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time1_end'], "%H:%M:%S").time(),
                        'status': cat['time1_status']},
                        #มื้อที่ 2
                        {'start': datetime.strptime(cat['time2_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time2_end'], "%H:%M:%S").time(),
                        'status': cat['time2_status']},
                        #มื้อที่ 3
                        {'start': datetime.strptime(cat['time3_start'], "%H:%M:%S").time(),
                        'end': datetime.strptime(cat['time3_end'], "%H:%M:%S").time(),
                        'status': cat['time3_status']}
                    ]
                    
                    current_time = datetime.now().time() #เวลาปัจจุบัน
                    print(id_cat)
                    print(current_time)
                    ### loop เก็บค่าเวลาและสถานะการกิน idx = มื้อ 
                    for idx, data in enumerate(time_data):
                        start_time = data['start']
                        end_time = data['end']
                        status = data['status']
                    
                        ### เช็คสถานะเวลาและการกินว่ากินไปหรือยัง ถ้ายังให้ทำอะไรก็ได้และตั้งค่าสถานะว่ากินไปแล้ว ###
                        #เวลาต้องอยู่ระหว่าง start and end staus ต้องเป็น false
                        if start_time <= current_time <= end_time and not status :
                            print("current_time pass")
                            ### รอเขียน process ทำการส่งค่าเพื่อเรียกใช้ Servo hardwareSelect.giveFood(food_give,id_tank) ปริมาณอาหาร,Servo ที่ต้องหมุน ###
                            times = idx + 1
                            print(f"Processed ID {select} for time {times}")
                            #เปลี่ยนสถานะ ณ เวลาที่มีการทำงาน  ให้เป็น True เพื่อป้องกันการทำซ้ำอีกรอบ
                            requests.get(f'http://localhost:3000/setstatus?id={select}&time={times}&status={True}')

                            ### แจ้งเตือนไลน์ ว่าตัวไหนมากิน ###
                            current_time_string = current_time.strftime("%H:%M:%S")
                            line.sendCatEat(name , current_time_string)
                            ### แจ้งเตือนไลน์ ###
                            haveEat = True

                        else:
                            #ไม่มีเวลาการกิน
                            print("not in time")
        else:
            print('Error:', response_cat.text)
    except Exception as e:
        print('Error occurred while processing responseCat:', e)

def mainapi():
    app.run(host="0.0.0.0", port=3000)

mainapi()
