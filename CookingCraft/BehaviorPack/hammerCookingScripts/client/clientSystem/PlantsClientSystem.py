'''
Description: 背包客户端系统
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 11:21:52
LastEditTime: 2022-05-31 13:46:34
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()


class PlantsClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.playerId = clientApi.GetLocalPlayerId()
