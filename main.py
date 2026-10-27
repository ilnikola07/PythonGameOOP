# main.py
import random
from models import Position
from terrain import Grass, Water, Mountain
from objects import HealthPotion, GoldCoin, Trap, Tree
from bases import Base
from units import Unit  

RESET = "\033[0m"

class GameField:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.entities = {}
        
        for y in range(height):
            for x in range(width):
                r = random.random()
                if r < 0.85: self.grid[y][x] = Grass()
                elif r < 0.95: self.grid[y][x] = Water()
                else: self.grid[y][x] = Mountain()
        
        self._place_neutrals()

    def _place_neutrals(self):
        neutrals = [HealthPotion(), GoldCoin(), Trap(), Tree()]
        for _ in range(10):
            attempts = 0
            while attempts < 50:
                pos = Position(random.randint(0, self.width-1), random.randint(0, self.height-1))
                terrain = self.grid[pos.y][pos.x]
                # Спавним только на проходимом ландшафте и на пустой клетке
                if terrain.passable and not self.get_entity_at(pos):
                    obj = random.choice(neutrals)
                    self.entities[pos] = obj
                    break
                attempts += 1

    def is_valid_pos(self, pos):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def get_terrain(self, pos):
        if self.is_valid_pos(pos): return self.grid[pos.y][pos.x]
        return None

    def get_entity_at(self, pos):
        return self.entities.get(pos)

    def add_entity(self, entity, pos):
        if self.is_valid_pos(pos) and pos not in self.entities:
            entity.position = pos
            self.entities[pos] = entity
            return True
        return False

    def remove_entity(self, pos):
        if pos in self.entities: del self.entities[pos]

    def move_entity(self, entity, new_pos):
        old_pos = entity.position
        if entity.move(new_pos, self):
            obj = self.get_entity_at(new_pos)
            if obj:
                try:
                    obj + entity
                    if isinstance(obj, (HealthPotion, GoldCoin)):
                        self.remove_entity(new_pos)
                except: pass
            
            self.entities[new_pos] = entity
            if old_pos in self.entities and self.entities[old_pos] == entity:
                 del self.entities[old_pos]
            return True
        return False

    def draw(self):
        CELL = 3
        print(" " * 4, end="")
        for x in range(self.width): print(f"{x:>{CELL}}", end="")
        print()
        
        for y in range(self.height):
            print(f"{y:3} ", end="")
            for x in range(self.width):
                pos = Position(x, y)
                ent = self.get_entity_at(pos)
                if ent:
                    print(f" {ent.color}{ent.symbol}{RESET} ", end="")
                else:
                    terrain = self.grid[y][x]
                    print(f" {terrain.color}{terrain.symbol}{RESET} ", end="")
            print(f"{y}")
        
        print(" " * 4, end="")
        for x in range(self.width): print(f"{x:>{CELL}}", end="")
        print()


def print_legend():
    print("\nЛЕГЕНДА ")
    print("Юниты:      W-Воин  G-Страж  A-Стрелок  S-Снайпер  R-Всадник  L-Улан")
    print("Объекты:    +-Аптечка  $-Золото  x-Ловушка  T-Дерево")
    print("Ландшафт:   .-Трава  ~-Вода  ^-Горы")
    print(" \n")


