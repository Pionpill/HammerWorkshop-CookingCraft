'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 13:22:33
LastEditTime: 2022-08-25 13:23:06
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
from hammerCookingScripts.client.controller import UIController, SystemController

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()


class WorkbenchClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.playerId = clientApi.GetLocalPlayerId()
        SystemController.SetModClientSystem(
            modConfig.ClientSystemName_Workbench, self)
        self.ListenWorkbenchEvent()

    def ListenWorkbenchEvent(self):
        engineNamespace = clientApi.GetEngineNamespace()
        engineSystemName = clientApi.GetEngineSystemName()
        # ============================== 监听客户端事件 ==============================
        self.ListenForEvent(engineNamespace, engineSystemName, 'UiInitFinished',
                            UIController, UIController.InitAllUI)
        # ============================== 监听服务端事件 ==============================
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.WorkbenchOpenEvent, self,
                            self.OnWorkbenchOpen)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.InventoryChangedEvent, self,
                            self.OnInventoryChanged)
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
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.WorkbenchChangedEvent, self,
                            self.OnWorkbenchChanged)

    def OnWorkbenchOpen(self, workbenchData):
        # type: (dict) -> None
        """获取 UINode 并显式 UI"""
        blockName = workbenchData['blockName']
        WorkbenchNode = UIController.GetUINode(blockName)
        WorkbenchNode.ShowUI(workbenchData)

    def OnInventoryChanged(self, inventoryData):
        # type: (dict) -> None
        """背包改变，通知改变背包栏 UI"""
        blockName = inventoryData["blockName"]
        uiNode = UIController.GetUINode(blockName)
        inventorySlotData = inventoryData.get("inventorySlotData")
        uiNode.UpdateInventoryUI(inventorySlotData)

    def OnUIShouldClose(self, args):
        # type: (dict) -> None
        """界面强制关闭：玩家死亡，block 摧毁时触发"""
        blockName = args["blockName"]
        uiNode = UIController.GetUINode(blockName)
        uiNode.CloseUI()

    def OnItemSwap(self, itemSwapData):
        # type: (dict) -> None
        """交换物品：UI界面更新"""
        blockName = itemSwapData["blockName"]
        uiNode = UIController.GetUINode(blockName)
        uiNode.SwapItem(itemSwapData)

    def OnItemDrop(self, args):
        # type: (dict) -> None
        """丢弃物品：UI界面删除物品"""
        blockName = args["blockName"]
        uiNode = UIController.GetUINode(blockName)
        uiNode.DropItem(args["slot"])

    def OnWorkbenchChanged(self, workbenchData):
        # type: (dict) -> None
        """容器界面发生变化时，更新 UI 界面"""
        blockName = workbenchData["blockName"]
        uiNode = UIController.GetUINode(blockName)
        uiNode.UpdateWorkbenchUI(workbenchData)

    def GetPlayerId(self):
        return self.playerId
