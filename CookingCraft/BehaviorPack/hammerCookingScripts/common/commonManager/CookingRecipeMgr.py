'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-27 17:29:17
LastEditTime: 2022-05-25 21:57:49
'''
from hammerCookingScripts.common.commonManager.RecipeMgrBase import RecipeManagerBase
from hammerCookingScripts.common.commonRecipe.cookingRecipes import cookingRecipes
from hammerCookingScripts import logger


class CookingRecipeManager(RecipeManagerBase):
    def __init__(self):
        RecipeManagerBase.__init__(self)
        self.__recipes = cookingRecipes
        # 存储上一次匹配到的材料
        self.lastUsedRecipe = None

    def GetResult(self, blockItems):
        """根据原材料匹配配方获取输出结果

        Args:
            blockItems (dict): key:slotName value:itemDict

        Returns:
            dict: itmDict
        """
        for _, recipe in self.__recipes.items():
            materials = recipe.get("material")
            result = recipe.get("result")
            index = 0
            for slotName, recipeItem in materials.items():
                index += 1
                blockItem = blockItems.get(slotName)
                if not self.IsSameRecipeItem(blockItem, recipeItem):
                    break
                if index == 9:
                    self.lastUsedRecipe = materials
                    return result
        self.lastUsedRecipe = None
        return

    def IsSameRecipeItem(self, materialItem, recipeItem):
        """判断是否匹配配方材料: itemName, auxValue, count, userDataS 都相同

        Args:
            materialItem (dict): 原材料信息字典
            recipeItem (dict): 配方信息字典

        Returns:
            bool: 匹配则返回 True
        """
        if not materialItem and not recipeItem:
            return True
        if not materialItem or not recipeItem:
            return False
        if materialItem.get("itemName") != recipeItem.get("itemName"):
            return False
        if materialItem.get("auxValue") != recipeItem.get("auxValue"):
            return False
        if materialItem.get("count") < recipeItem.get("count"):
            return False
        return True

    def GetLastUsedRecipe(self):
        return self.lastUsedRecipe


# {'count': 64, 'newItemName': 'minecraft:apple', 'isDiggerItem': False, 'enchantData': [], 'durability': 0, 'itemId': 260, 'customTips': '', 'extraId': '', 'newAuxValue': 0, 'modEnchantData': [], 'modId': '', 'userData': None, 'modItemId': '', 'itemName': 'minecraft:apple', 'auxValue': 0, 'showInHand': True}
