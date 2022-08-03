'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 15:26:32
LastEditTime: 2022-08-01 12:19:11
'''
from hammerCookingScripts import logger
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()


class SystemController(object):
    systemDict = {}  # key: systemName  value: system

    @classmethod
    def GetModClientSystem(cls, systemName):
        # type: (str) -> ClientSystem
        """获取 ClientSystem"""
        clientSystem = cls.systemDict.get(systemName)
        if not clientSystem:
            logger.error("{0} 未注册".format(systemName))
            return
        return clientSystem

    @classmethod
    def SetModClientSystem(cls, systemName, clientSystem):
        # type: (str, ClientSystem ) -> None
        """将 ClientSystem 加入到 systemDict 中"""
        cls.systemDict[systemName] = clientSystem
