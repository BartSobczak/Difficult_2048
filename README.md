Bartek's Difficult 2048

Hello,
Here's my implementation of a popular game known as 2048. The gameplay is based on standard 2048 rules, 
except for a feature I've added to make the game more difficult - the obstacles.

Currently, the user can select up to 8 obstacles to be spawned to the board in random places. 
The user can also choose 0 obstacles for standard gameplay.
An obstacle is represented by a blue cell/box with a sad emote ";(". It can be moved along with other cells,
but cannot be merged to any other cell and stays within the board till the end of the game.
The obstacle is coded as a standard cell, only having a unique odd number instead of an even one.

Also, handling and displaying the grid of board cells in the GUI file is based/inspired by Kite's youtube tutorial:
https://youtu.be/b4XP2IcI-Bg?si=yxHAH33DPhi0bIrY
Note: the implementation of the game mechanics itself is completely different to the one in the tutorial,
I recommend you to check that out!

Have fun with the game and the code!
Bartek
