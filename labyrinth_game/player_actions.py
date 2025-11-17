#!/usr/bin/env python3

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
