'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-02 15:57:46
LastEditTime: 2022-08-24 15:15:45
'''
cookingRecipes = {
    "minecraft:apple": {
        "materials": {
            "material_slot4": "minecraft:apple"
        },
        "results": {
            "newItemName": "minecraft:apple"
        }
    },
    "cookingcraft:seasoning": {
        "materials": {
            "material_slot3": {
                "newItemName": "cookingcraft:spices",
                "count": 2
            },
            "material_slot4": {
                "newItemName": "cookingcraft:chill_powder"
            }
        },
        "results": {
            "newItemName": "cookingcraft:seasoning",
            "count": 3
        }
    },
    "cookingcraft:raw_apple_pie": {
        "materials": {
            "material_slot3": "minecraft:apple",
            "material_slot5": "minecraft:apple",
            "material_slot6": "cookingcraft:flour",
            "material_slot7": "cookingcraft:flour",
            "material_slot8": "cookingcraft:flour",
            "material_slot10": "minecraft:sugar",
            "material_slot12": "cookingcraft:seasoning"
        },
        "results": {
            "newItemName": "cookingcraft:raw_apple_pie",
            "newAuxValue": 0,
            "count": 3
        }
    },
    "cookingcraft:raw_carrot_pie": {
        "materials": {
            "material_slot1": {
                "newItemName": "minecraft:sugar",
                "count": 3
            },
            "material_slot3": "minecraft:carrot",
            "material_slot4": "minecraft:carrot",
            "material_slot5": "minecraft:carrot",
            "material_slot6": "cookingcraft:flour",
            "material_slot7": "cookingcraft:flour",
            "material_slot8": "cookingcraft:flour"
        },
        "results": {
            "newItemName": "cookingcraft:raw_carrot_pie",
            "count": 3
        }
    },
    "cookingcraft:raw_egg_pie": {
        "materials": {
            "material_slot0": "cookingcraft:seasoning",
            "material_slot1": {
                "newItemName": "minecraft:sugar",
                "count": 3
            },
            "material_slot2": "cookingcraft:seasoning",
            "material_slot3": "minecraft:egg",
            "material_slot4": "minecraft:egg",
            "material_slot5": "minecraft:egg",
            "material_slot6": "cookingcraft:flour",
            "material_slot7": "cookingcraft:flour",
            "material_slot8": "cookingcraft:flour"
        },
        "results": {
            "newItemName": "cookingcraft:raw_egg_pie",
            "count": 3
        }
    },
    "cookingcraft:raw_berry_pie": {
        "materials": {
            "material_slot3": "minecraft:sweet_berries",
            "material_slot4": {
                "newItemName": "minecraft:glow_berries",
                "count": 3
            },
            "material_slot5": "minecraft:sweet_berries",
            "material_slot6": "cookingcraft:flour",
            "material_slot7": "cookingcraft:flour",
            "material_slot8": "cookingcraft:flour",
        },
        "results": {
            "newItemName": "cookingcraft:raw_berry_pie",
            "count": 3
        }
    }
}
