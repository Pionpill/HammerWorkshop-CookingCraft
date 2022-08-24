'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-24 15:33:07
LastEditTime: 2022-08-24 15:34:10
'''
from hammerCookingScripts.client.ui.base import BaseFurnaceScreen


class StewPotScreen(BaseFurnaceScreen):

    def __init__(self, namespace, name, param):
        BaseFurnaceScreen.__init__(self, namespace, name, param)
