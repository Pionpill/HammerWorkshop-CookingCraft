'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-21 23:40:29
LastEditTime: 2022-08-24 22:07:33
'''
from hammerCookingScripts.common.proxy.base.BaseRecipeProxy import \
    BaseRecipeProxy
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils


class BaseCraftingRecipeProxy(BaseRecipeProxy):

    def __init__(self, blockName):
        BaseRecipeProxy.__init__(self, blockName)

    def GetLastUsedRecipeMaterials(self):
        if self._lastUsedRecipeName:
            return self._GetRecipeMaterials(self._lastUsedRecipeName)
        return None
