'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-29 12:47:55
LastEditTime: 2022-05-30 16:51:25
'''

# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig


@Mod.Binding(name=modConfig.ModName, version="0.1.0")
class CookingCraft(object):
    def __init__(self):
        logger.info("CookingCraft Mod Scripts Init")

    @Mod.InitServer()
    def ServerInit(self):
        logger.info("CookingCraft Server Init")
        serverApi.RegisterSystem(modConfig.ModName,
                                 modConfig.ServerSystemName_Workbench,
                                 modConfig.ServerSystemClsPath_Workbench)
        serverApi.RegisterSystem(modConfig.ModName,
                                 modConfig.ServerSystemName_Plants,
                                 modConfig.ServerSystemClsPath_Plants)

    @Mod.DestroyServer()
    def ServerDestroy(self):
        logger.info("CookingCraft Server Destory")

    @Mod.InitClient()
    def ClientInit(self):
        logger.info("CookingCraft Client Init")
        serverApi.RegisterSystem(modConfig.ModName,
                                 modConfig.ClientSystemName_Workbench,
                                 modConfig.ClientSystemClsPath_Workbench)
        serverApi.RegisterSystem(modConfig.ModName,
                                 modConfig.ClientSystemName_Plants,
                                 modConfig.ClientSystemClsPath_Plants)

    @Mod.DestroyClient()
    def ClientDestroy(self):
        logger.info("CookingCraft Client Destory")
