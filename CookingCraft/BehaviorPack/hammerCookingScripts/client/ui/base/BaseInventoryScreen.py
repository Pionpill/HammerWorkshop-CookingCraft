'''
Description: 包含背包界面的 BaseBlockScreen，必须具有以下结构
|- main
    |- inventory_panel
        |- bag_grid
        |- hand_grid
        |- item_detail
        |- progressive_bar
grid 的元素 item_slot 具有以下结构
|- item_slot
    |- item_renderer
    |- count_label
    |- item_button
    |- selected_image
    |- durability_bar
        
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-14 21:30:58
LastEditTime: 2022-04-15 17:33:18
'''

from abc import abstractmethod
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.client.ui.base.BaseBlockScreen import BaseBlockScreen
from hammerCookingScripts.client.utils import pathUtils
from hammerCookingScripts.client.ui.utils.interactState import ContainerInteractionStateMachine, ButtonEventType, NodeId
from hammerCookingScripts.client.ui.manager import SlotManager
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.common.utils import itemUtils, workbenchUtils
from hammerCookingScripts.client.controller import SystemController

compFactory = clientApi.GetEngineCompFactory()


class BaseInventoryScreen(BaseBlockScreen):

    def __init__(self, namespace, name, param):
        BaseBlockScreen.__init__(self, namespace, name, param)
        self.inventoryPanelPath = "/inventory_panel"
        self.bagGridPath = "{0}/bag_grid".format(self.inventoryPanelPath)
        self.handGridPath = "{0}/hand_grid".format(self.inventoryPanelPath)
        self.progressiveBarPath = "{0}/progressive_bar".format(
            self.inventoryPanelPath)
        self.progressiveBarImagePath = "{0}/bar_mask".format(
            self.progressiveBarPath)
        self.itemDetailBgPath = "{0}/item_detail/item_detail_bg".format(
            self.inventoryPanelPath)
        self.itemDetailTextPath = "{0}/item_detail/item_detail_bg/item_detail_text".format(
            self.inventoryPanelPath)
        # 管理背包槽位信息
        self.slotManager = SlotManager()
        self.lastSelectedPath = None  # slot path
        self.lastTouchButtonPath = None
        self.lastTouchPosition = None
        self.alreadyRegisterEvent = False  # Inventory 背包槽注册
        self.heldTime = None
        self.blockName = None
        self.pos = None
        self.dimensionId = None
        self.isDoubleClick = False
        self.detailAlpha = 0.0
        self.clickInterval = 0
        self.takePercent = 1
        self.levelId = clientApi.GetLevelId()

    def Create(self):
        BaseBlockScreen.Create(self)
        self.progressiveBarImageControl = self.GetBaseUIControl(
            self.progressiveBarImagePath).asImage()
        self.progressiveBarControl = self.GetBaseUIControl(
            self.progressiveBarPath).asImage()
        self.containerStateMachine = ContainerInteractionStateMachine()
        self.itemDetailBgControl = self.GetBaseUIControl(
            self.itemDetailBgPath).asImage()
        self.itemDetailTextControl = self.GetBaseUIControl(
            self.itemDetailTextPath).asLabel()
        self.__DoRegisterStateMachine()

    def __DoRegisterStateMachine(self):
        """注册按钮状态节点以及转换条件"""
        # 注册状态节点
        self.containerStateMachine.AddNode(NodeId.Idle, self.__HandleIdle, None,
                                           True)
        self.containerStateMachine.AddNode(NodeId.SelectSlot,
                                           self.__HandleSelected)
        self.containerStateMachine.AddNode(NodeId.UnSelectSlot,
                                           self.__HandleUnSelected)
        self.containerStateMachine.AddNode(NodeId.Swap, self.__HandleSwap)
        self.containerStateMachine.AddNode(NodeId.DropAll, self.__HandleDropAll)
        self.containerStateMachine.AddNode(NodeId.TouchProgressiveSelect,
                                           self.__HandleTouchProgressiveSelect)
        self.containerStateMachine.AddNode(
            NodeId.TouchProgressiveSelectComplete,
            self.__HandleTouchProgressiveComplete)
        self.containerStateMachine.AddNode(NodeId.TouchProgressiveSelectCancel,
                                           self.__HandleTouchProgressiveCancel)
        self.containerStateMachine.AddNode(NodeId.Coalesce,
                                           self.__HandleCoalesce)
        # 注册状态转移条件
        self.containerStateMachine.AddEdge(NodeId.Idle, NodeId.SelectSlot,
                                           self.__CanSelected)
        self.containerStateMachine.AddEdge(NodeId.SelectSlot,
                                           NodeId.UnSelectSlot,
                                           self.__CanUnSelected)
        self.containerStateMachine.AddEdge(NodeId.SelectSlot, NodeId.Swap,
                                           self.__CanSwap)
        self.containerStateMachine.AddEdge(NodeId.SelectSlot, NodeId.DropAll,
                                           self.__CanDrop)
        self.containerStateMachine.AddEdge(NodeId.SelectSlot, NodeId.Coalesce,
                                           self.__CanCoalesce)
        self.containerStateMachine.AddEdge(NodeId.Idle,
                                           NodeId.TouchProgressiveSelect,
                                           self.__CanProgressiveSelect)
        self.containerStateMachine.AddEdge(
            NodeId.TouchProgressiveSelect,
            NodeId.TouchProgressiveSelectComplete,
            self.__CanProgressiveComplete)
        self.containerStateMachine.AddEdge(NodeId.TouchProgressiveSelect,
                                           NodeId.TouchProgressiveSelectCancel,
                                           self.__CanProgressiveCancel)
        self.containerStateMachine.AddEdge(
            NodeId.TouchProgressiveSelectComplete, NodeId.Swap, self.__CanSwap)
        self.containerStateMachine.AddEdge(
            NodeId.TouchProgressiveSelectComplete,
            NodeId.TouchProgressiveSelectCancel, self.__CanUnSelected)

    def Update(self):
        """
        背包更新
        1. 长按分堆的实现与 UI 显示
        2. 物品详细信息栏渐退效果
        """
        if self.heldTime is not None:
            self.heldTime += 1
            if self.heldTime == 10:
                self.containerStateMachine.ReceiveEvent(
                    self.lastTouchButtonPath, ButtonEventType.Pressed)
            if self.containerStateMachine.GetCurrentNodeId(
            ) == NodeId.TouchProgressiveSelect:
                self.__SetProgressiveBar()
        if self.clickInterval > 0:
            self.clickInterval -= 1
        if self.detailAlpha > 0:
            self.detailAlpha -= 0.04
        self.__DoShowDetail()

    def __SetProgressiveBar(self):
        """设置长按物品按比例拾取的 UI 显示条"""
        if not self.lastTouchButtonPath:
            logger.error("SetProgressiveBar Error!!! No Last Touch Button!!!")
            return
        item = self._GetItemByPath(self.lastTouchButtonPath)
        if not item:
            logger.error(
                "SetProgressiveBar Error!!! Try progressive none item!!!")
            return
        self.__DoCalculateProgressiveRatio(item)
        self.progressiveBarImageControl.SetSpriteClipRatio(1 - self.takePercent)

    def __DoCalculateProgressiveRatio(self, itemDict):
        # type: (dict) -> None
        """计算长按状态下分堆比例"""
        if self.heldTime is None:
            logger.error("Enter Progressive State But The Held Time is None!!!")
            return
        heldTime = self.heldTime - 10
        if heldTime > 20:
            self.takePercent = 1
            return
        totalNum = itemDict.get("count")
        takeNum = heldTime * totalNum / 20
        if takeNum == 0:
            takeNum = 1
            self.heldTime = takeNum * 20 / totalNum + 10
        self.takePercent = takeNum * 1.0 / totalNum

    def __DoShowDetail(self):
        """设置详情面板透明度"""
        if self.detailAlpha > 1:
            self.itemDetailBgControl.SetAlpha(1)
            self.itemDetailTextControl.SetAlpha(1)
        else:
            self.itemDetailBgControl.SetAlpha(self.detailAlpha)
            self.itemDetailTextControl.SetAlpha(self.detailAlpha)

    def ShowInventoryUI(self, workbenchData):
        # sourcery skip: use-fstring-for-concatenation
        """显示 UI 界面"""
        if self.lastSelectedPath:
            lastSelectedItemRenderControl = self.GetBaseUIControl(
                self.lastSelectedPath + "/selected_image").asImage()
            lastSelectedItemRenderControl.SetVisible(False)
            self.lastSelectedPath = None
        self.blockName = workbenchData["blockName"]
        self.pos = workbenchData["pos"]
        self.dimensionId = workbenchData["dimensionId"]
        self.containerStateMachine.ResetToDefault()
        BaseBlockScreen.ShowBlockUI(self)

    def UpdateInventoryUI(self, inventorySlotData):
        # type: (dict) -> None
        """更新 UI 的 Inventory 界面"""
        handGridList = self.GetChildrenName(self.handGridPath)
        bagGridList = self.GetChildrenName(self.bagGridPath)
        for index, inventoryGridSlot in enumerate(handGridList + bagGridList):
            gridPath = self.handGridPath if index < 9 else self.bagGridPath
            inventorySlotPath = pathUtils.JoinPath(gridPath, inventoryGridSlot)
            itemDict = inventorySlotData[index]
            # 更新UI记录的信息
            self.slotManager.SetSlotInfo(index,
                                         info=(inventorySlotPath, itemDict))
            self._SetSlotUI(inventorySlotPath, itemDict)
        self.__RegisterButtonEvents()

    def __RegisterButtonEvents(self):
        # type: () -> None
        """注册按钮交互事件"""
        if self.alreadyRegisterEvent:
            return
        for path in self.slotManager.GetAllSlotPath():
            buttonPath = pathUtils.JoinPath(path, "item_button")
            buttonControl = self.GetBaseUIControl(buttonPath).asButton()
            buttonControl.AddTouchEventParams({"isSwallow": True})
            # 结果槽点击后直接返回物品到背包
            if workbenchUtils.IsResultSlot(self.slotManager.GetSlotName(path)):
                buttonControl.SetButtonTouchDownCallback(
                    self.__OnResultButtonTouchDown)
            else:
                buttonControl.SetButtonTouchDownCallback(
                    self.__OnButtonTouchDown)
            buttonControl.SetButtonTouchUpCallback(self.__OnButtonTouchUp)
            buttonControl.SetButtonTouchCancelCallback(
                self.__OnButtonTouchCancel)
            buttonControl.SetButtonTouchMoveCallback(self.__OnButtonTouchMove)
            buttonControl.SetButtonTouchMoveInCallback(
                self.__OnButtonTouchMoveIn)
            buttonControl.SetButtonTouchMoveOutCallback(
                self.__OnButtonTouchMoveOut)
        self.alreadyRegisterEvent = True

    def __OnButtonTouchDown(self, args):  # sourcery skip: use-named-expression
        """按钮按下事件: 展示详细信息，判断是否双击，获取最后点击的按钮 path 与 position"""
        touchPos = args["TouchPosX"], args["TouchPosY"]
        buttonPath = args["ButtonPath"]
        slotPath = self._GetSlotPath(buttonPath)
        self.lastTouchButtonPath = args["ButtonPath"]
        self.lastTouchPosition = touchPos
        item = self._GetItemByPath(slotPath)
        if item:
            self._ShowItemDetail(item)
        if self.clickInterval > 0 and self.lastTouchButtonPath == args[
                "ButtonPath"]:
            self.isDoubleClick = True
            return
        self.isDoubleClick = False
        self.heldTime = 0

    def __OnResultButtonTouchDown(self, args):
        # sourcery skip: use-named-expression
        touchPos = args["TouchPosX"], args["TouchPosY"]
        buttonPath = args["ButtonPath"]
        slotPath = self._GetSlotPath(buttonPath)
        self.lastTouchButtonPath = args["ButtonPath"]
        self.lastTouchPosition = touchPos
        item = self._GetItemByPath(slotPath)
        if item:
            self._ShowItemDetail(item)
        self.isDoubleClick = False
        eventData = {"item": self._GetItemByPath(slotPath)}
        eventData["slot"] = slotPath.split("/")[-1]
        eventData["pos"] = self.pos
        eventData["dimensionId"] = self.dimensionId
        clientSystem = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench)
        eventData["playerId"] = clientSystem.GetPlayerId()
        clientSystem.NotifyToServer(modConfig.OutSlotClickEvent, eventData)
        self._SetSlotUI(slotPath, None)

    def _ShowItemDetail(self, itemDict):
        # type: (dict) -> None
        """显示物品详细信息 UI"""
        itemComp = compFactory.CreateItem(self.levelId)
        detailText = itemComp.GetItemFormattedHoverText(
            itemDict["newItemName"], itemDict["newAuxValue"], True,
            itemDict.get("userData"))
        self.itemDetailTextControl.SetText(detailText)
        self.itemDetailBgControl.SetPosition((0, 50))
        self.detailAlpha = 2.0

    def __OnButtonTouchUp(self, args):
        """按钮弹起事件: 双击，长按，普通弹起，交由 containerStateMachine 处理"""
        if self.isDoubleClick:
            self.containerStateMachine.ReceiveEvent(args["ButtonPath"],
                                                    ButtonEventType.DoubleClick)
        elif self.heldTime and self.heldTime < 10:
            self.containerStateMachine.ReceiveEvent(args["ButtonPath"],
                                                    ButtonEventType.Clicked)
        else:
            self.containerStateMachine.ReceiveEvent(args["ButtonPath"],
                                                    ButtonEventType.Released)
        self.heldTime = None
        self.clickInterval = modConfig.DOUBLE_CLICK_INTERVAL

    def __OnButtonTouchCancel(self, args):
        """按钮取消事件: 长按时间归零"""
        self.heldTime = None
        self.__OnTouchCancel()

    def __OnButtonTouchMove(self, args):
        """按钮移走事件"""
        self.__OnTouchCancel()

    def __OnButtonTouchMoveIn(self, args):
        """按钮移入事件: 不做处理"""
        pass

    def __OnButtonTouchMoveOut(self, args):
        """按钮移入出事件：按钮 release"""
        self.heldTime = None
        self.containerStateMachine.ReceiveEvent(self.lastTouchButtonPath,
                                                ButtonEventType.Released)

    def __OnTouchCancel(self):
        """传入取消按下事件"""
        self.containerStateMachine.ReceiveEvent(None, ButtonEventType.Released)

    def DropItem(self, slot):
        # type: (str|int) -> None
        """丢弃物品"""
        self.slotManager.SetSlotItem(slot, None)

    def SwapItem(self, swapData):
        # type: (dict) -> None
        """交换物品"""
        fromSlot = swapData["fromSlot"]
        toSlot = swapData["toSlot"]
        fromPath = self.slotManager.GetSlotPath(fromSlot)
        toPath = self.slotManager.GetSlotPath(toSlot)
        fromItem = swapData["fromItem"]
        toItem = swapData["toItem"]
        self._SetSlotUI(fromPath, toItem)
        self._SetSlotUI(toPath, fromItem)
        self.slotManager.SetSlotItem(fromSlot, toItem)
        self.slotManager.SetSlotItem(toSlot, fromItem)

    def _GetItemByPath(self, itemPath):
        """通过路径获取物品信息"""
        slotPath = self._GetSlotPath(itemPath)
        return self.slotManager.GetSlotItem(path=slotPath)

    def _GetSlotNameByPath(self, path):
        # type: (str|int) -> str|int
        """通过 slotPath 获取 slotName; path 的父路径包括 slot 路径"""
        path = self._GetSlotPath(path)
        return self.slotManager.GetSlotName(path)

    def _GetSlotPath(self, path):
        # type: (str) -> str
        """获取 slot 的UI路径"""
        oriPathList = path.split("/")
        if "slot" in oriPathList[-1]:
            return path
        newPathList = []
        for subPath in oriPathList:
            newPathList.append(subPath)
            if "slot" in subPath:
                break
        return ("/").join(newPathList)

    def _SetSlotUI(self, path, item):
        # sourcery skip: use-fstring-for-concatenation
        # type: (str|int, dict) -> None
        """设置 slotPath 的 item UI"""
        if item and item.get('count'):
            self.__DoSetSlotItemUI(path, item)
        else:
            self.GetBaseUIControl(path + "/item_renderer").SetVisible(False)
            self.GetBaseUIControl(path + "/count_label").SetVisible(False)
            self.GetBaseUIControl(path + "/durability_bar").SetVisible(False)

    def __DoSetSlotItemUI(self, path, item):
        # sourcery skip: use-fstring-for-concatenation
        self.__DoSetDurabilityBar(path, item)
        isEnchant = bool(item.get('enchatData'))
        userData = item.get('userData')
        self.SetUiItem(path + "/item_renderer", item["newItemName"],
                       item["newAuxValue"], isEnchant, userData)

        self.GetBaseUIControl(path + "/item_renderer").SetVisible(True)
        countLabelControl = self.GetBaseUIControl(path +
                                                  "/count_label").asLabel()
        if item["count"] > 1:
            countLabelControl.SetVisible(True)
            countLabelControl.SetText(str(item["count"]))
        else:
            countLabelControl.SetText("")
        del countLabelControl

    def __DoSetDurabilityBar(self, path, item):
        # sourcery skip: use-fstring-for-concatenation
        # type: (str, dict) -> None
        """设置目标 slot 耐久度 UI"""
        durabilityRatio = self.__DoCalculateDurabilityRatio(item)
        barImagePath = path + "/durability_bar/bar_mask"
        barImageControl = self.GetBaseUIControl(barImagePath).asImage()
        barControl = self.GetBaseUIControl(path + "/durability_bar")
        if durabilityRatio != 1:
            barImageControl.SetSpriteColor(
                (1 - durabilityRatio, durabilityRatio, 0))
            barImageControl.SetSpriteClipRatio(1 - durabilityRatio)
            barControl.SetVisible(True)
        else:
            barControl.SetVisible(False)
        del barImageControl
        del barControl

    def __DoCalculateDurabilityRatio(self, itemDict):
        # sourcery skip: use-named-expression
        # type: (dict) -> float
        """计算物品耐久度比例，用于显示耐久度槽"""
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("newItemName", ""),
                                              itemDict.get("newAuxValue", 0))
        if not basicInfo:
            return 1
        currentDurability = itemDict.get("durability")
        if currentDurability is None:
            return 1
        maxDurability = basicInfo.get("maxDurability", 0)
        if maxDurability != 0:
            return currentDurability * 1.0 / maxDurability
        return 1

    def __HandleIdle(self, buttonPath):
        """处理默认按钮: 基础属性重置，不显示特殊图片"""
        self.clickInterval = 0
        self.heldTime = None
        self.lastTouchButtonPath = None
        self.isDoubleClick = False
        self.takePercent = 1
        self.progressiveBarControl.SetVisible(False)
        if self.lastSelectedPath:
            self.GetBaseUIControl(self.lastSelectedPath +
                                  "/selected_image").SetVisible(False)
            self.lastSelectedPath = None

    def __HandleSelected(self, buttonPath):
        # type: (str) -> None
        """处理选中按钮: 显示选中图片"""
        self.lastSelectedPath = buttonPath.replace("/item_button", "")
        self.GetBaseUIControl(self.lastSelectedPath +
                              "/selected_image").SetVisible(True)

    def __HandleUnSelected(self, buttonPath):
        """处理未被选中: 状态重置"""
        self.containerStateMachine.ResetToDefault()

    def __HandleSwap(self, buttonPath):
        # type: (str) -> None
        """处理物品交换: 向服务端传入 ItemSwapClientEvent 事件及相关数据"""
        if not self.lastSelectedPath:
            logger.error("there is no last selected button, swap failed!!!")
            return
        swapData = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).CreateEventData()
        swapData["blockName"] = self.blockName
        swapData["fromSlot"] = self._GetSlotNameByPath(self.lastSelectedPath)
        swapData["toSlot"] = self._GetSlotNameByPath(buttonPath)
        swapData["playerId"] = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).GetPlayerId()
        swapData["fromItem"] = self._GetItemByPath(self.lastSelectedPath)
        swapData["toItem"] = self._GetItemByPath(buttonPath)
        swapData["pos"] = self.pos
        swapData["dimensionId"] = self.dimensionId
        swapData["takePercent"] = self.takePercent
        clientSystem = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench)
        clientSystem.NotifyToServer(modConfig.ItemSwapClientEvent, swapData)
        self.containerStateMachine.ResetToDefault()

    def __HandleDropAll(self, buttonPath):
        # FIXME 无法触发
        """处理物品丢弃: 向服务端传入 ItemDropClientEvent 事件及 相关数据"""
        if not self.lastSelectedPath:
            logger.error("there is no last selected button, drop failed!!!")
            return
        dropData = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).CreateEventData()
        dropData["blockName"] = self.blockName
        dropData["playerId"] = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).GetPlayerId()
        dropData["pos"] = self.pos
        dropData["dimensionId"] = self.dimensionId
        dropData["slot"] = self._GetSlotNameByPath(self.lastSelectedPath)
        dropData["item"] = self._GetItemByPath(self.lastSelectedPath)
        SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).NotifyToServer(
                modConfig.ItemDropClientEvent, dropData)
        self.containerStateMachine.ResetToDefault()

    def __HandleTouchProgressiveSelect(self, buttonPath):
        # type: (str) -> None
        """处理长按按钮"""
        self.__HandleSelected(buttonPath)
        inventoryPanelPos = self.GetBaseUIControl(
            self.inventoryPanelPath).GetPosition()
        self.progressiveBarControl.SetPosition(
            (self.lastTouchPosition[0] - inventoryPanelPos[0] - 8,
             self.lastTouchPosition[1] - inventoryPanelPos[1] - 4))
        self.progressiveBarControl.SetVisible(True)

    def __HandleTouchProgressiveComplete(self, buttonPath):
        """处理长按按钮分堆结束"""
        self.heldTime = None

    def __HandleTouchProgressiveCancel(self, buttonPath):
        """处理取消长按后分堆"""
        self.containerStateMachine.ResetToDefault()

    def __HandleCoalesce(self, buttonPath):
        # sourcery skip: use-named-expression
        # type: (str) -> None
        """处理合堆"""
        slotName = self._GetSlotNameByPath(buttonPath)
        if workbenchUtils.IsResultSlot(slotName):
            # 结果槽禁止进行合堆操作
            self.containerStateMachine.ResetToDefault()
        itemDict = self._GetItemByPath(buttonPath)
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        newItemName = itemDict.get("newItemName", "")
        newAuxValue = itemDict.get("newAuxValue", 0)
        itemInfo = itemComp.GetItemBasicInfo(newItemName, newAuxValue)
        if itemInfo:
            self.__DoCoalesce(itemInfo, itemDict, buttonPath)
        self.GetBaseUIControl(
            buttonPath.replace("/item_button", "") +
            "/selected_image").SetVisible(False)
        self.containerStateMachine.ResetToDefault()

    def __DoCoalesce(self, itemInfo, itemDict, buttonPath):
        # type: (dict, dict, str) -> None
        """遍历槽物品进行合堆"""
        maxStackSize = itemInfo.get("maxStackSize")
        if maxStackSize <= 1 or itemDict.get("count") == maxStackSize:
            return
        for path in self.slotManager.GetAllSlotPath():
            itemName = itemDict.get("newItemName")
            if self._GetSlotPath(
                    buttonPath) == path or workbenchUtils.IsResultSlot(
                        itemName):
                continue
            item = self._GetItemByPath(path)
            if itemUtils.IsSameItem(
                    item, itemDict) and item.get("count") != maxStackSize:
                self.lastSelectedPath = path
                self.__HandleSwap(buttonPath)

    def __CanSelected(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断是否可选"""
        if not buttonPath:
            return False
        item = self._GetItemByPath(buttonPath)
        if item and buttonEvent == ButtonEventType.Clicked:
            return True
        return False

    def __CanUnSelected(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断不被选中"""
        return buttonPath and buttonPath.replace(
            "/item_button", ""
        ) == self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanSwap(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断可以交换"""
        return buttonPath and buttonPath.replace(
            "/item_button", ""
        ) != self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanDrop(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断可以丢弃"""
        return self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanProgressiveSelect(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断可以长按分堆"""
        if not buttonPath:
            return False
        itemDict = self._GetItemByPath(buttonPath)
        if not itemDict or buttonEvent != ButtonEventType.Pressed:
            return False
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("newItemName", ""),
                                              itemDict.get("newAuxValue", 0))
        if not basicInfo:
            return False
        maxStackSize = basicInfo.get("maxStackSize")
        if maxStackSize > 1:
            return True

    def __CanProgressiveCancel(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断取消长按分堆"""
        return not buttonPath and buttonEvent == ButtonEventType.Released

    def __CanProgressiveComplete(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断完成长按分堆"""
        return buttonPath and buttonEvent == ButtonEventType.Released

    def __CanCoalesce(self, buttonPath, buttonEvent):
        # type: (str, int) -> bool
        """判断能否合并"""
        return buttonEvent == ButtonEventType.DoubleClick

    @abstractmethod
    def ShowUI(self, args):
        """子类显示 UI 函数"""
        pass

    @abstractmethod
    def UpdateWorkbenchUI(self, event):
        """工作台界面更新"""
        pass
