import turtle
import random
turtle.speed(0)
turtle.hideturtle()
turtle.title('MonteCarlo')
turtle.setheading(0)
turtle.shape('circle')
def function_draw():
    turtle.pencolor('black')
    turtle.pensize(1)
    turtle.penup()
    turtle.goto(-300,-300)
    turtle.pendown()
    for x in range(0,4):
        turtle.forward(600)
        turtle.left(90)
    for x in range(-300,301):
        y = (x + 300)/600
        y = y * y * 600
        y = y - 300
        turtle.goto(x,y)
def print_dot(dot_number):
    turtle.pensize(3)
    for i in range(0,dot_number):
        x = random.random()
        y = random.random()
        x_cords.append(x)
        y_cords.append(y)
    calculate(dot_number)
    turtle.penup()
    for i in range(0,dot_number):
        x = x_cords[i]
        y = y_cords[i]
        if x * x >= y:
            turtle.pencolor('blue')
        else:
            turtle.pencolor('red')
        x = x * 600 - 300
        y = y * 600 - 300
        turtle.goto(x,y)
        turtle.pendown()
        turtle.forward(3)
        turtle.penup()
def calculate(number):
    global valid_dot
    for i in range(0,number):
        x = x_cords[i]
        y = y_cords[i]
        if x * x >= y:
            valid_dot = valid_dot + 1
    print(valid_dot/number)
num = input('how many dots to draw?\n')
num = int(num)
x_cords = []
y_cords = []
valid_dot = 0
function_draw()
print_dot(num)

