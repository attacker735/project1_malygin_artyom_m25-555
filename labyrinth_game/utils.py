#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS


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
