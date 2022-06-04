'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 16:15:57
LastEditTime: 2022-06-04 21:09:29
'''
import time
import mod.server.extraServerApi as serverApi
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger
from hammerCookingScripts.common.commonManager.PlantsCommonMgr import PlantsCommonManager
from hammerCookingScripts.server.serverManager.PlantsMgr import PlantsManager

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()


class PlantsServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenPlantsEvent()
        self.levelId = serverApi.GetLevelId()
        self.playerId = None
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

    def OnAddServerPlayer(self, args):
        self.playerId = args["id"]

    def OnServerItemUse(self, args):
        playerId = args["entityId"]
        if not self.interactCoolDict.get(playerId):
            self.interactCoolDict[playerId] = time.time()
        elif time.time() - self.interactCoolDict[playerId] < 0.15:
            return
        else:
            self.interactCoolDict[playerId] = time.time()

        itemName = args["itemName"]

        if PlantsCommonManager.GetSeedInfo(itemName):
            seedName = itemName
            dimension = args["dimensionId"]
            blockPos = (args["x"], args["y"], args["z"])
            blockName = self.GetBlockName(blockPos, dimension)
            biomeName = compFactory.CreateBiome(self.levelId).GetBiomeName(
                blockPos, dimension)
            if PlantsManager.CanPlant(seedName, biomeName, blockName):
                plantFirstStageName = PlantsCommonManager.GetPlantFirstStageName(
                    seedName)
                plantBlockDict = {"name": plantFirstStageName, "aux": 0}
                aboveBlockPos = (args["x"], args["y"] + 1, args["z"])
                aboveBlockName = self.GetBlockName(aboveBlockPos, dimension)
                if PlantsManager.IsClimbingPlant(seedName):
                    belowBlockPos = (args["x"], args["y"] - 1, args["z"])
                    belowBlockName = self.GetBlockName(belowBlockPos, dimension)
                    if belowBlockName == "minecraft:farmland":
                        newBlockPos = (args["x"], args["y"], args["z"])
                        compFactory.CreateBlockInfo(self.levelId).SetBlockNew(
                            newBlockPos, plantBlockDict, dimensionId=dimension)
                        self.__ItemPlant()
                elif aboveBlockName == "minecraft:air":
                    newBlockPos = (args["x"], args["y"] + 1, args["z"])
                    compFactory.CreateBlockInfo(self.levelId).SetBlockNew(
                        newBlockPos, plantBlockDict, dimensionId=dimension)
                    self.__ItemPlant()

    def OnBlockNeighborChangedServer(self, args):
        pos = (args['posX'], args['posY'], args['posZ'])
        neighPos = (args['neighborPosX'], args['neighborPosY'],
                    args['neighborPosZ'])
        if (self.__IsBelow(pos, neighPos)):
            comp = compFactory.CreateBlockInfo(self.playerId)
            blockDict = comp.GetBlockNew(neighPos)
            seedName = PlantsCommonManager.GetPlantSeedNameByStage(
                args["blockName"])
            plantLandList = PlantsCommonManager.GetSeedPlantLandList(seedName)
            if blockDict["name"] not in plantLandList:
                blockDict = {'name': 'minecraft:air', 'aux': 0}
                comp.SetBlockNew(pos, blockDict)

    def OnBlockRandomTick(self, args):
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(args["fullName"])
        if PlantsCommonManager.GetSeedInfo(seedName):
            pos = (args["posX"], args["posY"], args["posZ"])
            dimension = args["dimensionId"]
            plantBlockName = args["fullName"]

            if PlantsManager.CanGrow(plantBlockName, pos, dimension,
                                     self.levelId, self.playerId):
                blockEntityComp = compFactory.CreateBlockEntityData(
                    self.playerId)
                blockEntityData = blockEntityComp.GetBlockEntityData(
                    dimension, pos)
                if not blockEntityData:
                    return
                growth = blockEntityData["growth"]
                if not growth:
                    growth = 0
                growth += 1
                blockEntityData["growth"] = growth

                if PlantsManager.CanChangeStage(plantBlockName, growth):
                    comp = compFactory.CreateBlockInfo(self.playerId)
                    blockDict = {
                        "name":
                        PlantsCommonManager.GetPlantNextStageName(
                            plantBlockName),
                        "aux":
                        0
                    }
                    comp.SetBlockNew(pos, blockDict)
                    blockEntityData["growth"] = 0

    def __IsBelow(self, pos, neighPos):
        return pos[0] == neighPos[0] and (
            pos[1] - 1 == neighPos[1]) and pos[2] == neighPos[2]

    def __ItemPlant(self):
        """农作物种下后，背包种子数-1
        """
        comp = compFactory.CreateItem(self.playerId)
        invSlotId = comp.GetSelectSlotId()
        carriedItemCount = comp.GetPlayerItem(
            serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0).get("count")
        comp.SetInvItemNum(invSlotId, carriedItemCount - 1)

    def GetBlockName(self, blockPos, dimension):
        blockDict = compFactory.CreateBlockInfo(self.levelId).GetBlockNew(
            blockPos, dimension)
        return blockDict.get("name")
