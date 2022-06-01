'''
Description: 背包客户端系统
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 11:21:52
LastEditTime: 2022-05-27 15:52:13
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
from hammerCookingScripts.client.clientManager.UIManager import UIManager

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()


class InventoryClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.uiManager = UIManager()
        self.playerId = clientApi.GetLocalPlayerId()
        self.ListenInventoryEvent()

    def ListenInventoryEvent(self):
        engineNamespace = clientApi.GetEngineNamespace()
        engineSystemName = clientApi.GetEngineSystemName()
        # ============================== 监听客户端事件 ==============================
        self.ListenForEvent(engineNamespace, engineSystemName, 'UiInitFinished',
                            self.uiManager, self.uiManager.InitAllUI)
        # ============================== 监听服务端事件 ==============================
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.InventoryOpenEvent, self,
                            self.OnInventoryOpen)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.BagChangedEvent, self, self.OnBagChanged)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.UIShouldCloseEvent, self,
                            self.OnUIShouldClose)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.ItemSwapServerEvent, self,
                            self.OnItemSwap)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.ItemDropServerEvent, self,
                            self.OnItemDrop)

    def OnBagChanged(self, event):
        """背包发生变化时，更新 UI 界面

        Args:
            event (dict): 事件数据
        """
        blockName = event["blockName"]
        uiData = modConfig.UI_DEFS.get(blockName)
        if not uiData:
            logger.error("%s has no UIData!!!" % blockName)
        uiNode = self.uiManager.GetUINode(uiData)
        uiNode.UpdateInventoryUI(event[modConfig.InventoryData])

    def OnUIShouldClose(self, args):
        """界面强制关闭：玩家死亡，block 摧毁时触发

        Args:
            args (dict): 事件数据
        """
        blockName = args["blockName"]
        uiData = modConfig.UI_DEFS.get(blockName)
        if not uiData:
            logger.error("%s Has No UIData!!!" % blockName)
        uiNode = self.uiManager.GetUINode(uiData)
        uiNode.CloseUI()

    def OnInventoryOpen(self, event):
        """打开工作台 UI

        Args:
            event (dict): 事件数据
        """
        blockName = event['blockName']
        uiData = modConfig.UI_DEFS.get(blockName)
        WorkbenchNode = self.uiManager.GetUINode(uiData)
        WorkbenchNode.ShowUI(event)

    def OnItemSwap(self, args):
        """交换物品：UI界面更新

        Args:
            args (dict): 事件数据
        """
        blockName = args["blockName"]
        uiData = modConfig.UI_DEFS.get(blockName)
        if not uiData:
            logger.error("%s Has No UIData!!!" % blockName)
        uiNode = self.uiManager.GetUINode(uiData)
        uiNode.SwapItem(args)

    def OnItemDrop(self, args):
        """丢弃物品：UI界面删除物品

        Args:
            args (dict): 事件数据
        """
        blockName = args["blockName"]
        uiData = modConfig.UI_DEFS.get(blockName)
        if not uiData:
            logger.error("%s Has No UIData!!!" % blockName)
        uiNode = self.uiManager.GetUINode(uiData)
        uiNode.DropItem(args["slot"])

    def GetPlayerId(self):
        return self.playerId
