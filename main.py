from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    owner = Owner(name="Ronin")
    buddy = Pet(name="Buddy", species="Dog", age=3, breed="Golden Retriever")
    owner.add_pet(buddy)

    # 1. Sorting Demo: Adding tasks out of order
    buddy.add_task(Task("Dinner", duration=15, priority=1, category="Feeding", time="18:00"))
    buddy.add_task(Task("Morning Walk", duration=30, priority=1, category="Walk", time="07:00"))
    buddy.add_task(Task("Afternoon Play", duration=20, priority=2, category="Exercise", time="15:00"))

    scheduler = Scheduler(available_time=120, tasks=owner.get_all_tasks())
    sorted_tasks = scheduler.sort_tasks_by_time()

    print("--- Sorted Tasks (By Time) ---")
    for t in sorted_tasks:
        print(f"[{t.time}] {t.description}")

    # 2. Conflict Detection Demo: Same pet, same time
    buddy.add_task(Task("Conflict Task", duration=10, priority=1, category="Test", time="07:00"))
    scheduler.tasks = owner.get_all_tasks() # Refresh scheduler tasks
    conflicts = scheduler.detect_conflicts()
    
    if conflicts:
        print("\n--- Conflicts Detected ---")
        for c in conflicts:
            print(c)

    # 3. Filtering Demo: Only 'Walk' category (manual filter for demo) or by pet
    print("\n--- Filtered Tasks (Only Buddy) ---")
    only_buddy = owner.filter_tasks(pet_name="Buddy")
    for t in only_buddy:
        print(f"{t.pet_name}: {t.description}")

    # 4. Recurring Task Demo
    print("\n--- Recurring Task Demo ---")
    daily_meds = Task("Daily Meds", duration=5, priority=1, category="Meds", frequency="Daily")
    buddy.add_task(daily_meds)
    
    # Simulate completing the task
    print(f"Completing: {daily_meds.description} ({daily_meds.frequency})")
    new_task = daily_meds.mark_completed()
    if new_task:
        print(f"Next task automatically created: {new_task.description} at {new_task.time} for tomorrow.")

if __name__ == "__main__":
    main()
