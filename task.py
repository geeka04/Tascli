import json
import os
import argparse
from argparse import Namespace
from datetime import datetime
from tabulate import tabulate

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
    delete_parser.add_argument('id', type = int, help = "id of the task to be deleted")

    # update sub command
    update_parser = subparsers.add_parser('update', help = "update a task")
    update_parser.add_argument('id', type = int, help = "id of the task")
    update_parser.add_argument('new_desc', help = "description to be updated")

    # update status
    inprogress_parser = subparsers.add_parser('mark-in-progress', help = "update the status of a task as in-progress")
    inprogress_parser.add_argument('id', type = int, help = "the id of the task to update its status")

    done_parser = subparsers.add_parser('mark-done', help = "update status of a task as done")
    done_parser.add_argument('id', type = int, help = "the id of the task to update its status")

    # list tasks
    list_parser = subparsers.add_parser('list', help = "command to list tasks")
    list_parser.add_argument('status', nargs = '?', choices = ['to-do', 'in-progress', 'done'])

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
            print("Task updated successfuly")
            return
    print("task id not found")

# delete a task
def delete_task(id : int, tasks: list[dict]) -> None:
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            print("task deleted successfully")
            return
    print("task id not found")

# mark-in-progress or mark-done
def status_update(status : str, id : int, tasks : list[dict]) -> None :
    for task in tasks:
        if task['id'] == id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            print("status updated successfully")
            return
    print("id not found")    

# list tasks
def list_tasks(status : str, tasks: list[dict]) -> None:
    if status == None:
            print(tabulate(tasks, headers='keys', tablefmt="grid"))
    else:
        status_table = [] 
        for task in tasks:
            if task['status'] == status:
                status_table.append(task)
        if status_table:
            print(tabulate(status_table, headers='keys', tablefmt="grid"))    
        else:
            print(f"No task found with {status}")          
    return
            

def handle_commands(args : Namespace, tasks : list[dict]) -> None :
    match(args.command):
        case "add":
            add_task(args.description, tasks)
        case "update":
            update_task(args.id, args.new_desc, tasks)     
        case "delete":
            delete_task(args.id, tasks)   
        case "mark-in-progress":
            status_update("in-progress", args.id, tasks)
        case "mark-done":
            status_update("done", args.id, tasks)
        case "list":
            list_tasks(args.status, tasks)
    
def main() -> None:
    tasks : list[dict] = load_file()
    args : Namespace = parser_function()
    handle_commands(args, tasks)
    save_file(tasks)

if __name__ == "__main__":
    main()