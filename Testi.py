points = 0

while points < 4:
    task1 = input("Solve the following sentence using Caesar Shift -1: 'fnnc ktbj rzuhmf sgd vnqkc'\n")
    if task1 == "good luck saving the world":
        print("Correct! Well done!")
        points += 1
    else:
        print("Incorrect. Try again!")
        threat(failure)

    task2 = input("Solve the following word using Caesar Shift -1: 'gnknfqzl'\n")
    if task2 == "hologram":
        print("Correct! Well done!")
        points += 1
    else:
        print("Incorrect. Try again!")
        threat(failure)

    task3= input("Solve the following sentence using Caesar Shift -1: 'zqd xnt rdqhntr'\n")
    if task3 == "are you serious":
        print("Correct! Well done!")
        points += 1
    else:
        print("Incorrect. Try again!")
        threat(failure)

    task4= input("Solve the following sentence using Caesar Shift -1: 'fnnc lnqmhmf uhdszml'\n")
    if task4 == "good morning vietnam":
        print("Correct! Well done!")
        points += 1
    else:
        print("Incorrect. Try again!")
        threat(failure)