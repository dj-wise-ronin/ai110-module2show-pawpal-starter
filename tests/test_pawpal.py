import pytest
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion_and_recurrence():
    """Verify that marking a daily task complete creates a new task for the following day."""
    task = Task("Daily Meds", duration=5, priority=1, category="Meds", frequency="Daily", time="08:00")
    
    assert task.is_completed is False
    new_task = task.mark_completed()
    
    assert task.is_completed is True
    assert new_task is not None
    assert new_task.description == "Daily Meds"
    assert new_task.is_completed is False
    assert new_task.time == "08:00"

def test_scheduler_sorting_by_time():
    """Verify tasks are returned in chronological order."""
    t1 = Task("Dinner", duration=15, priority=1, category="Food", time="18:00")
    t2 = Task("Breakfast", duration=10, priority=1, category="Food", time="07:30")
    t3 = Task("Lunch", duration=20, priority=1, category="Food", time="12:00")
    
    scheduler = Scheduler(available_time=100, tasks=[t1, t2, t3])
    sorted_tasks = scheduler.sort_tasks_by_time()
    
    assert sorted_tasks[0].time == "07:30"
    assert sorted_tasks[1].time == "12:00"
    assert sorted_tasks[2].time == "18:00"

def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times for the same pet."""
    pet_name = "Buddy"
    t1 = Task("Walk 1", duration=30, priority=1, category="Walk", time="09:00", pet_name=pet_name)
    t2 = Task("Feeding", duration=10, priority=1, category="Food", time="09:00", pet_name=pet_name)
    t3 = Task("Other Pet Task", duration=10, priority=1, category="Misc", time="09:00", pet_name="Whiskers")
    
    scheduler = Scheduler(available_time=120, tasks=[t1, t2, t3])
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 1
    assert "CONFLICT: Buddy" in conflicts[0]
    assert "Walk 1" in conflicts[0]
    assert "Feeding" in conflicts[0]
    # Should not conflict with Whiskers at the same time
    assert "Whiskers" not in "".join(conflicts)

def test_filtering_logic():
    """Verify that filtering tasks by pet and status works correctly."""
    owner = Owner(name="Ronin")
    buddy = Pet(name="Buddy", species="Dog", age=3, breed="Mix")
    whiskers = Pet(name="Whiskers", species="Cat", age=5, breed="Mix")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    
    t1 = Task("Buddy Walk", duration=30, priority=1, category="Walk")
    t2 = Task("Whiskers Feed", duration=10, priority=1, category="Food")
    
    buddy.add_task(t1)
    whiskers.add_task(t2)
    
    # Filter by pet
    buddy_tasks = owner.filter_tasks(pet_name="Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].description == "Buddy Walk"
    
    # Filter by completion
    t1.mark_completed()
    completed_tasks = owner.filter_tasks(status=True)
    assert len(completed_tasks) == 1
    assert completed_tasks[0].description == "Buddy Walk"

def test_generate_plan_priority_and_time():
    """Verify generate_plan respects priority first, then fits in time."""
    t_high = Task("High Prio Long", duration=60, priority=1, category="Work", time="10:00")
    t_med = Task("Med Prio Short", duration=10, priority=2, category="Work", time="08:00")
    
    # Only 65 minutes available. Should take High Prio Long (60) and then not have room for Med Prio
    # Wait, 60+10 = 70. 
    scheduler = Scheduler(available_time=65, tasks=[t_high, t_med])
    plan = scheduler.generate_plan()
    
    assert len(plan) == 1
    assert plan[0].description == "High Prio Long"
