'''
Description: 熔炉具有以下结构
|- main
    |- furnace_panel
        |- furnace_arrow_mask
        |- furnace_arrow_img
        |- flame_mask
        |- flame_img
        |- furnace_slot0
        |- furnace_slot1
        |- furnace_slot2
        
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-03 14:36:13
LastEditTime: 2022-08-03 19:48:50
'''
from hammerCookingScripts.client.ui.base.BaseInventoryScreen import BaseInventoryScreen
from hammerCookingScripts.client.controller import SystemController
from hammerCookingScripts.client.utils import pathUtils
from hammerCookingScripts.common import modConfig


class BaseFurnaceScreen(BaseInventoryScreen):
    def __init__(self, namespace, name, param):
        BaseInventoryScreen.__init__(self, namespace, name, param)
        self.furnacePanelPath = "/furnace_panel"
        self.flameMaskPath = pathUtils.JoinPath(self.furnacePanelPath,
                                                "flame_mask")
        self.arrowMaskPath = pathUtils.JoinPath(self.furnacePanelPath,
                                                "furnace_arrow_mask")
        self.isBurning = False
        self.isProducing = False
        self.burnProgress = 0
        self.burnDuration = 0
        self.produceProgress = 0

    def Create(self):
        BaseInventoryScreen.Create(self)
        self.flameMaskControl = self.GetBaseUIControl(
            self.flameMaskPath).asImage()
        self.arrowMaskControl = self.GetBaseUIControl(
            self.arrowMaskPath).asImage()
        self.flameMaskControl.SetClipDirection("fromTopToBottom")

    def Update(self):
        BaseInventoryScreen.Update(self)
        # 更新燃烧动画
        if not self.isBurning:
            self.burnProgress = 0
            self.flameMaskControl.SetSpriteClipRatio(1)
        else:
            # 更新火焰动画
            self.burnProgress += 1
            fireRatio = (self.burnProgress * 2.0) / (self.burnDuration * 3.0)
            self.flameMaskControl.SetSpriteClipRatio(fireRatio)
            if fireRatio == 1:
                self.burnProgress = 0
        if not self.isProducing:
            self.produceProgress = 0
            self.arrowMaskControl.SetSpriteClipRatio(1)
        else:
            # 更新箭头动画
            self.produceProgress += 1
            arrowRatio = self.produceProgress / (modConfig.BURN_INTERVAL * 30.0)
            self.arrowMaskControl.SetSpriteClipRatio(1.0 - arrowRatio)
            if arrowRatio == 1:
                self.produceProgress = 0

    def UpdateWorkbenchUI(self, workbenchData):
        slotItems = workbenchData["workbenchSlotData"]
        for slotName, itemDict in slotItems.items():
            slotPath = "{0}/{1}".format(self.craftingPanelPath, slotName)
            self.slotManager.SetSlotInfo(slotName,
                                         slotInfo=(slotPath, itemDict))
            self._SetSlotUI(slotPath, itemDict)

    def ShowUI(self, workbenchData):
        # type: (dict) -> None
        """显式 UI 并更新工作台数据"""
        BaseInventoryScreen.ShowInventoryUI(self, workbenchData)
        self.UpdateWorkbenchUI(workbenchData)

    def UpdateWorkbenchUI(self, workbenchData):
        # type: (dict) -> None
        """更新工作台数据"""
        for key, value in workbenchData.items():
            if key == "burnDuration":
                if value != self.burnDuration:
                    self.burnDuration = workbenchData["burnDuration"]
                    self.burnProgress = 0
            elif key == "burnProgress":
                self.burnProgress = value
            elif key == "isBurning":
                self.isBurning = value
            elif key == "isProducing":
                self.isProducing = value
            elif key == "produceProgress":
                self.produceProgress = value
            elif key == "workbenchSlotData":
                for slotName, itemDict in value.items():
                    slotPath = "{0}/{1}".format(self.furnacePanelPath, slotName)
                    self.slotManager.SetSlotInfo(slotName,
                                                 slotInfo=(slotPath, itemDict))
                    self._SetSlotUI(slotPath, itemDict)
