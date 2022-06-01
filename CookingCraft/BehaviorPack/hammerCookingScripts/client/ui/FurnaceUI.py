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
Date: 2022-05-15 13:00:48
LastEditTime: 2022-05-17 21:09:37
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.client.ui.InventoryUI import InventoryUI
from hammerCookingScripts.common import modConfig

compFactory = clientApi.GetEngineCompFactory()


class FurnaceUI(InventoryUI):
    def __init__(self, namespace, name, param):
        InventoryUI.__init__(self, namespace, name, param)
        self.furnacePanelPath = "/furnace_panel"
        self.flameMaskPath = self.furnacePanelPath + "/flame_mask"
        self.arrowMaskPath = self.furnacePanelPath + "/furnace_arrow_mask"
        self.isLit = False
        self.isCooking = False
        self.litProgress = 0
        self.litDuration = 0
        self.burnProgress = 0

    def Create(self):
        InventoryUI.Create(self)
        self.flameMaskControl = self.GetBaseUIControl(
            self.flameMaskPath).asImage()
        self.arrowMaskControl = self.GetBaseUIControl(
            self.arrowMaskPath).asImage()
        self.flameMaskControl.SetClipDirection("fromTopToBottom")

    def Destroy(self):
        InventoryUI.Destroy(self)

    def ShowFurnaceUI(self, args):
        InventoryUI.ShowInventoryUI(self, args)

    def Update(self):
        InventoryUI.Update(self)
        # 更新燃烧动画
        if not self.isLit:
            self.litProgress = 0
            self.flameMaskControl.SetSpriteClipRatio(1)
        else:
            # 更新火焰动画
            self.litProgress += 1
            fireRatio = (self.litProgress * 2.0) / (self.litDuration * 3.0)
            self.flameMaskControl.SetSpriteClipRatio(fireRatio)
            if fireRatio == 1:
                self.litProgress = 0
        if not self.isCooking:
            self.burnProgress = 0
            self.arrowMaskControl.SetSpriteClipRatio(1)
        else:
            # 更新箭头动画
            self.burnProgress += 1
            arrowRatio = self.burnProgress / (modConfig.BURN_INTERVAL * 30.0)
            self.arrowMaskControl.SetSpriteClipRatio(1.0 - arrowRatio)
            if arrowRatio == 1:
                self.burnProgress = 0
