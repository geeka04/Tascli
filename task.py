import sys
import json
import os
from datetime import datetime

TASK_FILE = "task.json"

# loading the json file
def load_file():
    if not os.path.exists(TASK_FILE):
        return[]
    with open(TASK_FILE,'r') as file:
        return json.load(file)

# saving a change to json file
def save_file(tasks):
    with open(TASK_FILE,'w') as file:
        json.dump(tasks, file, indent=2)
    
# add a task
def add_task(description):
    tasks = load_file()
    task_id = len(tasks) + 1
    new_task = {
        "id" : task_id,
        "description" : description,
        "status" : "to-do",
        "createdAt" :  datetime.now().isoformat(), #fix format to add to json file.
        "updatedAt" : datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_file(tasks)
    print("Task added successfully")

def main():
    if len(sys.argv) < 2:
        print("usage: task.py <command> [discription]")
        return 
    
    command = sys.argv[1]
    match command:
        case "add":
            if len(sys.argv) < 3:
                print("Error: Description is required for adding a task.")
                return
            description = sys.argv[2]
            add_task(description)

        case "update":
            return "one"
        case "delete":
            return "two"
        case default:
            return "Unexpected error occured. Check format"
        
if __name__ == "__main__":
    main()
