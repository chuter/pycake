#!/usr/bin/env python
# -*- encoding: utf-8 -*-


def info():
    return {
        "name": "Demo",
        "author": "chuter",
        "version": "0.0.1"
    }


def health():
    return {
        "cpu": 8,
        "mem": 6000,
        "net": 0.5
    }


def metrics():
    return "Metrics"
