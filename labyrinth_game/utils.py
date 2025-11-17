#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def describe_current_room(game_state):
    """Выводит описание текущей комнаты"""
    current_room_name = game_state['current_room']
    room_data = ROOMS.get(current_room_name, {})
    
    if not room_data:
        print("Ошибка: комната не найдена")
        return
    
    # Название комнаты в верхнем регистре
    print(f"== {current_room_name.upper()} ==")
    
    # Описание комнаты
    print(room_data.get('description', 'Нет описания'))
    
    # Список предметов
    items = room_data.get('items', [])
    if items:
        print("Заметные предметы:", ", ".join(items))
    
    # Доступные выходы
    exits = room_data.get('exits', {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))
    
    # Сообщение о загадке
    if room_data.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Позволяет игроку решить загадку в текущей комнате"""
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    puzzle = room_data.get('puzzle')
    
    if not puzzle:
        print("Загадок здесь нет.")
        return False
    
    question, correct_answer = puzzle
    print(question)
    
    user_answer = get_input("Ваш ответ: ")
    
    if user_answer.lower() == correct_answer.lower():
        print("Верно! Загадка решена.")
        # Убираем загадку из комнаты
        room_data['puzzle'] = None
        return True
    else:
        print("Неверно. Попробуйте снова.")
        return False


def attempt_open_treasure(game_state):
    """Пытается открыть сундук с сокровищами"""
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    
    # Проверяем, что игрок в комнате с сокровищами и есть сундук
    if current_room != 'treasure_room' or 'treasure_chest' not in room_data.get('items', []):
        print("Здесь нет сундука с сокровищами.")
        return False
    
    # Проверяем наличие ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        # Удаляем сундук из комнаты
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. У вас нет ключа. Попробовать ввести код?")
    choice = get_input("Ввести код? (да/нет): ")
    
    if choice.lower() in ['да', 'yes', 'y']:
        # Используем загадку из комнаты для кода
        puzzle = room_data.get('puzzle')
        if puzzle:
            _, correct_code = puzzle
            user_code = get_input("Введите код: ")
            
            if user_code == correct_code:
                print("Код верный! Сундук открыт!")
                room_data['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код.")
                return False
        else:
            print("Нет возможности ввести код.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False
