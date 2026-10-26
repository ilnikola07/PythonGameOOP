# units.py
from models import EntityInterface, Position
from objects import NeutralObjectInterface  # <-- ВАЖНО: импорт добавлен


class Unit(EntityInterface):
    """Базовый класс юнита"""
    def move(self, new_pos, field):
        # 1. Проверка границ карты
        if not field.is_valid_pos(new_pos):
            print("За пределами карты!")
            return False
        
        # 2. Сначала проверяем, есть ли на клетке объект
        entity_at_pos = field.get_entity_at(new_pos)
        if entity_at_pos:
            # Если там нейтральный объект (золото, аптечка, ловушка, дерево) —
            # разрешаем встать, игнорируя ландшафт под ним
            if isinstance(entity_at_pos, NeutralObjectInterface):
                self.position = new_pos
                return True
            else:
                # Другой юнит или база — нельзя
                print("Клетка занята!")
                return False
        
        # 3. Если объекта нет — проверяем ландшафт
        terrain = field.get_terrain(new_pos)
        if not terrain.passable:
            print(f"Нельзя пройти через {terrain.name}")
            return False
        
        self.position = new_pos
        return True


# --- Пехота ---
class Warrior(Unit):
    def __init__(self):
        super().__init__("Воин", 50, 10, "W", "\033[36m", range_=1)

class Guard(Unit):
    def __init__(self):
        super().__init__("Страж", 45, 12, "G", "\033[36m", range_=1)

# --- Лучники ---
class Archer(Unit):
    def __init__(self):
        super().__init__("Стрелок", 30, 15, "A", "\033[33m", range_=2)

class Marksman(Unit):
    def __init__(self):
        super().__init__("Снайпер", 35, 18, "S", "\033[33m", range_=3)

# --- Конница ---
class Rider(Unit):
    def __init__(self):
        super().__init__("Всадник", 60, 8, "R", "\033[35m", range_=1)

class Lancer(Unit):
    def __init__(self):
        super().__init__("Улан", 40, 14, "L", "\033[35m", range_=1)