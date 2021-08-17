#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sanic.response import text, json
from sanic import Blueprint
from sanic_openapi import doc
from {{cookiecutter.app.app_name}}.apis import predict as model_predict


__all__ = ['bp']


bp = Blueprint("model", url_prefix="/api")


class ModelInput:
    features = dict


@doc.tag("model api")
@doc.consumes(ModelInput, location="body")
@doc.description('模型预测')
@bp.post("/predict")
async def predict(request):
    result = model_predict(request.json)
    request.ctx.__predict_result = result
    if isinstance(result, dict):
        return json(result)
    else:
        return text(str(result))


{% if cookiecutter.app.model_sample == 'True' %}
import os
from .middleware import build_sample_middleware # noqa
{% if 'model_name' in cookiecutter.app %}
build_sample_middleware(
    bp,
    sample_percent=os.environ.get('model_sample_percent', None) or {{cookiecutter.app.model_sample_percent|int}},
    model_name='{{cookiecutter.app.model_name}}',
    model_version='{{cookiecutter.app.model_version|replace('_', '.')}}'
)
{% else %}
build_sample_middleware(
    bp,
    sample_percent=os.environ.get('model_sample_percent', None) or {{cookiecutter.app.model_sample_percent|int}}
)
{%- endif -%}
{% endif %}

# TODO(chuter): 自动load，切换模型的支持
