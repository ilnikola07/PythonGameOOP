# units.py
from models import EntityInterface, Position

class Unit(EntityInterface):
    """Базовый класс юнита"""
    def move(self, new_pos, field):
        if not field.is_valid_pos(new_pos):
            print("За пределами карты!")
            return False
        terrain = field.get_terrain(new_pos)
        if not terrain.passable:
            print(f"Нельзя пройти через {terrain.name}")
            return False
        if field.get_entity_at(new_pos):
            print("Клетка занята!")
            return False
        self.position = new_pos
        return True

# --- Пехота (Ближний бой, Range=1, Устойчивость к ловушкам выше) ---
class Warrior(Unit):
    def __init__(self):
        super().__init__("Воин", 50, 10, "W", "\033[36m", range_=1)

class Guard(Unit):
    def __init__(self):
        super().__init__("Страж", 45, 12, "G", "\033[36m", range_=1)

# --- Лучники (Дальний бой, Range=2/3, Слабые к ловушкам) ---
class Archer(Unit):
    def __init__(self):
        super().__init__("Стрелок", 30, 15, "A", "\033[33m", range_=2)

class Marksman(Unit):
    def __init__(self):
        super().__init__("Снайпер", 35, 18, "S", "\033[33m", range_=3)

# --- Конница (Мобильность, Range=1) ---
class Rider(Unit):
    def __init__(self):
        super().__init__("Всадник", 60, 8, "R", "\033[35m", range_=1)

class Lancer(Unit):
    def __init__(self):
        super().__init__("Улан", 40, 14, "L", "\033[35m", range_=1)