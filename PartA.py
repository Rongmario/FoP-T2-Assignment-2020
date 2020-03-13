options = ['A', 'N', 'L', 'P', 'Q']
descriptions = ['-> Add a string to the end of the queue',
                '-> Remove first element of the queue',
                '-> Remove the first occurrence of a string',
                '-> Print all elements in the queue in the same line',
                '-> Quit Program']

queue = list()  # Initialized an empty list at the start
executions = 0  # Counts the amount of times the user has chosen a menu option


def append(element):
    """ Appends an element onto the end of the queue """
    queue.append(element)
    print("Appended:", "'", element, "'", "into the queue")


def pop():
    """ Remove first element of the list to fit FIFO style """
    print("First element:", "'", queue.pop(0), "'", "is removed")


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
        print("Queue is Empty.")
    else:
        print("Queue:", end=" ")
        for string in queue:
            print(string, end=" ")


def leave():
    """ Exit program """
    print("Goodbye.")
    exit()


def choices():
    """ Handles making choices """
    global executions  # So we can change the global variable 'executions'
    print("\n")  # New line, looks neater
    if executions == 0:
        userInput = input("Please select a menu option: ")
    else:
        userInput = input("Please select another menu option: ")

    if userInput is 'A':
        append(input("Enter string to input into the list: "))
    elif userInput is 'N':
        pop()
    elif userInput == 'L':
        remove(input("Enter string to find and remove in the list: "))
    elif userInput == 'P':
        printAll()
    elif userInput == 'Q':
        leave()
    else:
        print("There is no options that correspond to your input... ")

    executions += 1  # Increment every time an option is selected


def drawMenu():  # This should only be called at the start of the program and should not display more than once
    """ Draws the menu """
    for i in range(len(options)):
        print(options[i], descriptions[i])


if __name__ == '__main__':  # Entry point, this block of code runs every time we run
    drawMenu()
    while True:  # Loops until user selects Q to exit
        choices()
