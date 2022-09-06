# coding=utf-8

from __future__ import print_function
from __future__ import absolute_import
import os
import logging
import datetime
import traceback
import subprocess
import requests

from bworker_app import app


base_url = 'http://39.104.228.249:8866/'
headers = {'content-type': 'application/json'}


def run_bash_cmd(cmd):
    ret_code, stdout, stderr = -1, "", ""
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = p.communicate()
        ret_code = p.returncode
    except:
        app.logger.exception(traceback.format_exc())
    return ret_code, stdout, stderr


def send_alarm_message(payload):
    url = base_url + "special_alarm"
    response = requests.post(url=url, headers=headers, json=payload, timeout=10)
    try:
        response = response.json()
    except:
        response = None

    return response



