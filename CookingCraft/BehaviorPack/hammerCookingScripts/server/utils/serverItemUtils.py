'''
Description: 服务端物品工具包
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-17 15:46:43
LastEditTime: 2022-07-17 22:03:28
'''
import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


def UseItem(playerId):
    # type: (int) -> None
    """玩家使用物品，背包中物品数量减1"""
    comp = compFactory.CreateItem(playerId)
    invSlotId = comp.GetSelectSlotId()
    carriedItemCount = comp.GetPlayerItem(minecraftEnum.ItemPosType.CARRIED,
                                          0).get("count")
    comp.SetInvItemNum(invSlotId, carriedItemCount - 1)


def GetPlayerItemName(playerId):  # sourcery skip: use-named-expression
    # type: (int) -> str
    """获取玩家手上的物品"""
    comp = compFactory.CreateItem(playerId)
    invSlotId = comp.GetSelectSlotId()
    itemDict = comp.GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0)
    if itemDict:
        return itemDict.get("newItemName")
