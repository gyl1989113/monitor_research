import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
import requests
import socket

# 参考https://blog.csdn.net/weixin_43914798/article/details/121928587
def get_data(url='http://127.0.0.1:9888/hosts'):
    r = requests.get(url)
    return r.json()

def send_data():
    # ip=get_host_ip()  # 本机ip
    hostname = socket.gethostname()  # 主机名

    REGISTRY = CollectorRegistry(auto_describe=False)
    hardware = Gauge("hardware", hostname, ['ip', 'instance', 'type'], registry=REGISTRY)

    hardware.labels(ip=get_data()['data'][1]['ip'], instance=hostname, type='cpu').set(int(get_data()['data'][1]['cpu']))
    hardware.labels(ip=get_data()['data'][1]['ip'], instance=hostname, type='mem').set(int(get_data()['data'][1]['mem']))

    requests.post("http://localhost:9091/metrics/job/host_info", data=prometheus_client.generate_latest(REGISTRY))
    print("发送了一次数据")

if __name__ == '__main__':
    # data = get_data("http://127.0.0.1:9888/hosts")
    send_data()