import time
import serial
from CRC16 import calc_CRC

global porta
global matricula

def init_uart():
    global porta
    global matricula
    porta = serial.Serial(port='/dev/serial0', baudrate=9600, timeout=1)
    matricula = [4, 3, 5, 7]

def close():
    global porta
    porta.close()

def send_message(command, valor=b'', tamanho = 7):
    global porta
    global matricula
    if porta.is_open():
        m1 = command+ bytes(matricula) + valor
        m2 = calc_CRC(m1, tamanho).to_bytes(2, 'little')
        msg = m1 + m2
        porta.write(msg)
    else:
        print("Failed to send message")

def receive_message():
    global porta
    global matricula
    time.sleep(0.2)
    buffer = porta.read(9)
    tamanho = len(buffer)
    if  tamanho == 9:
        data = buffer[3:7]
        crc16_recebido = buffer[7:9]
        crc16_calculado = calc_CRC(buffer[0:7], 7).to_bytes(2, 'little')

        if crc16_recebido == crc16_calculado:
            return data
        else:
            print('Mensagem recebida: {}'.format(buffer))
            print('CRC16 invalido')
            return None
    else:
        return None


