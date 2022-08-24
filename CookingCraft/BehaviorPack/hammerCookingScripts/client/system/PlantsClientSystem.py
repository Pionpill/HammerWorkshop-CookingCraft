'''
Description: 植物客户端系统
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 11:21:52
LastEditTime: 2022-08-16 14:48:49
'''
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()


class PlantsClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.playerId = clientApi.GetLocalPlayerId()
