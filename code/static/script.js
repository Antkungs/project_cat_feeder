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
function toggleBox() {
    const infoBox = document.querySelector('.info-box');
    infoBox.classList.toggle('show');
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
            // Display cat images if available

            


            if (data.error) {
                catInfoDiv.textContent = 'Error: ' + data.error;
            } else if (data.length === 0) {
                const recordDiv = document.createElement('div');
                    recordDiv.classList.add('record');

                    const foodGivenDiv = document.createElement('div');
                    foodGivenDiv.classList.add('info-box');
                    foodGivenDiv.innerHTML = `
                    <p class="info-detail">ยังไม่มีการกินวันนี้</p>
                    `;
                    recordDiv.appendChild(foodGivenDiv);

                    const foodEatenDiv = document.createElement('div');
                    foodEatenDiv.classList.add('info-box');
                    foodEatenDiv.innerHTML = `
                    <p class="info-detail">ยังไม่มีการกินวันนี้</p>
                    `;
                    recordDiv.appendChild(foodEatenDiv);

                    const foodRemainingDiv = document.createElement('div');
                    foodRemainingDiv.classList.add('info-box');
                    foodRemainingDiv.innerHTML = `
                    <p class="info-detail">ยังไม่มีการกินวันนี้</p>
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
                        <p class="info-title">ปริมาณอาหารที่ให้</p>
                        <p class="info-detail">ครั้งที่ ${index + 1} <br> เวลา ${eatingRecord.CurrentTime} น.</p>
                        <p class="info-amount"><span class="amount">${eatingRecord.food_give}</span> กรัม</p>
                    `;
                    recordDiv.appendChild(foodGivenDiv);

                    const foodEatenDiv = document.createElement('div');
                    foodEatenDiv.classList.add('info-box');
                    foodEatenDiv.innerHTML = `
                        <p class="info-title">ปริมาณอาหารที่กิน</p>
                        <p class="info-detail">ครั้งที่ ${index + 1} <br> เวลา ${eatingRecord.CurrentTime} น.</p>
                        <p class="info-amount"><span class="amount">${eatingRecord.food_eat}</span> กรัม</p>
                    `;
                    recordDiv.appendChild(foodEatenDiv);

                    const foodRemainingDiv = document.createElement('div');
                    foodRemainingDiv.classList.add('info-box');
                    foodRemainingDiv.innerHTML = `
                        <p class="info-title">ปริมาณอาหารที่เหลือ</p>
                        <p class="info-detail">ครั้งที่ ${index + 1} <br> เวลา ${eatingRecord.CurrentTime} น.</p>
                        <p class="info-amount"><span class="amount">${eatingRecord.food_remaining}</span> กรัม</p>
                    `;
                    recordDiv.appendChild(foodRemainingDiv);

                    catInfoDiv.appendChild(recordDiv);
                });
            }
            toggleCharts()

        })
        .catch(error => console.error('Error:', error));
}

function toggleCharts() {
    const catName = document.getElementById('catName').textContent.trim();
    const startDate = document.getElementById('startDate').value; // Get the value from the startDate input
    const endDate = document.getElementById('endDate').value; // Get the value from the endDate input


    // Call the function to update the chart
    showGrapeAll(catName, startDate, endDate);
}

let myChart; // Declare myChart at a higher scope if it's not already

