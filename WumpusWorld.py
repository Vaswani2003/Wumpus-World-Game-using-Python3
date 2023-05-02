'''
The Wumpus world is a simple world example to illustrate the worth of a knowledge-based agent and to represent knowledge representation.
It was inspired by a video game Hunt the Wumpus by Gregory Yob in 1973.

-> So there are total 16 rooms which are connected with each other.

-> We have a knowledge-based agent who will go forward in this world.

-> The cave has a room with a beast which is called Wumpus, who eats anyone who enters the room.

-> The Wumpus can be shot by the agent, but the agent has a single arrow.

-> In the Wumpus world, there are some Pits rooms which are bottomless, and if agent falls in Pits, then he will be stuck there forever.

-> The exciting thing with this cave is that in one room there is a possibility of finding a heap of gold.

-> So the agent goal is to find the gold and climb out the cave without fallen into Pits or eaten by Wumpus.

Info About the Environment

-> A 4*4 grid of rooms.

-> The agent initially in room square [1, 1], facing toward the right.

-> Location of Wumpus and gold are chosen randomly except the first square [1,1].

-> Each square of the cave can be a pit with probability 0.2 except the first square.

Defining Factors :

1) The rooms adjacent to the Wumpus room are smelly, so that it would have some stench.

2) The room adjacent to PITs has a breeze, so if the agent reaches near to PIT, then he will perceive the breeze.

3) There will be glitter in the room if and only if the room has gold.

4) The Wumpus can be killed by the agent if the agent is facing to it, and Wumpus will emit a horrible scream which can be heard anywhere in the cave.
'''

import random
import numpy as np


class Grid:

    # ====================================================== #

    def __init__(self):
        self.grid = np.array([[None] * 4 for i in range(4)])  # by default we build a 4x4 grid
        self.WumpusCords = None
        self.gold_cords = None
        self.pit_cords = []

    # ====================================================== #

    def addWumpus(self):  # creating co-ords for wumpus

        while True:

            x_cord = random.randint(0, 3)
            y_cord = random.randint(0, 3)

            if x_cord != 0 and y_cord != 0:
                break

        self.WumpusCords = [x_cord, y_cord]

    # ====================================================== #

    def addPits(self):  # creating co-ords for pits

        num = random.randint(1, 3)  # number of pits

        while num > 0:

            while True:

                x_cord = random.randint(0, 3)
                y_cord = random.randint(0, 3)

                if x_cord != 0 and y_cord != 0:
                    if [x_cord, y_cord] is not self.WumpusCords:
                        self.pit_cords.append([x_cord, y_cord])
                        num -= 1
                        break

    # ====================================================== #

    def addGold(self):  # creating co-ords for gold

        while True:

            x_cord = random.randint(0, 3)
            y_cord = random.randint(0, 3)

            if ([x_cord, y_cord] != self.WumpusCords) or ([x_cord, y_cord] != self.pit_cords):
                if x_cord != 0 and y_cord != 0:
                    self.gold_cords = [x_cord, y_cord]
                    break

    # ====================================================== #


