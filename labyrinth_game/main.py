#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS

# Состояние игрока
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    print("Первая попытка запустить проект!")
    print(f"Текущая комната: {game_state['current_room']}")
    print(f"Описание комнаты: {ROOMS[game_state['current_room']]['description']}")
    print(f"Инвентарь: {game_state['player_inventory']}")
    print(f"Шагов сделано: {game_state['steps_taken']}")


if __name__ == "__main__":
    main()
