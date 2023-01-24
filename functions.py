import time
import struct
from threading import Thread, Event
import TemperaturaExterna as temp
import pid 
import log as loguinho
import uart  as uart
import gpio  as gpio

#Funções de controle

class Reflowforno:
    def __init__(self):
        self.on = False
        self.working = False
        self.temperature_curve_mode = False
        self.outside_temperature = 9999.0
        self.forno_temperature_target = 9999.0
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

def botoes(forno):

    request_botaos_code = b'\x01\x23\xc3'
    uart.send_message(request_botaos_code)
    data_received = uart.receive_message()

    if data_received is not None:

        botao = int.from_bytes(data_received, 'little')

        if botao == 161:
            print("<Iniciar>")
            forno.on = True
            ligar_forno()
        elif botao == 162:
            print("<Desligar>")
            forno.on = False
            desligar_forno()
            forno.working = False
            pausar()
        elif botao == 163:
            print("<Iniciar>")
            forno.working = True
            funcionar()
        elif botao == 164:
            print("<Parar>")
            forno.working = False
            pausar()

    time.sleep(0.5)

def temperatura_de_referencia(forno):
    request_temperature_target_code = b'\x01\x23\xc2'
    uart.send_message(request_temperature_target_code)
    data_received = uart.receive_message()
    temp = struct.unpack('f', data_received)[0]
    forno.forno_temperature_target = temp
    print("Temperatura de referência - " + str(temp))


def temperatura_interna(forno):
    request_forno_temperature_code = b'\x01\x23\xc1'
    uart.send_message(request_forno_temperature_code)
    data_received = uart.receive_message()
    temp = struct.unpack('f', data_received)[0]
    forno.internal_temperature = temp
    print("Temperatura Interna- " + str(temp))