import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import json
import board
import adafruit_bme680


temp_offset = -5

# URLs to fetch from
SOCKET_URL = "http://192.168.1.3:2345/weather"

mock_data = mock_data = {
    "temperature": 23,
    "Humidity": 39,
    "Altitude":2000
}

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

headers = {"Content-Type": "application/json"}

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


i2c = board.STEMMA_I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

def get_temperature_string():
    temp = bme680.temperature + temp_offset
    gas = bme680.gas
    hum = bme680.relative_humidity
    pressure = bme680.pressure
    alt = bme680.altitude
    weather = {"temperature": temp,"gas": gas,"humidity": hum,"pressure": pressure,"altitude": alt}
    full_json = {"weather":weather}
    return json.dumps(full_json)

while True:
    weather_data = get_temperature_string()
    response = requests.post(SOCKET_URL, data=weather_data, headers=headers)
    print("Sent data:", response.text)
    time.sleep(5)

