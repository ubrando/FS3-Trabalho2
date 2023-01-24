from csv import writer
from os.path import exists
from datetime import datetime

logFile = 'log.csv'

def create_log_file():
    with open(logFile, 'w', encoding='UTF8') as log_file:
        file_writer = writer(log_file)
        data = ["Data", "Hora", "Temperatura Ambiente", "Temperatura Interna", "temperatura alvo", "Sinal PID"]
        file_writer.writerow(data)


class LogManager:
    def __init__(self):
        if not exists(logFile):
            create_log_file()

    def create_log_entry(self, ambient_temperature, oven_temperature, target_temperature, pid_signal):

        now = datetime.now()
        log_date = now.strftime("%d/%m/%Y")
        log_time = now.strftime("%H:%M:%S")

        values_list = [log_date, log_time, ambient_temperature, oven_temperature, target_temperature, pid_signal]

        with open(logFile, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(values_list)
            f_object.close()