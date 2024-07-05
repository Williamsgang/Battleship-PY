# main.py

from battleship import bsp


player1 = bsp.Player()
player2 = bsp.Player()

print("Player 1's ships:")

player1.show_ships(player1)


print()
print('===============================')
print()

print("Player 2's ships:")
player2.show_ships(player2)
