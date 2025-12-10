import os
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import inquirer

# --- Configuration ---
DATA_FILE = "tasks.json"
console = Console()

class TodoApp:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_tasks(self):
        """Save current tasks to the JSON file."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.tasks, f, indent=4)
        except IOError as e:
            console.print(f"[bold red]Error saving tasks: {e}[/bold red]")

    def get_priority_color(self, priority):
        """Return color tag based on priority."""
        colors = {
            "High": "bold red",
            "Medium": "bold yellow",
            "Low": "green"
        }
        return colors.get(priority, "white")

    def display_tasks(self):
        """Render the task table using Rich."""
        console.clear()
        
        # Header
        console.print(Panel.fit(
            "[bold cyan]✨ Ultimate CLI To-Do List ✨[/bold cyan]", 
            box=box.ROUNDED, 
            padding=(1, 4)
        ))

        if not self.tasks:
            console.print("\n[italic dim]No tasks yet! Select 'Add Task' to get started.[/italic dim]\n", justify="center")
            return

        # Task Table
        table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold magenta", expand=True)
        table.add_column("#", style="dim", width=4, justify="center")
        table.add_column("Status", width=8, justify="center")
        table.add_column("Priority", width=10, justify="center")
        table.add_column("Task Description", ratio=1)

        for idx, task in enumerate(self.tasks, 1):
            status_icon = "✅" if task['done'] else "⭕"
            status_style = "dim strike" if task['done'] else ""
            priority_style = self.get_priority_color(task['priority'])
            
            # Format the description (strikethrough if done)
            desc = Text(task['title'], style=status_style)
            
            table.add_row(
                str(idx),
                status_icon,
                f"[{priority_style}]{task['priority']}[/{priority_style}]",
                desc
            )

        console.print(table)
        console.print("\n")

    def add_task(self):
        """Interactive prompt to add a new task."""
        questions = [
            inquirer.Text('title', message="What needs to be done?"),
            inquirer.List('priority',
                          message="Select Priority",
                          choices=['High', 'Medium', 'Low'],
                          default='Medium'
            ),
        ]
        answers = inquirer.prompt(questions)
        if answers and answers['title'].strip():
            self.tasks.append({
                "title": answers['title'],
                "priority": answers['priority'],
                "done": False
            })
            self.save_tasks()
            console.print(f"[bold green]Task added![/bold green]")

    def toggle_task(self):
        """Menu to mark tasks as done/undone."""
        if not self.tasks:
            return

        choices = [
            (f"{'✅' if t['done'] else '⭕'}  {t['title']}", i) 
            for i, t in enumerate(self.tasks)
        ]
        choices.append(("⬅  Back", -1))

        questions = [
            inquirer.List('index',
                          message="Select a task to toggle status",
                          choices=choices,
                          carousel=True
            ),
        ]
        answer = inquirer.prompt(questions)
        
        if answer and answer['index'] != -1:
            idx = answer['index']
            self.tasks[idx]['done'] = not self.tasks[idx]['done']
            self.save_tasks()

    def delete_task(self):
        """Menu to delete tasks."""
        if not self.tasks:
            return

        choices = [
            (f"{t['title']}", i) 
            for i, t in enumerate(self.tasks)
        ]
        choices.append(("⬅  Back", -1))

        questions = [
            inquirer.List('index',
                          message="Select a task to DELETE",
                          choices=choices,
                          carousel=True
            ),
        ]
        answer = inquirer.prompt(questions)
        
        if answer and answer['index'] != -1:
            removed = self.tasks.pop(answer['index'])
            self.save_tasks()
            console.print(f"[bold red]Deleted: {removed['title']}[/bold red]")

    def run(self):
        """Main application loop."""
        while True:
            self.display_tasks()
            
            questions = [
                inquirer.List('action',
                              message="Choose an action",
                              choices=[
                                  ('Add Task', 'add'),
                                  ('Toggle Status (Done/Undo)', 'toggle'),
                                  ('Delete Task', 'delete'),
                                  ('Exit', 'exit')
                              ],
                              carousel=True
                ),
            ]
            
            answer = inquirer.prompt(questions)
            if not answer:
                break
                
            action = answer['action']
            
            if action == 'add':
                self.add_task()
            elif action == 'toggle':
                self.toggle_task()
            elif action == 'delete':
                self.delete_task()
            elif action == 'exit':
                console.print("[bold cyan]Goodbye! 👋[/bold cyan]")
                break

if __name__ == "__main__":
    try:
        app = TodoApp()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]")
