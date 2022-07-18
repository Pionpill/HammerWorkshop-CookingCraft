from hammerCookingScripts.common.data.plants import SEEDS_INFO
from hammerCookingScripts import logger


class Plant(object):
    """植物类，提供植物种植，生长相关的数据信息
    """
    def __init__(self, seedName):
        # type: (str) -> None
        object.__init__(self)
        self.seedName = seedName
        self._seedInfo = SEEDS_INFO.get(seedName)
        self._InitAttr()
        del self._seedInfo

    def _InitAttr(self):
        try:
            self._tickList = self._seedInfo.get("tickList")
            self._harvestCount = self._seedInfo.get("harvestCount")
        except KeyError:
            logger.warn("{self.seedName} 未设置 tickList/harvestCount 值")

        self._harvestBlock = self._seedInfo.get("harvestBlock", None)
        self._lootTable = self._seedInfo.get("lootTable", None)
        if self._lootTable:
            try:
                self._lootItemName = self._lootTable.get("newItemName")
                self._lootItemCount = self._lootTable.get("count")
                self._lootItemAux = self._lootTable.get("newAuxValue")
            except KeyError:
                logger.error("{self.seedName} 的 lootTable 存在未设置的值")

        try:
            plantConditions = self._seedInfo.get("plantConditions")
            self._plantLandList = plantConditions.get("plantLandList")
            self._plantBiome = plantConditions.get("plantBiome")
            self._plantSpecial = plantConditions.get("special", None)
            del plantConditions
        except KeyError:
            logger.error("{self.seedName} 的 plantsConditions 存在未设置的值")

        try:
            growthConditions = self._seedInfo.get("growthConditions")
            self._brightness = growthConditions.get("brightness")
            self._altitude = growthConditions.get("altitude")
            self._weather = growthConditions.get("Weather", None)
            self._sprout = growthConditions.get("sprout", None)
            self._growthSpecial = growthConditions.get("special", None)
            del growthConditions
        except KeyError:
            logger.error("{self.seedName} 的 growthConditions 存在未设置的值")

    def GetTickList(self):
        # type: () -> list
        """植物生长的 tick 列表"""
        return self._tickList

    def GetHarvestCount(self):
        # type: () -> int
        """植物可收获的次数"""
        return self._harvestCount

    def GetHarvestBlock(self):
        # type: () -> str/None
        """收获后回到的方块名"""
        return self._harvestBlock

    def GetPlantLandList(self):
        # type: () -> list
        """可种植的土地列表"""
        return self._plantLandList

    def GetPlantBiome(self):
        # type: () -> set
        """植物生长的生态集合"""
        return self._plantBiome

    def GetGrowthBrightness(self):
        # type: () -> tuple
        """光照需求，(min,max)"""
        return self._brightness

    def GetGrowthAltitude(self):
        # type: () -> tuple
        """海拔需求，(min,max)"""
        return self._altitude

    def GetGrowthWeather(self):
        # type: () -> str
        """生长需要的天气需求,可以是 'rain'/'thunder'"""
        return self._weather

    def GetGrowthSprout(self):
        # type: () -> list
        """发芽需求，可以是 'rain'/'thunder'"""
        return self._sprout

    def GetGrowthSpecial(self):
        # type: () -> dict
        """特殊生长需求，目前提供 "water" 键"""
        return self._growthSpecial

    def GetPlantSpecial(self):
        # type: () -> dict
        """特殊种植需求"""
        return self._plantSpecial

    def GetLootTable(self):
        # type: () -> dict
        """多次收获的掉落物，包含 "newItemName": str；"count": tuple；"newAuxValue": int 键
        """
        return self._lootTable

    def GetLootItemName(self):
        # type: () -> str
        """掉落物全称"""
        return self._lootItemName

    def GetLootItemCount(self):
        # type: () -> tuple
        """收获数 (min,max)"""
        return self._lootItemCount

    def GetLootItemAux(self):
        # type: () -> int
        """物品附加值，一般为 0"""
        return self._lootItemAux
