'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 12:59:32
LastEditTime: 2022-07-11 14:16:55
'''
from hammerCookingScripts.common.data.biome.BiomeForm import BiomeForm as BF


class PlantsBiomeForm(object):
    """植被生态群戏
    按温度分为: 热(high)，适中(medium)，冷(low)
    按降水分为: 湿润(high)，适中(medium)，干燥(low)
    按海拔分为: 高(high)，中(medium)，低(low)
    按土地分为: 草地(grass)，沙地(sand)，蘑菇(mushroom)，恶地(mesa)，水系(water)，石头(stone)
    特殊群戏
    """
    temperature = {"high": BF.tropic, "medium": BF.temperate, "low": BF.frigid}

    rainfall = {
        "high":
        BF.forest | BF.jungle | BF.birch | BF.swamp,
        "medium":
        BF.ocean | BF.river | BF.plains | BF.plateau | BF.mountain | BF.taiga
        | BF.shore | BF.mushroom | BF.beach,
        "low":
        BF.savanna | BF.mesa | BF.desert
    }

    altitude = {
        "high":
        BF.plateau | BF.mesa | BF.mountain,
        "medium":
        BF.river | BF.plains | BF.savanna | BF.desert | BF.forest | BF.jungle
        | BF.taiga | BF.birch | BF.bamboo | BF.mushroom | BF.swamp | BF.shore
        | BF.beach,
        "low":
        BF.ocean | BF.river
    }

    land = {
        "grass":
        BF.plains | BF.savanna | BF.plateau | BF.forest | BF.jungle | BF.taiga
        | BF.birch | BF.bamboo | BF.swamp,
        "sand":
        BF.desert | BF.shore | BF.beach,
        "mushroom":
        BF.mushroom,
        "mesa":
        BF.mesa,
        "water":
        BF.ocean | BF.river,
        "stone":
        BF.mountain
    }

    special = {
        "mesa": BF.mesa,
        "desert": BF.desert,
        "jungle": BF.jungle,
        "bamboo": BF.bamboo,
        "taiga": BF.taiga
    }

    common = land["grass"] | altitude["medium"]


__all__ = [PlantsBiomeForm]
