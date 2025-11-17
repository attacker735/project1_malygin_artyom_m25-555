#!/usr/bin/env python3

def get_rooms():
    from labyrinth_game.constants import ROOMS
    return ROOMS


def show_inventory(game_state):
    """Отображает инвентарь игрока"""
    inventory = game_state.get('player_inventory', [])
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")


def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой прерываний"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении"""
    ROOMS = get_rooms()
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    exits = room_data.get('exits', {})
    
    if direction in exits:
        new_room = exits[direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"Вы переместились {direction} в {new_room}.")
        
        from labyrinth_game.utils import random_event
        random_event(game_state)
        
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False


def take_item(game_state, item_name):
    """Позволяет игроку взять предмет из комнаты"""
    # Нельзя поднять сундук
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False
    
    ROOMS = get_rooms()
    current_room = game_state['current_room']
    room_data = ROOMS.get(current_room, {})
    items = room_data.get('items', [])
    
    if item_name in items:
        # Добавляем предмет в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем предмет из комнаты
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False


def use_item(game_state, item_name):
    """Позволяет игроку использовать предмет из инвентаря"""
    inventory = game_state.get('player_inventory', [])
    
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return False
    
    # Уникальные действия для каждого предмета
    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы почувствовали уверенность, держа меч в руках.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            game_state['player_inventory'].append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли внутри rusty_key!")
        else:
            print("Шкатулка пуста.")
    elif item_name == 'coin':
        print("Вы подбрасываете монетку. Она блестит в свете.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
    
    return True
