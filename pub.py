# python3.7
# pip3 install paho.mqtt requests
import numpy as np
import random
import time
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import Client
import requests
from requests import get

class MQtt_client(Client):
    def __init__(self, broker, port, topic, client_id, username, password, msg):
        # ddeclare all private variables
        super().__init__()
        self._broker = broker
        self._port = port
        self._topic = topic 
        self._client_id = client_id
        self._username = username
        self._password = password
        self._msg = msg
    def say_hello(self):
        print("hello, i am connected")
    def please_say_something(self):
        print(f"ok, i am saying it {self._msg}")
    def ok_i_am_listening(self):
        print(f"i am listening to {self._topic}")
        print(f"you say it ! {self._msg}")
    def publish25Percent(self, data):
        self.publish(self._topic,data)
        self._on_publish=print(data)
    # Defining __call__ method: call instance as func
    def __call__(self):
        self.connect(self._broker, self._port)
        self.on_connect=self.say_hello()
        time.sleep(1)

        self.publish(self._topic, self._msg)
        self.on_publish=self.please_say_something()
        time.sleep(1)

        self.subscribe(self._topic)
        self.on_subscribe = self.ok_i_am_listening()
        time.sleep(1)


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'
msg = "hahaha"

def get_data(url):
    response = get(endpoint, timeout=10)
    
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()
    
endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=nation;areaName=england&'
        'structure={"date":"date","newCases":"newCasesByPublishDate"}'
    )

def sort_this_data(data):
    sorted_data = data["data"]
    cases = []
    for i,v in enumerate(sorted_data):
        cases.append(sorted_data[i]["newCases"])
    return cases
def sort_data_under_25(data):
    sorted_data= np.percentile(data, 25)
    return sorted_data
if __name__ == '__main__':
    publisher = MQtt_client(broker, port, topic, client_id, username, password, msg)
    data = sort_this_data(get_data(endpoint))
    publisher.publish25Percent(data=sort_data_under_25(data))
