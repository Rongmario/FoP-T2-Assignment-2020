import turtle

''' Declare Global Variables and Constants '''


# Tuples in a list, left hand being option to type in, right hand being information on what the option will do
options = [('A', 'Add a string to the end of the queue'), ('N', 'Remove first element of the queue'),
           ('L', 'Remove the first occurrence of a string'),
           ('P', 'Print all elements in the queue in the same line'), ('Q', 'Quit Program')]

queue = list()

WIDTH, HEIGHT = 510, 510  # Little offset for screen border
X_PEAK, Y_PEAK = (WIDTH / 2) - 40, (HEIGHT / 2) - 50

TARGET_PRIME = 16777213

''' Method Declarations '''


def append(element):
    """ Appends an element onto the end of the queue """
    if isQueueFull():
        return "The queue is full - please try again later."
    else:
        t = TurtleElement(element)
        queue.append(t)
        length = len(queue) - 1
        x, y = X_PEAK - (length % 10) * 50, Y_PEAK - (length // 10) * 100
        t.setPosition(x, y)
    return "Appended: '" + element + "' into the queue"


def pop():
    """ Remove first element of the list to fit FIFO style """
    if len(queue) == 0:
        return "The queue is empty - please try again later."
    removed_element = queue.pop(0).destroy()  # Returns popped element
    updateTurtleStates()
    return "First element: '" + removed_element + "' is removed"


def remove(element):
    """ Remove specified element's first occurrence from the list """
    if len(queue) == 0:
        return "The queue is empty - please try again later."
    removed_element = None
    for index, turtle_element in enumerate(queue):
        if turtle_element.getElement() == element:
            removed_element = queue.pop(index).destroy()
            break
    if removed_element is None:
        return "No elements match the string: " + element
    else:
        updateTurtleStates()
        return "Element: '" + removed_element + "' is removed"


def printAll():
    """ Prints all elements in a single line, with a blank space as separator """
    if len(queue) == 0:
        return "EMPTY QUEUE"
    # .join a new iterable made of elements in TurtleElement objects in queue
    return "Queue: " + " ".join([turtle_element.getElement() for turtle_element in queue])


def leave():
    """ Exits the program """
    print("Goodbye.")
    return None  # Distinct singleton 'None' returned, while loop will get this and exit


def updateTurtleStates():
    """ Loops through the queue, sets new positions for turtles that was affected by pop() or remove() """
    for elements in range(len(queue)):
        x, y = X_PEAK - (elements % 10) * 50, Y_PEAK - (elements // 10) * 100
        queue[elements].setPosition(x, y)


def choices(choice):
    """ Handles making choices. All of these methods returns a string and print() is called in the main block """
    if choice is 'A':  # Append
        append_input = input("Please enter string to input into the list: ")
        while len(append_input) == 0:
            append_input = input("Nothing is entered, please enter string to input into the list: ")
        return append(append_input)
    elif choice is 'N':  # Next
        return pop()
    elif choice is 'L':  # Leave
        remove_input = input("Please enter string to find and remove the first occurrence in the list: ")
        while len(remove_input) == 0:
            remove_input = input("Nothing is entered, please enter string to remove the first occurrence in the list: ")
        return remove(remove_input)
    elif choice is 'P':  # Print
        return printAll()
    elif choice is 'Q':  # Quit
        return leave()  # Returns None
    return "There is no options that corresponds to your input, please try again."


def drawMenu():  # This is only called at the start of the program, displayed not more than once
    """ Draws the menu """
    for option in options:
        print("'" + option[0] + "' ->", option[1])


def getColour(identity):
    """ By using an algorithm to find the highest generator of a cyclic group (sampled between 2-50).
        We can find a number of generators giving ways to generate new colours, with a high variance at the same time.
        We then raise it to the power of a number that just increments every time we create a turtle.
        We then mod (%) to the prime (16777213, largest before 2^24), getting a 24-bit RGB integer.

        Reason why bitshift is used here, is because when we shift to the right by 16-bits, we're left with the
        leftmost 8-bit value, which is red's 8-bit value.
        Green is gotten from shifting to the right by 8-bits, with clearing anything but the rightmost 8-bit value
        with zeroes (by doing BITWISE AND 255). This also applies to blue's 8-bit values, which we do not need to
        shift as we want to get the rightmost 8-bit value from the whole 24-bit value, thus we clear the left-hand
        16-bit value by BITWISE AND 255 again and clearing them to zeroes.

        This method returns a tuple containing R, G, B values. """
    initial = pow(45, identity, TARGET_PRIME)
    return initial >> 16, (initial >> 8) & 255, initial & 255


def isQueueFull():
    """ Returns True if we hit maximum limit (50 elements, 10 elements per row, with 5 maximum rows) """
    return len(queue) == 50


''' Class Declarations '''


class TurtleElement:

    destroyed_ids = list()  # Don't need a set here since its guaranteed the elements won't duplicate
    total = 0  # Increments every time a TurtleElement object is created, caps at 16777213

    def __init__(self, element):
        self.element = element  # Stores the element the turtle is representing on-screen
        self.turtle = turtle.Turtle(visible=False)  # Hidden, so it doesn't show on-screen until positioned right
        self.turtle.speed(0)
        # If there's unused turtle identities, we use those first, otherwise increment and use counter
        try:
            self.identity = TurtleElement.destroyed_ids.pop(0)
        except IndexError:
            TurtleElement.total += 1
            self.identity = TurtleElement.total
        # Grab RGB values based on current object's identity
        self.turtle.color(Colour(self.identity).getRGB())
        self.turtle.penup()  # Doesn't draw a line on the screen
        self.turtle.shape("turtle")  # Change the shape of the turtle to the 'turtle' shape

    def setPosition(self, x, y):
        self.turtle.setpos(x, y)
        self.turtle.showturtle()

    def destroy(self):
        self.turtle.clear()
        self.turtle.hideturtle()
        TurtleElement.destroyed_ids.append(self.identity)
        return self.element

    def getPosition(self):
        return self.turtle.pos()

    def getTurtle(self):
        return self.turtle

    def getColour(self):
        return self.colour

    def getElement(self):
        return self.element


class Colour:

    def __init__(self, identity):
        self.rgb = getColour(identity)
        self.r, self.g, self.b = self.rgb

    def getRGB(self):
        return self.rgb

    def getRed(self):
        return self.r

    def getGreen(self):
        return self.g

    def getBlue(self):
        return self.b


if __name__ == '__main__':  # Entry point, this block of code runs first after catching all the method/class definitions
    screen = turtle.Screen()  # Initializes the screen
    screen.colormode(255)  # We change the colormode to 255 so turtles can take RGB values (0-255)
    screen.setup(WIDTH, HEIGHT)  # Sets up the screen to be a certain width and certain height (constants defined above)
    drawMenu()
    # Do-While loop, as it should print 'another' instead of 'a' after the first selection
    exiting = choices(input("Please select a menu option: "))
    # Loop until user chooses the 'Quit' option, every option except Quit returns strings, so the while loop continues
    # The option to quit returns None, therefore it exits the while loop
    while exiting is not None:
        print(exiting)
        exiting = choices(input("Please select a menu option: "))
    screen.bye()  # Gracefully exits the turtle window
