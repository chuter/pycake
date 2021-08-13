#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
进行模型样本收集的中间件.
"""

import os
import time
import random

from aiologger.loggers.json import JsonLogger
from aiologger.handlers.files import AsyncTimedRotatingFileHandler
from aiologger.handlers.files import RolloverInterval

from aiohttp.web import middleware


__all__ = ['build_model_sample_middleware']


MODEL_NAME = os.environ.get('model_name', None)
MODEL_VERSION = os.environ.get('model_version', None)
SAMPLE_LOG_BACKUP_COUNT = os.environ.get('model_sample_log_backup_count', 7)


sample_logger = JsonLogger(name='jcake', flatten=True)
handler = AsyncTimedRotatingFileHandler(
    filename="sample/sample",
    backup_count=SAMPLE_LOG_BACKUP_COUNT,
    when=RolloverInterval.DAYS,
    encoding='utf-8'
)
sample_logger.add_handler(handler)


async def build_sample_info(request_ms, request, response, model_name, model_version):
    """
    构造采样的信息.
    该采样实现目前只支持POST类型的请求.

    Args:
     request_ms: 请求耗时(ms)
     request: 请求信息
     response: 响应结果
    """

    request_body = await request.text()
    response_text = response.text
    return {
        "ts": int(time.time() * 1000),
        "cost": "%.2f" % request_ms,
        "sample": request_body,
        "prediction": response_text,
        "__mn": model_name,
        "__mv": model_version
    }


def build_model_sample_middleware(collect_api, sample_ratio=50, **kwargs):
    global MODEL_NAME
    global MODEL_VERSION
    global sample_logger

    if collect_api is None:
        raise Exception("empty target api")

    if (
        kwargs.get('model_name', MODEL_NAME) is None or
        kwargs.get('model_version', MODEL_VERSION) is None
    ):
        raise Exception('PYCAKE_SAMPLE_MODEL_NAME and PYCAKE_SAMPLE_MODEL_VERSION not defined')

    random_ins = random.Random()
    sample_ratio = int(sample_ratio)

    def should_sample(request, sample_ratio):
        if request._method == 'GET':
            return False
        return random_ins.randint(1, 100) <= sample_ratio

    @middleware
    async def sample(request, handler):
        """对于目标api的请求和响应结果进行采样"""
        if request.path.find(collect_api) == -1 or not should_sample(request, sample_ratio):
            response = await handler(request)
            return response

        start_time_s = time.time()
        response = await handler(request)
        end_time_s = time.time()
        delta_s = end_time_s - start_time_s
        sample_info = await build_sample_info(delta_s * 100, request, response,
                                              kwargs.get('model_name', MODEL_NAME),
                                              kwargs.get('model_version', MODEL_VERSION))
        sample_logger.info(sample_info)
        return response

    return sample
