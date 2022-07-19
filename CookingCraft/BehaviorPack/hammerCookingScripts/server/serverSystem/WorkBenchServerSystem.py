'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 15:20:19
LastEditTime: 2022-07-11 14:29:58
'''
# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import time
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import itemUtils
from hammerCookingScripts.server.serverSystem.InventoryServerSystem import InventoryServerSystem
from hammerCookingScripts.server.serverFactory.WorkbenchManagerFactory import WorkbenchManagerFactory

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()


class WorkbenchServerSystem(InventoryServerSystem):
    def __init__(self, namespace, systemName):
        InventoryServerSystem.__init__(self, namespace, systemName)
        logger.info("=== Server System Init ===")
        self.ListenWorkbenchEvent()
        # key: (x, y, z, dimension), value: workbenchManager
        self.workbenchManagerDict = {}

    def ListenWorkbenchEvent(self):
        engineNamespace = serverApi.GetEngineNamespace()
        engineSystemName = serverApi.GetEngineSystemName()
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ServerBlockEntityTickEvent", self,
                            self.OnBlockEntityTick)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.CloseCraftingTableEvent, self,
                            self.OnCloseCraftingTable)
        self.ListenForEvent(modConfig.ModName,
                            modConfig.ClientSystemName_Workbench,
                            modConfig.OutSlotClickEvent, self,
                            self.OnOutSlotClick)

    def OnBlockEntityTick(self, args):
        # 避免频繁输出，易造成卡顿
        blockName = args["blockName"]
        blockPos = (args["posX"], args["posY"], args["posZ"])
        dimension = args["dimension"]
        blockKey = (args["posX"], args["posY"], args["posZ"], args["dimension"])
        # 在这里进行实现自定义熔炉的tick逻辑
        if blockName in modConfig.WorkbenchBlocks:
            # 第一次tick的时候需要从blockEntity获取数据，之后只有数据更新才需要获取blockEntity进行更新
            workbenchMgr = self.workbenchManagerDict.get(blockKey)
            if not workbenchMgr:
                workbenchMgr = WorkbenchManagerFactory.GetWorkbenchManager(
                    blockName)
                blockEntityComp = compFactory.CreateBlockEntityData(
                    self.levelId)
                blockEntityData = blockEntityComp.GetBlockEntityData(
                    args["dimension"],
                    (args["posX"], args["posY"], args["posZ"]))
                furnaceItems = []
                for i in range(
                        0, modConfig.WORKBENCH_SLOT_NUM_DICT.get(blockName, 0)):
                    key = "{0}{1}".format(
                        modConfig.WORKBENCH_SLOT_PREFIX.get(blockName), i)
                    furnaceItems.append(blockEntityData[key])
                workbenchMgr.UpdateBlockData(furnaceItems)
                self.workbenchManagerDict[blockKey] = workbenchMgr
            # tick 当需要更新数据或UI时进入下面流程
            if workbenchMgr.Tick():
                # 更新blockEntity数据
                blockEntityComp = compFactory.CreateBlockEntityData(
                    self.levelId)
                blockEntityData = blockEntityComp.GetBlockEntityData(
                    args["dimension"],
                    (args["posX"], args["posY"], args["posZ"]))
                blockItems = workbenchMgr.GetBlockItems()
                for i in range(
                        0, modConfig.WORKBENCH_SLOT_NUM_DICT.get(blockName, 0)):
                    key = "{0}{1}".format(
                        modConfig.WORKBENCH_SLOT_PREFIX.get(blockName), i)
                    blockEntityData[key] = blockItems[i]
                if not self.curOpenedBlock:
                    return
                # 如果当前ui界面打开则通知客户端更新UI
                for playerId, blockInfo in self.curOpenedBlock.items():
                    if blockPos in blockInfo.values(
                    ) and dimension in blockInfo.values():
                        workbenchData = self.CreateEventData()
                        workbenchData[modConfig.WorkbenchData] = {}
                        for i in range(
                                0,
                                modConfig.WORKBENCH_SLOT_NUM_DICT.get(
                                    blockName, 0)):
                            key = "{0}{1}".format(
                                modConfig.WORKBENCH_SLOT_PREFIX.get(blockName),
                                i)
                            workbenchData[
                                modConfig.WorkbenchData][key] = blockItems[i]
                        workbenchData["blockName"] = blockName
                        workbenchData["stateData"] = workbenchMgr.GetStateData()
                        if blockName in modConfig.FurnaceBlockList:
                            workbenchData["isLit"] = workbenchMgr.IsLit()
                            workbenchData[
                                "litDuration"] = workbenchMgr.GetLitDuration()
                            workbenchData["isCooking"] = workbenchMgr.IsCooking(
                            )
                        self.NotifyToClient(playerId,
                                            modConfig.WorkbenchChangedEvent,
                                            workbenchData)
                        break

    def GetWorkbenchItems(self, dimension, blockName, blockPos):
        """通过 blockEntityData 获取工作台中所有物品

        Args:
            dimension (int): 工作台所在维度
            blockName (str): 工作台名称
            blockPos (tuple): 工作台位置信息

        Returns:
            dict: key : slotName，value : itemDict
        """
        items = {}
        blockEntityComp = compFactory.CreateBlockEntityData(self.levelId)
        blockEntityData = blockEntityComp.GetBlockEntityData(
            dimension, blockPos)
        if blockEntityData:
            for i in range(0,
                           modConfig.WORKBENCH_SLOT_NUM_DICT.get(blockName, 0)):
                key = "{0}{1}".format(
                    modConfig.WORKBENCH_SLOT_PREFIX.get(blockName), i)
                items[key] = blockEntityData[key]
        return items

    def OnCloseCraftingTable(self, args):
        blockPos = args["blockPos"]
        dimension = args["dimension"]
        playerId = args["playerId"]
        blockName = args["blockName"]
        blockKey = (blockPos[0], blockPos[1], blockPos[2], dimension)
        workbenchMgr = self.workbenchManagerDict.get(blockKey)
        itemComp = compFactory.CreateItem(playerId)
        # 将物品返回给玩家，重置工作台内容
        blockEntityComp = compFactory.CreateBlockEntityData(self.levelId)
        blockEntityData = blockEntityComp.GetBlockEntityData(
            dimension, blockPos)
        index = 0
        for craftingItem in workbenchMgr.GetBlockItems():
            # 仅返回原料槽的物品
            if craftingItem is not None and index < workbenchMgr.GetMaterialSlotNum(
            ):
                itemComp.SpawnItemToPlayerInv(craftingItem, playerId)
            blockEntityData["crafting_slot" + str(index)] = None
            index += 1
        workbenchMgr.UpdateBlockData(
            [None, None, None, None, None, None, None, None, None, None])
        # UI 界面删除工作台物品
        eventData = {}
        eventData["blockName"] = blockName
        eventData[modConfig.WorkbenchData] = self.GetWorkbenchItems(
            dimension, blockName, blockPos)
        self.NotifyToClient(playerId, modConfig.WorkbenchChangedEvent,
                            eventData)

    def OnWorkbenchItemSwap(self, blockName, playerId, fromSlot, fromItem,
                            toSlot, toItem):
        blockEntityComp = compFactory.CreateBlockEntityData(self.levelId)
        blockInfo = self.GetBlockInfoByPlayerId(playerId)
        if not blockInfo:
            logger.error("Get opened block key error!")
            return False
        blockEntityData = blockEntityComp.GetBlockEntityData(
            blockInfo.get("dimension"), blockInfo.get("blockPos"))
        blockPos = blockInfo.get("blockPos")
        dimension = blockInfo.get("dimension")
        blockKey = (blockPos[0], blockPos[1], blockPos[2], dimension)
        workbenchMgr = self.workbenchManagerDict.get(blockKey)
        # 工作台内部物品交换
        if isinstance(fromSlot, str) and isinstance(toSlot, str):
            # 原材料与生成物不能交换
            if workbenchMgr.IsOutSlot(fromSlot) or workbenchMgr.IsOutSlot(
                    toSlot):
                return False
            workbenchMgr.UpdateSlotData(toSlot, fromItem)
            blockEntityData[toSlot] = fromItem
            workbenchMgr.UpdateSlotData(fromSlot, toItem)
            blockEntityData[fromSlot] = toItem
        # 工作台与背包物品交换
        elif isinstance(fromSlot, str) or isinstance(toSlot, str):
            itemComp = compFactory.CreateItem(playerId)
            # 屏蔽物品放置到结果槽
            if not workbenchMgr.CanSet(toSlot, fromItem):
                return False
            # 从工作台取出物品到背包
            if isinstance(toSlot, int):
                # 从生成槽获取物品
                if workbenchMgr.IsOutSlot(fromSlot):
                    # 从生成槽取出物品时，只能在目标槽位为空时才可以取出
                    if toItem and not itemUtils.IsSameItem(fromItem, toItem):
                        return False
                    newWorkbenchItems = workbenchMgr.HandleGetResult()
                    for slotName, slotItem in newWorkbenchItems.items():
                        blockEntityData[slotName] = slotItem
                    itemComp.SpawnItemToPlayerInv(fromItem, playerId, toSlot)
                else:
                    workbenchMgr.UpdateSlotData(fromSlot, toItem)
                    blockEntityData[fromSlot] = toItem
                    itemComp.SpawnItemToPlayerInv(fromItem, playerId, toSlot)
            # 从背包放置物品到工作台
            else:
                workbenchMgr.UpdateSlotData(toSlot, fromItem)
                blockEntityData[toSlot] = fromItem
                if toItem:
                    itemComp.SpawnItemToPlayerInv(toItem, playerId, fromSlot)
                else:
                    itemComp.SetInvItemNum(fromSlot, 0)
        if blockName in modConfig.CraftingBlock:
            self.HandleCraftingResult(playerId, blockName, dimension, blockPos,
                                      blockEntityData)
        return True

    def ResetInventoryContainer(self, dimension, blockName, blockPos):
        workbenchKey = (blockPos[0], blockPos[1], blockPos[2], dimension)
        if workbenchKey in self.workbenchManagerDict:
            del self.workbenchManagerDict[workbenchKey]

    def UpdateWorkbench(self, playerId, blockPos, dimension):
        workbenchMgr = self.workbenchManagerDict.get(
            (blockPos[0], blockPos[1], blockPos[2], dimension))
        blockName = workbenchMgr.GetBlockName()
        if workbenchMgr:
            workbenchData = self.CreateEventData()
            workbenchData[modConfig.WorkbenchData] = self.GetWorkbenchItems(
                dimension, blockName, blockPos)
            workbenchData["blockName"] = blockName
            if blockName in modConfig.FurnaceBlockList:
                workbenchData["isLit"] = workbenchMgr.IsLit()
                workbenchData["litDuration"] = workbenchMgr.GetLitDuration()
                workbenchData["isCooking"] = workbenchMgr.IsCooking()
                # 若进入游戏且第一次打开熔炉，需要初始化进度
                if not workbenchMgr.UIInitCondition():
                    workbenchData[
                        "litProgress"] = workbenchMgr.CalculateLitProgress()
                    workbenchData[
                        "burnProgress"] = workbenchMgr.CalculateBurnProgress()
                    workbenchMgr.UIInit()
            self.NotifyToClient(playerId, modConfig.WorkbenchChangedEvent,
                                workbenchData)

    def OnWorkbenchItemDrop(self, playerId, slot):
        blockEntityComp = compFactory.CreateBlockEntityData(self.levelId)
        blockInfo = self.GetBlockInfoByPlayerId(playerId)
        if not blockInfo:
            logger.error("Get opened block key error!")
            return False
        blockPos = blockInfo.get("blockPos")
        dimension = blockInfo.get("dimension")
        blockKey = (blockPos[0], blockPos[1], blockPos[2], dimension)
        blockEntityData = blockEntityComp.GetBlockEntityData(
            blockInfo.get("dimension"), blockInfo.get("blockPos"))
        workbenchMgr = self.workbenchManagerDict.get(blockKey)
        workbenchMgr.UpdateSlotData(slot, None)
        blockEntityData[slot] = None
        return True

    def HandleCraftingResult(self, playerId, blockName, dimension, blockPos,
                             blockEntityData):
        """获取配方结果，若成功获取配方，通知客户端更新，更改 block 的数据

        Args:
            playerId (int): playerId
            blockName (str)): blockName
            craftingMgr (CraftingManager): block 对应的管理类
            workbenchItems (dict): 工作槽物品
            blockEntityData (dict): 方块数据
        """
        workbenchMgr = self.workbenchManagerDict.get(
            (blockPos[0], blockPos[1], blockPos[2], dimension))
        workbenchItem = self.GetWorkbenchItems(dimension, blockName, blockPos)
        resultItem = workbenchMgr.GetRecipeResult(workbenchItem)
        if not resultItem:
            return
        # 存在合成结果，更新 blockData
        for slotName, slotItem in resultItem.items():
            blockEntityData[slotName] = slotItem
        gameComp = compFactory.CreateGame(serverApi.GetLevelId())
        gameComp.AddTimer(0.01, self.UpdateWorkbench, playerId, blockPos,
                          dimension)

    def UpdateFurnace(self, playerId, blockPos, dimension):
        furnaceMgr = self.workbenchManagerDict.get(
            (blockPos[0], blockPos[1], blockPos[2], dimension))
        if furnaceMgr:
            furnaceData = self.CreateEventData()
            furnaceData["blockName"] = furnaceMgr.GetBlockName()
            furnaceData["isLit"] = furnaceMgr.IsLit()
            furnaceData["litDuration"] = furnaceMgr.GetLitDuration()
            furnaceData["isCooking"] = furnaceMgr.IsCooking()
            # furnaceData["litProgress"] = furnaceMgr.GetLitProgress()
            # furnaceData["burnProgress"] = furnaceMgr.GetBurnProgress()
            self.NotifyToClient(playerId, modConfig.WorkbenchChangedEvent,
                                furnaceData)

    def OnOutSlotClick(self, event):
        playerId = event["playerId"]
        blockPos = event["blockPos"]
        dimension = event["dimension"]
        blockKey = (blockPos[0], blockPos[1], blockPos[2], dimension)
        workbenchMgr = self.workbenchManagerDict.get(blockKey)
        itemComp = compFactory.CreateItem(playerId)
        blockEntityComp = compFactory.CreateBlockEntityData(self.levelId)
        blockEntityData = blockEntityComp.GetBlockEntityData(
            dimension, blockPos)
        newWorkbenchItems = workbenchMgr.HandleGetResult()
        for slotName, slotItem in newWorkbenchItems.items():
            blockEntityData[slotName] = slotItem
        itemComp.SpawnItemToPlayerInv(event["item"], playerId)
        blockInfo = self.GetBlockInfoByPlayerId(playerId)
        if blockInfo:
            blockName = blockInfo.get("blockName")
            self._UpdateBagUI(playerId, blockName)
        self.HandleCraftingResult(playerId, blockName, dimension, blockPos,
                                  blockEntityData)
