'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-27 22:54:59
LastEditTime: 2022-08-24 14:39:26
'''

from copy import deepcopy
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.server.factory import WorkbenchFactory
from hammerCookingScripts.server.utils import serverBlockUtils as blockUtils
from hammerCookingScripts.server.utils import serverItemUtils as itemUtils
from hammerCookingScripts import logger


class WorkbenchController(object):
    curOpenedBlock = {}

    @classmethod
    def SetCurOpenedBlock(cls, playerId, blockName, pos, dimensionId):
        # type: (int,str,tuple,int) -> None
        """设置玩家正在使用的Block信息"""
        cls.curOpenedBlock[playerId] = {
            "blockName": blockName,
            "pos": pos,
            "dimensionId": dimensionId
        }

    @classmethod
    def DeleteCurOpenedBlock(cls, playerId):
        # type: (int) -> None
        """删除玩家正在使用的 Block 信息"""
        if not cls.curOpenedBlock.get(playerId):
            return
        del cls.curOpenedBlock[playerId]

    @classmethod
    def GetCurOpenedBlockInfo(cls, playerId):
        # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
        # type: (int) -> dict
        """获取玩家正在使用的 Block 信息"""
        blockInfo = cls.curOpenedBlock.get(playerId)
        if not blockInfo:
            return
        return blockInfo

    @classmethod
    def IsPlayerOpeningBlock(cls, playerId):
        # type: (int) -> dict
        """判断玩家是否正打开某个方块UI界面"""
        return cls.curOpenedBlock.get(playerId) is not None

    @classmethod
    def IsPositionBlockUsing(cls, pos, dimensionId):
        """判断某个位置的方块是否正在被使用"""
        return any(pos == curOpenedBlockInfo.get("pos")
                   and dimensionId == curOpenedBlockInfo["dimensionId"]
                   for curOpenedBlockInfo in cls.curOpenedBlock.values())

    @classmethod
    def GetOpeningPlayerList(cls):
        # type: () -> list
        """获取正在打开方块UI的玩家列表"""
        return cls.curOpenedBlock.keys()

    @classmethod
    def FormWorkbenchData(cls, blockName, pos, dimensionId, levelId, **kwargs):
        # type: (str, tuple, int, int, dict) -> dict
        """
        生成 workbenchData 字典，作为时间的数据传输
        其他键:
        isBurning: bool  
        isProducing: bool  
        burnDuration: int  
        burnProgress: int  
        produceProgress: int
        pos: tuple
        dimensionId: int
        """
        workbenchSlotData = cls.GetBlockSlotData(blockName, pos, dimensionId,
                                                 levelId)
        workbenchData = {
            "blockName": blockName,
            "workbenchSlotData": workbenchSlotData,
            "pos": pos,
            "dimensionId": dimensionId,
            "levelId": levelId
        }
        for key, value in kwargs.items():
            workbenchData[key] = value
        return workbenchData

    @classmethod
    def FormFurnaceData(cls, blockName, pos, dimensionId, levelId):
        # type: (str, tuple, int, int) -> dict
        """生成 furnace 的 workbenchData"""
        exaPos = pos + (dimensionId, )
        WorkbenchMgr = WorkbenchFactory.GetWorkbenchManager(exaPos)
        isBurning = WorkbenchMgr.IsBurning()
        burnDurationTuple = WorkbenchMgr.GetFuelBurnDuration()
        if not burnDurationTuple:
            burnDuration = 0
        else:
            burnDuration = burnDurationTuple[-1]
        isProducing = WorkbenchMgr.IsProducing()
        if WorkbenchMgr.IsUIInit():
            WorkbenchMgr.clientUIInit()
            return WorkbenchController.FormWorkbenchData(
                blockName,
                pos,
                dimensionId,
                levelId,
                isBurning=isBurning,
                burnDuration=burnDuration,
                isProducing=isProducing)
        return WorkbenchController.FormWorkbenchData(
            blockName,
            pos,
            dimensionId,
            levelId,
            isBurning=isBurning,
            burnDuration=burnDuration,
            isProducing=isProducing,
            burnProgress=WorkbenchMgr.GetUIBurnProgress(),
            produceProgress=WorkbenchMgr.GetUIProducingProgress())

    @classmethod
    def ConvertBlockEntityDataToDict(cls, blockName, blockEntityData, exaPos):
        WorkbenchMgr = WorkbenchFactory.GetWorkbenchManager(exaPos, blockName)
        return {
            slotName: blockEntityData[slotName]
            for slotName in WorkbenchMgr.GetAllSlotName()
        }

    @classmethod
    def GetBlockSlotData(cls, blockName, pos, dimensionId, levelId):
        blockEntityData = blockUtils.GetBlockEntityData(pos, dimensionId,
                                                        levelId)
        return cls.ConvertBlockEntityDataToDict(blockName, blockEntityData,
                                                pos + (dimensionId, ))

    @staticmethod
    def FormInventoryData(playerId, blockName):
        inventorySlotData = {
            i: itemUtils.GetPlayerInventoryItem(playerId, i)
            for i in range(modConfig.Inventory_Slot_NUM)
        }
        return {"blockName": blockName, "inventorySlotData": inventorySlotData}
