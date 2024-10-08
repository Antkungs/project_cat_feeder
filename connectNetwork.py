import subprocess
def connect_to_wifi(ssid, password):
    # Construct the nmcli command
    command = f"sudo nmcli device wifi connect '{ssid}' password '{password}'"

    # Execute the command
    subprocess.run(command, shell=True)

def read_credentials_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            ssid = lines[0].strip()
            password = lines[1].strip()
            return ssid, password
    except FileNotFoundError:
        print("File not found.")
        return None, None
    

def read_credentials_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            ssid = lines[0].strip()
            password = lines[1].strip()
            token = lines[2].strip()
            return token
    except FileNotFoundError:
        print("File not found.")
        return None, None

def main():
    # File path containing SSID and password
    file_path = '/var/www/html/txt/wificonfig_.txt'

    # Read SSID and password from the file
    ssid, password = read_credentials_from_file(file_path)

    # Check if credentials were successfully read from the file
    if ssid is not None and password is not None:
        print(f"SSID: {ssid}")
        print(f"Password: {password}")
        print("--------------------------")

        # Connect to WiFi
        connect_to_wifi(ssid, password)
    else:
        print("Failed to read SSID and password from the file.")

x = '/var/www/html/txt/wificonfig_.txt'
token = read_credentials_from_file(x)
print(token)