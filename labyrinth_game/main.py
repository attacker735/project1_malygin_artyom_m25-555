#!/usr/bin/env python3

try:
    # Для запуска через poetry run project (из корня проекта)
    from labyrinth_game.constants import ROOMS
    from labyrinth_game.player_actions import get_input, show_inventory
    from labyrinth_game.utils import describe_current_room
except ImportError:
    # Для прямого запуска python3 main.py из директории labyrinth_game
    from constants import ROOMS
    from player_actions import get_input, show_inventory
    from utils import describe_current_room

# Состояние игрока
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    # Описание стартовой комнаты
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("\nЧто вы хотите сделать? ")
        
        if command in ['выход', 'quit', 'exit']:
            print("Спасибо за игру!")
            game_state['game_over'] = True
        
        elif command in ['осмотреться', 'look', 'осмотр']:
            describe_current_room(game_state)
        
        elif command in ['инвентарь', 'inventory', 'инв']:
            show_inventory(game_state)
        
        elif command in ['помощь', 'help']:
            print("Доступные команды:")
            print("  осмотреться - посмотреть вокруг")
            print("  инвентарь - посмотреть инвентарь")
            print("  выход - выйти из игры")
            print("  помощь - показать эту подсказку")
        
        else:
            print("Неизвестная команда. Напишите 'помощь' для списка команд.")


if __name__ == "__main__":
    main()
