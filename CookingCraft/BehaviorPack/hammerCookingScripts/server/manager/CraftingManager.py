'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-05 15:28:10
'''
from copy import deepcopy

from hammerCookingScripts import logger
from hammerCookingScripts.server.manager.base import BaseCraftingManager


class CraftingManager(BaseCraftingManager):
    def __init__(self, blockName):
        BaseCraftingManager.__init__(self, blockName)
