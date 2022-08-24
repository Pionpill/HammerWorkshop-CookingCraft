'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 16:15:57
LastEditTime: 2022-08-16 14:59:03
'''
import mod.server.extraServerApi as serverApi
from hammerCookingScripts import logger
from hammerCookingScripts.server.utils import serverItemUtils

ServerSystem = serverApi.GetServerSystemCls()
minecraftEnum = serverApi.GetMinecraftEnum()
compFactory = serverApi.GetEngineCompFactory()


class BookServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.levelId = serverApi.GetLevelId()
        self.ListenBookEvent()
        self.interactCoolDict = {}

    def ListenBookEvent(self):
        engineNamespace = serverApi.GetEngineNamespace()
        engineSystemName = serverApi.GetEngineSystemName()
        self.ListenForEvent(engineNamespace, engineSystemName,
                            "ClientLoadAddonsFinishServerEvent", self,
                            self.OnClientLoadAddonsFinish)

    def OnClientLoadAddonsFinish(self, args):
        playerId = args["playerId"]
        itemComp = compFactory.CreateItem(self.levelId)
        itemNameList = [
            "cookingcraft:author_book",
            "cookingcraft:cooking_book",
            "cookingcraft:plants_book",
        ]
        for itemName in itemNameList:
            itemDict = serverItemUtils.GenerateItemDict(itemName)
            itemComp.SpawnItemToPlayerInv(itemDict, playerId)
