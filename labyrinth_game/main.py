#!/usr/bin/env python3

# Абсолютные импорты для корректной работы с Poetry
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


def process_command(game_state, command):
    """Обрабатывает команды пользователя"""
    parts = command.split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    if main_command in ['осмотреться', 'look', 'осмотр']:
        describe_current_room(game_state)
    
    elif main_command in ['инвентарь', 'inventory', 'инв']:
        show_inventory(game_state)
    
    elif main_command in ['выход', 'quit', 'exit']:
        print("Спасибо за игру!")
        game_state['game_over'] = True
    
    elif main_command in ['помощь', 'help']:
        print("Доступные команды:")
        print("  осмотреться - посмотреть вокруг")
        print("  инвентарь - посмотреть инвентарь")
        print("  взять [предмет] - подобрать предмет")
        print("  использовать [предмет] - использовать предмет")
        print("  идти [направление] - переместиться")
        print("  решить - решить загадку в текущей комнате")
        print("  открыть - попытаться открыть сундук с сокровищами")
        print("  выход - выйти из игры")
        print("  помощь - показать эту подсказку")
    
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
        # Если в treasure_room, пытаемся открыть сундук
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
