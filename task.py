import json
import os
import argparse
from argparse import Namespace
from datetime import datetime

task_file = "task.json"

# loading the json file
def load_file():
    if not os.path.exists(task_file):
        return[]
    with open(task_file,'r') as file:
        return json.load(file)

# saving a change to json file
def save_file(tasks):
    with open(task_file,'w') as file:
        json.dump(tasks, file, indent=2)
    

def parser_function() -> Namespace: 
    parser = argparse.ArgumentParser(description = "A cli todo app")
    subparsers = parser.add_subparsers(dest = "command")    

    # add sub command
    add_parser = subparsers.add_parser('add', help = "add a new task")
    add_parser.add_argument('description', help = "the task description")

    # delete sub command
    delete_parser = subparsers.add_parser('delete', help = 'delete a task')
    delete_parser.add_argument('id', help = "id of the task to be deleted")

    # update sub command
    update_parser = subparsers.add_parser('update', help = "update a task")
    update_parser.add_argument('id', help = "id of the task")
    update_parser.add_argument('new_desc', help = "description to be updated")

    args = parser.parse_args() 
    return args

# add a task
def add_task(description : str, tasks : list[dict]) -> None:
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
    print("Task added successfully")

# update a task
def update_task(id : int, new_desc : str, tasks : list[dict]) -> None:
    for task in tasks:
        if task['id'] == id:
            task['description'] = new_desc
            task['updatedAt'] = datetime.now().isoformat()
    print("id not found")

def handle_commands(args : Namespace, tasks : list[dict]) -> None:
    match(args.command):
        case "add":
            add_task(args.description, tasks)
        case "update":
            update_task(args.id, args.new_desc, tasks)        
    
def main() -> None:
    tasks : list[dict] = load_file()
    args : Namespace = parser_function()
    handle_commands(args, tasks)
    save_file(tasks)

if __name__ == "__main__":
    main()