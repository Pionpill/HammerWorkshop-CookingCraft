'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-03 19:46:47
LastEditTime: 2022-08-03 19:51:29
'''
from hammerCookingScripts.client.ui.base import BaseCraftingScreen


class CookingTableScreen(BaseCraftingScreen):
    def __init__(self, namespace, name, param):
        BaseCraftingScreen.__init__(self, namespace, name, param)
