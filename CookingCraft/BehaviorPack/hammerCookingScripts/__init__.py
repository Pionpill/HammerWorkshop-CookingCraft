# -*- coding:utf-8 -*-
'''
Description: HammerWorkshop's CookingCraft Scripts
version: 0.1
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 12:48:07
LastEditTime: 2022-08-01 00:41:47
'''

# -*- coding: utf-8 -*-
# 该模块仅起全局监听作用，详细功能请在其它模块中实现
import logging
import sys
import os


def makeLogger():
    """日志生成器，格式:|CookingCraft| [log等级 - 时间]:消息"""
    logging.basicConfig(
        level=0,
        format='|CookingCraft| [%(levelname)s-%(asctime)s]:%(message)s')
    return logging.getLogger(__name__)


logger = makeLogger()
