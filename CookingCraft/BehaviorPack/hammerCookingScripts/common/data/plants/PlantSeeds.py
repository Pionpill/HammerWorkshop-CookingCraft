'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-06-01 15:43:39
LastEditTime: 2022-07-17 13:38:55
'''
from hammerCookingScripts.common.data.biome import PlantsBiomeForm as PlantsBF

SEEDS_INFO = {
    "cookingcraft:herb_seeds": {
        "tickList": [3, 3, 5],
        "harvestCount": 1,
        "harvestBlock": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome":
            PlantsBF.common & PlantsBF.temperature["medium"]
            & PlantsBF.rainfall["medium"]
        },
        "growthConditions": {
            "brightness": (9, 15),
            "altitude": (63, 192),
            "weather": None,  # 可填写 "rain", "thunder"
            "sprout": None,  # 可填写 "rain", "thunder"
        },
    },
    "cookingcraft:pepper": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestBlock": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland", "minecraft:grass"],
            "plantBiome":
            PlantsBF.common & PlantsBF.temperature["medium"]
            & PlantsBF.rainfall["medium"]
        },
        "growthConditions": {
            "brightness": (9, 15),
            "altitude": (63, 128),
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:rice_fruit": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestBlock": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            PlantsBF.common &
            (PlantsBF.temperature["high"] | PlantsBF.temperature["medium"]) &
            (PlantsBF.rainfall["medium"] | PlantsBF.rainfall["high"])
        },
        "growthConditions": {
            "brightness": (11, 15),
            "altitude": (63, 128),
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
        "harvestBlock": "cookingcraft:corn_stage_3",
        "lootTable": {
            "newItemName": "cookingcraft:corn",
            "count": (2, 3),
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            set(PlantsBF.common &
                (PlantsBF.temperature["high"] | PlantsBF.temperature["medium"])
                & PlantsBF.rainfall["medium"]) | PlantsBF.special["taiga"]
        },
        "growthConditions": {
            "brightness": (9, 15),
            "altitude": (63, 192),
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:tomato": {
        "tickList": [3, 4, 4],
        "harvestCount": 1,
        "harvestBlock": "cookingcraft:fence_post",
        "lootTable": {
            "newItemName": "cookingcraft:tomato",
            "count": (2, 5),
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["cookingcraft:fence_post"],
            "plantBiome":
            PlantsBF.common &
            (PlantsBF.temperature["high"] | PlantsBF.temperature["medium"])
            & PlantsBF.rainfall["medium"]
        },
        "growthConditions": {
            "brightness": (6, 15),
            "altitude": (63, 128),
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:onion": {
        "tickList": [2, 2, 3],
        "harvestCount": 1,
        "harvestBlock": None,
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            PlantsBF.common &
            (PlantsBF.temperature["low"] | PlantsBF.temperature["medium"])
            & (PlantsBF.rainfall["medium"] | PlantsBF.rainfall["low"])
        },
        "growthConditions": {
            "brightness": (9, 15),
            "altitude": (63, 128),
            "weather": None,
            "sprout": None,
        },
    },
    "cookingcraft:banana": {
        "tickList": [3, 3, 3, 3, 4],
        "harvestCount": 3,
        "harvestBlock": "cookingcraft:banana_stage_3",
        "lootTable": {
            "newItemName": "cookingcraft:banana",
            "count": (4, 7),
            "newAuxValue": 0
        },
        "plantConditions": {
            "plantLandList": ["minecraft:farmland"],
            "plantBiome":
            PlantsBF.common & PlantsBF.temperature["high"]
            & (PlantsBF.rainfall["medium"] | PlantsBF.rainfall["high"])
        },
        "growthConditions": {
            "brightness": (9, 15),
            "altitude": (63, 128),
            "weather": None,
            "sprout": None,
        },
    },
}

__all__ = [SEEDS_INFO]
