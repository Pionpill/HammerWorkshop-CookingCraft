'''
Description: 烘焙炉界面的 UI

version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-15 13:00:48
LastEditTime: 2022-08-05 14:08:38
'''
from hammerCookingScripts.client.ui.base import BaseFurnaceScreen
from hammerCookingScripts import logger


class BakingFurnaceScreen(BaseFurnaceScreen):
    def __init__(self, namespace, name, param):
        BaseFurnaceScreen.__init__(self, namespace, name, param)
