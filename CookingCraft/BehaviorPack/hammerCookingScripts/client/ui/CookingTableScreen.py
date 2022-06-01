'''
Description: 厨务台界面的 UI，新增以下 UI 控件:
|- main
    |- crafting_panel
        |- crafting_slot0
        |- crafting_slot1
        |- ......
        |- crafting_slot9
        |- arrow_image

version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 20:46:04
LastEditTime: 2022-05-25 22:55:13
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.client.ui.CraftingUI import CraftingUI
from hammerCookingScripts.common import modConfig

compFactory = clientApi.GetEngineCompFactory()


class CookingTableScreen(CraftingUI):
    def __init__(self, namespace, name, param):
        CraftingUI.__init__(self, namespace, name, param)
        self.materialSlotNames = [
            "crafting_slot0", "crafting_slot1", "crafting_slot2",
            "crafting_slot3", "crafting_slot4", "crafting_slot5",
            "crafting_slot6", "crafting_slot7", "crafting_slot8"
        ]
        self.outSlotNames = ["crafting_slot9"]

    def Create(self):
        CraftingUI.Create(self)

    def Destroy(self):
        CraftingUI.Destroy(self)

    def Update(self):
        CraftingUI.Update(self)

    def ShowUI(self, args):
        CraftingUI.ShowCraftingUI(self, args)
        self.InitWorkbenchUI(args)

    def InitWorkbenchUI(self, args):
        """初始化厨务台界面，无需服务端数据，界面应为空

        Args:
            args (dict): 包含 "workbenchData" 键，用于获取工作台数据
        """
        items = args[modConfig.WorkbenchData]
        for slotName, itemDict in items.items():
            slotPath = "{0}/{1}".format(self.craftingPanelPath, slotName)
            self.slotData[slotPath] = {"slot": slotName, "item": itemDict}
            self.slotPath[slotName] = slotPath
            self.SetSlotUI(slotPath, itemDict)

    def UpdateWorkbenchUI(self, event):
        workbenchItems = event[modConfig.WorkbenchData]
        for slotName, itemDict in workbenchItems.items():
            workbenchSlotPath = self.craftingPanelPath + "/" + slotName
            self.slotData[workbenchSlotPath] = {
                "slot": slotName,
                "item": itemDict
            }
            self.SetSlotUI(self.slotPath[slotName], itemDict)
