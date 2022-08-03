'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-03 20:06:21
'''
from hammerCookingScripts.server.manager.base import BaseFurnaceManager


class FurnaceManager(BaseFurnaceManager):
    def __init__(self, blockName):
        BaseFurnaceManager.__init__(self, blockName)
