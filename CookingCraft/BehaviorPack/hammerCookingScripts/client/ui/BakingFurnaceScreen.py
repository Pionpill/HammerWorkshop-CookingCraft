'''
Description: 烘焙炉界面的 UI

version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-15 13:00:48
LastEditTime: 2022-05-25 23:02:11
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.client.ui.FurnaceUI import FurnaceUI
from hammerCookingScripts.common import modConfig

compFactory = clientApi.GetEngineCompFactory()


class BakingFurnaceScreen(FurnaceUI):
    def __init__(self, namespace, name, param):
        FurnaceUI.__init__(self, namespace, name, param)

    def Create(self):
        FurnaceUI.Create(self)

    def Destroy(self):
        FurnaceUI.Destroy(self)

    def Update(self):
        FurnaceUI.Update(self)

    def ShowUI(self, args):
        FurnaceUI.ShowFurnaceUI(self, args)
        self.InitWorkbenchUI(args)

    def InitWorkbenchUI(self, args):
        """初始化烘焙炉界面，需要服务端数据

        Args:
            args (dict): 包含 "WorkbenchData" 键，获取熔炉物品数据
        """
        items = args[modConfig.WorkbenchData]
        for slotName, itemDict in items.items():
            slotPath = "{0}/{1}".format(self.furnacePanelPath, slotName)
            self.slotData[slotPath] = {"slot": slotName, "item": itemDict}
            self.slotPath[slotName] = slotPath
            self.SetSlotUI(slotPath, itemDict)
        # 初始化燃烧进度
        self.flameMaskControl.SetSpriteClipRatio(1)
        self.arrowMaskControl.SetSpriteClipRatio(1)

    def UpdateWorkbenchUI(self, args):
        """更新熔炉界面，需要服务端数据

        Args:
            args (dict): 包含 "WorkbenchData" 键，用于更新 UI
        """
        for key, value in args.items():
            # 更新燃料状态
            if key == "isLit":
                self.isLit = value
            elif key == "litDuration":
                if value != self.litDuration:
                    self.litDuration = args["litDuration"]
                    self.litProgress = 0
            elif key == "isCooking":
                self.isCooking = value
            elif key == "litProgress":
                self.litProgress = value
            elif key == "burnProgress":
                self.burnProgress = value
            # 更新物品信息
            elif key == modConfig.WorkbenchData:
                for slotName, itemDict in value.items():
                    slotPath = "{0}/{1}".format(self.furnacePanelPath, slotName)
                    self.slotData[slotPath] = {
                        "slot": slotName,
                        "item": itemDict
                    }
                    self.SetSlotUI(slotPath, itemDict)
