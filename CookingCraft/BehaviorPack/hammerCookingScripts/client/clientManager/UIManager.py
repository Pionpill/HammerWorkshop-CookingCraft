'''
Description: UI 管理类，这里会负责将所有自定义 UI 进行注册，需要在 modConfig.UI_DEFS 中写入对应的 UI 信息
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-13 18:19:57
LastEditTime: 2022-05-27 16:26:41
'''
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
import mod.client.extraClientApi as clientApi


class UIManager(object):
    def __init__(self):
        super(UIManager, self).__init__()
        # 所有被注册的 UI 的信息字典: uiName:uiNode
        self.UIDict = {}
        # 启用的 UI 信息字典
        # self.presentUIDict = {}
        self.layer = 25123

    def InitAllUI(self, *args, **kwargs):
        """初始化所有 UI
        """
        self.Clear()
        for _, uiData in modConfig.UI_DEFS.items():
            self.InitUI(uiData)

    def InitUI(self, uiData):
        """初始化单个 UI

        Args:
            uiData (dict): ui 数据，modConfig.UI_DEFS 值
        """
        uiName = uiData.get("uiName")
        clientApi.RegisterUI(modConfig.ModName, uiName, uiData['uiClassPath'],
                             uiData['uiScreenDef'])

    def CreateUINode(self, uiData):
        """通过 clientApi.CreateUI() 创建UI并保存，若已经存在直接返回 UI 节点

        Args:
            uiData (dict): modConfig.UI_DEFS 值

        Returns:
            ScreenNode: ui 节点
        """
        uiName = uiData.get("uiName")
        if self.UIDict.get(uiName):
            return self.UIDict[uiName]
        else:
            uiNode = clientApi.CreateUI(modConfig.ModName, uiName, {'isHub': 1})
            uiNode.SetLayer("", self.layer)
            self.UIDict[uiName] = uiNode
            return uiNode

    def GetUINode(self, uiData):
        """从 UIDict 中取 UINode，若没有，则通过 clientApi.GetUI 获取

        Args:
            uiData (dict): modConfig.UI_DEFS 值

        Returns:
            ScreenNode: ui 节点
        """
        uiName = uiData['uiName']
        uiNode = self.UIDict.get(uiName, None)
        if uiNode:
            uiNode.SetLayer("", self.layer)
            return uiNode
        return self.CreateUINode(uiData)

    def Clear(self):
        """清除保存的 UI 节点
        """
        # self.presentUIDict.clear()
        self.UIDict.clear()

    def RemoveUINode(self, uiName):
        """删除某个 UI 节点

        Args:
            uiName (str): ui 名，可通过 uiData 获得

        Returns:
            bool: 成功删除返回 True
        """
        uiNode = clientApi.GetUI(modConfig.ModName, uiName)
        if uiNode:
            if uiName in self.UIDict:
                del self.UIDict[uiName]
            uiNode.SetRemove()
            return True
        return False
