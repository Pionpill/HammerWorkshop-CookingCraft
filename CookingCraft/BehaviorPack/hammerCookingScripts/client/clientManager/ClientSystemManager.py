'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-25 15:26:32
LastEditTime: 2022-04-25 16:10:30
'''
from hammerCookingScripts import logger

clientSystemDict = {}


class ClientSystemManager(object):
    def __init__(self):
        object.__init__(self)

    def GetModClientSystem(self, systemName):
        """获取 ClientSystem

        Args:
            systemName (str): modConfig 中的系统名

        Returns:
            ClientSystem: 客户端系统
        """
        clientSystem = clientSystemDict.get(systemName)
        if not clientSystem:
            logger.error("{0} 未注册".format(systemName))
            return
        else:
            return clientSystem

    def SetModClientSystem(self, systemName, clientSystem):
        """将 ClientSystem 加入到 clientSystemDict 中

        Args:
            systemName (str): modConfig 中的客户端系统名
            clientSystem (ClientSystem): 客户端系统
        """
        clientSystemDict[systemName] = clientSystem
