# Import the turtle module:
import turtle

# Create a turtle object to represent our robot.
robot = turtle.Turtle()
robot.shape("turtle")   # Set the shape to "turtle" for visual clarity.
robot.speed(20)          # Control the drawing speed (1-slowest, 10-fastest).

# Define functions to control the robot's motion:
def go_forward():
    """Moves the robot forward by 20 pixels."""
    robot.forward(20)

def go_backward():
    """Moves the robot backward by 20 pixels."""
    robot.backward(20)

def turn_left():
    """Turns the robot left by 30 degrees."""
    robot.left(30)

def turn_right():
    """Turns the robot right by 30 degrees."""
    robot.right(30)

# Set up the screen to listen to key presses.
screen = turtle.Screen()
screen.title("Simple Robot Teleoperation Demo")
screen.listen()  # Enable keyboard quitevent listening.

# Bind the arrow keys to the corresponding functions.
screen.onkey(go_forward, "Up")    # When the "Up" arrow key is pressed, call go_forward().
screen.onkey(go_backward, "Down") # When the "Down" arrow key is pressed, call go_backward().
screen.onkey(turn_left, "Left")   # When the "Left" arrow key is pressed, call turn_left().
screen.onkey(turn_right, "Right") # When the "Right" arrow key is pressed, call turn_right().

# Keep the window open until it is closed by the user.
turtle.done()