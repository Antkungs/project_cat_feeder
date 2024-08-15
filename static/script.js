function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function displayCurrentDateTime() {
    let now = new Date();

    let date = now.getDate();
    let month = now.getMonth() + 1;
    let year = now.getFullYear();

    // Extract time components
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    // Format date components to ensure they have two digits
    date = formatTime(date);
    month = formatTime(month);

    // Format time components to ensure they have two digits
    hours = formatTime(hours);
    minutes = formatTime(minutes);
    seconds = formatTime(seconds);

    let currentDateTimeDiv = document.getElementById('currentDateTime');
    currentDateTimeDiv.textContent = `${date}/${month}/${year} ${hours}:${minutes}:${seconds} น.`;

    // Call displayCurrentDateTime again after 1 second (1000 milliseconds)
    setTimeout(displayCurrentDateTime, 1000);
}

// Function to format time values to ensure they have two digits
function formatTime(time) {
    return time < 10 ? `0${time}` : time;
}

function showCatInfo(catName) {
    fetch('/get_cat_info/' + catName)
        .then(response => response.json())
        .then(data => {

            const catInfoDiv = document.getElementById('catInfo');
            catInfoDiv.innerHTML = ''; 
            const tageTitle = document.getElementById('tageTitle');
            tageTitle.innerHTML = '';  
            const chartAll = document.getElementById('chartAll');
            chartAll.style.display = 'block'; 
            const video_feed = document.getElementById('video_feed');
            video_feed.src = ''; 
            video_feed.style.display = 'none';    
            const catNameDiv = document.getElementById('catName');
            catNameDiv.textContent = catName;
            const switchChart = document.getElementById('switchChart');
            switchChart.style.display = 'flex';
            const blockChart = document.getElementById('blockChart');
            blockChart.style.display = 'block';


            if (data.error) {
                catInfoDiv.textContent = 'Error: ' + data.error;
            } else if (data.length === 0) {
                const recordDiv = document.createElement('div');
                    recordDiv.classList.add('record');

                    const foodGivenDiv = document.createElement('div');
                    foodGivenDiv.classList.add('info-box');
                    foodGivenDiv.innerHTML = `
                    <p>ยังไม่มีการกินวันนี้</p>
                    `;
                    recordDiv.appendChild(foodGivenDiv);

                    const foodEatenDiv = document.createElement('div');
                    foodEatenDiv.classList.add('info-box');
                    foodEatenDiv.innerHTML = `
                    <p>ยังไม่มีการกินวันนี้</p>
                    `;
                    recordDiv.appendChild(foodEatenDiv);

                    const foodRemainingDiv = document.createElement('div');
                    foodRemainingDiv.classList.add('info-box');
                    foodRemainingDiv.innerHTML = `
                    <p>ยังไม่มีการกินวันนี้</p>
                    `;
                    recordDiv.appendChild(foodRemainingDiv);

                    catInfoDiv.appendChild(recordDiv);
                    

            } else {
                // Show cat eating information
                data.forEach((eatingRecord, index) => {
                    const recordDiv = document.createElement('div');
                    recordDiv.classList.add('record');

                    const foodGivenDiv = document.createElement('div');
                    foodGivenDiv.classList.add('info-box');
                    foodGivenDiv.innerHTML = `
                        <p class="info-number">ครั้งที่ ${index + 1} เวลา ${eatingRecord.CurrentTime} น.</p>
                        <b>ปริมาณอาหารที่ให้ : ${eatingRecord.food_give} กรัม</b>
                    `;
                    recordDiv.appendChild(foodGivenDiv);

                    const foodEatenDiv = document.createElement('div');
                    foodEatenDiv.classList.add('info-box');
                    foodEatenDiv.innerHTML = `
                        <p class="info-number">ครั้งที่ ${index + 1} เวลา ${eatingRecord.CurrentTime} น.</p>
                        <b>ปริมาณอาหารที่กิน : ${eatingRecord.food_eat} กรัม</b>
                    `;
                    recordDiv.appendChild(foodEatenDiv);

                    const foodRemainingDiv = document.createElement('div');
                    foodRemainingDiv.classList.add('info-box');
                    foodRemainingDiv.innerHTML = `
                        <p class="info-number">ครั้งที่ ${index + 1} เวลา ${eatingRecord.CurrentTime} น.</p>
                        <b>ปริมาณอาหารที่เหลือ : ${eatingRecord.food_remaining} กรัม</b>
                    `;
                    recordDiv.appendChild(foodRemainingDiv);

                    catInfoDiv.appendChild(recordDiv);
                });
            }
            toggleCharts()

        })
        .catch(error => console.error('Error:', error));
}

