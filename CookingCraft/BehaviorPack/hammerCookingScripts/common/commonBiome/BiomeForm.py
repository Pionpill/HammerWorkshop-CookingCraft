'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-30 17:02:38
LastEditTime: 2022-06-02 22:43:51
'''
from mod.common.minecraftEnum import BiomeType


class BiomeForm(object):
    """植物的生态群戏
    按温度分为: 热带，寒带，温带
    按地域分为: 海洋，河流，水系(海洋+河流)", 草原", 沙漠", 山地", 森林", 丛林", 恶地等
    按位面可分为: 地域，末地
    """
    # 热带
    tropic = {
        "desert", "desert_hills", "jungle", "jungle_hills", "jungle_edge",
        "savanna", "savanna_plateau", "mesa", "mesa_plateau_stone",
        "mega_taiga", "mega_taiga_hills", "mesa_plateau", "warm_ocean",
        "deep_warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean",
        "desert_mutated", "jungle_mutated", "jungle_edge_mutated",
        "savanna_mutated", "savanna_plateau_mutated", "mesa_bryce",
        "mesa_plateau_stone_mutated", "mesa_plateau_mutated"
    }
    # 温带
    temperate = {
        "ocean", "river", "plains", "extreme_hills", "forest", "beach",
        "forest_hills", "extreme_hills_edge", "birch_forest",
        "birch_forest_hills", "roofed_forest", "extreme_hills_plus_trees",
        "ocean", "legacy_frozen_ocean", "deep_ocean", "bamboo_jungle",
        "bamboo_jungle_hills", "sunflower_plains", "extreme_hills_mutated",
        "flower_forest", "swampland", "swampland_mutated",
        "birch_forest_mutated", "birch_forest_hills_mutated",
        "roofed_forest_mutated", "redwood_taiga_mutated",
        "redwood_taiga_hills_mutated", "extreme_hills_plus_trees_mutated",
        "mushroom_island", "mushroom_island_shore"
    }
    # 寒带
    frigid = {
        "taiga", "legacy_frozen_ocean", "frozen_river", "ice_plains",
        "ice_mountains", "taiga_hills", "cold_beach", "cold_taiga",
        "cold_taiga_hills", "cold_ocean", "deep_cold_ocean", "frozen_ocean",
        "deep_frozen_ocean", "taiga_mutated", "ice_plains_spikes",
        "cold_taiga_mutated", "redwood_taiga_mutated",
        "redwood_taiga_hills_mutated"
    }

    # 海洋，泛指咸水区域
    ocean = {
        "ocean", "legacy_frozen_ocean", "deep_ocean", "warm_ocean",
        "deep_warm_ocean", "lukewarm_ocean", "deep_lukewarm_ocean",
        "cold_ocean", "deep_cold_ocean", "frozen_ocean", "deep_frozen_ocean"
    }
    # 河流，泛指淡水区域
    river = {"river", "frozen_river", "desert_mutated"}

    # 平原，包括草原等
    plains = {
        "plains", "ice_plains", "savanna", "sunflower_plains",
        "ice_plains_spikes", "savanna_mutated"
    }
    savanna = {
        "savanna", "savanna_mutated", "savanna_plateau",
        "savanna_plateau_mutated"
    }

    # 高原
    plateau = {
        "savanna_plateau", "mesa_plateau", "savanna_plateau_mutated",
        "mesa_plateau_stone_mutated", "mesa_plateau_mutated"
    }
    # 恶地
    mesa = {
        "mesa", "mesa_plateau_stone", "mesa_plateau", "mesa_bryce",
        "mesa_plateau_stone_mutated", "mesa_plateau_mutated"
    }
    # 沙漠，包括沙漠山脉等
    desert = {"desert", "desert_hills", "desert_mutated"}
    # 山地，包括各种山地
    mountain = {
        "extreme_hills", "ice_mountains", "desert_hills", "forest_hills",
        "taiga_hills", "extreme_hills_edge", "jungle_hills",
        "birch_forest_hills", "cold_taiga_hills", "mega_taiga_hills",
        "extreme_hills_plus_trees", "bamboo_jungle_hills",
        "extreme_hills_mutated", "taiga_mutated", "swampland_mutated",
        "birch_forest_hills_mutated", "roofed_forest_mutated",
        "cold_taiga_mutated", "redwood_taiga_hills_mutated",
        "extreme_hills_plus_trees_mutated"
    }
    # 泛森林，包括各种森林
    woods = {
        "forest", "taiga", "forest_hills", "taiga_hills", "jungle",
        "jungle_hills", "jungle_edge", "birch_forest", "birch_forest_hills",
        "roofed_forest", "cold_taiga", "cold_taiga_hills", "mega_taiga",
        "mega_taiga_hills", "extreme_hills_plus_trees", "bamboo_jungle",
        "bamboo_jungle_hills", "flower_forest", "taiga_mutated",
        "jungle_mutated", "jungle_edge_mutated", "birch_forest_mutated",
        "birch_forest_hills_mutated", "roofed_forest_mutated",
        "cold_taiga_mutated", "redwood_taiga_mutated",
        "redwood_taiga_hills_mutated"
    }
    # 森林
    forest = {
        "forest", "forest_hills", "birch_forest", "birch_forest_hills",
        "birch_forest_hills_mutated", "birch_forest_mutated", "roofed_forest",
        "roofed_forest_mutated", "warped_forest", "flower_forest",
        "crimson_forest"
    }
    # 丛林
    jungle = {
        "jungle", "jungle_edge", "jungle_edge_mutated", "jungle_hills",
        "jungle_mutated"
    }
    # 针叶林
    taiga = {
        "taiga", "taiga_hills", "taiga_mutated", "cold_taiga",
        "cold_taiga_hills", "cold_taiga_mutated", "mega_taiga",
        "mega_taiga_hills", "redwood_taiga_hills_mutated",
        "redwood_taiga_mutated"
    }
    # 桦树林
    birch = {
        "birch_forest", "birch_forest_hills", "birch_forest_hills_mutated",
        "birch_forest_mutated"
    }

    # 竹林
    bamboo = {"bamboo_jungle", "bamboo_jungle_hills"}

    # 沼泽
    swamp = {"swampland", "swampland_mutated"}
    # 海岸
    shore = {"mushroom_island_shore"}
    # 蘑菇岛
    mushroom = {"mushroom_island", "mushroom_island_shore"}
    # 沙滩
    beach = {"beach", "stone_beach", "cold_beach"}
    # 边缘
    edge = {"extreme_hills_edge", "jungle_edge", "jungle_edge_mutated"}

    # 末地
    the_end = {"the_end"}
    # 地狱
    the_nether = {
        "hell", "soulsand_valley", "crimson_forest", "warped_forest",
        "basalt_deltas"
    }

    water = ocean | river
