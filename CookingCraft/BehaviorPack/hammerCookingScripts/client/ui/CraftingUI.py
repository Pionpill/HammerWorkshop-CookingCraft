'''
Description: 工作台具有几下结构
|- main
    |- crafting_panel
        |- crafting_slot0
        |- crafting_slot1
        |- ......
        |- crafting_slot9
        |- arrow_image
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-01 12:20:36
LastEditTime: 2022-07-17 00:06:46
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts.client.ui.InventoryUI import InventoryUI
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.utils import itemUtils
from hammerCookingScripts import logger

compFactory = clientApi.GetEngineCompFactory()


class CraftingUI(InventoryUI):
    def __init__(self, namespace, name, param):
        InventoryUI.__init__(self, namespace, name, param)
        self.craftingPanelPath = "/crafting_panel"
        self.materialSlotNames = []
        self.outSlotNames = []

    def Create(self):
        InventoryUI.Create(self)

    def Destroy(self):
        InventoryUI.Destroy(self)

    def Update(self):
        InventoryUI.Update(self)

    def ShowCraftingUI(self, args):
        InventoryUI.ShowInventoryUI(self, args)

    def OnCloseBthClicked(self, event):
        """CraftingTable 关闭界面时需要返回物品到背包栏

        Args:
            event (dict): 回调函数事件信息
        """
        clientSystem = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench)
        eventData = clientSystem.CreateEventData()
        eventData["playerId"] = clientSystem.GetPlayerId()
        clientSystem.NotifyToServer(modConfig.CloseInventoryEvent, eventData)
        # 返回物品
        eventData = clientSystem.CreateEventData()
        eventData["blockPos"] = self.blockPos
        eventData["dimension"] = self.dimension
        eventData["playerId"] = clientSystem.GetPlayerId()
        eventData["blockName"] = self.blockName
        clientSystem.NotifyToServer(modConfig.CloseCraftingTableEvent,
                                    eventData)
        # 延迟 0.1s 关闭界面
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(0.1, self.CloseUI)

    def HandleCoalesce(self, buttonPath):
        """处理合堆：CraftingTable 的原料槽应该也允许合堆

        Args:
            buttonPath (str): 按钮路径
        """
        slotName = self.GetSlotByPath(buttonPath)
        if isinstance(slotName, str) and slotName not in self.materialSlotNames:
            self.containerStateMachine.ResetToDefault()
        itemDict = self.GetItemByPath(buttonPath)
        itemComp = compFactory.CreateItem(clientApi.GetLevelId())
        basicInfo = itemComp.GetItemBasicInfo(itemDict.get("itemName", ""),
                                              itemDict.get("auxValue", 0))
        if basicInfo:
            maxStackSize = basicInfo.get("maxStackSize")
            if maxStackSize > 1 and itemDict.get("count") != maxStackSize:
                for path, bagInfo in self.slotData.items():
                    if buttonPath.replace(
                            "/item_button",
                            "") == path or "crafting_slot9" in path:
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

    def RegisterButtonEvents(self, pathDict):
        """按钮交互式事件重写，输出槽点击后直接返回到背包，无需交换

        Args:
            pathDict (iterable): 所有 button 所在的 slot 集合
        """
        if self.alreadyRegisterEvent:
            return
        outSlotList = []
        for slotPath in pathDict:
            for outSlotName in self.outSlotNames:
                if outSlotName in slotPath:
                    outSlotList.append(slotPath)
                    continue
            buttonPath = slotPath + "/item_button"
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
        self.RegisterOutButtonEvents(outSlotList)
        self.alreadyRegisterEvent = True

    def RegisterOutButtonEvents(self, slotPathList):
        """合成台的输出槽应该直接点击获取
        """
        for slotPath in slotPathList:
            buttonPath = slotPath + "/item_button"
            buttonControl = self.GetBaseUIControl(buttonPath).asButton()
            buttonControl.AddTouchEventParams({"isSwallow": True})
            buttonControl.SetButtonTouchDownCallback(
                self.__OnOutButtonTouchDown)

    def __OnOutButtonTouchDown(self, args):
        """输出按钮按下事件: 返回物品到背包，清空输出槽

        Args:
            args (dict): 按钮事件
        """
        touchPos = args["TouchPosX"], args["TouchPosY"]
        buttonPath = args["ButtonPath"]
        slotPath = buttonPath.replace("/item_button", "")
        self.lastTouchButtonPath = args["ButtonPath"]
        self.lastTouchPosition = touchPos
        item = self.GetItemByPath(slotPath)
        if item:
            self._ShowItemDetail(item)
        self.isDoubleClick = False

        eventData = {}
        eventData["item"] = self.GetItemByPath(slotPath)
        eventData["blockPos"] = self.blockPos
        eventData["dimension"] = self.dimension
        eventData["playerId"] = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).GetPlayerId()
        self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench).NotifyToServer(
                modConfig.OutSlotClickEvent, eventData)
        self.SetSlotUI(slotPath, None)
