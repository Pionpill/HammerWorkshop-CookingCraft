'''
Description: 包含背包界面的 BlockUI，必须具有以下结构
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
from mod.client.ui.viewBinder import ViewBinder
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.client.ui.BlockUI import BlockUI
from hammerCookingScripts.client.clientUtils.interactState import ContainerInteractionStateMachine, ButtonEventType, NodeId
from hammerCookingScripts.utils import itemUtils

compFactory = clientApi.GetEngineCompFactory()


class InventoryUI(BlockUI):
    def __init__(self, namespace, name, param):
        BlockUI.__init__(self, namespace, name, param)
        self.inventoryPanelPath = "/inventory_panel"
        self.bagGridPath = self.inventoryPanelPath + "/bag_grid"
        self.handGridPath = self.inventoryPanelPath + "/hand_grid"
        self.progressiveBarPath = self.inventoryPanelPath + "/progressive_bar"
        self.progressiveBarImagePath = self.progressiveBarPath + "/bar_mask"
        self.itemDetailBgPath = self.inventoryPanelPath + "/item_detail/item_detail_bg"
        self.itemDetailTextPath = self.inventoryPanelPath + "/item_detail/item_detail_bg/item_detail_text"
        # 管理背包槽位信息
        # key: slotPath value: index, item
        self.slotData = {}
        # key: index/slotName value: slotPath
        self.slotPath = {}
        # 交互信息
        self.lastSelectedPath = None  # slot path
        self.lastTouchButtonPath = None
        self.lastTouchPosition = None
        self.alreadyRegisterEvent = False  # Inventory 背包槽注册
        self.heldTime = None
        self.blockName = None
        self.blockPos = None
        self.dimension = None
        self.isDoubleClick = False
        self.detailAlpha = 0.0
        self.clickInterval = 0
        self.takePercent = 1

    def Create(self):
        BlockUI.Create(self)
        self.progressiveBarImageControl = self.GetBaseUIControl(
            self.progressiveBarImagePath).asImage()
        self.progressiveBarControl = self.GetBaseUIControl(
            self.progressiveBarPath).asImage()
        self.containerStateMachine = ContainerInteractionStateMachine()
        self.itemDetailBgControl = self.GetBaseUIControl(
            self.itemDetailBgPath).asImage()
        self.itemDetailTextControl = self.GetBaseUIControl(
            self.itemDetailTextPath).asLabel()
        self.__RegisterStateMachine()

    def Destroy(self):
        BlockUI.Destroy(self)

    def Update(self):
        """背包更新
        
        content:
            长按分堆的实现与 UI 显示
            物品详细信息栏渐退效果
        """
        if self.heldTime is not None:
            self.heldTime += 1
            if self.heldTime == 10:
                self.containerStateMachine.ReceiveEvent(
                    self.lastTouchButtonPath, ButtonEventType.Pressed)
            if self.containerStateMachine.GetCurrentNodeId(
            ) == NodeId.TouchProgressiveSelect:
                self.SetProgressiveBar()
        if self.clickInterval > 0:
            self.clickInterval -= 1
        if self.detailAlpha > 0:
            self.detailAlpha -= 0.04
        self.__OnDetailShow()

    def ShowInventoryUI(self, args):
        """ 显示 UI 界面

        Args:
            args (dict): 包含 "blockName" 键
        """
        if self.lastSelectedPath:
            lastSelectedItemRenderControl = self.GetBaseUIControl(
                self.lastSelectedPath + "/selected_image").asImage()
            lastSelectedItemRenderControl.SetVisible(False)
            self.lastSelectedPath = None
        self.blockName = args["blockName"]
        self.blockPos = args["blockPos"]
        self.dimension = args["dimension"]
        self.containerStateMachine.ResetToDefault()
        BlockUI.ShowBlockUI(self)

    def UpdateInventoryUI(self, event):
        """更新 UI 的 Inventory 界面

        Args:
            event (dict): 背包数据字典，包含所有物品信息
        """
        handGridList = self.GetChildrenName(self.handGridPath)
        bagGridList = self.GetChildrenName(self.bagGridPath)
        index = 0
        for inventoryGridSlot in handGridList + bagGridList:
            if index < 9:
                gridPath = self.handGridPath
            else:
                gridPath = self.bagGridPath
            inventoryGridSlotPath = gridPath + "/" + inventoryGridSlot
            itemDict = event[index]
            # 更新UI记录的信息
            self.slotData[inventoryGridSlotPath] = {
                "slot": index,
                "item": itemDict
            }
            self.slotPath[index] = inventoryGridSlotPath
            index += 1
            self.SetSlotUI(inventoryGridSlotPath, itemDict)
        self.RegisterButtonEvents(self.slotData.keys())

    def DropItem(self, slot):
        """丢弃物品

        Args:
            slot (int): slot Id
        """
        dropPath = self.slotPath[slot]
        self.SetItemAtPath(dropPath, None)

    def SwapItem(self, args):
        """交换物品

        Args:
            args (dict): 交换物品信息字典
        """
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        fromPath = self.slotPath[fromSlot]
        toPath = self.slotPath[toSlot]
        fromItem = args["fromItem"]
        toItem = args["toItem"]
        self.__SwapItemUI(fromPath, toPath, fromItem, toItem)
        self.SetItemAtPath(fromPath, toItem)
        self.SetItemAtPath(toPath, fromItem)

    def SetProgressiveBar(self):
        """设置长按物品按比例拾取的 UI 显示条
        """
        if not self.lastTouchButtonPath:
            logger.error("SetProgressiveBar Error!!! No Last Touch Button!!!")
            return
        item = self.GetItemByPath(self.lastTouchButtonPath)
        if not item:
            logger.error(
                "SetProgressiveBar Error!!! Try progressive none item!!!")
            return
        self.__CalculateProgressiveRatio(item)
        self.progressiveBarImageControl.SetSpriteClipRatio(1 - self.takePercent)

    def SetItemAtPath(self, itemPath, item):
        """设置背包数据中的物品

        Args:
            itemPath (str): slot 路径
            item (dict): 物品信息
        """
        self.slotData[itemPath]["item"] = item

    def GetItemByPath(self, itemPath):
        """通过路径获取物品信息

        Args:
            itemPath (str): slot path

        Returns:
            dict: 单个物品信息
        """
        slotPath = self.__GetSlotPath(itemPath)
        return self.slotData[slotPath]["item"]

    def GetSlotByPath(self, path):
        """通过路径获取 slot Id

        Args:
            path (str): slot path

        Returns:
            int: slot id
        """
        path = self.__GetSlotPath(path)
        return self.slotData[path]["slot"]

    def SetSlotUI(self, path, item):
        """设置目标 slot 的 item UI

        Args:
            path (str): slot path
            item (dict): 物品信息
        """
        if item and item.get('count'):
            self.__SetDurabilityBar(path, item)
            isEnchant = False
            if item.get('enchatData'):
                isEnchant = True
            userData = item.get('userData')
            self.SetUiItem(path + "/item_renderer", item["itemName"],
                           item["auxValue"], isEnchant, userData)
            self.GetBaseUIControl(path + "/item_renderer").SetVisible(True)
            countLabelControl = self.GetBaseUIControl(path +
                                                      "/count_label").asLabel()
            if item["count"] > 1:
                countLabelControl.SetVisible(True)
                countLabelControl.SetText(str(item["count"]))
            else:
                countLabelControl.SetText("")
            del countLabelControl
        else:
            self.GetBaseUIControl(path + "/item_renderer").SetVisible(False)
            self.GetBaseUIControl(path + "/count_label").SetVisible(False)
            self.GetBaseUIControl(path + "/durability_bar").SetVisible(False)

    def RegisterButtonEvents(self, pathDict):
        """注册按钮交互事件

        Args:
            pathDict (iterable): button 所在的 slot 集合
        """
        if self.alreadyRegisterEvent:
            return
        for path in pathDict:
            buttonPath = path + "/item_button"
            buttonControl = self.GetBaseUIControl(buttonPath).asButton()
            buttonControl.AddTouchEventParams({"isSwallow": True})
            buttonControl.SetButtonTouchDownCallback(self._OnButtonTouchDown)
            buttonControl.SetButtonTouchUpCallback(self._OnButtonTouchUp)
            buttonControl.SetButtonTouchCancelCallback(
                self._OnButtonTouchCancel)
            buttonControl.SetButtonTouchMoveCallback(self._OnButtonTouchMove)
            buttonControl.SetButtonTouchMoveInCallback(
                self._OnButtonTouchMoveIn)
            buttonControl.SetButtonTouchMoveOutCallback(
                self._OnButtonTouchMoveOut)
        self.alreadyRegisterEvent = True

    def __RegisterStateMachine(self):
        logger.debug("RegisterStateMachine")
        """注册按钮状态节点以及转换条件
        """
        # 注册状态节点
        self.containerStateMachine.AddNode(NodeId.Idle, self.__HandleIdle, None,
                                           True)
        self.containerStateMachine.AddNode(NodeId.SelectSlot,
                                           self.__HandleSelected)
        self.containerStateMachine.AddNode(NodeId.UnSelectSlot,
                                           self.__HandleUnSelected)
        self.containerStateMachine.AddNode(NodeId.Swap, self.HandleSwap)
        self.containerStateMachine.AddNode(NodeId.DropAll, self.__HandleDropAll)
        self.containerStateMachine.AddNode(NodeId.TouchProgressiveSelect,
                                           self.__HandleTouchProgressiveSelect)
        self.containerStateMachine.AddNode(
            NodeId.TouchProgressiveSelectComplete,
            self.__HandleTouchProgressiveComplete)
        self.containerStateMachine.AddNode(NodeId.TouchProgressiveSelectCancel,
                                           self.__HandleTouchProgressiveCancel)
        self.containerStateMachine.AddNode(NodeId.Coalesce, self.HandleCoalesce)
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

    def __SetDurabilityBar(self, path, item):
        """设置目标 slot 耐久度 UI

        Args:
            path (str): slot 路径
            item (dict): 玩家背包单个物品信息字典
        """
        durabilityRatio = self.__CalculateDurabilityRatio(item)
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

    def __CalculateDurabilityRatio(self, itemDict):
        """计算物品耐久度比例，用于显示耐久度槽

        Args:
            itemDict (dict): 单个物品信息字典

        Returns:
            float: 耐久度比值
        """
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("itemName", ""),
                                              itemDict.get("auxValue", 0))
        if basicInfo:
            currentDurability = itemDict.get("durability")
            if currentDurability is None:
                return 1
            maxDurability = basicInfo.get("maxDurability", 0)
            if maxDurability != 0:
                return currentDurability * 1.0 / maxDurability
        return 1

    def __CalculateProgressiveRatio(self, itemDict):
        """计算长按状态下分堆比例

        Args:
            itemDict (dict): 单个物品信息字典
        """
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

    def _ShowItemDetail(self, item):
        """显示物品详细信息 UI

        Args:
            item (dict): 单个物品信息字典
        """
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        detailText = itemComp.GetItemFormattedHoverText(item["itemName"],
                                                        item["auxValue"], True,
                                                        item.get("userData"))
        self.itemDetailTextControl.SetText(detailText)
        self.itemDetailBgControl.SetPosition((0, 50))
        self.detailAlpha = 2.0

    def __OnDetailShow(self):
        """绑定 json 的 itemDetailAlpha 与 UI 中的 detailAlpha

        Returns:
            float: 详细信息面板的 alpha 值
        """
        if self.detailAlpha > 1:
            self.itemDetailBgControl.SetAlpha(1)
            self.itemDetailTextControl.SetAlpha(1)
        else:
            self.itemDetailBgControl.SetAlpha(self.detailAlpha)
            self.itemDetailTextControl.SetAlpha(self.detailAlpha)

    def _OnButtonTouchDown(self, args):
        """按钮按下事件: 展示详细信息，判断是否双击，获取最后点击的按钮 path 与 position

        Args:
            args (dict): buttonControl 传入的事件
        """
        touchPos = args["TouchPosX"], args["TouchPosY"]
        buttonPath = args["ButtonPath"]
        slotPath = buttonPath.replace("/item_button", "")
        self.lastTouchButtonPath = args["ButtonPath"]
        self.lastTouchPosition = touchPos
        item = self.GetItemByPath(slotPath)
        if item:
            self._ShowItemDetail(item)
        if self.clickInterval > 0 and self.lastTouchButtonPath == args[
                "ButtonPath"]:
            self.isDoubleClick = True
            return
        self.isDoubleClick = False
        self.heldTime = 0

    def _OnButtonTouchUp(self, args):
        """按钮弹起事件: 双击，长按，普通弹起，交由 containerStateMachine 处理

        Args:
            args (dict): buttonControl 传入事件
        """
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

    def _OnButtonTouchCancel(self, args):
        """按钮取消事件: 长按时间归零

        Args:
            args (dict): buttonControl 传入事件
        """
        self.heldTime = None
        self.__OnTouchCancel()

    def _OnButtonTouchMove(self, args):
        """按钮移走事件

        Args:
            args (dict): buttonControl 传入事件
        """
        self.__OnTouchCancel()

    def _OnButtonTouchMoveIn(self, args):
        """按钮移入事件: 不做处理

        Args:
            args (dict): buttonControl 传入事件
        """
        pass

    def _OnButtonTouchMoveOut(self, args):
        """按钮移入出事件：按钮 release

        Args:
            args (dict): buttonControl 传入事件
        """
        self.heldTime = None
        self.containerStateMachine.ReceiveEvent(self.lastTouchButtonPath,
                                                ButtonEventType.Released)

    def __OnTouchCancel(self):
        """传入取消按下事件"""
        self.containerStateMachine.ReceiveEvent(None, ButtonEventType.Released)

    def __HandleIdle(self, buttonPath):
        """处理默认按钮: 基础属性重置，不显示特殊图片

        Args:
            buttonPath (_type_): _description_
        """
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
        """处理选中按钮: 显示选中图片

        Args:
            buttonPath (str): 按钮路径
        """
        self.lastSelectedPath = buttonPath.replace("/item_button", "")
        self.GetBaseUIControl(self.lastSelectedPath +
                              "/selected_image").SetVisible(True)

    def __HandleUnSelected(self, buttonPath):
        """处理未被选中: 状态重置

        Args:
            buttonPath (str): 按钮路径
        """
        self.containerStateMachine.ResetToDefault()

    def HandleSwap(self, buttonPath):
        """处理物品交换: 向服务端传入 ItemSwapClientEvent 事件及相关数据

        Args:
            buttonPath (str): 按钮路径
        """
        if not self.lastSelectedPath:
            logger.error("there is no last selected button, swap failed!!!")
            return
        swapData = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).CreateEventData()
        swapData["blockName"] = self.blockName
        swapData["fromSlot"] = self.GetSlotByPath(self.lastSelectedPath)
        swapData["toSlot"] = self.GetSlotByPath(buttonPath)
        swapData["playerId"] = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).GetPlayerId()
        swapData["fromItem"] = self.GetItemByPath(self.lastSelectedPath)
        swapData["toItem"] = self.GetItemByPath(buttonPath)
        swapData["blockPos"] = self.blockPos
        swapData["dimension"] = self.dimension
        swapData["takePercent"] = self.takePercent
        self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).NotifyToServer(
                modConfig.ItemSwapClientEvent, swapData)
        self.containerStateMachine.ResetToDefault()

    def __HandleDropAll(self, buttonPath):
        # FIXME 无法触发
        """处理物品丢弃: 向服务端传入 ItemDropClientEvent 事件及 相关数据

        Args:
            buttonPath (str): 按钮路径
        """
        if not self.lastSelectedPath:
            logger.error("there is no last selected button, drop failed!!!")
            return
        dropData = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).CreateEventData()
        dropData["blockName"] = self.blockName
        dropData["playerId"] = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).GetPlayerId()
        dropData["blockPos"] = self.blockPos
        dropData["dimension"] = self.dimension
        dropData["slot"] = self.GetSlotByPath(self.lastSelectedPath)
        dropData["item"] = self.GetItemByPath(self.lastSelectedPath)
        self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).NotifyToServer(
                modConfig.ItemDropClientEvent, dropData)
        self.containerStateMachine.ResetToDefault()

    def __HandleTouchProgressiveSelect(self, buttonPath):
        """处理长按按钮

        Args:
            buttonPath (str): 按钮路径
        """
        self.__HandleSelected(buttonPath)
        inventoryPanelPos = self.GetBaseUIControl(
            self.inventoryPanelPath).GetPosition()
        self.progressiveBarControl.SetPosition(
            (self.lastTouchPosition[0] - inventoryPanelPos[0] - 8,
             self.lastTouchPosition[1] - inventoryPanelPos[1] - 4))
        self.progressiveBarControl.SetVisible(True)

    def __HandleTouchProgressiveComplete(self, buttonPath):
        """处理长按按钮分堆结束

        Args:
            buttonPath (str): 按钮路径
        """
        self.heldTime = None

    def __HandleTouchProgressiveCancel(self, buttonPath):
        """处理取消长按后分堆

        Args:
            buttonPath (str): 按钮路径
        """
        self.containerStateMachine.ResetToDefault()

    def HandleCoalesce(self, buttonPath):
        """处理合堆

        Args:
            buttonPath (str): 按钮路径
        """
        if isinstance(self.GetSlotByPath(buttonPath), str):
            # 非背包栏位禁止合堆
            self.containerStateMachine.ResetToDefault()
        itemDict = self.GetItemByPath(buttonPath)
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("itemName", ""),
                                              itemDict.get("auxValue", 0))
        if basicInfo:
            maxStackSize = basicInfo.get("maxStackSize")
            if maxStackSize > 1 and itemDict.get("count") != maxStackSize:
                for path, bagInfo in self.slotData.items():
                    if buttonPath.replace("/item_button",
                                          "") == path or isinstance(
                                              self.GetSlotByPath(path), str):
                        continue
                    item = self.GetItemByPath(path)
                    if itemUtils.IsSameItem(
                            item,
                            itemDict) and item.get("count") != maxStackSize:
                        self.lastSelectedPath = path
                        self.HandleSwap(buttonPath)
        self.GetBaseUIControl(
            buttonPath.replace("/item_button", "") +
            "/selected_image").SetVisible(False)
        self.containerStateMachine.ResetToDefault()

    def __GetSlotPath(self, path):
        """获取 slot 位置

        Args:
            path (str): slot 的子节点路径

        Returns:
            str: slot path
        """
        oriPathList = path.split("/")
        if "slot" in oriPathList[-1]:
            return path
        newPathList = []
        for subPath in oriPathList:
            newPathList.append(subPath)
            if "slot" in subPath:
                break
        slotPath = ("/").join(newPathList)
        return slotPath

    def __SwapItemUI(self, fromPath, toPath, fromItem, toItem):
        """交换物品 UI

        Args:
            fromPath (str): slot path
            toPath (str): slot path
            fromItem (dict): 物品信息
            toItem (dict)): 物品信息
        """
        self.SetSlotUI(fromPath, toItem)
        self.SetSlotUI(toPath, fromItem)

    def __CanSelected(self, buttonPath, buttonEvent):
        """判断是否可选

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否可以被选中
        """
        if not buttonPath:
            return False
        item = self.GetItemByPath(buttonPath)
        if item and buttonEvent == ButtonEventType.Clicked:
            return True
        return False

    def __CanUnSelected(self, buttonPath, buttonEvent):
        """判断不被选中

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否不被选中
        """
        return buttonPath and buttonPath.replace(
            "/item_button", ""
        ) == self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanSwap(self, buttonPath, buttonEvent):
        """判断可以交换

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否可以交换
        """
        return buttonPath and buttonPath.replace(
            "/item_button", ""
        ) != self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanDrop(self, buttonPath, buttonEvent):
        """判断可以丢弃

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否可以丢弃
        """
        return self.lastSelectedPath and buttonEvent == ButtonEventType.Clicked

    def __CanProgressiveSelect(self, buttonPath, buttonEvent):
        """判断可以长按分堆

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否可以长按分堆
        """
        if not buttonPath:
            return False
        itemDict = self.GetItemByPath(buttonPath)
        if not itemDict or buttonEvent != ButtonEventType.Pressed:
            return False
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("itemName", ""),
                                              itemDict.get("auxValue", 0))
        if basicInfo:
            maxStackSize = basicInfo.get("maxStackSize")
            if maxStackSize > 1:
                return True
        return False

    def __CanProgressiveCancel(self, buttonPath, buttonEvent):
        """判断取消长按分堆

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否取消长按分堆
        """
        return not buttonPath and buttonEvent == ButtonEventType.Released

    def __CanProgressiveComplete(self, buttonPath, buttonEvent):
        """判断完成长按分堆

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否完成长按分堆
        """
        return buttonPath and buttonEvent == ButtonEventType.Released

    def __CanCoalesce(self, buttonPath, buttonEvent):
        """判断能否合并

        Args:
            buttonPath (str): 按钮路径
            buttonEvent (int): ButtonEventType

        Returns:
            bool: 是否能否合并
        """
        return buttonEvent == ButtonEventType.DoubleClick

    @abstractmethod
    def InitWorkbenchUI(self, args):
        """初始化工作台的合成逻辑 UI

        Args:
            args (dict): 暂无
        """
        pass

    @abstractmethod
    def ShowUI(self, args):
        """子类显示 UI 函数

        Args:
            args (dict): 事件数据
        """
        pass

    @abstractmethod
    def UpdateWorkbenchUI(self, event):
        """工作台界面更新

        Args:
            event (dict): 包含 blockName,modConfig.WorkbenchData,stateData 三个键盘
        """
        pass