function toggleCharts(){
    const infoToggle = document.getElementById('infoToggle');
    const catName = document.getElementById('catName').textContent.trim();
    
    if (infoToggle.checked) {
        showGrapeAll(catName,"chartAll");
    } else {
        showGrapeMonth(catName,"chartAll");
    }
}
function showGrapeMonth(catName,chart) {
    fetch('/get_cat_oneMonthInfoGrape/' + catName)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById(chart).getContext('2d');
            const labels = data.map(item => item.date); 
            const totalFoodEaten = data.map(item => item.total_food_eat); 
            if (window.myChart) {
                window.myChart.destroy();
            }

            const config = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'ปริมาณการกินเดือนปัจจุบัน',
                        data: totalFoodEaten,
                        fill: false,
                        borderColor: '#512da8',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            min: 0,
                            max: 300
                        }
                    }
                }
            };

            window.myChart = new Chart(ctx, config);
        })
        .catch(error => console.error('Error:', error));
}

function showGrapeAll(catName) {
    fetch('/get_cat_allInfoGrape/' + catName)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartAll').getContext('2d');
            const labels = data.map(item => item.date); 
            const totalFoodEaten = data.map(item => item.total_food_eat); 
            if (window.myChart) {
                window.myChart.destroy();
            }

            const config = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'ปริมาณการกินอาหารทั้งหมด',
                        data: totalFoodEaten,
                        fill: false,
                        borderColor: '#512da8',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            min: 0,
                            max: 300
                        }
                    }
                }
            };

            window.myChart = new Chart(ctx, config);
        })
        .catch(error => console.error('Error:', error));
}

function catSetting(ids,names) {
    fetch('/getTank')
    .then(response => response.json())
    .then(data => {
        const catSetting = document.getElementById('catSetting');
        catSetting.innerHTML = `
        <div style="align=center; ,padding: 20px;" id="contrainnerSetting">
            <h3 style="text-align: center;  padding-top:30px "><b style="color: #512da8;">แก้ไขรายละเอียดแมว ${names}</b></h3>
            <div style="text-align: center;">

            <form id="updateForm" action="/insertData/${ids}" method="post">
                
                <div  style="padding-top:20px">
                    <label for="name"><b>ตั้งค่าชื่อแมว</b></label><br>
                    <input type="text" id="name" name="name" value="${names}" placeholder="${names}" required><br>
                </div>
            
                <div  style="padding-top:20px">
                    <label for="food_quantity"><b>ปริมาณอาหารต่อมื้อ (กรัม) </b></label><br>
                    <input type="number" id="food_quantity" name="food_quantity" placeholder="ปริมาณอาหาร" min="1" max="1000" required><br>
                </div>
                <p><b>ช่วงเวลาการให้อาหาร</b></p>

                <div class="padding-time" >
                <div>
                    <div style="display:flex;justify-content: space-around;align-items: center;">
                        <label for="stime_1">เริ่มมื้อ 1  </label>
                        <input type="time" id="stime_1" name="stime_1" required  >
                    </div>

                    <div style="display:flex;justify-content: space-around;align-items: center; padding-right:5px;">
                        <label for="etime_1">สิ้นสุดมื้อ 1  </label>
                        <input type="time" id="etime_1" name="etime_1" required  >
                    </div>
                </div>
                
                <div>
                    <div style="display:flex;justify-content: space-around;align-items: center; ">
                        <label for="stime_2">เริ่มมื้อ 2  </label>
                        <input type="time" id="stime_2" name="stime_2" required  >
                    </div>

                    <div style="display:flex;justify-content: space-around;align-items: center; padding-right:5px;">
                        <label for="etime_2">สิ้นสุดมื้อ 2  </label>
                        <input type="time" id="etime_2" name="etime_2" required  >
                    </div>
                </div>
                
                <div>
                    <div style="display:flex;justify-content: space-around;align-items: center;">
                        <label for="stime_3">เริ่มมื้อ 3  </label>
                        <input type="time" id="stime_3" name="stime_3" required  >
                    </div>

                    <div style="display:flex;justify-content: space-around;align-items: center; padding-right:5px;">
                        <label for="etime_3">สิ้นสุดมื้อ 3  </label>
                        <input type="time" id="etime_3" name="etime_3" required  >
                    </div>
                </div>
                </div>
            
                <br>
                <label for="food_container"><b>ถังอาหาร</b>                  
                <div class="tooltip" style="color: #512da8;">
                        <i class="fas fa-info-circle"></i><span class="tooltiptext">ใช้สำหรับการตั้งค่าถังอาหารที่ต้องการให้</span>
                    </div></label><br>
                <div style="display:flex;align-items: center;padding-right:5px;flex-direction: row;justify-content: center;padding-top:20px">
                
                    <input type="radio" id="tank1" name="tank" value="${data[0]['id_tank']}" required>
                    <label for="tank1" id="tank1">${data[0].name_tank}</label><br>
                                
                    <input type="radio" id="tank2" name="tank" value="${data[1]['id_tank']}" required>
                    <label for="tank2" id="tank2">${data[1].name_tank}</label><br>
                </div>
                <div  style="display:flex;align-items: center;padding-right:5px;flex-direction: row;justify-content: center;padding-top:20px">
                    <select>
                        <option value="${data[0]['id_tank']}">${data[0].name_tank}</option>
                        <option value="${data[1]['id_tank']}">${data[1].name_tank}</option>
                    </select>
                </div>
                <br>
                <button type="submit" value="Submit">Submit</button>
                <button type="reset" onclick="redirectToSetting()">Cancel</button>
        
            </form>
            </div>
            </div>
        `;
    });

    document.getElementById('updateForm').addEventListener('submit', function(event) {
        // เมื่อ submit ให้เรียกฟังก์ชัน redirect และป้องกัน default behavior ของ form
        event.preventDefault();
    });
    

}

