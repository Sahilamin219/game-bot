# Imports
import pygame
from random import randint,shuffle
import numpy as np
from math import pi, asin, sqrt, degrees, radians
import pandas as pds
from keras.models import Sequential
from keras.layers import Dense
import coremltools

# Enums
class Direction:
    left, right, up, down = range(4)
class NodeType:
    empty, snake_head, food, wall = range(4)

# Screen constants
block_size = 10
screen_size = (50,50)
screen_color = (0, 0, 0)
wall_color = (128, 128, 128)
snake_color = (0, 255, 255)
food_color = (0, 255, 0)

# Grid constants
columns, rows = screen_size[0], screen_size[1];

# Snake constants
snake_initial_size = 1

class SnakeNode:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def removeDuplicates(input_file_name,output_file_name):
    with open(input_file_name,"r") as input_file, open(output_file_name,"w") as output_file:
        output_file.writelines(unique_everseen(input_file))

def getGrid():
    grid = [[0 for x in range(columns)] for y in range(rows)]

    for x in range(columns):
        grid[x][0] = NodeType.wall
        grid[x][columns-1] = NodeType.wall

    for y in range(rows):
        grid[0][y] = NodeType.wall
        grid[rows-1][y] = NodeType.wall

    return grid

def getSnakeNodes(x,y,grid):
    # Create initial snake
    snake_nodes = []
    for i in range(snake_initial_size):
        segment = SnakeNode(x+i, y)
        snake_nodes.append(segment)

    grid[x][y] = NodeType.snake_head
    for i in range(1,len(snake_nodes)):
        grid[snake_nodes[i].x][snake_nodes[i].y] = NodeType.wall

    return snake_nodes

def getGrownSnake(snake_nodes,direction,grid):
    tail = snake_nodes[-1]

    if direction == Direction.right:   new_tail = SnakeNode(tail.x-1, tail.y)
    elif direction == Direction.left:  new_tail = SnakeNode(tail.x+1, tail.y)
    elif direction == Direction.up:    new_tail = SnakeNode(tail.x, tail.y+1)
    else:                              new_tail = SnakeNode(tail.x, tail.y-1)

    grid[new_tail.x][new_tail.y] = NodeType.wall

    snake_nodes.append(new_tail)

    return snake_nodes,grid

def drawNode(x,y,grid,screen):
    if grid[x][y] == NodeType.snake_head:  color = snake_color
    elif grid[x][y] == NodeType.food: color = food_color
    elif grid[x][y] == NodeType.wall: color = wall_color
    else:                             color = screen_color

    pygame.draw.rect(screen,color,pygame.Rect(x*block_size,y*block_size,block_size,block_size))

def isGameOver(snake_nodes,grid):
    head = snake_nodes[0]

    return grid[head.x][head.y] == NodeType.wall\
        or head.x == 0\
        or head.y == 0\
        or head.x == columns-1\
        or head.y == rows-1

def advanceSnake(snake_nodes,direction,grid):
    head = snake_nodes[0]
    tail = snake_nodes.pop()
    grid[tail.x][tail.y] = NodeType.empty
    
    if direction == Direction.up:
        tail.x = head.x
        tail.y = head.y - 1
    elif direction == Direction.down:
        tail.x = head.x
        tail.y = head.y + 1
    elif direction == Direction.left:
        tail.x = head.x - 1
        tail.y = head.y
    elif direction == Direction.right:
        tail.x = head.x + 1
        tail.y = head.y

    snake_nodes.insert(0,tail)

    if grid[tail.x][tail.y] != NodeType.food and grid[tail.x][tail.y] != NodeType.wall:
        grid[tail.x][tail.y] = NodeType.snake_head

    for i in range(1,len(snake_nodes)):
        grid[snake_nodes[i].x][snake_nodes[i].y] = NodeType.wall

    return snake_nodes

def drawNodes(grid,screen):
    for x in range(columns):
        for y in range(rows):
            drawNode(x,y, grid,screen)

def getNeighboringNodes(snake_nodes,direction,grid): # Left, forward, right nodes of snake
    head = snake_nodes[0]

    if direction == Direction.right:
        return (grid[head.x][head.y-1],grid[head.x+1][head.y],grid[head.x][head.y+1])
    elif direction == Direction.left:
        return (grid[head.x][head.y+1],grid[head.x-1][head.y],grid[head.x][head.y-1])
    elif direction == Direction.up:
        return (grid[head.x-1][head.y],grid[head.x][head.y-1],grid[head.x+1][head.y])
    else:
        return (grid[head.x+1][head.y],grid[head.x][head.y+1],grid[head.x-1][head.y])

def areNeighboringNodesBlocked(left,forward,right):
    return (int(left == NodeType.wall),int(forward == NodeType.wall),int(right == NodeType.wall))

