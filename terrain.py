# terrain.py
from models import TerrainInterface

class Grass(TerrainInterface):
    def __init__(self):
        super().__init__("Трава", ".", True, "\033[32m")

class Water(TerrainInterface):
    def __init__(self):
        super().__init__("Вода", "~", False, "\033[34m")

class Mountain(TerrainInterface):
    def __init__(self):
        super().__init__("Горы", "^", False, "\033[37m")