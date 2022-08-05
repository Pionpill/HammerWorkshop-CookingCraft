'''
Description: 植物客户端系统
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 11:21:52
LastEditTime: 2022-07-31 13:22:40
'''
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()


class PlantsClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.playerId = clientApi.GetLocalPlayerId()
