'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-18 23:04:36
LastEditTime: 2022-07-26 17:18:00
'''
# -*- coding:utf-8 -*-


def IsSameItem(item1, item2):
    # type: (dict, dict) -> bool
    """判断是否为同一item，只有itemName和auxValue均相同才返回True"""
    if not item1 or not item2:
        return False
    if item1.get("newItemName", "item1") != item2.get("newItemName", "item2"):
        return False
    if item1.get("newAuxValue") != item2.get("newAuxValue"):
        return False
    # if item1.get("userData") != item2.get("userData"):
    #     return False
    # if item1.get("durability") != item2.get("durability"):
    #     return False
    return True
