import time
import struct
from threading import Thread, Event
import TemperaturaExterna as temp
import pid 
import log as log
import uart  as uart
import gpio  as gpio

# init gpio
gpio.init_gpio()

#init uart
uart.init_uart()

# sensor bme280
temperatura = temp.TemperaturaExterna()

# PID
pid_control = pid.PID()

#Funções de controle

class ReflowOven:
    def __init__(self):
        self.on = False
        self.working = False
        self.temperature_curve_mode = False
        self.outside_temperature = 9999.0
        self.oven_temperature_target = 9999.0
        self.internal_temperature = 9999.0

def ligar_forno():
    print('Forno ligado\n')
    comando_ligar =  b'\x01\x23\xd3'
    uart.send_message(comando_ligar, b'\x01', 8)
    resposta = uart.receive_message()
    resposta_int = int.from_bytes(resposta,'little')
    print(resposta_int)

def desligar_forno():
    print('Forno desligado\n')
    comando_ligar =  b'\x01\x23\xd3'
    uart.send_message(comando_ligar, b'\x00', 8)
    resposta = uart.receive_message()
    resposta_int = int.from_bytes(resposta,'little')
    print(resposta_int)

def funcionar():
    print('Forno funcionando\n')
    comando_ligar =  b'\x01\x23\xd5'
    uart.send_message(comando_ligar, b'\x01', 8)
    resposta = uart.receive_message()
    resposta_int = int.from_bytes(resposta,'little')
    print(resposta_int)

def pausar():
    print('Forno pausado\n')
    comando_ligar =  b'\x01\x23\xd5'
    uart.send_message(comando_ligar, b'\x00', 8)
    resposta = uart.receive_message()
    resposta_int = int.from_bytes(resposta,'little')
    print(resposta_int)

def controle_de_temperatura(intensidade):

    sinal_de_controle= b'\x01\x23\xd1'
    valor = (round(intensidade)).to_bytes(4, 'little', signed=True)
    uart.send_message(sinal_de_controle, valor, 11)
    resposta = uart.receive_message()

def watch_for_buttons(oven):

    request_buttons_code = b'\x01\x23\xc3'
    uart.send_code(request_buttons_code)
    data_received = uart.message_receiver()

    if data_received is not None:

        button = int.from_bytes(data_received, 'little')

        if button == 161:
            print("[1] pressed")
            oven.on = True
            ligar_forno()
        elif button == 162:
            print("[2] pressed")
            oven.on = False
            desligar_forno()
            oven.working = False
            stop_work()
        elif button == 163:
            print("[3] pressed")
            oven.working = True
            funcionar()
        elif button == 164:
            print("[4] pressed")
            oven.working = False
            pausar()

    time.sleep(0.5)

def read_and_update_temperature_target(oven):
    request_temperature_target_code = b'\x01\x23\xc2'
    uart.send_message(request_temperature_target_code)
    data_received = uart.receive_message()
    temp = struct.unpack('f', data_received)[0]
    oven.oven_temperature_target = temp
    print("Target Temperature - " + str(temp))


def read_and_update_oven_temperature(oven):
    request_oven_temperature_code = b'\x01\x23\xc1'
    uart.send_message(request_oven_temperature_code)
    data_received = uart.receive_message()
    temp = struct.unpack('f', data_received)[0]
    oven.internal_temperature = temp
    print("Oven temperature - " + str(temp))


def system_update_routine():

    oven = ReflowOven()

    while True:

        read_and_update_temperature_target(oven)
        watch_for_buttons(oven)
        read_and_update_oven_temperature(oven)
        watch_for_buttons(oven)
        pid_result = pid.output(oven.oven_temperature_target, oven.internal_temperature)

        if oven.on and oven.working:


            print(pid_result)

            controle_de_temperatura(pid_result)

            if pid_result > 0:
                gpio.aquecer(pid_result)
                gpio.esfriar(0)
            else:
                pid_result = pid_result * -1
                if pid_result < 40:
                    pid_result = 40
                gpio.esfriar(pid_result)
                gpio.aquecer(0)

        log.create_log_entry(temperatura.atualizar_temperatura(), oven.internal_temperature, oven.oven_temperature_target, pid_result)


system_routine_thread = Thread(target=system_update_routine, args=())
system_routine_thread.start()