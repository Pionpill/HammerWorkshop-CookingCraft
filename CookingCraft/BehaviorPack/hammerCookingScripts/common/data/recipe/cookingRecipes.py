'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-02 15:57:46
LastEditTime: 2022-08-14 00:11:55
'''
cookingRecipes = {
    "minecraft:apple": {
        "materials": {
            "material_slot4": {
                "newItemName": "minecraft:apple"
            }
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
            "material_slot1": {
                "newItemName": "cookingcraft:seasoning"
            },
            "material_slot3": {
                "newItemName": "minecraft:apple"
            },
            "material_slot4": {
                "newItemName": "minecraft:sugar"
            },
            "material_slot5": {
                "newItemName": "minecraft:apple"
            },
            "material_slot6": {
                "newItemName": "cookingcraft:flour"
            },
            "material_slot7": {
                "newItemName": "cookingcraft:flour"
            },
            "material_slot8": {
                "newItemName": "cookingcraft:flour"
            }
        },
        "results": {
            "newItemName": "cookingcraft:raw_apple_pie",
            "newAuxValue": 0,
            "count": 3
        }
    },
    "cookingcraft:raw_carrot_pie": {
        "materials": {
            "material_slot0": None,
            "material_slot1": {
                "newItemName": "minecraft:sugar",
                "count": 3
            },
            "material_slot2": None,
            "material_slot3": {
                "newItemName": "minecraft:carrot",
            },
            "material_slot4": {
                "newItemName": "minecraft:carrot",
            },
            "material_slot5": {
                "newItemName": "minecraft:carrot",
            },
            "material_slot6": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot7": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot8": {
                "newItemName": "cookingcraft:flour",
            }
        },
        "results": {
            "newItemName": "cookingcraft:raw_carrot_pie",
            "count": 3
        }
    },
    "cookingcraft:raw_egg_pie": {
        "materials": {
            "material_slot0": {
                "newItemName": "cookingcraft:seasoning",
            },
            "material_slot1": {
                "newItemName": "minecraft:sugar",
                "count": 3
            },
            "material_slot2": {
                "newItemName": "cookingcraft:seasoning",
            },
            "material_slot3": {
                "newItemName": "minecraft:egg",
            },
            "material_slot4": {
                "newItemName": "minecraft:egg",
            },
            "material_slot5": {
                "newItemName": "minecraft:egg",
            },
            "material_slot6": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot7": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot8": {
                "newItemName": "cookingcraft:flour",
            }
        },
        "results": {
            "newItemName": "cookingcraft:raw_egg_pie",
            "count": 3
        }
    },
    "cookingcraft:raw_berry_pie": {
        "materials": {
            "material_slot3": {
                "newItemName": "minecraft:sweet_berries",
            },
            "material_slot4": {
                "newItemName": "minecraft:glow_berries",
                "count": 3
            },
            "material_slot5": {
                "newItemName": "minecraft:sweet_berries",
            },
            "material_slot6": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot7": {
                "newItemName": "cookingcraft:flour",
            },
            "material_slot8": {
                "newItemName": "cookingcraft:flour",
            }
        },
        "results": {
            "newItemName": "cookingcraft:raw_berry_pie",
            "count": 3
        }
    }
}
