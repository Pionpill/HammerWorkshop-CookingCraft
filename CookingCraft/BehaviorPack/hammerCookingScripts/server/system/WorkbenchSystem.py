import copy
from abc import abstractmethod

import mod.server.extraServerApi as serverApi
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.common.utils import itemUtils, workbenchUtils
from hammerCookingScripts.server.controller import WorkbenchController
from hammerCookingScripts.server.factory import WorkbenchFactory
from hammerCookingScripts.server.utils import serverBlockUtils as blockUtils
from hammerCookingScripts.server.utils import serverItemUtils

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()


class InventoryServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenWorkbenchEvent()
        self.levelId = serverApi.GetLevelId()

    def ListenWorkbenchEvent(self):
        engineNamespace = serverApi.GetEngineNamespace()
        engineSystemName = serverApi.GetEngineSystemName()
        # ============================== 监听服务端事件 ==============================
        self.ListenForEvent(engineNamespace, engineSystemName,
                            'ServerBlockUseEvent', self, self.OnServerBlockUse)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            'ServerItemUseOnEvent', self,
                            self.OnServerItemUseOn)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            'ActorAcquiredItemServerEvent', self,
                            self.OnActorAcquiredItemServer)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            'ServerPlayerTryDestroyBlockEvent', self,
                            self.OnServerPlayerTryDestroyBlock)
        self.ListenForEvent(engineNamespace, engineSystemName, 'PlayerDieEvent',
                            self, self.OnPlayerDieServer)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ServerBlockEntityTickEvent", self,
                            self.OnBlockEntityTick)
        # ============================== 监听客户端事件 ==============================
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.ItemSwapClientEvent, self,
                            self.OnItemSwap)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.ItemDropClientEvent, self,
                            self.OnItemDrop)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.CloseInventoryEvent, self,
                            self.OnCloseWorkbenchUI)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.CloseCraftingTableEvent, self,
                            self.OnCloseCraftingTableUI)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.OutSlotClickEvent, self,
                            self.OnResultSlotClick)

    def OnServerBlockUse(self, event):
        # type: (dict) -> None
        """工作台使用回调函数"""
        blockName, playerId = event['blockName'], event["playerId"]
        pos = (event['x'], event['y'], event['z'])
        dimensionId = event['dimensionId']

        if not workbenchUtils.IsWorkbenchBlock(
                blockName) or WorkbenchController.IsPlayerOpeningBlock(
                    playerId):
            return

        workbenchData = WorkbenchController.FormWorkbenchData(
            blockName, pos, dimensionId, self.levelId)
        WorkbenchController.SetCurOpenedBlock(playerId, blockName, pos,
                                              dimensionId)

        self.NotifyToClient(playerId, modConfig.WorkbenchOpenEvent,
                            workbenchData)
        self.__UpdateWorkbenchUI(playerId, blockName, pos, dimensionId)
        self.__UpdateInventoryUI(playerId, blockName)

    def OnServerItemUseOn(self, args):
        # type: (dict) -> None
        """使用物品
        如果是自定义工作台: 拦截使用物品"""
        pos = (args["x"], args["y"], args["z"])
        blockDict = blockUtils.GetBlockInfo(pos, self.levelId)
        if workbenchUtils.IsWorkbenchBlock(blockDict["name"]):
            args["ret"] = True

    def OnActorAcquiredItemServer(self, event):
        # sourcery skip: use-named-expression
        # type: (dict) -> None
        """
        获取新物品时
        如果正打开自定义工作台: 需要更新背包界面"""
        playerId = event["actor"]
        blockInfo = WorkbenchController.GetCurOpenedBlockInfo(playerId)
        if blockInfo:
            blockName = blockInfo.get("blockName")
            self.__UpdateInventoryUI(playerId, blockName)

    def OnServerPlayerTryDestroyBlock(self, args):
        # type: (dict) -> None
        """工作台被破坏，如果工作台上有物品
        1. 需要掉落
        2. 删除使用工作台状态
        3. 客户端: 关闭 UI
        """
        blockName = args["fullName"]
        if not workbenchUtils.IsWorkbenchBlock(blockName):
            return
        pos = (args["x"], args["y"], args["z"])
        playerId = args['playerId']
        dimensionId = args["dimensionId"]
        workbenchSlotData = blockUtils.GetBlockEntityData(
            pos, dimensionId, playerId)
        if not workbenchSlotData:
            return
        itemComp = compFactory.CreateItem(self.levelId)
        for itemDict in workbenchSlotData.values():
            if itemDict:
                itemComp.SpawnItemToLevel(itemDict, dimensionId, pos)
        WorkbenchController.DeleteCurOpenedBlock(playerId)
        # 如果当前该方块的ui被打开需要关闭
        if WorkbenchController.IsPositionBlockUsing(pos, dimensionId):
            eventData = {"blockName": blockName}
            self.NotifyToClient(playerId, modConfig.UIShouldCloseEvent,
                                eventData)

    def OnPlayerDieServer(self, args):  # sourcery skip: use-named-expression
        # type: (dict) -> None
        """玩家死亡，如果正打开工作台
        1. 客户端: 关闭 UI
        2. 删除使用工作台状态
        """
        playerId = args["id"]
        blockInfo = WorkbenchController.GetCurOpenedBlockInfo(playerId)
        if blockInfo:
            eventData = {"blockName": blockInfo.get("blockName")}
            self.NotifyToClient(playerId, modConfig.UIShouldCloseEvent,
                                eventData)
        WorkbenchController.DeleteCurOpenedBlock(playerId)

    def OnBlockEntityTick(self, args):
        # type: (dict) -> None
        """
        自定义工作台 tick
        1. 获取相应的管理类
        2. 执行管理类的 Tick
        3. 根据 Tick 返回值决定是否要更新客户端 UI
        """
        blockName = args["blockName"]
        if blockName not in modConfig.WorkbenchBlocks:
            return
        pos = (args["posX"], args["posY"], args["posZ"])
        dimensionId = args["dimensionId"]
        WBManager = self.__DoGetNewWorkbenchManager(blockName, pos, dimensionId)
        if WBManager.Tick():
            self.__DoUpdateUI(blockName, pos, dimensionId)

    def __DoGetNewWorkbenchManager(self, blockName, pos, dimensionId):
        # type: (str, tuple, int) -> manager
        """尝试获取一个新的 manager，如果不存在，则创建并初始化槽数据"""
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey, blockName)
        if not WBManager.IsDataInit():
            blockEntityData = blockUtils.GetBlockEntityData(
                pos, dimensionId, self.levelId)
            WBManager.DataInit(blockEntityData)
        return WBManager

    def __DoUpdateUI(self, blockName, pos, dimensionId):
        # type: (str, tuple, int) -> None
        """管理类的 UI 界面有动画需要进行 tick"""
        self.__UpdateBlockEntitySlotData(pos, dimensionId, blockName)
        if not WorkbenchController.IsPositionBlockUsing(pos, dimensionId):
            return
        # 如果当前ui界面打开则通知客户端更新UI
        for playerId in WorkbenchController.GetOpeningPlayerList():
            if WorkbenchController.IsPositionBlockUsing(pos, dimensionId):
                self.__UpdateWorkbenchUI(playerId, blockName, pos, dimensionId)
                break

    def OnItemSwap(self, itemSwapData):
        # type: (dict) -> None
        """物品交换"""
        fromSlot, toSlot = itemSwapData["fromSlot"], itemSwapData["toSlot"]
        fromItem, toItem = itemSwapData["fromItem"], itemSwapData["toItem"]
        takePercent = itemSwapData["takePercent"]
        playerId, blockName = itemSwapData["playerId"], itemSwapData[
            "blockName"]
        logger.info("Try swap [{0}] to [{1}]".format(fromSlot, toSlot))
        self.__DoHandleItemSwapData(fromSlot, fromItem, toSlot, toItem,
                                    takePercent, playerId)
        if isinstance(fromSlot, str) or isinstance(toSlot, str):
            if not self.__DoWorkbenchItemSwap(blockName, playerId, fromSlot,
                                              fromItem, toSlot, toItem):
                return
            self.__UpdateWorkbenchUI(playerId, blockName, itemSwapData["pos"],
                                     itemSwapData["dimensionId"])
        else:
            itemComp = compFactory.CreateItem(playerId)
            itemComp.SetInvItemExchange(fromSlot, toSlot)
        itemSwapData["fromItem"] = fromItem
        itemSwapData["toItem"] = toItem
        self.NotifyToClient(playerId, modConfig.ItemSwapServerEvent,
                            itemSwapData)

    def __DoHandleItemSwapData(self, fromSlot, fromItem, toSlot, toItem,
                               takePercent, playerId):
        """处理物品交换逻辑并修正一些数据"""
        # type: (int/str, dict, int/str, dict, float, int) -> None
        """处理交换物品的数据"""
        if isinstance(toSlot, int):
            toItem = serverItemUtils.GetPlayerInventoryItem(playerId, toSlot)
        if isinstance(fromSlot, int):
            fromItem = serverItemUtils.GetPlayerInventoryItem(playerId, toSlot)
        if itemUtils.IsSameItem(fromItem, toItem):
            self.__DoHandleSameItemSwapData(fromSlot, fromItem, toSlot, toItem,
                                            takePercent, playerId)
        if takePercent < 1 and not toItem:
            self.__DoHandlePercentItemSwapData(fromSlot, fromItem, toSlot,
                                               toItem, takePercent, playerId)

    def __DoHandleSameItemSwapData(self, fromSlot, fromItem, toSlot, toItem,
                                   takePercent, playerId):
        # type (int/str, dict, int/str, dict, float, int) -> None
        """处理相同物品交换逻辑"""
        itemComp = compFactory.CreateItem(playerId)
        basicInfo = itemComp.GetItemBasicInfo(toItem.get("newItemName"),
                                              toItem.get("newAuxValue"))
        if not basicInfo:
            return
        maxStackSize = basicInfo.get("maxStackSize")
        takeNum = int(fromItem.get("count") * takePercent)
        fromNum, toNum = fromItem.get("count"), toItem.get("count")
        if not takeNum and not toNum:
            return
        if toNum == maxStackSize:
            return
        if toNum + takeNum >= maxStackSize:
            fromNum -= maxStackSize - toNum
            toNum = maxStackSize
        else:
            toNum += takeNum
            fromNum -= takeNum
        fromItem["count"] = toNum
        toItem["count"] = fromNum
        if fromNum == 0:
            toItem = None
        if isinstance(fromSlot, int):
            itemComp.SetInvItemNum(fromSlot, toNum)
        if isinstance(toSlot, int):
            itemComp.SetInvItemNum(toSlot, fromNum)

    def __DoHandlePercentItemSwapData(self, fromSlot, fromItem, toSlot, toItem,
                                      takePercent, playerId):
        # type (int/str, dict, int/str, dict, float, int) -> None
        """处理部分物品交换逻辑"""
        itemComp = compFactory.CreateItem(playerId)
        toNum = int(fromItem.get("count") * takePercent)
        fromNum = int(fromItem.get("count")) - toNum
        fromItem["count"] = toNum
        toItem = copy.deepcopy(fromItem)
        toItem["count"] = fromNum
        if isinstance(toSlot, int):
            itemComp.SpawnItemToPlayerInv(toItem, playerId, toSlot)
        if isinstance(fromSlot, int):
            itemComp.SpawnItemToPlayerInv(fromItem, playerId, fromSlot)

    def __DoWorkbenchItemSwap(self, blockName, playerId, fromSlot, fromItem,
                              toSlot, toItem):
        # type: (str, int, str|int, dict, str|int, dict) -> bool
        """工作台物品交换，如果交换失败，返回 False"""
        blockInfo = WorkbenchController.GetCurOpenedBlockInfo(playerId)
        if not blockInfo:
            logger.error("Get opened block key error!")
            return False
        pos, dimensionId = blockInfo["pos"], blockInfo["dimensionId"]
        blockKey = pos + (dimensionId, )
        # 工作台内部物品交换
        if isinstance(fromSlot, str) and isinstance(toSlot, str):
            if not self.__DoWorkbenchInnerItemSwap(
                    self, fromSlot, fromItem, toSlot, toItem, pos, dimensionId):
                return False
        # 工作台与物品栏交换
        elif isinstance(fromSlot, str) or isinstance(toSlot, str):
            if not self.__DoWorkbenchOuterItemSwap(
                    self, fromSlot, fromItem, toSlot, toItem, pos, dimensionId,
                    playerId):
                return False
        if blockName in modConfig.CraftingBlock:
            self.__MatchCraftingRecipe(playerId, blockName, dimensionId, pos)
        return True

    def __DoWorkbenchOuterItemSwap(self, fromSlot, fromItem, toSlot, toItem,
                                   pos, dimensionId, playerId):
        # type: (str|int, dict, str|int, dict, tuple, int, int) -> bool
        """工作台与背包物品交换"""
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey)
        if not WBManager.CanSlotSet(toSlot):
            return False
        itemComp = compFactory.CreateItem(playerId)
        blockEntityData = blockUtils.GetBlockEntityData(pos, dimensionId,
                                                        self.levelId)
        # 从工作台取出物品到背包
        if isinstance(toSlot, int):
            # 从生成槽获取物品
            if not WBManager.CanSlotSet(fromSlot):
                # 从生成槽取出物品时，只能在目标槽位为空时才可以取出
                if toItem and not itemUtils.IsSameItem(fromItem, toItem):
                    return False
                newWorkbenchItems = WBManager.MatchRecipe()
                for slotName, slotItem in newWorkbenchItems.items():
                    blockEntityData[slotName] = slotItem
            else:
                WBManager.UpdateItemData(fromSlot, toItem)
                blockEntityData[fromSlot] = toItem
            itemComp.SpawnItemToPlayerInv(fromItem, playerId, toSlot)
        else:
            WBManager.UpdateItemData(toSlot, fromItem)
            blockEntityData[toSlot] = fromItem
            if toItem:
                itemComp.SpawnItemToPlayerInv(toItem, playerId, fromSlot)
            else:
                itemComp.SetInvItemNum(fromSlot, 0)
        return True

    def __DoWorkbenchInnerItemSwap(self, fromSlot, fromItem, toSlot, toItem,
                                   pos, dimensionId):
        # type: (str, dict, str, dict, tuple, int) -> bool
        """工作台内部物品交换"""
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey)
        # 原材料与生成物不能交换
        if not WBManager.CanSlotSet(fromSlot, toSlot):
            return False
        WBManager.UpdateItemData(toSlot, fromItem)
        WBManager.UpdateItemData(fromSlot, toItem)
        self.__UpdateBlockEntitySlotData(pos, dimensionId)
        return True

    def OnItemDrop(self, args):
        # type: (dict) -> None
        """丢弃物品"""
        item = args["item"]
        slot = args["slot"]
        playerId = args["playerId"]
        logger.info("Try drop item in slot[{0}]".format(slot))
        # 丢弃背包物品
        itemComp = compFactory.CreateItem(playerId)
        if isinstance(slot,
                      str) and not self.__DoWorkbenchItemDrop(playerId, slot):
            return
        itemComp.SetInvItemNum(slot, 0)
        dimensionId = args["dimensionId"]
        pos = args["pos"]
        itemComp.SpawnItemToLevel(item, dimensionId, pos)
        self.NotifyToClient(playerId, modConfig.ItemDropServerEvent, args)

    def __DoWorkbenchItemDrop(self, playerId, slotName):
        blockInfo = WorkbenchController.GetCurOpenedBlockInfo(playerId)
        if not blockInfo:
            logger.error("Get opened block key error!")
        pos = blockInfo.get("pos")
        dimensionId = blockInfo.get("dimensionId")
        blockKey = pos + (dimensionId, )
        blockEntityData = blockUtils.GetBlockEntityData(pos, dimensionId,
                                                        self.levelId)
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey)
        WBManager.UpdateItemData(slotName, None)
        blockEntityData[slotName] = None

    def OnCloseWorkbenchUI(self, args):
        playerId = args["playerId"]
        WorkbenchController.DeleteCurOpenedBlock(playerId)

    def __UpdateInventoryUI(self, playerId, blockName):
        # type: (int, str) -> None
        """更新背包槽UI: 收集背包数据并传入客户端，让客户端更新 UI 中的 Inventory 面板"""
        inventoryData = WorkbenchController.FormInventoryData(
            playerId, blockName)
        self.NotifyToClient(playerId, modConfig.InventoryChangedEvent,
                            inventoryData)

    def __UpdateWorkbenchUI(self, playerId, blockName, pos, dimensionId):
        # type: (int, str, tuple, int) -> None
        """更新客户端 UI 界面，收集数据并向客户端传递 modConfig.WorkbenchChangedEvent 事件"""
        if workbenchUtils.IsCraftingBlock(blockName):
            workbenchData = WorkbenchController.FormWorkbenchData(
                blockName, pos, dimensionId, self.levelId)
            self.NotifyToClient(playerId, modConfig.WorkbenchChangedEvent,
                                workbenchData)
        elif workbenchUtils.IsFurnaceBlock(blockName):
            workbenchData = WorkbenchController.FormFurnaceData(
                blockName, pos, dimensionId, self.levelId)
            self.NotifyToClient(playerId, modConfig.WorkbenchChangedEvent,
                                workbenchData)

    def OnCloseCraftingTableUI(self, args):
        # type: (dict) -> None
        """
        关闭工作台界面
        1. 将工作台物品返回给玩家
        2. 清空工作台UI界面的物品
        """
        pos, dimensionId = args["pos"], args["dimensionId"]
        playerId, blockName = args["playerId"], args["blockName"]
        # 将物品返回给玩家，重置工作台内容
        self.__DoResetCraftingTable(self, blockName, pos, dimensionId, playerId)
        # UI 界面删除工作台物品
        self.__UpdateWorkbenchUI(playerId, blockName, pos, dimensionId)

    def __DoResetCraftingTable(self, blockName, pos, dimensionId, playerId):
        # type: (str,tuple,int,int) -> None
        """
        重置工作台
        1. 重置管理类
        2. 掉落管理类中的原材料
        3. 重置blockEntityData数据
        """
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey, blockName)
        materialsItems = WBManager.Reset()
        itemComp = compFactory.CreateItem(playerId)
        for materialItem in materialsItems.values():
            if materialItem is not None:
                itemComp.SpawnItemToPlayerInv(materialItem, playerId)
        self.__UpdateBlockEntitySlotData(pos, dimensionId, blockName)

    def OnResultSlotClick(self, event):  # sourcery skip: use-named-expression
        # type: (dict) -> dict
        """
        点击结果槽(快捷获取生成物)
        1. 更新 block 数据
        2. 更新背包槽 UI 数据
        3. 工作台适配新的配方
        """
        playerId, pos = event["playerId"], event["pos"]
        dimensionId = event["dimensionId"]
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey, blockName)
        WBManager.Produce()
        self.__UpdateBlockEntitySlotData(pos, dimensionId, blockName)

        itemComp = compFactory.CreateItem(playerId)
        itemComp.SpawnItemToPlayerInv(event["item"], playerId)
        blockInfo = WorkbenchController.GetCurOpenedBlockInfo(playerId)
        if blockInfo:
            blockName = blockInfo.get("blockName")
            self.__UpdateInventoryUI(playerId, blockName)
        self.__MatchCraftingRecipe(playerId, blockName, dimensionId, pos)

    def __UpdateBlockEntitySlotData(self, pos, dimensionId, blockName=None):
        # type: (tuple, int, str) -> None
        """根据管理类更新 blockEntity 的槽数据"""
        # sourcery skip: use-named-expression
        blockKey = pos + (dimensionId, )
        WBManager = WorkbenchFactory.GetWorkbenchManager(blockKey, blockName)
        newSlotData = WBManager.ConvertToBlockEntityData()
        blockEntityData = blockUtils.GetBlockEntityData(pos, dimensionId,
                                                        self.levelId)
        for slotName in blockEntityData.keys():
            newItemDict = newSlotData.get(slotName)
            if newItemDict:
                blockEntityData[slotName] = newItemDict

    def __MatchCraftingRecipe(self, playerId, blockName, dimensionId, pos):
        # type: (int, str, int, tuple, dict) -> None
        """匹配工作台配方，如果能合成新的产品，向客户端发送事件"""
        WBManager = WorkbenchFactory.GetWorkbenchManager(
            pos + (dimensionId, ), blockName)
        resultsItems = WBManager.MatchRecipe(self)
        if not resultsItems:
            return
        gameComp = compFactory.CreateGame(serverApi.GetLevelId())
        gameComp.AddTimer(0.01, self.__UpdateWorkbenchUI, playerId, blockName,
                          pos, dimensionId)
