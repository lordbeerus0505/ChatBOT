import re

from sys import exit


#Whenever is_number(x) exists, it is checking to see if x is a number, obviously.
def is_number(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


def set_up_list(exp):
    #First part gets string and deletes whitespace
    astring = exp#input("Calculation: ")
    astring = astring.replace(" ", "")
    #Next it will check if there are any unsupported characters in the string
    for item in astring:
        if item not in ["0", "1", "2", "3" , "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", "(", ")"]:
            print ("Unsupported Character: " + item)
            exit()
    #Then it creates the list and adds each individual character to the list
    a_list = []
    for item in astring:
        a_list.append(item)
    count = 0
    #Finally it combines individual numbers into actual numbers based on user input
    while count < len(a_list) - 1:
        if is_number(a_list[count]) and a_list[count + 1] == "(":
            print ("Program does not accept parentheses directly after number, must have operator in between.")
            exit()
        if is_number(a_list[count]) and is_number(a_list[count + 1]):
            a_list[count] += a_list[count + 1]
            del a_list[count + 1]
        elif is_number(a_list[count]) and a_list[count + 1] == ".":
            try:
                x = a_list[count+2]
            except IndexError:
                print ("Your formatting is off somehow.")
                exit()
            if is_number(a_list[count + 2]):
                a_list[count] += a_list[count + 1] + a_list[count + 2]
                del a_list[count + 2]
                del a_list[count + 1]
        else:
            count += 1
    return a_list


def perform_operation(n1, operand, n2):
    if operand == "+":
        return str(float(n1) + float(n2))
    elif operand == "-":
        return str(float(n1) - float(n2))
    elif operand == "*":
        return str(float(n1) * float(n2))
    elif operand == "/":
        try:
            n = str(float(n1) / float(n2))
            return n
        except ZeroDivisionError:
            print ("You tried to divide by 0.")
            print ("Just for that I am going to terminate myself")
            exit()



class Calculate:
    def convert_to_number(self):
        return
    def calc(self,exp):
        expression = set_up_list(exp)
        emergency_count = 0
        # Makes code shorter, short for parentheses
        P = ["(", ")"]
        # If the length of the list is 1, there is only 1 number, meaning an answer has been reached.
        while len(expression) != 1:
            # If there are parentheses around a single list item, the list item is obviously just a number, eliminate parentheses
            # Will check to see if the first parentheses exists first so that it does not throw an index error
            count = 0
            while count < len(expression) - 1:
                if expression[count] == "(":
                    if expression[count + 2] == ")":
                        del expression[count + 2]
                        del expression[count]
                count += 1
            # After that is done, it will multiply and divide what it can
            count = 0
            while count < len(expression) - 1:
                if expression[count] in ["*", "/"] and not (expression[count + 1] in P or expression[count - 1] in P):
                    expression[count - 1] = perform_operation(expression[count - 1], expression[count],
                                                              expression[count + 1])
                    del expression[count + 1]
                    del expression[count]
                count += 1
            # Then it will add and subtact what it can
            count = 0
            while count < len(expression) - 1:
                if expression[count] in ["+", "-"] and not (expression[count + 1] in P or expression[count - 1] in P):
                    expression[count - 1] = perform_operation(expression[count - 1], expression[count],
                                                              expression[count + 1])
                    del expression[count + 1]
                    del expression[count]
                count += 1
            # The steps will repeat until only one character is left. Operations that fail will be stopped by emergency count.
            emergency_count += 1
            if emergency_count >= 1000:
                print("Operation was too long or was bugged")
                exit()

        print(float(expression[0]))

# obj=Calculate()
# obj.calc("(20*30)+5-2")