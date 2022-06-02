'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-06-01 15:43:39
LastEditTime: 2022-06-02 23:39:50
'''
from hammerCookingScripts.common.commonBiome.BiomeForm import BiomeForm as BF

SEEDS_INFO = {
    "cookingcraft:herb_seeds": {
        "stageNum": 4,
        "tickList": [3, 3, 5],
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome": set(BF.woods | BF.plains | BF.water) & BF.temperate
        },
        "growthConditions": {
            "brightness": [9, 15],
            "weather": None,
            "altitude": [64, 192]
        }
    }
}
