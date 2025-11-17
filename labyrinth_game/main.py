#!/usr/bin/env python3

# Абсолютные импорты для корректной работы с Poetry
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    solve_puzzle,
)

# Состояние игрока
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}


def show_help(commands):
    """Показывает доступные команды с красивым форматированием"""
    print("Доступные команды:")
    for command, description in commands.items():
        # Форматируем команду с выравниванием в 16 символов
        formatted_command = command.ljust(16)
        print(f"  {formatted_command} - {description}")


def process_command(game_state, command):
    """Обрабатывает команды пользователя"""
    parts = command.split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    # Обработка односложных команд движения
    direction_commands = ['north', 'south', 'east', 'west']
    if main_command in direction_commands:
        move_player(game_state, main_command)
        # После перемещения показываем новую комнату
        describe_current_room(game_state)
        return
    
    if main_command in ['осмотреться', 'look', 'осмотр']:
        describe_current_room(game_state)
    
    elif main_command in ['инвентарь', 'inventory', 'инв']:
        show_inventory(game_state)
    
    elif main_command in ['выход', 'quit', 'exit']:
        print("Спасибо за игру!")
        game_state['game_over'] = True
    
    elif main_command in ['помощь', 'help']:
        show_help(COMMANDS)
    
    elif main_command in ['взять', 'take']:
        if argument:
            take_item(game_state, argument)
        else:
            print("Укажите предмет для взятия. Например: 'взять torch'")
    
    elif main_command in ['использовать', 'use']:
        if argument:
            use_item(game_state, argument)
        else:
            print("Укажите предмет для использования. Например: 'использовать torch'")
    
    elif main_command in ['идти', 'go']:
        if argument:
            move_player(game_state, argument)
            # После перемещения показываем новую комнату
            describe_current_room(game_state)
        else:
            print("Укажите направление. Например: 'идти north'")
    
    elif main_command in ['решить', 'solve']:
        # В treasure_room команда solve всегда открывает сундук
        if game_state['current_room'] == 'treasure_room':
            attempt_open_treasure(game_state)
        else:
            # В других комнатах решаем загадки
            solve_puzzle(game_state)
    
    elif main_command in ['открыть', 'open']:
        attempt_open_treasure(game_state)
    
    else:
        print("Неизвестная команда. Напишите 'помощь' для списка команд.")


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    # Описание стартовой комнаты
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("\nЧто вы хотите сделать? ")
        process_command(game_state, command)
    
    print("Игра завершена. Спасибо за игру!")


if __name__ == "__main__":
    main()
