import RPi.GPIO as GPIO

global resistor
global ventoinha
global pwm_resistor
global pwm_ventoinha

def init_gpio():
    GPIO.setwarnings(False)
    global resistor
    global ventoinha
    global pwm_resistor
    global pwm_ventoinha
    resistor = 23
    ventoinha = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(resistor, GPIO.OUT)
    GPIO.setup(ventoinha, GPIO.OUT)
    pwm_resistor = GPIO.PWM(resistor, 1000)
    pwm_resistor.start(0)
    pwm_ventoinha = GPIO.PWM(ventoinha, 1000)
    pwm_ventoinha.start(0)

def aquecer(pid):
    global pwm_resistor
    pwm_resistor.ChangeDutyCycle(pid)

def esfriar(pid):
    global pwm_ventoinha
    pwm_ventoinha.ChangeDutyCycle(pid)