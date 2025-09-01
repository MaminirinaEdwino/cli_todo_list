import click 
import json
from pathlib import Path
from colored import Fore, Back, Style

FILE_PATH = f"{Path.home()}"+'/task.json'

class Task:
    def __init__(self, name, description):
        self.id = 0
        self.name = name
        self.description = description
        self.status = 'en attente'
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status
        }
    def set_status_to_on_going(self):
        self.status = 'en cours'
    def set_status_to_done(self):
        self.status = 'terminée'
    def set_status_to_blocked(self):
        self.status = 'bloquée'
    def set_id(self, id):
        self.id = id

class TaskList:
    def __init__(self):
        self.tasks = []
    def add_task(self, task):
        self.tasks.append(task)
    def remove_task(self, task):
        self.tasks.remove(task)
    def get_tasks(self):
        return self.tasks
    def to_dict(self):
        return [task.to_dict() for task in self.tasks]
    def load_from_file(self, filename):
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
            for task_data in data['task']:
                task = Task(task_data['name'], task_data['description'])
                task.status = task_data['status']
                task.id = task_data['id']
                self.add_task(task)
    
def save_file(filename, taskList):
    with open(filename, 'w+') as file:
        json.dump(taskList, file, indent=4)
        
@click.group()
def cli():
    pass

@click.command()
def InitTask():
    print("Task Initialisation")
    with open(FILE_PATH, 'w+') as file:
        json.dump({"task": []}, file)
    print("Task Initialised")

@click.command()
@click.option('--name', help='The name of the task.')
@click.option('--description', help='The description of the task.')
@click.argument('name')
@click.argument('description')
def addTask(name, description):
    taskList = TaskList()
    taskList.load_from_file(FILE_PATH)
    status = False
    response = "task already exist"
    task = Task(name, description)
    # task.set_id(len(taskList.get_tasks()) + 1)
    
    if len(taskList.tasks) > 0:
        task.set_id(taskList.tasks[len(taskList.tasks) - 1].id + 1)
    else :
        task.set_id(1)
        
    for task_tmp in taskList.tasks:
        if task_tmp.name == name:
            status = True
            break
        
    if not status:
        taskList.add_task(task)
        response = "Task Added"
    
    save_file(FILE_PATH, {"task": taskList.to_dict()})
    print(response)


@click.command()
@click.option('--id', help="The task id")  
@click.argument("id")
def deleteTask(id):
    taskList = TaskList()
    taskList.load_from_file('task.json')
    status = 'task not found'
    for task in taskList.tasks:
        # print(type(id))
        if task.id == int(id):
            taskList.remove_task(task)
            status = "task deleted"
            
            
    save_file(FILE_PATH, {"task": taskList.to_dict()})
    print(status)
    
@click.command()
def listTask():
    taskList = TaskList()
    taskList.load_from_file(FILE_PATH)
    # print(FILE_PATH)
    if taskList.tasks == []:
        print("empty list")
    for task in taskList.tasks:
        print(f" {Fore.red} {task.id} {Style.reset} | {task.name} | {task.description} | {task.status}")

@click.command()
@click.option("--id", help="task's id")
@click.argument("id")
def starttask(id):
    taskList = TaskList()
    taskList.load_from_file(FILE_PATH)
    tmp = ""
    for task in taskList.tasks:
        if task.id == int(id):
            task.set_status_to_on_going()
            tmp = task
            
    save_file(FILE_PATH, {"task": taskList.to_dict()})
    print(f"{tmp.id} | {tmp.name} | {tmp.description} | {tmp.status}")

@click.command()
@click.option("--id", help="task's id")
@click.argument("id")
def finishTask(id):
    taskList = TaskList()
    taskList.load_from_file(FILE_PATH)
    tmp = ""
    for task in taskList.tasks:
        if task.id == int(id):
            task.set_status_to_done()
            tmp = task
            
    save_file(FILE_PATH, {"task": taskList.to_dict()})
    print(f"{tmp.id} | {tmp.name} | {tmp.description} | {tmp.status}")


@click.command()
@click.option("--id", help="task's id")
@click.argument("id")
def blockTask(id):
    taskList = TaskList()
    taskList.load_from_file(FILE_PATH)
    tmp = ""
    for task in taskList.tasks:
        if task.id == int(id):
            task.set_status_to_done()
            tmp = task
            
    save_file(FILE_PATH, {"task": taskList.to_dict()})
    print(f"{tmp.id} | {tmp.name} | {tmp.description} | {tmp.status}")

cli.add_command(InitTask)
cli.add_command(addTask)
cli.add_command(deleteTask)
cli.add_command(listTask)
cli.add_command(starttask)
cli.add_command(finishTask)
cli.add_command(blockTask)


if __name__ == '__main__':
    cli()