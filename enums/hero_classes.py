from enum import Enum


class HeroClass(str, Enum):
    warrior = "warrior"
    hunter = "hunter"
    mage = "mage"
    druid = "druid"
