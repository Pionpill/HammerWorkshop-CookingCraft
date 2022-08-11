# sourcery skip: use-fstring-for-concatenation
'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 13:49:04
LastEditTime: 2022-08-11 15:03:11
'''
uiDirPath = "hammerCookingScripts.client.ui."

UI_DEFS = {
    "cookingcraft:cooking_table": {
        "name": "cooking_table_screen",
        "classPath": uiDirPath + "CookingTableScreen.CookingTableScreen",
        "screenDef": "cooking_table_screen.main"
    },
    "cookingcraft:baking_furnace": {
        "name": "baking_furnace_screen",
        "classPath": uiDirPath + "BakingFurnaceScreen.BakingFurnaceScreen",
        "screenDef": "baking_furnace_screen.main"
    },
    "cookingcraft:mill": {
        "name": "mill_screen",
        "classPath": uiDirPath + "MillScreen.MillScreen",
        "screenDef": "mill_screen.main"
    }
}
