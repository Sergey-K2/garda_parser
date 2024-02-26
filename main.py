"""Основной модуль парсера."""
import json
import socket

SERVER_ADDRESS = "194.87.46.252"
SERVER_PORT = 8000
USERNAME = "Sergey Kozlov"
SUCCESS_PHRASE = "Nice, you're smart boy!"


def parse():
    """Функция для парсинга данных, полученных от сервера."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    s.recv(1024)
    s.send(USERNAME.encode())
    s.recv(1024)
    response = ""
    while SUCCESS_PHRASE not in str(response):
        string = s.recv(1024)
        print(string)
        structured_data = {
            string[0:5].decode("utf-8").lstrip("0"): {
                string[28:44].strip().decode("utf-8"): {
                    "date": (string[129:131].decode("utf-8") + "." +
                             string[126:128].decode("utf-8") + "." +
                             string[121:125].decode("utf-8")),
                    "duration":
                        string[142:151].decode("utf-8").lstrip("0") + " sec",
                    "name_from": string[45:64].strip().decode("utf-8"),
                    "name_to": string[95:114].strip().decode("utf-8"),
                    "numb_from": string[5:16].strip().decode("utf-8"),
                    "numb_to": string[84:94].strip().decode("utf-8"),
                    "time":
                    string[132:140].strip().decode("utf-8").replace(':', '-')
                }
                }
        }
        if structured_data[string[0:5].decode("utf-8").lstrip("0")][string[28:44].strip().decode("utf-8")]["duration"] == " sec":
            structured_data[string[0:5].decode("utf-8").lstrip("0")][string[28:44].strip().decode("utf-8")]["duration"] = "0 sec"

        print(json.dumps(structured_data, indent=4).encode())
        s.send(json.dumps(structured_data, indent=4).encode())
        response = s.recv(1028)
        print(response)
    s.close()


if __name__ == "__main__":
    parse()
