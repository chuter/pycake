#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sanic.response import text
from sanic import Blueprint

__all__ = ['bp']

bp = Blueprint("monitor", url_prefix="/monitor")


@bp.route("/ping")
async def bp_root(request):
    return text('pong')
