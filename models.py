# models.py

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x},{self.y})"

    def distance_to(self, other):
        """Манхэттенское расстояние для сетки"""
        return abs(self.x - other.x) + abs(self.y - other.y)


class EntityInterface:
    """Общий интерфейс для всех сущностей"""
    def __init__(self, name, hp, attack, symbol, color, range_=1):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.symbol = symbol
        self.color = color
        self.range = range_  # Дальность атаки/взаимодействия
        self.position = None

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return self.hp <= 0

    def __str__(self):
        return f"{self.name} [HP:{self.hp}/{self.max_hp} Atk:{self.attack} Rng:{self.range}]"

    # Перегрузка оператора "-" для атаки
    def __sub__(self, target):
        dist = self.position.distance_to(target.position) if target.position else 999
        if dist <= self.range:
            print(f"\033[31m{self.name} атакует {target.name}! Нанесено {self.attack} урона.\033[0m")
            is_dead = target.take_damage(self.attack)
            if is_dead:
                print(f"\033[31m{target.name} уничтожен!\033[0m")
            return is_dead
        else:
            print(f"\033[33mЦель слишком далеко! (Дистанция: {dist}, Макс: {self.range})\033[0m")
            return False


class TerrainInterface:
    """Интерфейс ландшафта"""
    def __init__(self, name, symbol, passable=True, color="\033[32m"):
        self.name = name
        self.symbol = symbol
        self.passable = passable
        self.color = color


class NeutralObjectInterface:
    """Интерфейс нейтральных объектов"""
    def __init__(self, name, symbol, color="\033[33m"):
        self.name = name
        self.symbol = symbol
        self.color = color