# Tuples in a list, left hand being option to type in, right hand being information on what the option will do
options = [('A', 'Add a string to the end of the queue'), ('N', 'Remove first element of the queue'),
           ('L', 'Remove the first occurrence of a string'),
           ('P', 'Print all elements in the queue in the same line'), ('Q', 'Quit Program')]

queue = list()  # Initialized an empty list at the start


def append(element):
    """ Appends an element onto the end of the queue """
    queue.append(element)
    print("Appended:", "'" + element + "'", "into the queue")


def pop():
    """ Remove first element of the list to fit FIFO style """
    if len(queue) == 0:
        print("The queue is empty - please try again later.")
    else:
        print("First element:", "'" + queue.pop(0) + "'", "is removed")


def remove(element):
    """ Remove specified element's first occurrence from the list """
    try:
        queue.remove(element)
        print("Element:", element, "is removed")
    except ValueError:  # remove method throws a ValueError if no element is found to remove
        print("No elements match the string:", element)


def printAll():
    """ Prints all elements in a single line, with a blank space as separator """
    if len(queue) == 0:
        print("EMPTY QUEUE")
    else:
        """ * in front of an iterable (list in this case) unpacks it, and print() prints out all the unpacked elements
            Using sep=" " means we can include a space between elements when printing """
        print("Queue:", *queue, sep=" ")


def leave():
    """ Exit program """
    print("Goodbye.")


def choices(userInput):
    """ Handles making choices """
    if userInput is 'A':
        appendInput = input("Please enter string to input into the list: ")
        while len(appendInput) == 0:
            appendInput = input("Nothing is entered, please enter string to input into the list: ")
        append(appendInput)
    elif userInput is 'N':
        pop()
    elif userInput == 'L':
        removeInput = input("Please enter string to find and remove the first occurrence in the list: ")
        while len(removeInput) == 0:
            removeInput = input("Nothing is entered, please enter string to remove the first occurrence in the list: ")
        remove(removeInput)
    elif userInput == 'P':
        printAll()
    elif userInput == 'Q':
        leave()
        return True  # Return True for the program to successfully exit without any error messages
    else:
        print("There is no options that corresponds to your input, please try again.")
    return False  # Return False for the program to continue


def drawMenu():  # This is only called at the start of the program, displayed not more than once
    """ Draws the menu """
    for option in options:
        print("'" + option[0] + "' ->", option[1])


if __name__ == '__main__':  # Entry point, this block of code runs every time we run
    drawMenu()
    # Do-While loop, as it should print 'another' instead of 'a' after the first selection
    exiting = choices(input("Please select a menu option: "))
    # Loop until user chooses the 'Quit' option, None == False, so the while loop continues as print() returns None
    while not exiting:
        exiting = choices(input("Please select another menu option: "))
