'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-24 15:30:04
LastEditTime: 2022-08-25 13:56:07
'''
from hammerCookingScripts.client.ui.base import BaseCraftingScreen


class CraftingScreen(BaseCraftingScreen):

    def __init__(self, namespace, name, param):
        BaseCraftingScreen.__init__(self, namespace, name, param)
