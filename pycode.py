import serial
import subprocess
import time

# Set up the serial connection to Arduino (adjust COM port as needed)
ser = serial.Serial('COM5', 115200)  # Windows example, use the correct port for your system (e.g., '/dev/ttyUSB0' for Linux/Mac)

# Splunk HEC details
splunk_url = 'http://X.X.X.X:XXXX/services/collector/event'
splunk_token = 'token'

def send_to_splunk(humidity):
    # Construct the payload for Splunk HEC
    event_data = f'{{"sourcetype": "test_hec_logs", "event": {{"humidity": {humidity}}}}}'

    # Execute the curl command to send data to Splunk
    curl_command = [
        'curl', '-k', splunk_url, 
        '-H', f'Authorization: Splunk {splunk_token}',
        '-d', event_data
    ]
    print(curl_command)
    subprocess.run(curl_command)

while True:
    if ser.in_waiting > 0:
        # Read data from Arduino (assuming it's sent as "humidity, rssi" on a single line)
        data = ser.readline().decode('utf-8').strip()

        # Check if the data is in the expected format, e.g., "humidity_value, rssi_value"
        try:
            humidity_str, rssi_str = data.split(',')  # Assuming data is sent as "humidity,rssi"
            humidity = float(humidity_str)  # Convert humidity to a float
            rssi = int(rssi_str)  # Convert RSSI to an integer
            
            # Check RSSI value and decide whether to send to Splunk
            if rssi >= -50:
                send_to_splunk(humidity)
                print(f"Sent humidity: {humidity} to Splunk (RSSI: {rssi})")
            else:
                print(f"RSSI is too low ({rssi}), not sending data.")

        except ValueError:
            # Handle any data formatting issues
            print("Error reading humidity and RSSI data from Arduino. Data might be malformed.")
        
    time.sleep(1)  # wait for the next reading
