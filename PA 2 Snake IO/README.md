# Assignment 2: Snake IO

**Introduction:**
In this assignment you will be creating a multiplayer version of the classic game “Snake”. The
rules of the game will be as follows:

1. When the game starts, all players will have a snake spawn in a random position on the
    board.
2. Each player will be able to move their snake in in four directions (up, down, left or right)
    using their arrow keys.
3. If a snake collides with the border of the stage, it gets eliminated.
4. If a snake (A) collides with another snake (B) from the side, then snake A gets eliminated
    while snake B survives.
5. If two snakes have a head-on collision, they both get eliminated (if these were the last
    two snakes, then nobody wins).
6. The last snake alive wins the game.
**Implementation:**
1. You must create a server (​ **server.py** ​) that will do the following:
● Connect with all the clients
● Start the game and spawn a snake for each player on the board
● Communicate the positions and moves of each player to every other player
● The command for starting the server should be as follows:
○ python3 server.py *IP address* *port* *number of players*
○ E.g python3 server.py 192.168.5.5 2000 5
○ E.g python3 server.py 127.0.0.1 2000 3
2. You must create a client (​ **client.py** ​) that will do the following:
● Connect with the server
● Display the board and all of the players and their positions in real time
once the game starts by receiving this information from the server
● The command for starting the client should be as follows:
○ python3 client.py *IP address* *port*
○ E.g python3 client.py 192.168.5.5 2000
○ E.g python3 client..py 127.0.0.1 2000
3. Use the “curses” library in python to make the game. You can use these guides for making
the classic (non-multiplayer) version of the game as a reference:
(​https://www.youtube.com/watch?v=tgt02bFoOu0​)
(​https://www.youtube.com/watch?v=rbasThWVb-c&t=2s​)

4. This assignment will be done in pairs. You are advised to make the game functional for
    two players before scaling up to “n” players for ease in testing. Once the game is working
    perfectly for two players, it should not be too difficult to scale it up to allow more
    players.
**Bonus:**
Add food on the stage which snakes can eat to grow.
Add scores/kill counters.
**Submission:**
    1. The deadline for this assignment is 25th March 2019.
    2. You are advised to start as early as possible in order to be able to finish on time.
    3. The assignment can be completed in ​ **pairs** ​.
    4. All assignment submissions will be checked for plagiarism.
