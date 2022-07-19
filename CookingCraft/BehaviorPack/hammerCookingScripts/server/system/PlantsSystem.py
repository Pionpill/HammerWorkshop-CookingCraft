'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 16:15:57
LastEditTime: 2022-07-19 14:46:44
'''
import time
import mod.server.extraServerApi as serverApi
from hammerCookingScripts import logger
from hammerCookingScripts.server.controller import PlantsController
from hammerCookingScripts.server.utils import serverItemUtils, serverBlockUtils
from hammerCookingScripts.common.facade import PlantsFacade
from hammerCookingScripts.common.utils import positionUtils, RelativePosition, engineUtils

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()
plantsUtils = PlantsFacade.GetPlantsUtils()


class PlantsSystem(ServerSystem):
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
            dimension = args["dimensionId"]
            blockPos = (args["x"], args["y"], args["z"])
            self.__ModSeedUse(seedName, blockPos, dimension)
        elif plantsUtils.IsFence(itemName):
            dimension = args["dimensionId"]
            blockPos = (args["x"], args["y"], args["z"])
            self.__ModFenceUse(itemName, blockPos, dimension)

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
            dimension = args["dimensionId"]
            blockName = args["fullName"]
            self.__ModPlantTick(pos, blockName, dimension)

    def OnServerBlockUse(self, args):
        playerId, dimension = args["playerId"], args["dimensionId"]
        if not engineUtils.coolDown(playerId, self.interactCoolDict):
            return
        blockPos = (args['x'], args['y'], args['z'])
        blockName = args["blockName"]
        itemName = serverItemUtils.GetPlayerItemName(self.playerId)
        # 在篱笆上种植藤蔓植物
        if PlantsController.IsClimbingPlant(itemName):
            plantBlockDict = PlantsController.GetPlantFirstStageDict(itemName)
            self.__PlantClimbingCrop(blockPos, plantBlockDict, dimension)
        # 收获可多次收获的植物
        elif PlantsController.CanHarvest(blockName):
            self.__HarvestPlant(blockName, blockPos, dimension)

    def __HarvestPlant(self, blockName, blockPos, dimension):
        # type: (str, tuple, int) -> None
        """收获植株(藤蔓与多次种植)"""
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        lootItem = PlantsController.GetPlantLootItem(seedName)
        if not PlantsController.CanHarvest(blockName):
            return
        # 多次收获植物: 将收获次数计入植物中
        if PlantsController.IsClimbingPlant(seedName):
            self.__HarvestClimbingPlant(blockPos, seedName, dimension)
        else:
            self.__HarvestMultiPlant(blockPos, blockName, dimension)

    def __HarvestClimbingPlant(self, blockPos, seedName, dimension):
        # type: (tuple, str, int) -> None
        """收获藤蔓植物"""
        self.__SpawnPlantFruit(seedName, blockPos, dimension)
        harvestStageBlockDict = PlantsController.GetHarvestBlock(seedName)
        comp = compFactory.CreateBlockInfo(self.playerId)
        comp.SetBlockNew(blockPos, harvestStageBlockDict, dimension)

    def __HarvestMultiPlant(self, blockPos, blockName, dimension):
        # type: (tuple, str, int) -> None
        """收获多次种植植株的果实"""
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            blockPos, dimension, self.playerId)
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
        self.__SpawnPlantFruit(seedName, blockPos, dimension)
        # 设置新的植株状态
        self.__SetNewMultiPlantBlock(seedName, harvestNum, blockPos, dimension)

    def __SetNewMultiPlantBlock(self, seedName, harvestNum, blockPos,
                                dimension):
        # type: (str, int, tuple, int) -> None
        """设置新的可多次收获植株"""
        harvestStageBlockDict = PlantsController.GetHarvestBlock(seedName)
        comp = compFactory.CreateBlockInfo(self.playerId)
        comp.SetBlockNew(blockPos, harvestStageBlockDict, dimension)
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            blockPos, dimension, self.playerId)
        blockEntityData["harvestNum"] = harvestNum

    def __SpawnPlantFruit(self, seedName, blockPos, dimension):
        # type: (str, tuple, int) -> None
        """掉落植物果实"""
        lootItem = PlantsController.GetPlantLootItem(seedName)
        itemComp = compFactory.CreateItem(serverApi.GetLevelId())
        itemComp.SpawnItemToLevel(lootItem, dimension, blockPos)

    def __ModPlantTick(self, blockPos, blockName, dimension):
        # type: (tuple,str,int) -> None
        """植物进行 tick 生长"""
        if not PlantsController.CanTick(blockName, blockPos, dimension,
                                        self.levelId, self.playerId):
            return
        blockEntityData = serverBlockUtils.GetBlockEntityData(
            blockPos, dimension, self.playerId)
        if not blockEntityData:
            return
        growth = blockEntityData["growth"] or 0
        growth += 1
        blockEntityData["growth"] = growth
        harvestNum = blockEntityData["harvestNum"] or 0
        self.__ModPlantGrow(blockPos, blockName, growth, blockEntityData,
                            harvestNum)

    def __ModPlantGrow(self, pos, blockName, growth, blockEntityData,
                       harvestNum):
        # type: (tuple, str, int, dict,int) -> None
        """植物生长到下一状态"""
        if not PlantsController.CanGrowNextStage(blockName, growth):
            return
        blockDict = PlantsController.GetNextBlockStageDict(blockName)
        comp = compFactory.CreateBlockInfo(self.playerId)
        comp.SetBlockNew(pos, blockDict)
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
            if blockDict["name"] == "minecraft:farmland":
                return
            comp.SetBlockNew(pos, airBlockDict)
        elif not PlantsController.JudgePlantLand(seedName, blockDict["name"]):
            blockDict = {'name': 'minecraft:air', 'aux': 0}
            comp.SetBlockNew(pos, airBlockDict)

    def __ModSeedUse(self, seedName, blockPos, dimension):
        # type: (str, tuple, int) -> None
        """种植植物"""
        blockName = serverBlockUtils.GetBlockName(self.levelId, blockPos,
                                                  dimension)
        biomeName = compFactory.CreateBiome(self.levelId).GetBiomeName(
            blockPos, dimension)
        if not PlantsController.CanPlant(seedName, biomeName, blockName):
            logger.debug("{0} can't plant on land:[{1}] biome:[{2}]".format(
                seedName, blockName, biomeName))
            return

        plantBlockDict = PlantsController.GetPlantFirstStageDict(seedName)
        aboveBlockPos = positionUtils.GetRelativePosition(blockPos, "above")
        aboveBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       aboveBlockPos, dimension)
        if aboveBlockName == "minecraft:air":
            self.__SetBlock(aboveBlockPos, plantBlockDict, dimension)

    def __PlantClimbingCrop(self, blockPos, plantBlockDict, dimension):
        # type: (tuple, dict, int) -> None
        """藤蔓植物的种植"""
        belowBlockPos = positionUtils.GetRelativePosition(blockPos, "below")
        belowBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       belowBlockPos, dimension)
        if belowBlockName == "minecraft:farmland":
            self.__SetBlock(blockPos, plantBlockDict, dimension)

    def __SetBlock(self, blockPos, blockDict, dimension):
        # type: (tuple, dict, int) -> None
        """普通植物的种植"""
        newBlockPos = blockPos
        compFactory.CreateBlockInfo(self.levelId).SetBlockNew(
            newBlockPos, blockDict, dimensionId=dimension)
        serverItemUtils.UseItem(self.playerId)

    # FIXME 没有办法阻止放置栅栏
    def __ModFenceUse(self, itemName, blockPos, dimension):
        # type: (str, tuple, int) -> None
        """放置篱笆"""
        aboveBlockPos = positionUtils.GetRelativePosition(blockPos, "above")
        aboveBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       aboveBlockPos, dimension)
        belowBlockPos = positionUtils.GetRelativePosition(blockPos, "below")
        belowBlockName = serverBlockUtils.GetBlockName(self.levelId,
                                                       belowBlockPos, dimension)
        if aboveBlockName == "minecraft:air" and belowBlockName == "minecraft:farmland":
            blockDict = {"name": itemName, "aux": 0}
        else:
            blockDict = {"name": "minecraft:air", "aux": 0}