function showGrapeAll(catName, startDate, endDate) {
    fetch(`/get_cat_allInfoGrape/${catName}?start=${startDate}&end=${endDate}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('chartAll').getContext('2d');

            // Prepare data for the chart
            let labels = data.length > 0 ? data.map(item => item.date) : ['No Data'];
            let totalFoodEaten = data.length > 0 ? data.map(item => item.total_food_eat) : [0];
            let maxValue = data.length > 0 ? Math.max(...totalFoodEaten) + 10 : 10;

            // Destroy the existing chart if it exists
            if (myChart) {
                myChart.destroy();
            }
            const formatDate = (date) => {
                const day = String(date.getDate()).padStart(2, '0');
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const year = date.getFullYear();
              
                return `${day}/${month}/${year}`;
            };
  
            const parseDate = (dateStr) => new Date(dateStr);
            
            const formattedStartDate = formatDate(parseDate(startDate));
            const formattedEndDate = formatDate(parseDate(endDate));
            // Create a new chart
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'การกินทั้งหมด',
                        data: totalFoodEaten,
                        fill: false,
                        borderColor: '#512da8',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: `${formattedStartDate} ถึง ${formattedEndDate}`
                            }
                        },
                        y: {
                            min: 0,
                            max: maxValue,
                            title: {
                                display: true,
                                text: 'การกินทั้งหมด'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `ปริมาณ: ${context.raw}`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
}
function catSetting(id) {
    fetch(`/settingCat/${id}`)
        .then(response => response.json())
        .then(data => {
            const catData = data.cats;  // Access cat data
            const tankData = data.tanks;  // Access tank data

            const catSetting = document.getElementById('catSetting');
            catSetting.innerHTML = catData.map(cat => `
            <div style="padding: 20px;" id="containerSetting">
                <h3><b style="color: #512da8;">แก้ไขรายละเอียดแมว ${cat.name_cat}</b></h3>
                <form id="updateForm" action="/insertData/${cat.id_cat}" method="POST"  enctype="multipart/form-data">
                    <div>
                        <img id="existingImage" src="/static/images/cat${cat.id_cat}.jpg" alt="Current Cat Image" style="max-width: 200px; max-height: 200px;">
                    </div>
                                        

                    <!-- File input for new image -->
                    <div style="padding-top: 20px;">
                        <label for="name"><b>ตั้งค่าชื่อแมว</b></label><br>
                        <input type="text" id="name" name="name" value="${cat.name_cat}" placeholder="name" required><br>
                    </div>
                
                    <div style="padding-top: 20px;">
                        <label for="food_quantity"><b>ปริมาณอาหารต่อมื้อ (กรัม)</b></label><br>
                        <input type="number" id="food_quantity" name="food_quantity" placeholder="ปริมาณอาหาร" min="10" max="200" value="${cat.food_give}" required><br>
                    </div>

                    <p><b>ช่วงเวลาการให้อาหาร</b></p>
                    <div class="padding-time">
                    <label for="stime_2">มื้อที่ 1:</label>
                        <div class="line">
                            <div class="line-time">
                                <label for="stime_1">เริ่มมื้อ 1:</label>
                                <input type="time" id="stime_1" name="stime_1" value="${cat.time1_start}" required>
                            </div>
                            <div class="line-time">
                                <label for="etime_1">สิ้นสุดมื้อ 1:</label>
                                <input type="time" id="etime_1" name="etime_1" value="${cat.time1_end}" required>
                            </div>
                        </div>
                        <label for="stime_2">มื้อที่ 2:</label>
                        <div class="line">
                            <div class="line-time">
                                <label for="stime_2">เริ่มมื้อ 2:</label>
                                <input type="time" id="stime_2" name="stime_2" value="${cat.time2_start}" required>
                            </div>
                            <div class="line-time">
                                <label for="etime_2">สิ้นสุดมื้อ 2:</label>
                                <input type="time" id="etime_2" name="etime_2" value="${cat.time2_end}" required>
                            </div>
                        </div>
                        <label for="stime_2">มื้อที่ 3:</label>
                        <div class="line">
                            <div class="line-time">
                                <label for="stime_3">เริ่มมื้อ 3:</label>
                                <input type="time" id="stime_3" name="stime_3" value="${cat.time3_start}" required>
                            </div>
                            <div class="line-time">
                                <label for="etime_3">สิ้นสุดมื้อ 3:</label>
                                <input type="time" id="etime_3" name="etime_3" value="${cat.time3_end}" required>
                            </div>
                        </div>
                    </div>
                
                    <br>
                    <label for="food_container"><b>ถังอาหาร</b></label>
                    <div class="tooltip" style="color: #d1c4e9;">
                        <i class="fas fa-info-circle"></i><span class="tooltiptext">ใช้สำหรับการตั้งค่าถังอาหารที่ต้องการให้</span>
                    </div> 
                    
                    <div style="display: flex; align-items: center; justify-content: center; padding-top: 20px">
                        ${tankData.map(tank => `
                            <div style="margin: 0 10px;">
                                <input type="radio" id="tank${tank.id_tank}" name="tank" value="${tank.id_tank}" required>
                                <label for="tank${tank.id_tank}">${tank.name_tank}</label>
                            </div>
                        `).join('')}
                    </div>

            
                    <br>
                    <div>
                        <div>
                        <label for="food_container"><b>แก้ไขรูปภาพ</b></label>
                        <div class="tooltip">
                            <i class="fas fa-info-circle"></i>
                        <span class="tooltiptext">ใช้สำหรับการเปลี่ยนรูปภาพของแมว</span>
                        </div>
                        </div>
                        <div  style="display: flex; align-items: center; justify-content: center; padding-top: 20px">
                            <div class="file-input-container">
                                <input type="file" name="file" id="file">
                            </div>
                        </div>
                    </div>
                    
                    <br>
                    <button type="submit" value="Submit">Submit</button>
                    <button type="reset" onclick="redirectToSetting()">Cancel</button>
                </form>
            </div>
            `).join('');
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
        <div  style="padding-top: 20px;" id="contrainnerSetting">
            <form id="updateFormLine" action="/insertLine" method="post">
                <h3><b style="color: #512da8;">ตั้งค่าการแจ้งเตือน</b></h3>
                    <label for="token"><b>LineToken</b></label>                    
                    <div class="tooltip">
                        <i class="fas fa-info-circle"></i><span class="tooltiptext">Token สำหรับรับการแจ้งเตือนผ่านแอพ Line</span>
                    </div><br>
                    <input type="text" id="token" name="token" placeholder="LineToken" required><br>
                    <br>
                    <label for="token"><b>เวลาการแจ้งเตือนซ้ำ (ชั่วโมง)</b></label>                    
                    <div class="tooltip">
                        <i class="fas fa-info-circle"></i><span class="tooltiptext">ใช้สำหรับการตั้งค่าเวลาสำหรับการแจ้งเตือนผ่านแอพ Line ซ้ำ</span>
                    </div><br>
                    <input type="text" id="hour" name="hour" placeholder="hour" required><br>
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
<div style="padding-top: 20px;" id="contrainnerSetting">
    <form id="updateFormTank" action="/insertTank" method="post">
        <h3><b style="color: #512da8;">ตั้งค่าถังอาหาร</b></h3>

        <label for="percenTank1"><b>ตั้งค่าถังที่ 1</b> </label>
        <div style="border: 1px solid #666; padding: 15px; margin-bottom: 20px;">
            <label for="Tank1"><b>ตั้งค่าชื่อถังอาหารที่ 1</b>
                <div class="tooltip">
                    <i class="fas fa-info-circle"></i>
                    <span class="tooltiptext">ใช้สำหรับการเปลี่ยนชื่อถังอาหารที่ 1</span>
                </div>
            </label><br>
            <input type="text" id="Tank1" name="Tank1" placeholder="Rename tank1" value="${data[0].name_tank}" required><br>
            <label for="percenTank1"><b>ตั้งค่าการแจ้งเตือน ${data[0].name_tank}b>
                <div class="tooltip">
                    <i class="fas fa-info-circle"></i>
                    <span class="tooltiptext">ใช้สำหรับการตั้งค่าการแจ้งเตือนเมื่อปริมาณอาหารในถัง ${data[0].name_tank} ต่ำกว่าร้อยละ (0-90) % ที่กำหนด</span>
                </div>
            </label><br>
            <input type="number" id="percenTank1" name="percenTank1" placeholder="ร้อยละ" value="${data[0].notification_percen}" min="10" max="90" required><br>
        </div>
        <label for="percenTank1"><b>ตั้งค่าถังที่ 2</b> </label>
        <div style="border: 1px solid #666; padding: 15px; margin-bottom: 20px; padding-top: 30px;">
            <label for="Tank2"><b>ตั้งค่าชื่อถังอาหารที่ 2</b>
                <div class="tooltip">
                    <i class="fas fa-info-circle"></i>
                    <span class="tooltiptext">ใช้สำหรับการเปลี่ยนชื่อถังอาหารที่ 2</span>
                </div>
            </label><br>
            <input type="text" id="Tank2" name="Tank2" placeholder="Rename tank2" value="${data[1].name_tank}" required><br>
            
            <label for="percenTank2"><b>แจ้งเตือน ${data[1].name_tank}</b>
                <div class="tooltip">
                    <i class="fas fa-info-circle"></i>
                    <span class="tooltiptext">ใช้สำหรับการตั้งค่าการแจ้งเตือนเมื่อปริมาณอาหารในถัง ${data[1].name_tank} ต่ำกว่าร้อยละ (0-90) % ที่กำหนด</span>
                </div>
            </label><br>
            <input type="number" id="percenTank2" name="percenTank2" placeholder="ร้อยละ" value="${data[1].notification_percen}" min="10" max="90" required>
            </div>

        <button type="submit" value="Submit">Submit</button>
        <button type="reset" onclick="redirectToSetting()">Cancel</button>
    </form>
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

function buttonLine() {
    fetch('/lineTest', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    redirectToAdmin()
}

function button1(){
    fetch('/switch1', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    redirectToAdmin()
}


function button2(){
    fetch('/switch2', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    redirectToAdmin()
}

function button3(){
    fetch('/switch3', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    redirectToAdmin()
}

function button4(select){
    var value = document.getElementById("range").value
    console.log(select)
    if(value === 0){
        redirectToAdmin()
    }

    else{
        var url = `/switch4?select=${select}&value=${value}`;
        // Use fetch to send the GET request with query parameters
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    document.getElementById("range").value = 0
    redirectToAdmin()
}

