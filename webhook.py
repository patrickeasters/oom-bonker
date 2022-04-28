from flask import Flask, request
from gpiozero import Servo
from time import sleep
from pprint import pprint

SERVO_ACTIVE_DURATION = 0.5
SERVO_PIN = 18

# initial setup for GPIO/servo
servo = Servo(SERVO_PIN)
pos = True
servo.min()
# due to instability from PWM output, we wait enough for the servo to move
# and then detach from the pin
sleep(SERVO_ACTIVE_DURATION)
servo.detach()

# initialize Flask app for webhook receiver
app = Flask(__name__)

@app.route('/')
def root():
    return '¯\_(ツ)_/¯'

@app.route('/hook', methods=['POST'])
def webhook():
    payload = request.get_json()
    if 'status' in payload and payload['status'] == 'firing':
        bonk()
        return 'OK'
    else:
        return 'Bad Request', 400

def bonk():
    global pos
    if pos:
        servo.max()
    else:
        servo.min()
    sleep(SERVO_ACTIVE_DURATION)
    servo.detach()
    pos = not pos

if __name__ == '__main__':
    app.run()
