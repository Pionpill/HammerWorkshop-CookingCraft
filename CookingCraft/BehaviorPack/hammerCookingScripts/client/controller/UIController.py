'''
Description: UI 管理类，这里会负责将所有自定义 UI 进行注册，需要在 modConfig.UI_DEFS 中写入对应的 UI 信息
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-13 18:19:57
LastEditTime: 2022-08-05 15:53:25
'''
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.common.facade import WorkbenchFacade
import mod.client.extraClientApi as clientApi

ScreenNode = clientApi.GetScreenNodeCls()


class UIController(object):
    UIProxy = WorkbenchFacade.GetUIProxy()
    UIDict = {}
    layer = 25123

    @classmethod
    def InitAllUI(cls, args):
        """初始化所有 UI"""
        cls.Clear()
        blockNames = cls.UIProxy.GetAllUIBlockName()
        logger.info("=====注册UI界面=====")
        for blockName in blockNames:
            cls.__InitUI(blockName)

    @classmethod
    def __InitUI(cls, blockName):
        # type: (str) -> None
        """初始化单个 UI"""
        uiName = cls.UIProxy.GetName(blockName)
        uiClassPath = cls.UIProxy.GetClassPath(blockName)
        uiScreenDef = cls.UIProxy.GetScreenDef(blockName)
        if clientApi.RegisterUI(modConfig.ModName, uiName, uiClassPath,
                                uiScreenDef):
            logger.info("成功注册 {0} 界面".format(blockName))

    @classmethod
    def GetUINode(cls, blockName):  # sourcery skip: use-named-expression
        # type: (str) -> BaseInventoryScreen
        """从 cls.UIDict 中取 UINode，若没有，则通过 clientApi.GetUI 获取"""
        uiName = cls.UIProxy.GetName(blockName)
        if not uiName:
            return
        uiNode = cls.UIDict.get(uiName)
        if uiNode:
            uiNode.SetLayer("", cls.layer)
            return uiNode
        return cls.CreateUINode(blockName)

    @classmethod
    def CreateUINode(cls, blockName):
        # type: (str) -> BaseInventoryScreen
        """通过 clientApi.CreateUI() 创建UI并保存，若已经存在直接返回 UI 节点"""
        uiName = cls.UIProxy.GetName(blockName)
        if cls.UIDict.get(uiName):
            return cls.UIDict[uiName]
        uiNode = clientApi.CreateUI(modConfig.ModName, uiName, {'isHub': 1})
        uiNode.SetLayer("", cls.layer)
        cls.UIDict[uiName] = uiNode
        logger.debug("创建 {0} 的 UI 节点".format(blockName))
        return uiNode

    @classmethod
    def Clear(cls):
        """清除保存的 UI 节点"""
        # cls.presentUIDict.clear()
        cls.UIDict.clear()

    @classmethod
    def RemoveUINode(cls, blockName):  # sourcery skip: use-named-expression
        # type: (str) -> bool
        """删除某个 UI 节点"""
        uiName = cls.UIProxy.GetName(blockName)
        uiNode = clientApi.GetUI(modConfig.ModName, uiName)
        if uiNode:
            if uiName in cls.UIDict:
                del cls.UIDict[uiName]
            uiNode.SetRemove()
            return True
        return False

    @classmethod
    def IsBlockHasUI(cls, blockName):
        blockNames = cls.UIProxy.GetAllUIBlockName()
        return blockName in blockNames
