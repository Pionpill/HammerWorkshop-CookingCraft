'''
Description: 烘焙炉界面的 UI
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-15 13:00:48
LastEditTime: 2022-08-25 17:09:15
'''
from hammerCookingScripts.client.ui.base import BaseFurnaceScreen
from hammerCookingScripts.client.utils import pathUtils


class MeterFurnaceScreen(BaseFurnaceScreen):

    def __init__(self, namespace, name, param):
        BaseFurnaceScreen.__init__(self, namespace, name, param)
        self.meterMaskPath = pathUtils.JoinPath(self.furnacePanelPath, "meter",
                                                "liquid")
        self.liquidAmount = 0
        self.liquidVolume = 100

    def Create(self):
        BaseFurnaceScreen.Create(self)
        self.meterMaskControl = self.GetBaseUIControl(
            self.meterMaskPath).asImage()
        self.meterMaskControl.SetClipDirection("fromTopToBottom")

    def UpdateWorkbenchUI(self, workbenchData):
        # type: (dict) -> None
        """更新计量器的 UI"""
        BaseFurnaceScreen.UpdateWorkbenchUI(self, workbenchData)
        for key, value in workbenchData.items():
            if key == "liquidAmount":
                self.liquidAmount = value
                self.__DoUpdateMeterUI()

    def __DoUpdateMeterUI(self):
        meterRatio = 1 - self.liquidAmount * 1.0 / 100
        self.meterMaskControl.SetSpriteClipRatio(meterRatio)
