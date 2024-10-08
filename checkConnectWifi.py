import urllib.request
import time
import subprocess
import connectNetwork as connect
from gpiozero import LED
#from pyaccesspoint import pyaccesspoint
led = LED('GPIO17')
def check_internet():
	try:
		urllib.request.urlopen("http://www.google.com",timeout=2)
		return True
	except urllib.request.URLError:
		return False

def create_hotspot(ssid, pwd):
    try:
        ap = pyaccesspoint.AccessPoint(ssid, pwd)
        ap.start()
        print("Hotspot created. SSID: {}, Password: {}".format(ssid, pwd))
    except Exception as e:
        print("Error creating hotspot:", e)
	
def main():
	while not check_internet():
		led.on()
		print("no internet")
		#create_hotspot("RaspberryPI5","helloworld")
		connect.main()
		time.sleep(10)
	
	print("Internet Connect")
	led.off()
	#subprocess.run(["python3","/home/antkung/Desktop/Project/Time/code/api.py"])

if __name__ == "__main__":
	main()
