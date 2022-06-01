'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 16:15:57
LastEditTime: 2022-05-28 16:15:48
'''
from abc import abstractmethod
import mod.server.extraServerApi as serverApi
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
from hammerCookingScripts.common.commonUtils import itemUtils

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()


class InventoryServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenInventoryEvent()
        # key:playerId value:blockName blockPos dimension
        self.curOpenedBlock = {}
        self.levelId = serverApi.GetLevelId()

    def ListenInventoryEvent(self):
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
                            self.OnPlayerTryDestroyBlockServer)
        self.ListenForEvent(engineNamespace, engineSystemName, 'PlayerDieEvent',
                            self, self.OnPlayerDieServer)
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
                            self.CloseInventoryContainer)

    def OnServerBlockUse(self, event):
        """工作台使用回调函数: 注册正在使用的工作台，向客户端传送 InventoryOpenEvent 事件，更新背包槽UI

        Args:
            event (dict): 事件数据
        """
        blockName = event['blockName']
        blockPos = (event['x'], event['y'], event['z'])
        playerId = event["playerId"]
        dimension = compFactory.CreateDimension(playerId).GetPlayerDimensionId()
        if blockName in modConfig.InventoryContainerBlocks and not self.curOpenedBlock.get(
                playerId):
            event["workbenchData"] = self.GetWorkbenchItems(
                dimension, blockName, blockPos)
            self.__SetCurOpenedBlock(event)
            eventData = self.CreateEventData()
            eventData["blockName"] = blockName
            eventData["blockPos"] = blockPos
            eventData["dimension"] = dimension
            eventData[modConfig.WorkbenchData] = self.GetWorkbenchItems(
                dimension, blockName, blockPos)
            self.NotifyToClient(playerId, modConfig.InventoryOpenEvent,
                                eventData)
            self.UpdateWorkbench(playerId, blockPos, dimension)
            self._UpdateBagUI(playerId, blockName)

    def OnServerItemUseOn(self, args):
        """自定义工作台拦截，防止误操作放置东西

        Args:
            args (dict): 事件数据
        """
        playerId = args["entityId"]
        x = args["x"]
        y = args["y"]
        z = args["z"]
        blockComp = compFactory.CreateBlockInfo(playerId)
        blockDict = blockComp.GetBlockNew((x, y, z))
        if blockDict["name"] in modConfig.InventoryContainerBlocks:
            args["ret"] = True

    def OnActorAcquiredItemServer(self, event):
        """玩家获取新物品时，需要更新 UI 界面

        Args:
            event (dict): 事件数据
        """
        playerId = event["actor"]
        blockInfo = self.GetBlockInfoByPlayerId(playerId)
        if blockInfo:
            blockName = blockInfo.get("blockName")
            self._UpdateBagUI(playerId, blockName)

    def OnPlayerTryDestroyBlockServer(self, args):
        """工作台被破坏，如果有物品则需要掉落或其他处理，需要子类实现抽象方法

        Args:
            args (dict): 事件数据
        """
        blockName = args["fullName"]
        if blockName in modConfig.InventoryContainerBlocks:
            logger.info("Destroy Custom Furnace Block")
            blockPos = (args["x"], args["y"], args["z"])
            playerId = args['playerId']
            dimensionComp = compFactory.CreateDimension(playerId)
            dimension = dimensionComp.GetPlayerDimensionId()
            containerDict = self.GetWorkbenchItems(dimension, blockName,
                                                   blockPos)
            if not isinstance(containerDict, dict):
                logger.info("Block has no item to drop")
                return
            itemComp = compFactory.CreateItem(self.levelId)
            for _, item in containerDict.items():
                if item:
                    res = itemComp.SpawnItemToLevel(item, dimension, blockPos)
                    if not res:
                        logger.error("Spawn Item Error: {0}".format(item))
            self.ResetInventoryContainer(dimension, blockName, blockPos)
            # 如果当前该方块的ui被打开需要关闭
            for openedPlayerId, blockInfo in self.curOpenedBlock.items():
                if blockPos in blockInfo.values(
                ) and dimension in blockInfo.values():
                    eventData = self.CreateEventData()
                    eventData["blockName"] = blockName
                    self.NotifyToClient(openedPlayerId,
                                        modConfig.UIShouldCloseEvent, eventData)
                    break

    def OnPlayerDieServer(self, args):
        """玩家死亡: 关闭 UI，取消注册 curOpenedBlock

        Args:
            args (dict): 事件数据
        """
        playerId = args["id"]
        blockInfo = self.GetBlockInfoByPlayerId(playerId)
        if blockInfo:
            blockName = blockInfo.get("blockName")
            eventData = self.CreateEventData()
            eventData["blockName"] = blockName
            self.NotifyToClient(playerId, modConfig.UIShouldCloseEvent,
                                eventData)
        del self.curOpenedBlock[playerId]

    def OnItemSwap(self, args):
        """物品交换逻辑

        Args:
            args (dict): 服务端发动的交换事件数据
        """
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        fromItem = args["fromItem"]
        toItem = args["toItem"]
        takePercent = args["takePercent"]
        playerId = args["playerId"]
        blockName = args["blockName"]
        logger.info("Try swap [{0}] to [{1}]".format(fromSlot, toSlot))
        itemComp = compFactory.CreateItem(playerId)
        if isinstance(toSlot, int):
            toItem = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY,
                                            toSlot, True)
        if isinstance(fromSlot, int):
            fromItem = itemComp.GetPlayerItem(
                minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        if itemUtils.IsSameItem(fromItem, toItem):
            basicInfo = itemComp.GetItemBasicInfo(toItem.get("itemName"),
                                                  toItem.get("auxValue"))
            if not basicInfo:
                return
            maxStackSize = basicInfo.get("maxStackSize")
            takeNum = int(fromItem.get("count") * takePercent)
            fromNum = fromItem.get("count")
            toNum = toItem.get("count")
            if not takeNum and not toNum:
                logger.error("OnItemSwap Error!!!")
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
        if takePercent < 1 and not toItem:
            toNum = int(fromItem.get("count") * takePercent)
            fromNum = int(fromItem.get("count")) - toNum
            fromItem["count"] = toNum
            import copy
            toItem = copy.deepcopy(fromItem)
            toItem["count"] = fromNum
            if isinstance(toSlot, int):
                itemComp.SpawnItemToPlayerInv(toItem, playerId, toSlot)
            if isinstance(fromSlot, int):
                itemComp.SpawnItemToPlayerInv(fromItem, playerId, fromSlot)
        if isinstance(fromSlot, str) or isinstance(toSlot, str):
            if not self.OnWorkbenchItemSwap(blockName, playerId, fromSlot,
                                            fromItem, toSlot, toItem):
                return
            self.UpdateWorkbench(playerId, args["blockPos"], args["dimension"])
        else:
            itemComp.SetInvItemExchange(fromSlot, toSlot)
        args["fromItem"] = fromItem
        args["toItem"] = toItem
        self.NotifyToClient(playerId, modConfig.ItemSwapServerEvent, args)

    def OnItemDrop(self, args):
        item = args["item"]
        slot = args["slot"]
        playerId = args["playerId"]
        logger.info("Try drop item in slot[{0}]".format(slot))
        # 丢弃背包物品
        itemComp = compFactory.CreateItem(playerId)
        if isinstance(slot, str):
            if not self.OnWorkbenchItemDrop(playerId, slot):
                return
        else:
            itemComp.SetInvItemNum(slot, 0)
        dimension = args["dimension"]
        pos = args["blockPos"]
        itemComp.SpawnItemToLevel(item, dimension, pos)
        self.NotifyToClient(playerId, modConfig.ItemDropServerEvent, args)

    def CloseInventoryContainer(self, args):
        playerId = args["playerId"]
        del self.curOpenedBlock[playerId]

    def _UpdateBagUI(self, playerId, blockName):
        """更新背包UI: 收集背包数据并传入客户端，让客户端更新 UI 中的 Inventory 面板

        Args:
            playerId (int): 用户 id
            blockName (str): modConfig 中的 BlockName
        """
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        eventData = self.CreateEventData()
        eventData["blockName"] = blockName
        eventData[modConfig.InventoryData] = {}
        itemComp = compFactory.CreateItem(playerId)
        for i in range(modConfig.Inventory_Slot_NUM):
            eventData[modConfig.InventoryData][i] = itemComp.GetPlayerItem(
                serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i, True)
        self.NotifyToClient(playerId, modConfig.BagChangedEvent, eventData)

    def __SetCurOpenedBlock(self, args):
        """注册正在使用的工作台

        Args:
            args (dict): 事件数据
        """
        playerId = args["playerId"]
        dimension = compFactory.CreateDimension(playerId).GetPlayerDimensionId()
        self.curOpenedBlock[playerId] = {
            "blockName": args["blockName"],
            "blockPos": (args['x'], args['y'], args['z']),
            "dimension": dimension
        }

    def GetBlockInfoByPlayerId(self, playerId):
        return self.curOpenedBlock.get(playerId)

    @abstractmethod
    def GetWorkbenchItems(self, dimension, blockName, blockPos):
        """
        @description 获取自定义容器中的所有物品，该数据保存在blockEntityData中
        @param dimension int 自定义容器所在维度
        @param blockName str 自定义容器的方块名，即identifier
        @param blockPos tuple 自定义容器的位置信息，格式为(x, y, z)
        @return dict 返回dict，key为槽位名，value为itemDict
        """
        pass

    @abstractmethod
    def ResetInventoryContainer(self, dimension, blockName, blockPos):
        """
        @description 方块被摧毁时需要重置的数据在这里处理
        @param dimension int 自定义容器所在维度
        @param blockName str 自定义容器的方块名，即identifier
        @param blockPos tuple 自定义容器的位置信息，格式为(x, y, z)
        @return dict 返回dict，key为槽位名，value为itemDict
        """
        pass

    @abstractmethod
    def UpdateWorkbench(self, playerId, blockPos, dimension):
        """
        @description 自定义容器内容发生变化或者打开的时候会调用，可在该函数中实现其他初始化，比如通知客户端初始化容器状态。切记不要在该函数中更新自定义容器槽内物品的数据，可能会导致飞行动画异常
        @param playerId str 打开容器的玩家id，用于通知
        @param blockPos tuple 自定义容器的位置信息，格式为(x, y, z)
        @param dimension int 自定义容器所在维度
        """
        pass

    @abstractmethod
    def OnWorkbenchItemSwap(self, blockName, playerId, fromSlot, fromItem,
                            toSlot, toItem):
        """
        @description 当交换的物品涉及自定义容器时调用，需在子类实现，返回True表示允许交换，返回False禁止交换，交换成功时需要更新对应容器方块的blockEntityData
        @param playerId 玩家Id
        @param fromSlot 第一次点击的槽位
        @param fromItem 第一次点击槽位的itemDict
        @param toSlot 第二次点击的槽位
        @param toItem 第二次点击槽位的itemDict
        @return bool True表示交换成功，False表示禁止交换"""
        return False

    @abstractmethod
    def OnWorkbenchItemDrop(self, playerId, slot):
        """
        @description 当丢弃物品涉及自定义容器时调用，需在子类实现，返回True表示允许丢弃，返回False禁止丢弃，丢弃成功时需要更新对应容器方块的blockEntityData
        @param playerId 玩家Id
        @param slot 需要丢弃物品所在的槽位
        @return bool True表示丢弃成功并更新blockEntityData，False表示禁止丢弃
        """
        return False

    @abstractmethod
    def UpdateFurnace(self, playerId, blockPos, dimension):
        return False
