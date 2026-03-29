from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    duration: int  # in minutes
    priority: int  # 1 (High), 2 (Medium), 3 (Low)
    category: str  # e.g., 'Feeding', 'Walk', 'Meds'
    time: str = "09:00"  # HH:MM format
    frequency: str = "Once"  # 'Once', 'Daily'
    pet_name: str = ""
    is_completed: bool = False

    def mark_completed(self) -> Optional['Task']:
        """Marks the task as completed. If recurring, returns a new task for the next day."""
        self.is_completed = True
        if self.frequency == "Daily":
            # In a real app, we'd handle dates, but for this logic, 
            # we'll just return a fresh instance of the same task.
            return Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                time=self.time,
                frequency=self.frequency,
                pet_name=self.pet_name
            )
        return None

@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a new care task specifically for this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_info(self) -> str:
        """Returns a formatted string containing the pet's basic information."""
        return f"{self.name} ({self.species}, {self.age} years old, {self.breed})"

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a new pet instance to the owner's collection."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Gathers and returns all tasks from every pet owned by this person."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_tasks(self, pet_name: Optional[str] = None, status: Optional[bool] = None) -> List[Task]:
        """Filters tasks by pet name or completion status."""
        tasks = self.get_all_tasks()
        if pet_name:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if status is not None:
            tasks = [t for t in tasks if t.is_completed == status]
        return tasks

@dataclass
class Scheduler:
    available_time: int  # available time in minutes for the day
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Appends a new task to the scheduler's internal list of activities."""
        self.tasks.append(task)

    def sort_tasks_by_time(self) -> List[Task]:
        """Returns tasks sorted by their scheduled time (HH:MM)."""
        return sorted(self.tasks, key=lambda x: datetime.strptime(x.time, "%H:%M"))

    def detect_conflicts(self) -> List[str]:
        """Checks if multiple tasks for the same pet overlap in time (simple exact match check)."""
        warnings = []
        time_map = {} # (pet_name, time) -> task_description
        
        for task in self.tasks:
            key = (task.pet_name, task.time)
            if key in time_map:
                warnings.append(f"CONFLICT: {task.pet_name} has two tasks scheduled at {task.time}: '{time_map[key]}' and '{task.description}'")
            else:
                time_map[key] = task.description
        return warnings

    def generate_plan(self) -> List[Task]:
        """Creates an optimized daily task list based on priority and time constraints."""
        # Sort by priority first, then by time
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.priority, datetime.strptime(x.time, "%H:%M")))
        
        plan = []
        current_time = 0
        for task in sorted_tasks:
            if current_time + task.duration <= self.available_time:
                plan.append(task)
                current_time += task.duration
        return plan

    def get_total_duration(self, task_list: List[Task]) -> int:
        """Calculates the combined duration in minutes for all tasks in the provided list."""
        return sum(task.duration for task in task_list)
