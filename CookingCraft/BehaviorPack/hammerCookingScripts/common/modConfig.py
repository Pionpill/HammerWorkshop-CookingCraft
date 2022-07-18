'''
Description: 常量保存文件,只读
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 15:12:41
LastEditTime: 2022-07-17 15:38:46
'''

# -*- coding: utf-8 -*-
# ————————————————————————————————————————————————————————————————————————————————————————————————————
### Mod 名称与基础信息
ModName_en = "HammerCookingCraft"
ModName_zh = "锤子工坊烹饪工艺"
ModName = ModName_en
ModVersion = "0.0.1"

# Engine
Minecraft = "Minecraft"

# ————————————————————————————————————————————————————————————————————————————————————————————————————
# Server System
# 工作台
ServerSystemName_Workbench = "WorkbenchServerSystem"
ServerSystemClsPath_Workbench = "hammerCookingScripts.server.serverSystem.WorkbenchServerSystem.WorkbenchServerSystem"
# 植物
ServerSystemName_Plants = "PlantsServerSystem"
ServerSystemClsPath_Plants = "hammerCookingScripts.server.system.PlantsSystem.PlantsSystem"

# Client System
# 工作台
ClientSystemName_Workbench = "WorkbenchClientSystem"
ClientSystemClsPath_Workbench = "hammerCookingScripts.client.clientSystem.WorkbenchClientSystem.WorkbenchClientSystem"
# 植物
ClientSystemName_Plants = "PlantsClientSystem"
ClientSystemClsPath_Plants = "hammerCookingScripts.client.clientSystem.PlantsClientSystem.PlantsClientSystem"

# ————————————————————————————————————————————————————————————————————————————————————————————————————
# Block
CookingTable_Block_Name = "cookingcraft:cooking_table"
CookingTable_UI_Name = "cooking_table_screen"  # Name 名必须和类名相同，但写法不同
CookingTable_UI_ScreenDef = "cooking_table_screen.main"
CookingTable_UI_ClsPath = "hammerCookingScripts.client.ui.CookingTableScreen.CookingTableScreen"
BakingFurnace_Block_Name = "cookingcraft:baking_furnace"
BakingFurnace_UI_Name = "baking_furnace_screen"  # Name 名必须和类名相同，但写法不同
BakingFurnace_UI_ScreenDef = "baking_furnace_screen.main"
BakingFurnace_UI_ClsPath = "hammerCookingScripts.client.ui.BakingFurnaceScreen.BakingFurnaceScreen"
# Inventory UI
InventoryContainerBlocks = [CookingTable_Block_Name, BakingFurnace_Block_Name]
WorkbenchBlocks = [CookingTable_Block_Name, BakingFurnace_Block_Name]
CraftingBlock = [CookingTable_Block_Name]  # 合成台，block 内不包含数据
FurnaceBlockList = [BakingFurnace_Block_Name]

# ————————————————————————————————————————————————————————————————————————————————————————————————————
# UI
UI_DEFS = {
    "cookingcraft:cooking_table": {
        "uiName": "cooking_table_screen",
        "uiClassPath":
        "hammerCookingScripts.client.ui.CookingTableScreen.CookingTableScreen",
        "uiScreenDef": "cooking_table_screen.main"
    },
    "cookingcraft:baking_furnace": {
        "uiName": "baking_furnace_screen",
        "uiClassPath":
        "hammerCookingScripts.client.ui.BakingFurnaceScreen.BakingFurnaceScreen",
        "uiScreenDef": "baking_furnace_screen.main"
    }
}

# ————————————————————————————————————————————————————————————————————————————————————————————————————
# Event
BagChangedEvent = "BagChangedEvent"  # 玩家获取新的物品事件
ItemSwapClientEvent = "ItemSwapClientEvent"
ItemDropClientEvent = "ItemDropClientEvent"  # 物品交换事件
CloseInventoryEvent = "CloseInventoryEvent"
CloseCraftingTableEvent = "CloseCraftingTableEvent"  # 关闭工作台，应该返回物品

UIShouldCloseEvent = "UIShouldCloseEvent"  # 玩家死亡等情况下，UI强制关闭事件
WorkbenchChangedEvent = "WorkbenchChangedEvent"  # 工作台改变事件
InventoryOpenEvent = "InventoryOpenEvent"
ItemSwapServerEvent = "ItemSwapServerEvent"
ItemDropServerEvent = "ItemDropServerEvent"
WorkBenchOpenEvent = "WorkBenchOpenEvent"
OutSlotClickEvent = "OutSlotClickEvent"
# ————————————————————————————————————————————————————————————————————————————————————————————————————
# data
Inventory_Slot_NUM = 36
InventoryData = "inventoryData"
WorkbenchData = "workbenchData"

# 双击间隔
DOUBLE_CLICK_INTERVAL = 4
# 工作台槽位数量
WORKBENCH_SLOT_NUM_DICT = {
    CookingTable_Block_Name: 10,
    BakingFurnace_Block_Name: 3
}
# 工作台槽前缀名
WORKBENCH_SLOT_PREFIX = {
    CookingTable_Block_Name: "crafting_slot",
    BakingFurnace_Block_Name: "furnace_slot"
}
# 燃烧时间间隔
BURN_INTERVAL = 5
MAX_STACK_SIZE = 64

# Plants
SeedsList = ["cookingcraft:herb_seeds"]
