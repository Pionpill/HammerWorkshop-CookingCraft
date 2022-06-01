'''
Description: 工作台客户端系统
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 15:26:04
LastEditTime: 2022-05-01 21:18:29
'''

import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.client.clientSystem.InventoryClientSystem import InventoryClientSystem
from hammerCookingScripts.client.clientManager.ClientSystemManager import ClientSystemManager

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()


class WorkbenchClientSystem(InventoryClientSystem):
    def __init__(self, namespace, systemName):
        InventoryClientSystem.__init__(self, namespace, systemName)
        self.clientSysMgr = ClientSystemManager()
        self.clientSysMgr.SetModClientSystem(
            modConfig.ClientSystemName_Workbench, self)
        self.ListenWorkbenchEvent()

    def ListenWorkbenchEvent(self):
        # 监听服务端事件
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ServerSystemName_Workbench,
                            modConfig.WorkbenchChangedEvent, self,
                            self.OnWorkbenchChanged)

    def OnWorkbenchChanged(self, event):
        """容器界面发生变化时，更新 UI 界面

        Args:
            event (dict): 事件数据，必须包含 blockName，modConfig.WorkbenchData 键
        """
        blockName = event["blockName"]
        uiData = modConfig.UI_DEFS.get(blockName)
        if not uiData:
            logger.error("%s Has No UIData!!!" % blockName)
        uiNode = self.uiManager.GetUINode(uiData)
        uiNode.UpdateWorkbenchUI(event)