def isAnyNeighboringNodesBlocked(left,forward,right):
    return left == NodeType.wall or forward == NodeType.wall or right == NodeType.wall

def distanceBetweenSnakeAndFood(snake_nodes,food_position):
    head = snake_nodes[0]

    food_x,food_y = food_position

    base = abs(food_x - head.x)
    perpendicular = abs(food_y - head.y)

    hypotenuse = sqrt(base**2 + perpendicular**2)
    return hypotenuse

def getOrthogonalAngle(snake_nodes,food_position,absolute_direction):
    head = snake_nodes[0]

    food_x,food_y = food_position

    base = food_x - head.x
    perpendicular = food_y - head.y

    hypotenuse = sqrt(base**2 + perpendicular**2)+0.00001

    angle = degrees(asin(perpendicular/hypotenuse))%90

    if absolute_direction == Direction.right:
        if base >= 0 and perpendicular <= 0:   angle = angle + 0
        elif base <= 0 and perpendicular <= 0: angle = angle + 90
        elif base <= 0 and perpendicular >= 0: angle = angle + 90
        else:                                  angle = angle + 0
    elif absolute_direction == Direction.up:
        if base >= 0 and perpendicular <= 0:   angle = angle + 0
        elif base <= 0 and perpendicular <= 0: angle = angle + 0
        elif base <= 0 and perpendicular >= 0: angle = angle + 90
        else:                                  angle = angle + 90
    elif absolute_direction == Direction.left:
        if base >= 0 and perpendicular <= 0:   angle = angle + 90
        elif base <= 0 and perpendicular <= 0: angle = angle + 0
        elif base <= 0 and perpendicular >= 0: angle = angle + 0
        else:                                  angle = angle + 90
    else:
        if base >= 0 and perpendicular <= 0:   angle = angle + 90
        elif base <= 0 and perpendicular <= 0: angle = angle + 90
        elif base <= 0 and perpendicular >= 0: angle = angle + 0
        else:                                  angle = angle + 0

    return radians(angle-90)/(pi/2)

def neuralInputs(snake_nodes,grid,absolute_direction,food_position):
    return (areNeighboringNodesBlocked(*getNeighboringNodes(snake_nodes,absolute_direction,grid)),
        getOrthogonalAngle(snake_nodes,food_position,absolute_direction))

def getTrainedModel(data, labels):

    model = Sequential()
    model.add(Dense(5,input_shape=(5,),activation="relu"))
    model.add(Dense(25,activation="relu"))
    model.add(Dense(25,activation="relu"))
    model.add(Dense(1,activation="linear"))
    model.summary()
    model.compile(loss="mean_squared_error",optimizer="adam",metrics=["accuracy"])
    model.fit(data,labels,epochs=1)
    
    return model

def getRelativeDirection(current_direction,next_direction):

    if current_direction == Direction.right:
        if next_direction == Direction.up: return -1
        elif next_direction == Direction.right: return 0
        else:                         return 1
    elif current_direction == Direction.left:
        if next_direction == Direction.down: return -1
        elif next_direction == Direction.left: return 0
        else:                         return 1
    elif current_direction == Direction.up:
        if next_direction == Direction.left: return -1
        elif next_direction == Direction.up: return 0
        else:                         return 1
    else:
        if next_direction == Direction.right: return -1
        elif next_direction == Direction.down: return 0
        else:                         return 1

def getPredictedDirection(snake_nodes,absolute_direction,model,inputs,grid,shuffle_predictions):
    head = snake_nodes[0]

    relative_directions = [-1,0,1]

    if shuffle_predictions == True:
        shuffle(relative_directions)

    no_match_found = False
    for relative_direction in relative_directions:
        prediction = model.predict(np.array([[inputs[0][0],inputs[0][1],inputs[0][2],inputs[1],relative_direction]]))
        if prediction > 0.9:
            break
        no_match_found = True

    if no_match_found == True and shuffle_predictions == True:
        for relative_direction in relative_directions:
            prediction = model.predict(np.array([[inputs[0][0],inputs[0][1],inputs[0][2],inputs[1],relative_direction]]))
            if prediction >= 0:
                break

    if absolute_direction == Direction.right:
        if relative_direction == -1:  return Direction.up,relative_direction
        elif relative_direction == 0: return Direction.right,relative_direction
        else:                         return Direction.down,relative_direction
    elif absolute_direction == Direction.left:
        if relative_direction == -1:  return Direction.down,relative_direction
        elif relative_direction == 0: return Direction.left,relative_direction
        else:                         return Direction.up,relative_direction
    elif absolute_direction == Direction.up:
        if relative_direction == -1:  return Direction.left,relative_direction
        elif relative_direction == 0: return Direction.up,relative_direction
        else:                         return Direction.right,relative_direction
    else:
        if relative_direction == -1:  return Direction.right,relative_direction
        elif relative_direction == 0: return Direction.down,relative_direction
        else:                         return Direction.left,relative_direction

