'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-06-01 15:43:39
LastEditTime: 2022-07-05 16:31:44
'''
from hammerCookingScripts.common.commonBiome.BiomeForm import BiomeForm as BF

SEEDS_NAME = [
    "cookingcraft:herb_seeds", "cookingcraft:pepper", "cookingcraft:rice_fruit",
    "cookingcraft:corn_pieces", "cookingcraft:tomato", "cookingcraft:onion",
    "cookingcraft:banana"
]

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
        },
    },
    "cookingcraft:pepper": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestStage": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome": set(BF.woods | BF.plains) & BF.temperate
        },
        "growthConditions": {
            "brightness": [9, 15],
            "altitude": [64, 128],
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:rice_fruit": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestStage": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            set(BF.woods | BF.plains | BF.water) & (BF.temperate | BF.tropic)
        },
        "growthConditions": {
            "brightness": [11, 15],
            "altitude": [64, 128],
            "weather": None,
            "sprout": "rain",
            "special": {
                "water": 3
            }
        },
    },
    "cookingcraft:corn_pieces": {
        "tickList": [3, 3, 3, 5],
        "harvestCount": 3,
        "harvestStage": 3,
        "lootTable": {
            "newItemName": "cookingcraft:corn",
            "count": [2, 3],
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            set(
                set(BF.woods | BF.plains | BF.water)
                & (BF.temperate | BF.tropic)) | BF.taiga
        },
        "growthConditions": {
            "brightness": [9, 15],
            "altitude": [64, 192],
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:tomato": {
        "tickList": [3, 4, 4],
        "harvestCount": 1,
        "harvestStage": "cookingcraft:fence_post",
        "lootTable": {
            "newItemName": "cookingcraft:tomato",
            "count": [2, 5],
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["cookingcraft:fence_post"],
            "plantBiome":
            set(BF.woods | BF.plains | BF.water) & (BF.temperate | BF.tropic)
        },
        "growthConditions": {
            "brightness": [6, 15],
            "altitude": [64, 128],
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:onion": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestStage": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome":
            set(set(BF.woods | BF.plains | BF.water) & BF.temperate) | BF.taiga
        },
        "growthConditions": {
            "brightness": [9, 15],
            "altitude": [64, 128],
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:banana": {
        "tickList": [3, 3, 3, 3, 4],
        "harvestCount": 3,
        "harvestStage": 3,
        "lootTable": {
            "newItemName": "cookingcraft:banana",
            "count": [4, 7],
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome": BF.tropic & BF.woods
        },
        "growthConditions": {
            "brightness": [9, 15],
            "altitude": [64, 128],
            "weather": None,
            "sprout": None,
        },
    },
}