function redirectToHomePage() {
    window.location.href = "/";
}

function redirectToSetting() {
    window.location.href = "/setting";
}

function redirectToAdmin() {
    window.location.href = "/admin";
}


function lineSetting() {
    const catSetting = document.getElementById('catSetting');
    catSetting.innerHTML = `
        <div  style="text-align: center; padding-top: 50px;" id="contrainnerSetting">
            <form id="updateFormLine" action="/insertLine" method="post">
                <h3 style="text-align: center;"><b style="color: #512da8;">ตั้งค่าการแจ้งเตือน</b></h3>
                    <label for="token">LineToken</label>                    
                    <div class="tooltip">
                        <i class="fas fa-info-circle" style="color: #512da8;"></i><span class="tooltiptext">Token สำหรับรับการแจ้งเตือนผ่านแอพ Line</span>
                    </div><br>
                    <input type="text" id="token" name="token" placeholder="LineToken" required><br>
                    <br>
                <button type="submit" value="Submit">Submit</button>
                <button type="reset" onclick="redirectToSetting()">Cancel</button>
            </form>
        </div>
    `;

}

function tankSetting() {
    fetch('/getTank')
    .then(response => response.json())
    .then(data => {
    const catSetting = document.getElementById('catSetting');
    catSetting.innerHTML = `
        <div  style="text-align: center; padding-top: 50px; " id="contrainnerSetting">
            <form id="updateFormTank" action="/insertTank" method="post">
                <h3 style="text-align: center;"><b style="color: #512da8;">ตั้งค่าถังอาหาร</b></h3>
                <div>
                    <label for="Tank1">${data[0].name_tank}                 
                    <div class="tooltip">
                        <i class="fas fa-info-circle" style="color: #512da8;"></i><span class="tooltiptext">ใช้สำหรับการ Rename ${data[0].name_tank}</span>
                    </div></label><br>
                    <input type="text" id="Tank1" name="Tank1" placeholder="Rename tank1" value="${data[0].name_tank}" required><br>
                </div><br>
                <div>
                    <label for="percenTank1">แจ้งเตือน ${data[0].name_tank}                   
                    <div class="tooltip">
                        <i class="fas fa-info-circle" style="color: #512da8;"></i><span class="tooltiptext">ใช้สำหรับการตั้งค่าการแจ้งเตือนเมื่อปริมาณอาหารในถัง ${data[0].name_tank} ต่ำกว่าร้อยละ ที่กำหนด</span>
                    </div></label><br>
                    <input type="number" id="percenTank1" name="percenTank1" placeholder="ร้อยละ" value="${data[0].notification_percen}" min="1" max="99" required><br>
                </div><br>

                <div style="padding-top:30px">
                    <label for="percenTank2">${data[1].name_tank}</label>                    
                    <div class="tooltip">
                        <i class="fas fa-info-circle" style="color: #512da8;"></i><span class="tooltiptext">ใช้สำหรับการ Rename ${data[1].name_tank}</span>
                    </div><br>
                    <input type="text" id="Tank2" name="Tank2" placeholder="Rename tank2" value="${data[1].name_tank}" required><br>
                </div><br>
                <div>
                    <label for="percenTank2">แจ้งเตือน ${data[1].name_tank}
                    <div class="tooltip">
                        <i class="fas fa-info-circle" style="color: #512da8;"></i><span class="tooltiptext">ใช้สำหรับการตั้งค่าการแจ้งเตือนเมื่อปริมาณอาหารในถัง ${data[1].name_tank} ต่ำกว่าร้อยละ ที่กำหนด</span>
                    </div></label><br>
                    <input type="number" id="percenTank2" name="percenTank2" placeholder="ร้อยละ" value="${data[1].notification_percen}" min="1"  max="99" required><br>
                </div><br>
                
                <button type="submit" value="Submit">Submit</button>
                <button type="reset" onclick="redirectToSetting()">Cancel</button>
            </form>
        </div>
    `;
    });
}

function resetStatusToFalse() {
    fetch('/resetStatusToFalse', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Update status successfully');
    })
    .catch((error) => {
        alert('Update status Failed');
    });
    redirectToAdmin()
}

function resetStatusToTrue() {
    fetch('/resetStatusToTrue', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Update status successfully');
    })
    .catch((error) => {
        alert('Update status Failed');
    });
    redirectToAdmin()
}
function button1(){
    console.log("1");
    redirectToAdmin()
}

function button2(){
    console.log("2");
    redirectToAdmin()
}

function button3(){
    console.log("3");
    redirectToAdmin()
}



