import json
import argparse
from argparse import Namespace



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

def handle_commands(args : Namespace) -> None:
    match(args.command):
        case "add":
            add_task(args.description)
    
def main() -> None:
    file_path = 'task.json'
    handle_commands(parser_function())

if __name__ == "__main__":
    main()