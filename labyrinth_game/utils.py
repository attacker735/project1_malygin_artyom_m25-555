#!/usr/bin/env python3

import math

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
    
    # Создаем список альтернативных ответов
    alternative_answers = []
    
    # Для числовых ответов добавляем текстовые альтернативы
    if correct_answer == '10':
        alternative_answers = ['десять', '10']
    elif correct_answer == 'шаг шаг шаг':
        alternative_answers = ['шаг шаг шаг', 'step step step']
    elif correct_answer == 'резонанс':
        alternative_answers = ['резонанс', 'resonance']
    elif correct_answer == 'дыхание':
        alternative_answers = ['дыхание', 'breath']
    elif correct_answer == 'обещание':
        alternative_answers = ['обещание', 'promise']
    else:
        alternative_answers = [correct_answer]
    
    # Проверяем ответ
    if user_answer.lower() in [ans.lower() for ans in alternative_answers]:
        print("Верно! Загадка решена.")
        
        # Награда за решение загадки зависит от комнаты
        if current_room == 'hall':
            print("Пьедестал опускается, открывая проход на север.")
        elif current_room == 'trap_room':
            print("Плиты пола перестают двигаться. Теперь можно безопасно пройти.")
        elif current_room == 'library':
            print("Один из свитков светится, указывая на скрытый отсек.")
        elif current_room == 'garden':
            print("Цветок расцветает, и вы чувствуете прилив сил.")
        elif current_room == 'forge':
            print("Механизм в стене щёлкает, открывая потайной ящик.")
        
        # Убираем загадку из комнаты
        room_data['puzzle'] = None
        return True
    else:
        print("Неверно. Попробуйте снова.")
        
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            print("Неверный ответ активирует ловушку!")
            trigger_trap(game_state)
        
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
            
            # Для кода также принимаем альтернативные варианты
            if user_code == correct_code or (correct_code == '10' and user_code == 'десять'):
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


def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное число в диапазоне [0, modulo)
    на основе синусоидальной функции для предсказуемой случайности
    """
    # Используем синус для генерации "случайного" значения
    sin_value = math.sin(seed * 12.9898)
    multiplied = sin_value * 43758.5453
    
    # Получаем дробную часть
    fractional = multiplied - math.floor(multiplied)
    
    # Приводим к нужному диапазону и возвращаем целое число
    result = int(fractional * modulo)
    return result


def trigger_trap(game_state):
    """
    Обрабатывает срабатывание ловушки - удаляет случайный предмет
    или наносит урон игроку
    """
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state.get('player_inventory', [])
    
    if inventory:
        # Выбираем случайный предмет для удаления
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Из-за тряски вы потеряли: {lost_item}!")
    else:
        # Если инвентарь пуст - наносим "урон"
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:  # 30% шанс проигрыша
            print("Сильная тряска сбивает вас с ног! Вы падаете и теряете сознание...")
            game_state['game_over'] = True
        else:
            print("Вам удается удержаться на ногах, но это было близко!")


def random_event(game_state):
    """
    Случайные события, которые могут произойти при перемещении игрока
    """
    # Проверяем, происходит ли событие (10% шанс)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    if event_chance != 0:
        return  # Событие не происходит
    
    # Выбираем тип события
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    
    print("\n--- Случайное событие! ---")
    
    if event_type == 0:
        # Находка: добавляем монетку в текущую комнату
        if 'coin' not in room_data.get('items', []):
            room_data.setdefault('items', []).append('coin')
            print("Вы заметили блестящую монетку на полу! Она добавлена в комнату.")
    
    elif event_type == 1:
        # Испуг: шорох
        print("Вы слышите странный шорох из темного угла...")
        if 'sword' in game_state.get('player_inventory', []):
            print("Вы достаете меч, и шорох мгновенно прекращается.")
        else:
            print("Шорох усиливается... Вам стало не по себе.")
    
    elif event_type == 2:
        # Срабатывание ловушки (только в trap_room без факела)
        if (current_room == 'trap_room' and 
            'torch' not in game_state.get('player_inventory', [])):
            print("В темноте вы не заметили ловушку под ногами!")
            trigger_trap(game_state)
        else:
            # Если условия не выполнены, превращаем в обычную находку
            if 'coin' not in room_data.get('items', []):
                room_data.setdefault('items', []).append('coin')
                print("На вашем пути лежит забытая монетка!")
    
    print("--- Событие завершено ---\n")
