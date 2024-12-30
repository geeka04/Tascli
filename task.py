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
    if not tasks:
        task_id = 1
    else:
        task_id = max(task['id'] for task in tasks) + 1

    new_task = {
        "id" : task_id,
        "description" : description,
        "status" : "to-do",
        "createdAt" :  datetime.now().isoformat(), 
        "updatedAt" : datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_file(tasks)
    print("Task added successfully")

# update a task
def update_task(id, new_description):
    tasks = load_file()
    for task in tasks:
        if task["id"] == int(id):
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_file(tasks)
            print("Task updated successffully")
            return
    print("Task not found")    

#  delete a task 
def delete_task(id):
    tasks = load_file()
    tasks = [task for task in tasks if task['id'] != int(id)]
    save_file(tasks)
    print("Task deleted successfuly")

# mark in-progress and done
def mark_ip(id):
    tasks = load_file()
    for task in tasks:
        if task['id'] == int(id):
            task['status'] = "in-progress"
            task['updatedAt'] = datetime.now().isoformat()
            save_file(tasks)
            print('updated successfully')

def mark_done(id):
    tasks = load_file()
    for task in tasks:
        if task['id'] == int(id):
            task['status'] = "done"
            task['updatedAt'] = datetime.now().isoformat()
            save_file(tasks)
            print('updated successfully')


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
            id = sys.argv[2]
            new_desc = sys.argv[3]
            update_task(id, new_desc)

        case "delete":
            id = sys.argv[2]
            return delete_task(id)    

        case "mark-in-progress":
            id = sys.argv[2]
            return mark_ip(id)    
        
        case "mark-done":
            id = sys.argv[2]
            return mark_done(id)    
        
        case default:
            return "Invalid command"
        
if __name__ == "__main__":
    main()
