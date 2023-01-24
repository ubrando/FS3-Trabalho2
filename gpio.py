import RPI.GPiO as GPIO

global resistor
global ventoinha

def init_gpio():
    global resistor
    global ventoinha
    resistor = 23
    ventoinha = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(resistor, GPIO.OUT)
    GPIO.setup(ventoinha, GPIO.OUT)
    pwm_resistor = GPIO.PWM(resistor, 1000)
    pwm_resistor.start(0)
    pwm_ventoinha = GPIO.PWM(resistor, 1000)
    pwm_ventoinha.start(0)

def aquecer(pid):
    global resistor
    resistor.ChangeDutyCycle(pid)

def esfriar(pid)
    global ventoinha
    ventoinha.ChangeDutyCycle(pid)