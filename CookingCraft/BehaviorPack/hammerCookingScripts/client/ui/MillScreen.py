'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-11 15:03:36
LastEditTime: 2022-08-24 15:31:46
'''
from hammerCookingScripts.client.ui.base import BaseFurnaceScreen


class MillScreen(BaseFurnaceScreen):

    def __init__(self, namespace, name, param):
        BaseFurnaceScreen.__init__(self, namespace, name, param)
