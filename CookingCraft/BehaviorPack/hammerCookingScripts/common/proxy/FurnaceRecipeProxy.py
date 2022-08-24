'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 17:26:47
LastEditTime: 2022-08-24 22:24:17
'''
from hammerCookingScripts.common.proxy.base import BaseFurnaceRecipeProxy


class FurnaceRecipeProxy(BaseFurnaceRecipeProxy):

    def __init__(self, blockName):
        BaseFurnaceRecipeProxy.__init__(self, blockName)
