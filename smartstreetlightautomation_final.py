import urequests
import network
from machine import Pin, ADC
from time import sleep, time
from machine import Pin,I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()
ssid ='Galaxy'
password ='chinmayi'
# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass
    print("Not Connected")

print('Connection successful')
print(wlan.ifconfig())

# Google Apps Script web app URL
WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbzicfg_RiZDUp96IjVamiWUlfc-YBy0wznJGjJ2z81cnqmQ60kAPLUIJM9EAHgHTt8/exec'

# Define pins for LEDs, ADC, and Buzzer
led1_pin = Pin(15, Pin.OUT)  # Green LED
led2_pin = Pin(14, Pin.OUT)  # Orange LED
monitor1_pin = ADC(27)  # Analog input for monitoring LED 1
monitor2_pin = ADC(28)  # Analog input for monitoring LED 2
ldr_pin = ADC(26)  # LDR pin
buz = Pin(16, Pin.OUT)  # Buzzer pin

# Threshold values (will be calculated)
threshold1_on = 0
threshold1_off = 0
threshold2_on = 0
threshold2_off = 0
ldr_threshold =600#600  #900 # Threshold for LDR sensor

# Margin to avoid false positives
margin = 50

# Function to get the average sensor reading
def get_average_reading(adc_pin, samples=10, delay=0.01):#0.1
    total = 0
    for _ in range(samples):
        total += adc_pin.read_u16()
        sleep(delay)
    return total // samples

def calibrate_thresholds():
    global threshold1_on, threshold1_off, threshold2_on, threshold2_off
    print("Calibrating thresholds...")

    # Ensure LEDs are off for initial readings
    led1_pin.off()
    led2_pin.off()
    sleep(1)
    led1_off_value = get_average_reading(monitor1_pin)
    led2_off_value = get_average_reading(monitor2_pin)
    print(f"LED 1 Off Value: {led1_off_value}")
    print(f"LED 2 Off Value: {led2_off_value}")

    # Ensure LEDs are on for next readings
    led1_pin.on()
    led2_pin.on()
    sleep(0.5)
    led1_on_value = get_average_reading(monitor1_pin)
    led2_on_value = get_average_reading(monitor2_pin)
    print(f"LED 1 On Value: {led1_on_value}")
    print(f"LED 2 On Value: {led2_on_value}")

    # Adjust thresholds based on calibration
    threshold1_on = led1_on_value - margin
    threshold1_off = led1_off_value + margin
    threshold2_on = led2_on_value - margin
    threshold2_off = led2_off_value + margin

    print(f"New Thresholds - LED 1 On: {threshold1_on}, Off: {threshold1_off}")
    print(f"New Thresholds - LED 2 On: {threshold2_on}, Off: {threshold2_off}")
    sleep(0.5)

# Function to log data to Google Sheets
def log_to_sheets(led1_status, led2_status, message=None):
    data = {
        "led1_name": "Green LED",
        "led1_status": led1_status,
        "led2_name": "Orange LED",
        "led2_status": led2_status,
        "message": message
    }

    try:
        print(f"Sending data: {data} to {WEB_APP_URL}")
        response = urequests.post(WEB_APP_URL, json=data)
        print("Response status:", response.status_code)
        if response.status_code != 200:
            print("Failed to log data:", response.text)
        response.close()
    except Exception as e:
        print("Error sending data to Google Sheets:", e)

# Calibrate the thresholds at the start
calibrate_thresholds()

last_log_time = time()
led1_status = "off"
led2_status = "off"

while True:
    # Read the LDR value
    ldr_value = get_average_reading(ldr_pin)
    print(f"LDR Value: {ldr_value}")  # Print LDR value for debugging

    # Control LEDs based on LDR value
    if ldr_value > ldr_threshold:
        led1_pin.on()  # Turn on LED 1
        led2_pin.on()  # Turn on LED 2
        new_led1_status = "on"
        new_led2_status = "on"
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("GreenLed:ON")
        lcd.move_to(0,1)
        lcd.putstr("OrangeLed:ON")
        
        
    else:
        led1_pin.off()  # Turn off LED 1
        led2_pin.off()  # Turn off LED 2
        new_led1_status = "off"
        new_led2_status = "off"
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("GreenLed:OFF")
        lcd.move_to(0,1)
        lcd.putstr("OrangeLed:OFF")

    # Log status immediately if LED status changes to off
    if led1_status == "on" and new_led1_status == "off":
        log_to_sheets("off", new_led2_status)
    if led2_status == "on" and new_led2_status == "off":
        log_to_sheets(new_led1_status, "off")

    led1_status = new_led1_status
    led2_status = new_led2_status

    # Log status every minute
    current_time = time()
    if current_time - last_log_time >= 30:
        log_to_sheets(led1_status, led2_status)
        last_log_time = current_time

    sleep(0.5)  # Adjust delay if needed

    # Check LED 1
    sensor1_value = get_average_reading(monitor1_pin)
    print(f"LED 1 Value: {sensor1_value}")  # Print sensor value for debugging
    if led1_status == "on":  # LEDs are supposed to be on
        if sensor1_value < threshold1_on:
            print("LED 1 is damaged or not functioning.")
            buz.value(1)
            led1_status="Damaged"#off
            led2_status="on"
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("GreenLed:Damaged")
            lcd.move_to(0,1)
            lcd.putstr("OrangeLed:ON")
            log_to_sheets(led1_status, led2_status, "LED 1 is damaged or not functioning.")
         
        else:
            print("LED 1 is functioning correctly.")
            buz.value(0)
    else:  # LEDs are supposed to be off
        if sensor1_value > threshold1_off:
            print("LED 1 is stuck on.")
            log_to_sheets(led1_status, led2_status, "LED 1 is stuck on.")
            #lcd.clear()
            #lcd.move_to(0,0)
            #lcd.putstr("stuck ON")
            
            
        else:
            print("LED 1 is off as expected.")
    
    sleep(0.5)  # Adjust delay if needed

    # Check LED 2
    sensor2_value = get_average_reading(monitor2_pin)
    print(f"LED 2 Value: {sensor2_value}")  # Print sensor value for debugging
    if led2_status == "on":  # LEDs are supposed to be on
        if sensor2_value < threshold2_on:
            print("LED 2 is damaged or not functioning.")
            buz.value(1)
            led2_status="Damaged"#off
            led1_status="on"
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr("GreenLed:ON")
            lcd.move_to(0,1)
            lcd.putstr("OrangeLed:Damaged")
            
            log_to_sheets(led1_status, led2_status, "LED 2 is damaged or not functioning.")
           
        else:
            print("LED 2 is functioning correctly.")
            buz.value(0)
    else:  # LEDs are supposed to be off
        if sensor2_value > threshold2_off:
            print("LED 2 is stuck on.")
            log_to_sheets(led1_status, led2_status, "LED 2 is stuck on.")
        else:
            print("LED 2 is off as expected.")


    sleep(0.5)  # Adjust delay if needed


