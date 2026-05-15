import random
characters = "adcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
length = int(input("Enter password length:"))
password = ""
for i in range(length):
    password += random.choice(characters)
print("Generated Password:", password)
