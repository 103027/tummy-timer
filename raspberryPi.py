import paho.mqtt.client as mqtt
import serial
import time
import json
from datetime import datetime
import RPi.GPIO as GPIO

#MQTT stuff
MQTT_BROKER = "493700728f8244298020d35f5eeadd2e.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "hassan"
MQTT_PASSWORD = "IOTproject10"
MQTT_TOPIC_SCHEDULE = "petfeeder/schedule"
MQTT_TOPIC_CONTROL = "petfeeder/control"
MQTT_TOPIC_SENSOR = "petfeeder/sensor"

#pins
MOTOR_PIN1 = 17
MOTOR_PIN2 = 18
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PIN2, GPIO.OUT, initial=GPIO.LOW)

#Arduino port setup
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600


def initialize_serial():
    global ser
    for attempt in range(3):  #Retry 3 times max
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print(f"Connected to Arduino on {SERIAL_PORT}")
            time.sleep(2)
            return True
        except serial.SerialException as e:
            print(f"Serial connection attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    print("Failed to connect to Arduino after multiple attempts")
    return False

#serial connection
ser = None
if not initialize_serial():
    exit(1)

#pet presence stuff
last_signal = False
presence_counter = 0
PRESENCE_THRESHOLD_SECONDS = 2
last_dispense_time = 0



#read from Arduino T and F 
def read_signal():
    global ser
    try:
        if ser.in_waiting > 0:
            raw_byte = ser.read(1)
            if raw_byte:
                char = raw_byte.decode('ascii')
                if char == 'T':
                    return True
                elif char == 'F':
                    return False
                else:
                    print(f"Invalid data received: '{char}'")
                    return None
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        ser.close()
        
        if initialize_serial():
            print("Reconnected to Arduino")
        return None
    except Exception as e:
        print(f"Error reading data: {e}")
        return None
    return None



def is_pet_present():
    global last_signal, presence_counter
    signal = read_signal()
    if signal is not None:
        if signal:
            presence_counter += 0.1
            if presence_counter >= PRESENCE_THRESHOLD_SECONDS:
                last_signal = True
                presence_counter = PRESENCE_THRESHOLD_SECONDS
        else:
            presence_counter = 0
            last_signal = False
    return last_signal



#reset presence
def reset_presence():
    global last_signal, presence_counter
    last_signal = False
    presence_counter = 0

#dispense food -- portions
def dispense_portions(portion_count):
    duration = 0.5  #tune this later
    for i in range(portion_count):
        print(f"Dispensing portion {i + 1}/{portion_count} - Opening")
        GPIO.output(MOTOR_PIN1, GPIO.HIGH)
        GPIO.output(MOTOR_PIN2, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(MOTOR_PIN1, GPIO.LOW)
        GPIO.output(MOTOR_PIN2, GPIO.LOW)
        print("Closing")
        time.sleep(0.5)
        GPIO.output(MOTOR_PIN1, GPIO.LOW)
        GPIO.output(MOTOR_PIN2, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(MOTOR_PIN1, GPIO.LOW)
        GPIO.output(MOTOR_PIN2, GPIO.LOW)
        time.sleep(duration)
    print("Dispensing complete")





def publish_sensor_data(pet_present, portion):
    data = {
        "pet_present": pet_present,
        "food_dispensed": True,
        "weight": portion * 25,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish(MQTT_TOPIC_SENSOR, json.dumps(data))




schedule_data = None
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT")
        client.subscribe(MQTT_TOPIC_SCHEDULE)
        client.subscribe(MQTT_TOPIC_CONTROL)
        print("Subscribed to topics")
        client.publish(MQTT_TOPIC_CONTROL, "", retain=True)
    else:
        print(f"Failed to connect, code {rc}")





def on_message(client, userdata, msg):
    global schedule_data
    payload = msg.payload.decode().strip()
    if not payload:
        print(f"Empty payload on {msg.topic}, skipping")
        return
    try:
        data = json.loads(payload)
        if msg.topic == MQTT_TOPIC_CONTROL:
            if data.get("action") == "dispense":
                portion = data["portion"]
                dispense_portions(portion)
                publish_sensor_data(False, portion)
        elif msg.topic == MQTT_TOPIC_SCHEDULE:
            schedule_data = data
            print(f"Updated schedule: {schedule_data}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON on {msg.topic}: {e}")
        
        
        

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)






last_print = time.time()
try:
    client.loop_start()
    while True:
        if schedule_data:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.strftime("%a")
            for feeding in schedule_data:
                if current_day in feeding["days"] and feeding["startTime"] <= current_time <= feeding["endTime"]:
                    if feeding.get("flag", True):
                        continue
                    #if time did pass since last dispense
                    current_time_seconds = time.time()
                    if current_time_seconds - last_dispense_time < 60:
                        continue
                    if is_pet_present():
                        print(f"Conditions met for {feeding['startTime']}-{feeding['endTime']}: Pet present: {last_signal}")
                        print("Pet-presence: ", last_signal)
                        dispense_portions(feeding["portion"])
                        publish_sensor_data(True, feeding["portion"])
                        reset_presence()
                        last_dispense_time = time.time()
            if time.time() - last_print >= 10:
                print(f"Current schedule: {schedule_data}")
                last_print = time.time()
        else:
            print("No schedule data available yet")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
    ser.close()
    print("Serial connection closed.")