def main():
    width, height = 15, 15
    field = GameField(width, height)
    
    player_base = Base(" ", 1)
    base_pos = Position(1, 1)
    field.add_entity(player_base, base_pos)
    
    # СТАРТОВЫЙ ЮНИТ УБРАН. ИГРА НАЧИНАЕТСЯ С ПУСТОЙ БАЗОЙ.
    
    print("Консольная стратегия \n")
    
    while True:
        field.draw()
        print_legend()
        
        print("ГЛАВНОЕ МЕНЮ ")
        print("1 - Управление базой")
        print("2 - Управление юнитом")
        print("3 - Состояние базы")
        print("4 - Выход")
        
        choice = input("\nВыбор: ").strip()
        
        if choice == "1":
            print("\nУправление базой ")
            print("1 - Создать юнита (10 золота)")
            print("2 - Назад")
            sub = input("Выбор: ").strip()
            
            if sub == "1":
                print("\nДоступные типы:")
                print("1 - Воин (Здоровье:50, Урон:10, Дальноость:1)")
                print("2 - Страж (Здоровье:45, Урон:12, Дальноость:1)")
                print("3 - Стрелок (Здоровье:30, Урон:15, Дальноость:2)")
                print("4 - Снайпер (Здоровье:35, Урон:18, Дальноость:3)")
                print("5 - Всадник (Здоровье:60, Урон:8, Дальноость:1)")
                print("6 - Улан (Здоровье:40, Урон:14, Дальноость:1)")
                
                t_map = {"1":"Warrior","2":"Guard","3":"Archer","4":"Marksman","5":"Rider","6":"Lancer"}
                t_choice = input("Тип: ").strip()
                
                if t_choice in t_map:
                    spawn_pos = Position(base_pos.x + 1, base_pos.y)
                    if not field.get_entity_at(spawn_pos):
                        new_u = player_base.create_unit(t_map[t_choice], spawn_pos, field)
                        if new_u:
                            print(f"Юнит {new_u.name} создан и готов к бою!")
                    else:
                        print("Клетка рядом с базой занята! Освободите её или переместите юнитов.")
                else:
                    print("Неверный выбор.")
                    
        elif choice == "2":
            units_list = player_base.my_units
            if not units_list:
                print("\nНет юнитов! Создайте их через меню базы.")
                continue
                
            print("\nВыберите юнита ")
            for i, u in enumerate(units_list):
                print(f"{i+1}. {u} на {u.position}")
            
            try:
                u_idx = int(input("Номер юнита: ")) - 1
                if 0 <= u_idx < len(units_list):
                    active_unit = units_list[u_idx]
                    
                    while True:
                        field.draw()
                        print_legend()

                        print(f"\nУправление: {active_unit.name} ")
                        print("1 - Переместить")
                        print("2 - Атаковать")
                        print("3 - Состояние")
                        print("4 - Назад в меню юнитов")
                        
                        act = input("Действие: ").strip()
                        
                        if act == "1":
                            print("Направления: 1-Вверх 2-Вниз 3-Влево 4-Вправо")
                            d = input("Куда: ").strip()
                            x, y = active_unit.position.x, active_unit.position.y
                            if d=="1": y-=1
                            elif d=="2": y+=1
                            elif d=="3": x-=1
                            elif d=="4": x+=1
                            
                            field.move_entity(active_unit, Position(x, y))
                            if active_unit.hp <= 0:
                                player_base.remove_unit(active_unit)
                                break
                                
                        elif act == "2":
                            # Поиск целей в радиусе: вражеские юниты + деревья
                            targets = []
                            for e_pos, e in field.entities.items():
                                if e == active_unit:
                                    continue
                                if active_unit.position.distance_to(e_pos) <= active_unit.range:
                                    if isinstance(e, Unit):
                                        targets.append((e_pos, e, "unit"))
                                    elif isinstance(e, Tree):
                                        targets.append((e_pos, e, "tree"))
                            
                            if not targets:
                                print("Нет целей в радиусе атаки!")
                            else:
                                print("Доступные цели:")
                                for i, (pos, t, ttype) in enumerate(targets):
                                    if ttype == "unit":
                                        print(f"{i+1}. {t} на {pos} [Враг]")
                                    else:
                                        print(f"{i+1}. {t.name} на {pos} [Дерево]")
                                try:
                                    t_idx = int(input("Цель: ")) - 1
                                    target_pos, target, ttype = targets[t_idx]
                                    if ttype == "unit":
                                        is_dead = active_unit - target
                                        if is_dead:
                                            player_base.remove_unit(target)
                                            field.remove_entity(target_pos)
                                    else:
                                        # Срубаем дерево
                                        field.remove_entity(target_pos)
                                        print(f"\033[32m{active_unit.name} срубил дерево!\033[0m")
                                except (ValueError, IndexError):
                                    print("Ошибка выбора цели.")
                                
                        elif act == "3":
                            print(f"\nИмя: {active_unit.name}")
                            print(f"Здоровье: {active_unit.hp}/{active_unit.max_hp}")
                            print(f"Атака: {active_unit.attack}")
                            print(f"Дальность: {active_unit.range}")
                            print(f"Позиция: {active_unit.position}")
                            input("Enter...")
                            
                        elif act == "4":
                            break
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число!")
                
        elif choice == "3":
            print("\n" + player_base.get_status())
            input("\nНажмите Enter...")
            
        elif choice == "4":
            print("Игра завершена.")
            break
            
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()