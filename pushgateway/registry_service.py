import requests
# import json
import sys


def send_data_to_pro(monitor_ip, item_name, item_addr, item_port, isremove=False):

    url = "http://" + monitor_ip + ":8500/v1/agent/service/register"
    monitor_data = {
    "id":item_addr+"-" + item_name,
    "name":item_name,
    "address":item_addr,
    "port": int(item_port),
    "meta": {
            "location": "us",
        },
    "tags":[
        "us"
    ],
    "checks":[
        {
            "http":"http://" + item_addr + ":" + item_port + "/metrics",
            "interval":"5s"
        }
    ]
    }
    if isremove=="false":
        # sendData = json.dumps(monitor_data).encode('utf-8')
        r = requests.put(url, json=monitor_data)
        return r
    elif isremove=="true":
        url = "http://" + monitor_ip + ":8500/v1/agent/service/deregister/" + item_addr + "-" + item_name
        r = requests.put(url)


if __name__ == '__main__':
    monitor_ip = "localhost"
    item_name = "node-exporter"
    item_addr = "192.168.50.224"
    item_port = "9100"
    isremove = "false"
    if "," in item_addr:
        for item_ip in item_addr.split(","):
            r = send_data_to_pro(monitor_ip, item_name, item_ip, item_port, isremove)
            print(r)
    else:
        r = send_data_to_pro(monitor_ip, item_name, item_addr, item_port, isremove)
        print(r)