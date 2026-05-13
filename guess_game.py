import random
secret_number = random.randint(1, 10)
while True:
    guess = int(input("Guess a number between 1 and 10:"))
    if guess == secret_number:
        print("Correct! You guessed the number.")
        break
    elif guess < secret_number:
        print("Too low!")
    else:
        print("Too high!")