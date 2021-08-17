#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
进行模型样本收集的中间件.
"""

import os
import json
import time
import random
import logging

from aiologger.loggers.json import JsonLogger
from aiologger.handlers.files import AsyncTimedRotatingFileHandler
from aiologger.handlers.files import RolloverInterval


__all__ = ['build_sample_middleware']


MODEL_NAME = os.environ.get('model_name', None)
MODEL_VERSION = os.environ.get('model_version', None)
SAMPLE_LOG_BACKUP_COUNT = os.environ.get('model_sample_log_backup_count', 7)


sample_logger = JsonLogger(name='jcake', flatten=True)
api_logger = logging.getLogger("demo.predict")

handler = AsyncTimedRotatingFileHandler(
    filename="sample/sample",
    backup_count=SAMPLE_LOG_BACKUP_COUNT,
    when=RolloverInterval.DAYS,
    encoding='utf-8'
)
sample_logger.add_handler(handler)


def build_sample_info(request_ms, request, response, model_name, model_version):
    """
    构造采样的信息.
    该采样实现目前只支持POST类型的请求.

    Args:
     request_ms: 请求耗时(ms)
     request: 请求信息
     response: 响应结果
    """

    request_body = request.json
    predict_result = request.ctx.__predict_result

    if isinstance(predict_result, str):
        try:
            predict_result = json.loads(predict_result)
        except:
            pass

    return {
        "ts": int(request.ctx.__start_time_s * 1000),
        "cost": request_ms,
        "sample": request_body,
        "prediction": predict_result,
        "__mn": model_name,
        "__mv": model_version
    }


def build_sample_middleware(bp, sample_percent=50, **kwargs):
    global MODEL_NAME
    global MODEL_VERSION
    global sample_logger

    if (
        kwargs.get('model_name', MODEL_NAME) is None or
        kwargs.get('model_version', MODEL_VERSION) is None
    ):
        raise Exception('PYCAKE_SAMPLE_MODEL_NAME and PYCAKE_SAMPLE_MODEL_VERSION not defined')

    random_ins = random.Random()
    sample_percent = int(sample_percent)

    def should_sample(request, sample_percent):
        if request.method == 'GET':
            return False
        return random_ins.randint(1, 100) <= sample_percent

    @bp.middleware("request")
    async def on_request(request):
        request.ctx.__start_time_s = time.time()

    @bp.middleware("response")
    async def on_response(request, response):
        end_time_s = time.time()
        start_time_s = request.ctx.__start_time_s
        delta_ms = int((end_time_s - start_time_s) * 1000)
        api_logger.info("cost {}ms predict for {}".format(delta_ms, request.body))

        if response.status != 200 or not should_sample(request, sample_percent):
            return response

        sample_info = build_sample_info(delta_ms, request, response,
                                        kwargs.get('model_name', MODEL_NAME),
                                        kwargs.get('model_version', MODEL_VERSION))
        sample_logger.info(sample_info)

        return response
