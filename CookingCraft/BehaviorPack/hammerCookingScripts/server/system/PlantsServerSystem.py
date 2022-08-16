'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 16:15:57
LastEditTime: 2022-08-16 15:32:39
'''
import time

import mod.server.extraServerApi as serverApi
from hammerCookingScripts import logger
from hammerCookingScripts.common.facade import PlantsFacade
from hammerCookingScripts.common.utils import (RelativePosition, engineUtils,
                                               positionUtils)
from hammerCookingScripts.server.controller import PlantsController
from hammerCookingScripts.server.utils import serverBlockUtils, serverItemUtils

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
plantsUtils = PlantsFacade.GetPlantsUtils()


class PlantsServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.levelId = serverApi.GetLevelId()
        self.playerId = None
        self.ListenPlantsEvent()
        self.interactCoolDict = {}

    def ListenPlantsEvent(self):
        engineNamespace = serverApi.GetEngineNamespace()
        engineSystemName = serverApi.GetEngineSystemName()
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "AddServerPlayerEvent", self,
                            self.OnAddServerPlayer)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ServerItemUseOnEvent", self, self.OnServerItemUse)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "BlockNeighborChangedServerEvent", self,
                            self.OnBlockNeighborChangedServer)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "BlockRandomTickServerEvent", self,
                            self.OnBlockRandomTick)
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ServerBlockUseEvent", self, self.OnServerBlockUse)

    def OnAddServerPlayer(self, args):
        self.playerId = args["id"]

    def OnServerItemUse(self, args):  # sourcery skip: use-named-expression
        # type: (dict) -> None
        playerId = args["entityId"]
        if not engineUtils.coolDown(playerId, self.interactCoolDict):
            return
        """使用种子种地"""
        itemName = args["itemName"]
        if plantsUtils.IsModSeed(itemName):
            seedName = itemName
            dimensionId = args["dimensionId"]
            pos = (args["x"], args["y"], args["z"])
            self.__ModSeedUse(seedName, pos, dimensionId, playerId)
        elif plantsUtils.IsFence(itemName):
            dimensionId = args["dimensionId"]
            pos = (args["x"], args["y"], args["z"])
            self.__ModFenceUse(itemName, pos, dimensionId)

    def OnBlockNeighborChangedServer(self, args):
        # type: (dict) -> None
        """植物周边方块变化"""
        pos = (args['posX'], args['posY'], args['posZ'])
        neighPos = (args['neighborPosX'], args['neighborPosY'],
                    args['neighborPosZ'])
        seedName = plantsUtils.GetSeedNameByStageBlock(args["blockName"])
        if seedName and positionUtils.JudgeBasicPosition(
                pos, neighPos) == RelativePosition.above:
            self.__BelowBlockChange(pos, neighPos, seedName)

    def OnBlockRandomTick(self, args):
        # type: (dict) -> None
        """植物 Tick"""
        seedName = plantsUtils.GetSeedNameByStageBlock(args["fullName"])
        if plantsUtils.IsModSeed(seedName):
            pos = (args["posX"], args["posY"], args["posZ"])
            dimensionId = args["dimensionId"]
            blockName = args["fullName"]
            self.__ModPlantTick(pos, blockName, dimensionId)

    def OnServerBlockUse(self, args):
        playerId, dimensionId = args["playerId"], args["dimensionId"]
        if not engineUtils.coolDown(playerId, self.interactCoolDict):
            return
        pos = (args['x'], args['y'], args['z'])
        blockName = args["blockName"]
        itemName = serverItemUtils.GetPlayerCarriedItemName(playerId)
        # 在篱笆上种植藤蔓植物
        if PlantsController.IsClimbingPlant(itemName):
            plantBlockDict = PlantsController.GetPlantFirstStageDict(itemName)
            self.__PlantClimbingCrop(pos, plantBlockDict, dimensionId, playerId)
        # 收获可多次收获的植物
        elif PlantsController.CanHarvest(blockName):
            self.__HarvestPlant(blockName, pos, dimensionId, playerId)

    def __HarvestPlant(self, blockName, pos, dimensionId, playerId):
        # type: (str, tuple, int,int) -> None
        """收获植株(藤蔓与多次种植)"""
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        lootItem = PlantsController.GetPlantLootItem(seedName)
        if not PlantsController.CanHarvest(blockName):
            return
        # 多次收获植物: 将收获次数计入植物中
        if PlantsController.IsClimbingPlant(seedName):
            self.__HarvestClimbingPlant(pos, seedName, dimensionId, playerId)
        else:
            self.__HarvestMultiPlant(pos, blockName, dimensionId, playerId)

    def __HarvestClimbingPlant(self, pos, seedName, dimensionId, playerId):
        # type: (tuple, str, int, int) -> None
        """收获藤蔓植物"""
        self.__SpawnPlantFruit(seedName, pos, dimensionId)
        harvestStageBlockDict = PlantsController.GetHarvestBlock(seedName)
        comp = compFactory.CreateBlockInfo(playerId)
        comp.SetBlockNew(pos, harvestStageBlockDict, dimensionId)

    def __HarvestMultiPlant(self, pos, blockName, dimensionId, playerId):
        # type: (tuple, str, int,int) -> None
        """收获多次种植植株的果实"""
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            pos, dimensionId, playerId)
        if not blockEntityData:
            return
        harvestNum = blockEntityData["harvestNum"] or 0
        harvestNum += 1
        # 如果已近到达收获次数上限，返回
        if not PlantsController.CanHarvest(blockName, harvestNum):
            return
        blockEntityData["harvestNum"] = harvestNum
        # 生成掉落物
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        self.__SpawnPlantFruit(seedName, pos, dimensionId)
        # 设置新的植株状态
        self.__SetNewMultiPlantBlock(seedName, harvestNum, pos, dimensionId,
                                     playerId)

    def __SetNewMultiPlantBlock(self, seedName, harvestNum, pos, dimensionId,
                                playerId):
        # type: (str, int, tuple, int,int) -> None
        """设置新的可多次收获植株"""
        harvestStageBlockDict = PlantsController.GetHarvestBlock(seedName)
        comp = compFactory.CreateBlockInfo(playerId)
        comp.SetBlockNew(pos, harvestStageBlockDict, dimensionId)
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            pos, dimensionId, playerId)
        blockEntityData["harvestNum"] = harvestNum

    def __SpawnPlantFruit(self, seedName, pos, dimensionId):
        # type: (str, tuple, int) -> None
        """掉落植物果实"""
        lootItem = PlantsController.GetPlantLootItem(seedName)
        itemComp = compFactory.CreateItem(self.levelId)
        itemComp.SpawnItemToLevel(lootItem, dimensionId, pos)

    def __ModPlantTick(self, pos, blockName, dimensionId):
        # type: (tuple,str,int) -> None
        """植物进行 tick 生长"""
        if not PlantsController.CanTick(blockName, pos, dimensionId,
                                        self.levelId):
            return
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            pos, dimensionId, self.levelId)
        if not blockEntityData:
            return
        growth = blockEntityData["growth"] or 0
        growth += 1
        blockEntityData["growth"] = growth
        harvestNum = blockEntityData["harvestNum"] or 0
        self.__ModPlantGrow(pos, blockName, growth, blockEntityData, harvestNum)

    def __ModPlantGrow(self, pos, blockName, growth, blockEntityData,
                       harvestNum):
        # type: (tuple, str, int, dict,int) -> None
        """植物生长到下一状态"""
        if not PlantsController.CanGrowNextStage(blockName, growth):
            return
        blockDict = PlantsController.GetNextBlockStageDict(blockName)
        comp = compFactory.CreateBlockInfo(self.playerId)
        result = comp.SetBlockNew(pos, blockDict)
        blockEntityData["growth"] = 0
        if harvestNum != 0:
            blockEntityData["harvestNum"] = harvestNum

    def __BelowBlockChange(self, pos, neighPos, seedName):
        # type: (tuple,tuple,str) -> None
        """植物下面方块变化，植物可能直接消失"""
        comp = compFactory.CreateBlockInfo(self.playerId)
        blockDict = comp.GetBlockNew(neighPos)
        airBlockDict = {'name': 'minecraft:air', 'aux': 0}
        if PlantsController.IsClimbingPlant(seedName):
            if blockDict.get("name") == "minecraft:farmland":
                return
            comp.SetBlockNew(pos, airBlockDict)
        elif not PlantsController.JudgePlantLand(seedName,
                                                 blockDict.get("name")):
            blockDict = {'name': 'minecraft:air', 'aux': 0}
            comp.SetBlockNew(pos, airBlockDict)

    def __ModSeedUse(self, seedName, pos, dimensionId, playerId):
        # type: (str, tuple, int, int) -> None
        """种植植物"""
        blockName = serverBlockUtils.GetBlockName(self.levelId, pos,
                                                  dimensionId)
        biomeName = compFactory.CreateBiome(self.levelId).GetBiomeName(
            pos, dimensionId)
        if not PlantsController.CanPlant(seedName, biomeName, blockName):
            logger.debug("{0} can't plant on land:[{1}] biome:[{2}]".format(
                seedName, blockName, biomeName))
            return

        plantBlockDict = PlantsController.GetPlantFirstStageDict(seedName)
        aboveBlockPos = positionUtils.GetRelativePosition(pos, "above")
        aboveBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       aboveBlockPos,
                                                       dimensionId)
        if aboveBlockName == "minecraft:air":
            self.__SetBlock(aboveBlockPos, plantBlockDict, dimensionId,
                            playerId)

    def __PlantClimbingCrop(self, pos, plantBlockDict, dimensionId, playerId):
        # type: (tuple, dict, int,int) -> None
        """藤蔓植物的种植"""
        belowBlockPos = positionUtils.GetRelativePosition(pos, "below")
        belowBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       belowBlockPos,
                                                       dimensionId)
        if belowBlockName == "minecraft:farmland":
            self.__SetBlock(pos, plantBlockDict, dimensionId, playerId)

    def __SetBlock(self, pos, blockDict, dimensionId, playerId):
        # type: (tuple, dict, int,int) -> None
        """普通植物的种植"""
        newBlockPos = pos
        compFactory.CreateBlockInfo(self.levelId).SetBlockNew(
            newBlockPos, blockDict, dimensionId=dimensionId)
        serverItemUtils.UseItem(playerId)

    # FIXME 没有办法阻止放置栅栏
    def __ModFenceUse(self, itemName, pos, dimensionId):
        # type: (str, tuple, int) -> None
        """放置篱笆"""
        aboveBlockPos = positionUtils.GetRelativePosition(pos, "above")
        aboveBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       aboveBlockPos,
                                                       dimensionId)
        belowBlockPos = positionUtils.GetRelativePosition(pos, "below")
        belowBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       belowBlockPos,
                                                       dimensionId)
        if aboveBlockName == "minecraft:air" and belowBlockName == "minecraft:farmland":
            blockDict = {"name": itemName, "aux": 0}
        else:
            blockDict = {"name": "minecraft:air", "aux": 0}