class Rooms:

    # ====================================================== #

    def __init__(self):

        self.grid = np.array([[None] * 4 for i in range(4)])  # by default we build a 4x4 grid

        self.WumpusCords = None
        self.gold_cords = None
        self.pit_cords = []

        self.rooms = np.array([[[False] * 4 for i in range(4)] for j in range(4)])
        # Stench , Breeze, Glitter, Agent
        self.rooms[0][0][3] = True

    # ====================================================== #

    def insertStench(self, w_cords):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if [i, j] == w_cords:
                    if i == 1:
                        if j == 0:
                            self.rooms[i][j + 1][0] = True
                            self.rooms[i + 1][j][0] = True
                        elif j == 3:
                            self.rooms[i][j - 1][0] = True
                            self.rooms[i - 1][j][0] = True
                            self.rooms[i + 1][j][0] = True
                    elif i == 2 and j == 0:
                        self.rooms[i - 1][j][0] = True
                        self.rooms[i + 1][j][0] = True
                        self.rooms[i][j + 1][0] = True
                    elif i == 2 and j == 3:
                        self.rooms[i - 1][j][0] = True
                        self.rooms[i + 1][j][0] = True
                        self.rooms[i][j - 1][0] = True
                    elif i == 3:
                        if j == 0:
                            self.rooms[i - 1][j][0] = True
                            self.rooms[i][j + 1][0] = True
                        elif j == 1 or j == 2:
                            self.rooms[i - 1][j][0] = True
                            self.rooms[i][j - 1][0] = True
                            self.rooms[i][j + 1][0] = True
                        if j == 3:
                            self.rooms[i - 1][j][0] = True
                            self.rooms[i][j - 1][0] = True
                    else:
                        self.rooms[i][j + 1][0] = True
                        self.rooms[i][j - 1][0] = True
                        self.rooms[i - 1][j][0] = True
                        self.rooms[i + 1][j][0] = True

    # ====================================================== #

    def insertBreeze(self, pit_cords):

        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if [i, j] == pit_cords:
                    if i == 1:
                        if j == 0:
                            self.rooms[i][j + 1][1] = True
                            self.rooms[i + 1][j][1] = True
                        elif j == 3:
                            self.rooms[i][j - 1][1] = True
                            self.rooms[i - 1][j][1] = True
                            self.rooms[i + 1][j][1] = True
                    elif i == 2 and j == 0:
                        self.rooms[i - 1][j][1] = True
                        self.rooms[i + 1][j][1] = True
                        self.rooms[i][j + 1][1] = True
                    elif i == 2 and j == 3:
                        self.rooms[i - 1][j][1] = True
                        self.rooms[i + 1][j][1] = True
                        self.rooms[i][j - 1][1] = True
                    elif i == 3:
                        if j == 0:
                            self.rooms[i - 1][j][1] = True
                            self.rooms[i][j + 1][1] = True
                        elif j == 1 or j == 2:
                            self.rooms[i - 1][j][1] = True
                            self.rooms[i][j - 1][1] = True
                            self.rooms[i][j + 1][1] = True
                        if j == 3:
                            self.rooms[i - 1][j][1] = True
                            self.rooms[i][j - 1][1] = True
                    else:
                        self.rooms[i][j + 1][1] = True
                        self.rooms[i][j - 1][1] = True
                        self.rooms[i - 1][j][1] = True
                        self.rooms[i + 1][j][1] = True

    # ====================================================== #

    def insertGlitter(self, g_cords):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                if [i, j] == g_cords:
                    self.rooms[i][j][2] = True

    # ====================================================== #

    def Mark(self, x, y):

        ans = ''
        cur = self.rooms
        if True in cur[x][y]:
            if cur[x][y][3]:
                ans += '🤖 '
        if ans == '':
            ans = '❌'

        return ans

    # ====================================================== #

    def Final_Mark(self, x, y):

        ans = ''
        cur = self.rooms

        if True in cur[x][y]:
            if cur[x][y][0]:
                ans += '🤢 '
            if cur[x][y][1]:
                ans += '🥶 '
            if cur[x][y][2]:
                ans += '💲 '
            if cur[x][y][3]:
                ans += '🤖 '
        if ans == '':
            ans = '❌'

        return ans

        # ====================================================== #

    def Max_finalize(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                self.grid[i][j] = self.Final_Mark(i, j)

    # ====================================================== #

    # ====================================================== #

    def finalize(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                self.grid[i][j] = self.Mark(i, j)

    # ====================================================== #

    def printRooms(self):
        for i in self.rooms:
            for j in i:
                print(j, end=' ')
            print()

    # ====================================================== #

    def printGrids(self):
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                print(self.grid[i][j], end='\t\t')
            print(end='\n\n')

    # ====================================================== #

class Agent:

    # ====================================================== #

    def __init__(self, room, w_cords, g_cords, p_cords):
        self.location = [0, 0]
        self.Cord_Stack = []
        self.prev_location = []
        self.foundGold = False

        self.room_object = room
        self.wumpusAt = w_cords
        self.pitsAt = p_cords
        self.goldAt = g_cords

    # ====================================================== #

    def GameOver(self, success):
        if success:
            print("You've won !")
        else:
            print('Better luck next time')

    # ====================================================== #

    def perceive(self):
        x = self.location[0]
        y = self.location[1]

        if [x, y] == [0, 0] and self.foundGold:
            print('You made it Back!!!')
            self.GameOver(True)

        if self.room_object.rooms[x][y][0]:
            print(" Ewe!!!! There's a weird Stench in Here !")

        if self.room_object.rooms[x][y][1]:
            print(" Yikes!!!! There's cool Breeze in Here !")
        if self.room_object.rooms[x][y][0]:
            print(" Yeezy!!!! There's shiny Glitter in Here !")
            self.foundGold = True

        if [x, y] in self.pitsAt:
            print('You fell into a Pit !!!!')
            self.GameOver(False)

        if [x, y] == self.wumpusAt:
            print('Wumpus Got You Now!!')
            self.GameOver(False)

    # ====================================================== #

    def left(self):
        if self.location[1] > 0:

            x, y = self.location[0], self.location[1]

            self.Cord_Stack.append([x, y])
            self.prev_location = [x, y]
            self.prev_location = [x, y]

            self.location[1] = self.location[1] - 1

            self.room_object.rooms[self.location[0]][self.location[1]][3] = True

            self.room_object.Mark(self.location[0], self.location[1])

            i = self.prev_location[0]
            j = self.prev_location[1]
            self.room_object.rooms[i][j][3] = False

        else:
            print('Oops! Bumped into a Wall !')

    # ====================================================== #

    def right(self):

        if self.location[1] < 3:

            x, y = self.location[0], self.location[1]
            self.Cord_Stack.append([x, y])
            self.prev_location = [x, y]

            self.location[1] = self.location[1] + 1

            self.room_object.rooms[self.location[0]][self.location[1]][3] = True

            self.room_object.Mark(self.location[0], self.location[1])

            i = self.prev_location[0]
            j = self.prev_location[1]
            self.room_object.rooms[i][j][3] = False

        else:
            print('Oops! Bumped into a Wall !')

    # ====================================================== #

    def up(self):
        if self.location[0] > 0:

            x, y = self.location[0], self.location[1]
            self.Cord_Stack.append([x, y])
            self.prev_location = [x, y]
            self.location[0] = self.location[0] - 1

            self.room_object.rooms[self.location[0]][self.location[1]][3] = True

            self.room_object.Mark(self.location[0], self.location[1])

            i = self.prev_location[0]
            j = self.prev_location[1]
            self.room_object.rooms[i][j][3] = False

        else:
            print('Oops! Bumped into the Ceiling !')

    # ====================================================== #

    def down(self):
        if self.location[0] < 3:

            x, y = self.location[0], self.location[1]
            self.Cord_Stack.append([x, y])
            self.prev_location = [x, y]

            self.location[0] = self.location[0] + 1

            self.room_object.rooms[self.location[0]][self.location[1]][3] = True

            self.room_object.Mark(self.location[0], self.location[1])

            i = self.prev_location[0]
            j = self.prev_location[1]
            self.room_object.rooms[i][j][3] = False

        else:
            print('Oops! Bumped into a Wall !')

    # ====================================================== #
    
    
class Game:

    # ====================================================== #

    def __init__(self):

        self.Main_GridFrame = None
        self.Main_RoomsFrame = None
        self.Main_Agent = None

    # ====================================================== #

    def InitializeAll(self):
        # we initialize our gold, pits and monster co-ordinates
        self.Main_GridFrame = Grid()
        self.Main_GridFrame.addWumpus()
        self.Main_GridFrame.addPits()
        self.Main_GridFrame.addGold()

        self.Main_RoomsFrame = Rooms()
        # we insert everything into rooms and add breeze, stench and glitter
        self.Main_RoomsFrame.insertStench(self.Main_GridFrame.WumpusCords)
        self.Main_RoomsFrame.insertGlitter(self.Main_GridFrame.gold_cords)

        for i in self.Main_GridFrame.pit_cords:
            self.Main_RoomsFrame.insertBreeze(i)

        self.Main_RoomsFrame.finalize()
        self.Main_Agent = Agent(self.Main_RoomsFrame, self.Main_GridFrame.WumpusCords,
                                self.Main_GridFrame.pit_cords, self.Main_GridFrame.gold_cords)

    # ====================================================== #

    def Start(self):

        self.InitializeAll()
        print("\n\nYou have now entered the maze!!\nFind the gold and return back safely\n")
        print("Controls:\n\n\tW to move Up\n\n\tA to move Left\n\n\tS to move Down\n\n\tD to move Right\n\n\tX to "
              "EndGame")

        print('\nYou are here !\n')
        self.Main_RoomsFrame.printGrids()

        moves = 0

        while moves > -1:

            move = input('Move : ').lower()

            if move == 'w':
                self.Main_Agent.up()

            elif move == 'a':
                self.Main_Agent.left()

            elif move == 'd':
                self.Main_Agent.right()

            elif move == 's':
                self.Main_Agent.down()

            elif move == 'x':
                self.Main_Agent.GameOver(False)
                break

            x = self.Main_Agent.location[0]
            y = self.Main_Agent.location[1]

            if [x, y] == [0, 0] and self.Main_Agent.foundGold:
                print('You made it Back!!!')
                self.Main_Agent.GameOver(True)
                moves -= 1

            if self.Main_Agent.room_object.rooms[x][y][0]:
                print(" Ewe!!!! There's a weird Stench in Here !")

            if self.Main_Agent.room_object.rooms[x][y][1]:
                print(" Yikes!!!! There's cool Breeze in Here !")
            if self.Main_Agent.room_object.rooms[x][y][0]:
                print(" Yeezy!!!! There's shiny Glitter in Here !")
                self.Main_Agent.foundGold = True

            if [x, y] in self.Main_Agent.pitsAt:
                print('You fell into a Pit !!!!')
                self.Main_Agent.GameOver(False)
                moves -= 1

            if [x, y] == self.Main_Agent.wumpusAt:
                print('Wumpus Got You Now!!')
                self.Main_Agent.GameOver(False)
                moves -= 1

            self.Main_RoomsFrame.finalize()
            self.Main_RoomsFrame.printGrids()

    # ====================================================== #


if __name__ == '__main__':
    Test = Game()
    Test.Start()
