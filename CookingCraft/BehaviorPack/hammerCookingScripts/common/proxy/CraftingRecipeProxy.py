'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 16:14:17
LastEditTime: 2022-08-24 22:24:12
'''
from hammerCookingScripts.common.proxy.base import BaseCraftingRecipeProxy


class CraftingRecipeProxy(BaseCraftingRecipeProxy):

    def __init__(self, blockName):
        BaseCraftingRecipeProxy.__init__(self, blockName)
