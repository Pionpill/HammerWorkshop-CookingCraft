'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-06-01 15:43:39
LastEditTime: 2022-06-04 15:55:33
'''
from hammerCookingScripts.common.commonBiome.BiomeForm import BiomeForm as BF

SEEDS_INFO = {
    "cookingcraft:herb_seeds": {
        "tickList": [3, 3, 5],
        "harvestCount": 1,
        "harvestStage": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome": set(BF.woods | BF.plains | BF.water) & BF.temperate
        },
        "growthConditions": {
            "brightness": [9, 15],
            "altitude": [64, 192],
            "weather": None,  # 可填写 "rain", "thunder"
            "sprout": None,  # 可填写 "rain", "thunder"
            "special": {
                "water": 3
            }
        },
    }
}