def getOutputForTraining(target_output,inputs,snake_nodes,relative_direction):

    return "\n{},{},{},{},{},{}".format(target_output,
                                     inputs[0][0],
                                     inputs[0][1],
                                     inputs[0][2],
                                     inputs[1],
                                     relative_direction)

def generateFood(grid):
    food_position = (randint(1, columns-snake_initial_size-1),randint(1, rows-snake_initial_size-1))
    grid[food_position[0]][food_position[1]] = NodeType.food
    return food_position

def checkForFoodCollision(snake_nodes,grid):
    head = snake_nodes[0]
    return grid[head.x][head.y] == NodeType.food

def resetStuckPosition():
    return [[0 for x in range(columns)] for y in range(rows)]

def runGame(death_count,font,model):

    # Game objects
    score_count = 0
    grid = getGrid()
    directions = [Direction.right,Direction.left,Direction.up,Direction.down]
    direction = directions[randint(0,len(directions)-1)]
    snake_position = (randint(1, columns-snake_initial_size-1),randint(1, rows-snake_initial_size-1))
    food_position = generateFood(grid)
    snake_nodes = getSnakeNodes(snake_position[0],
                                snake_position[1],
                                grid)
    screen = pygame.display.set_mode((screen_size[0]*block_size,
                                      screen_size[1]*block_size))

    stuck_position = resetStuckPosition()

    # Game loop
    while not isGameOver(snake_nodes,grid):

        # Update score
        game_stats_label = font.render("Deaths: {}               Score: {}".format(death_count,score_count), 1, (255,255,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Drawing
        screen.fill(screen_color)
        drawNodes(grid,screen)
        screen.blit(game_stats_label, (0, 0))
        pygame.display.flip()

        # Clock ticking
        pygame.time.Clock().tick(999999999999)

        # If snake gets stuck in the same position for too long (5 times), shuffle the predictions
        stuck_position[snake_nodes[0].x][snake_nodes[0].y] += 1
        shuffle_predictions = (stuck_position[snake_nodes[0].x][snake_nodes[0].y] > 5)

        # Manual controls
        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP] and direction!=Direction.down: direction = Direction.up
        # elif pressed[pygame.K_DOWN] and direction!=Direction.up: direction = Direction.down
        # elif pressed[pygame.K_LEFT] and direction!=Direction.right: direction = Direction.left
        # elif pressed[pygame.K_RIGHT] and direction!=Direction.left: direction = Direction.right

        # Random controls
        # pressed = randint(0, 3)
        # if pressed == 0 and direction!=Direction.down: direction = Direction.up
        # elif pressed == 1 and direction!=Direction.up: direction = Direction.down
        # elif pressed == 2 and direction!=Direction.right: direction = Direction.left
        # elif pressed == 3 and direction!=Direction.left: direction = Direction.right

        # AI controls
        current_direction = direction
        inputs = neuralInputs(snake_nodes,grid,direction,food_position)
        direction,relative_direction = getPredictedDirection(snake_nodes,direction,model,inputs,grid,shuffle_predictions)

        previous_distance_between_snake_and_food = distanceBetweenSnakeAndFood(snake_nodes,food_position)
        snake_nodes = advanceSnake(snake_nodes,direction,grid)
        current_distance_between_snake_and_food = distanceBetweenSnakeAndFood(snake_nodes,food_position)

        # If game is over, target output is -1
        # If snake has moved away from the goal, target output is 0
        # If snake has moved closer to the goal, target output is 1
        if isGameOver(snake_nodes,grid):                                                          target_output = -1
        elif current_distance_between_snake_and_food >= previous_distance_between_snake_and_food: target_output = 0
        else:                                                                                     target_output = 1

        output = getOutputForTraining(target_output,inputs,snake_nodes,getRelativeDirection(current_direction,direction))
        # file = open("Data.csv","a")
        # file.write(output)
        # file.close()

        if checkForFoodCollision(snake_nodes,grid):
            score_count += 1
            food_position = generateFood(grid)
            shuffle_predictions = False
            stuck_position = resetStuckPosition()
            snake_nodes,grid = getGrownSnake(snake_nodes,direction,grid)

# Load CSV file, indicate that the first column represents labels
data = pds.read_csv("Data.csv",usecols=[1,2,3,4,5])
labels = pds.read_csv("Data.csv",usecols=[0])
model = getTrainedModel(data,labels)
# coreml_model = coremltools.converters.keras.convert(model)
# coreml_model.save("SnakeModel.mlmodel")
death_count = 0
pygame.init()
font = pygame.font.SysFont("monospace", 50)

while True:
    death_count += 1
    runGame(death_count,font,model)
    
