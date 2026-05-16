tasks = []

while True:
    print("\nTo-Do List Menu")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        if len(tasks) == 0:
            print("No tasks yet.")
        else:
            print("\nYour Tasks:")
            for task in tasks:
                print("-", task)
    
    elif choice == "2":
        task = input("Enter new task: ")
        tasks.append(task)
        print("Task added.")
    
    elif choice == "3":
        task = input("Enter task to remove: ")
        if task in tasks:
            tasks.remove(task)
            print("Task remove.")
        else:
            print("Task not found.")
    
    elif choice == "4":
        print("Goodbye!")
        break
    
    else:
        print("Invalid choice.")
