import numpy as np
msg = "'Now roll the dice!'"
print(msg)
int = np.random.randint(1,7)
int2 = np.random.randint(1,7)
#delay 2 seconds
import time
time.sleep(1)
print("\nThowing them in the cup...")
time.sleep(1)
print("\nSlamming it down...")
time.sleep(1)
print("\nlifting the cup...")
time.sleep(1)
#new line
print("\n")
print("\n'Lets have a Look!'")
time.sleep(2)
print("\n",int, " and ", int2)

time.sleep(2)

print("\n\n")
if int == 1 and int2 == 1:
    print("'Haha! Snake Eyes! Pay up!'")
    print("you hand him two Dollars")
#if int and int2 are the same but not 1
if int == int2 and int != 1:
    print("'Thats doubles! Pay up!'")
    print("you hand him a Dollar")
if int == 6 and int2 == 6:
    print("'Dammit thats 12, take my money!'")
    time.sleep(1)
    print("Reaches into poket pulling out $5")
    print("'Here you go!'")

#if int and int2 added together is an odd number
if (int + int2) % 2 != 0:
    print("'Thats ", int + int2, ", no one wins!'")
    print("lets play again!")

#if int and int2 added together is an even number
if (int + int2) % 2 == 0:
    print("'Damn, thats ", int + int2, ", no one wins!'")
    print("lets play again!")



