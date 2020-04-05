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
    if isQueueFull():  # Inform the user that the queue is full
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
    removedElement = queue.pop(0).destroy()  # Returns popped element
    updateTurtleStates()
    return "First element: '" + removedElement + "' is removed"


def remove(element):
    """ Remove specified element's first occurrence from the list """
    if len(queue[0]) == 0:
        return "The queue is empty - please try again later."
    removed_element = None
    for queueIndex, nested in enumerate(queue):
        for nestedIndex, turtleElement in enumerate(nested):
            if turtleElement.getElement() == element:
                removed_element = nested.pop(nestedIndex).destroy()
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
    return "Queue: " + " ".join([turtleElement.getElement() for turtleElement in queue])


def leave():
    """ Exits the program """
    print("Goodbye.")
    return exit(0)  # Code 0 for successful termination


def updateTurtleStates():
    """ Loops through the queue, sets new positions for turtles that was affected by pop() or remove() """
    for i in range(len(queue)):
        x, y = X_PEAK - (i % 10) * 50, Y_PEAK - (i // 10) * 100
        queue[i].setPosition(x, y)


def choices(choice):
    """ Handles making choices. All of these methods returns a string and print() is called in the main block """
    if choice is 'A':  # Append
        appendInput = input("Please enter string to input into the list: ")
        while len(appendInput) == 0:
            appendInput = input("Nothing is entered, please enter string to input into the list: ")
        return append(appendInput)
    elif choice is 'N':  # Next
        return pop()
    elif choice is 'L':  # Leave
        removeInput = input("Please enter string to find and remove the first occurrence in the list: ")
        while len(removeInput) == 0:
            removeInput = input("Nothing is entered, please enter string to remove the first occurrence in the list: ")
        return remove(removeInput)
    elif choice is 'P':  # Print
        return printAll()
    elif choice is 'Q':  # Quit
        return leave()
    return "There is no options that corresponds to your input, please try again."


def drawMenu():  # This is only called at the start of the program, displayed not more than once
    """ Draws the menu """
    for option in options:
        print("'" + option[0] + "' ->", option[1])


def getColour(identity):
    """ By using an algorithm to find the highest generator of a cyclic group (sampled between 2-50).
        We can find a number of generators giving us ways to generate unique colours at the same time a high variance.
        We then raise it to the power of a number that just increments every time we create a turtle.
        We then mod (%) to the prime (16777213, largest before 2^24), getting a 24-bit RGB integer.

        Reason why bitshift is used here, is because when we shift to the right by 16-bits, we're left with the
        leftmost 8-bit value, which is red's 8-bit value.
        Green is gotten from shifting to the right by 8-bits, with clearing anything but the rightmost 8-bit value
        with zeroes (by doing BITWISE AND 255). This also applies to blue's 8-bit values, which we do not need to
        shift as we want to get the rightmost 8-bit value from the whole 24-bit value, thus we clear the left-hand
        16-bit value by BITWISE AND 255 again and clearing them to zeroes. """
    initial = pow(45, identity, TARGET_PRIME)
    return initial >> 16, (initial >> 8) & 255, initial & 255


def isQueueFull():
    """ Returns True if there are 5 or more rows populated and if last row is full, False if there's less than 5 """
    # return len(queue) >= 5 and isRowFull()
    return len(queue) == 50


''' Class Declarations '''


class TurtleElement:

    destroyedIds = list()  # Don't need a set here since its guaranteed the elements won't duplicate
    total = 0  # Increments every time a TurtleElement object is created, caps at 16777213

    def __init__(self, element):
        self.element = element  # Stores the element the turtle is representing on-screen
        self.turtle = turtle.Turtle(visible=False)  # Hidden, so it doesn't show on-screen until positioned right
        self.turtle.speed(0)
        # If there's unused turtle identities, we use those first, otherwise increment and use counter
        try:
            self.identity = TurtleElement.destroyedIds.pop(0)
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
        TurtleElement.destroyedIds.append(self.identity)
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


if __name__ == '__main__':  # Entry point, this block of code runs every time we run
    screen = turtle.Screen()  # Initializes the screen
    screen.colormode(255)  # We change the colormode to 255 so it can take 8-bit RGB values
    screen.setup(WIDTH, HEIGHT)  # Offset accounting for border
    drawMenu()  # Draws menu
    # Do-While loop, as it should print 'another' instead of 'a' after the first selection
    print(choices(input("Please select a menu option: ")))
    while True:  # Loop until user chooses the 'Quit' option
        print(choices(input("Please select another menu option: ")))
