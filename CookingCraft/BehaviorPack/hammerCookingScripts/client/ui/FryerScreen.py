'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-24 15:32:24
LastEditTime: 2022-08-24 15:32:40
'''
from hammerCookingScripts.client.ui.base import BaseFurnaceScreen


class FryerScreen(BaseFurnaceScreen):

    def __init__(self, namespace, name, param):
        BaseFurnaceScreen.__init__(self, namespace, name, param)
