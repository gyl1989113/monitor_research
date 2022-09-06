# coding=utf-8

from __future__ import print_function
from __future__ import absolute_import
import os
import re
import logging
import traceback
from flask import request, abort, jsonify
from flask_api import status

from bworker_app import app
import bworker_utils


@app.route('/logpath')
@app.route('/logpath/')
def get_log_path():
    try:
        for h in app.logger.handlers:
            if isinstance(h, logging.handlers.RotatingFileHandler):
                log_path = os.path.dirname(h.baseFilename)
                return log_path
    except:
        pass
    return ''


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    #return 'You want path: %s' % path
    return '', status.HTTP_404_NOT_FOUND


@app.route('/version/')
@app.route('/version')
def version():
    return '1.0.0', status.HTTP_200_OK


@app.route('/diskinfo/<string:disk_path>')
def get_diskinfo(disk_path):
    """
    获取指定容器名对应的镜像信息
    容器名包含查询字符串即可查询成功, 非精确匹配
    1) 若有多个容器, 返回错误码400, 并返回所有镜像名称
    2) 若查询结果为0, 返回码200, 和空{}
    3) 若查询到单个镜像, 返回码200, 和具体镜像信息
    """

    # 本语法查询所有包含{0}的镜像, 不是精确匹配
    # 例如查询: "bsi", 可能会有多条记录返回
    cmd = "df -h|grep {0}|grep -v 'grep'".format(disk_path)
    ret_code, stdout, stderr = bworker_utils.run_bash_cmd(cmd)
    if ret_code != 0:
        return '"{0}" failed, return code {1}\n{2}\n{3}'.format(cmd, ret_code, stdout, stderr),\
               status.HTTP_500_INTERNAL_SERVER_ERROR
    disk_info = stdout.splitlines()
    if len(disk_info) == 0:
        return "", status.HTTP_200_OK
    elif len(disk_info) == 1:
        return disk_info[0], status.HTTP_200_OK
    elif len(disk_info) > 1:
        return "多个查询结果", status.HTTP_400_BAD_REQUEST


@app.route('/gpu_status/')
@app.route('/gpu_status')
def check_gpu_status():

    master_name = os.popen("hostname -I").read().strip()
    alarm_dict = {"name": "COMPUTING_GPU_DISABLE_ERROR",
                  "code": 30001,
                  "message": "GPU消失",
                  'host_id': master_name,
                  "location": {
                      "level_1": [],
                      "level_2": "gpu",
                  }}
    cmd = "nvidia-smi -L"
    ret_code, stdout, stderr = bworker_utils.run_bash_cmd(cmd)
    if ret_code != 0:
        return '"{0}" failed, return code {1}\n{2}\n{3}'.format(cmd, ret_code, stdout, stderr), \
               status.HTTP_500_INTERNAL_SERVER_ERROR
    gpu_info = stdout.splitlines()
    for info in gpu_info:
        if not info.startwith('gpu'):
            bworker_utils.send_alarm_message(alarm_dict)
            return gpu_info[0], status.HTTP_200_OK
    return gpu_info[0], status.HTTP_200_OK



