from threading import Thread
import TemperaturaExterna as temp
import pid 
import log as loguinho
import uart  as uart
import gpio  as gpio
import functions
import os

# init gpio
gpio.init_gpio()

#init uart
uart.init_uart()

# sensor bme280
temperatura = temp.TemperaturaExterna()

# PID
pid_control = pid.PID()

# Log
log = loguinho.LogManager()

#Loop Principal

def loop_de_funcionamento():

    forno = functions.Reflowforno()

    while True:
        print('-------------------------------')
        functions.temperatura_de_referencia(forno)
        functions.botoes(forno)
        functions.temperatura_interna(forno)
        functions.botoes(forno)
        print(f"Temperatura externa = {temperatura.atualizar_temperatura()}\n")
        print('-------------------------------')

        pid_result = pid_control.output(forno.forno_temperature_target, forno.internal_temperature)

        if forno.on and forno.working:


            print(pid_result)

            functions.controle_de_temperatura(pid_result)

            if pid_result > 0:
                gpio.aquecer(pid_result)
                gpio.esfriar(0)
            else:
                pid_result = pid_result * -1
                if pid_result < 40:
                    pid_result = 40
                gpio.esfriar(pid_result)
                gpio.aquecer(0)

        log.create_log_entry(temperatura.atualizar_temperatura(), forno.internal_temperature, forno.forno_temperature_target, pid_result)


system_routine_thread = Thread(target=loop_de_funcionamento, args=())
system_routine_thread.start()