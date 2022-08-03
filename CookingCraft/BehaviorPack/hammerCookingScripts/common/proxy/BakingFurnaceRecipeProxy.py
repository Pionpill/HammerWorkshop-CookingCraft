'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 17:26:47
LastEditTime: 2022-07-31 17:48:26
'''
from hammerCookingScripts.common.data.recipe import bakingFuels, bakingRecipes
from hammerCookingScripts.common.proxy.base import BaseFurnaceRecipeProxy


class BakingFurnaceRecipeProxy(BaseFurnaceRecipeProxy):
    def __init__(self):
        BaseFurnaceRecipeProxy.__init__(self, bakingRecipes, bakingFuels)
