# PawPal+ Project Reflection

## 0. User Actions (Brainstorming)

Three core actions a user should be able to perform:
1. **Add and Manage Pets**: Users can register their pets with details like name, species, and age.
2. **Schedule and Prioritize Tasks**: Users can add care tasks (e.g., feeding, walks, medications) with specific durations and priority levels.
3. **Generate a Daily Care Plan**: Users can view an organized schedule of tasks for the day, sorted by priority and fitting within their available time.

## 1. System Design

**a. Initial design**

My initial UML design consists of four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.
- **Owner**: Manages a list of pets and stores the owner's name. It has a one-to-many relationship with the `Pet` class.
- **Pet**: Represents a pet with attributes like name, species, age, and breed. It stores its own care-related tasks.
- **Task**: Represents a specific care activity (e.g., walking, feeding) with a description, duration, priority level, and category. It is associated with a specific pet.
- **Scheduler**: The logic engine that holds a collection of tasks and a time constraint. Its primary responsibility is to sort tasks by priority and generate a daily plan that fits within the owner's available time.

**b. Design changes**

I modified the `Pet` and `Task` relationship slightly. Instead of just a generic list of tasks in the `Scheduler`, I ensured that each `Pet` instance maintains its own list of `Task` objects. This allows for better encapsulation, as tasks are directly associated with the pet they belong to. I also added a `pet_name` attribute to the `Task` class to simplify displaying which pet a task is for when generating a combined schedule in the `Scheduler`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two primary constraints:
1. **Priority**: Tasks are assigned a priority level (1 for High, 2 for Medium, 3 for Low). High-priority tasks are always scheduled before lower-priority ones.
2. **Available Time**: The user provides a total duration (in minutes) they have available for pet care. The scheduler fits as many high-priority tasks as possible within this limit.

I decided that priority should be the primary constraint because essential care (like medications or feeding) should never be skipped in favor of optional activities (like extra playtime), even if the latter fits better into a time slot.

**b. Tradeoffs**

One tradeoff my scheduler makes is using a **Greedy Approach** based on priority and then duration. If two tasks have the same priority, it picks the shorter one first to maximize the number of tasks completed. A potential downside is that a very long but important task might be skipped if multiple shorter, equal-priority tasks fill up the remaining time. This is reasonable for pet care because completing several smaller essential tasks (like multiple quick feedings or bathroom breaks) is often better than doing one long task and neglecting others.

Another tradeoff is in **Conflict Detection**. My current implementation only flags tasks scheduled at the exact same start time. It does not account for overlapping durations (e.g., a 60-minute walk starting at 8:00 and a 10-minute feeding starting at 8:30). While less precise, this "lightweight" approach avoids the complexity of interval checking while still catching obvious scheduling errors. This is reasonable for a basic assistant where the user can manually adjust for overlaps after seeing the conflict warning.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project for:
- **Design Brainstorming**: I started by asking the AI to generate a Mermaid.js class diagram based on my initial ideas for `Owner`, `Pet`, `Task`, and `Scheduler` classes.
- **Scaffolding**: I used AI to quickly generate the Python dataclass skeletons from my UML design.
- **Refactoring**: I asked for a more readable way to print the schedule in `main.py` and for help integrating my logic into the Streamlit `app.py`.
- **Testing**: I used AI to generate `pytest` cases for my core scheduling logic, which helped me identify edge cases like fitting exactly within the time limit or handling multiple priorities.

**b. Judgment and verification**

In one instance, the AI suggested that the `Scheduler` should be responsible for storing all tasks. I realized that it was better for the `Pet` objects to hold their own tasks to maintain a clearer association between pets and their needs. I chose to have the `Owner` class collect tasks from all its pets and then pass that consolidated list to the `Scheduler`. I verified this approach by ensuring that my `Pet` objects remained the "source of truth" for their own care data.

**c. AI Strategy**

- **Effective Features**: The ability to generate Mermaid.js diagrams and boilerplate `pytest` code was incredibly effective. It saved time on repetitive syntax tasks, allowing me to focus on the architectural relationships.
- **Rejected Suggestions**: I rejected a suggestion to use a complex nested dictionary for the schedule. Instead, I opted for a simple list of `Task` objects, which was much easier to filter and sort using Python's built-in `sorted()` and list comprehensions.
- **Separation of Phases**: I treated each phase as a distinct task (Research, Implementation, Testing), which kept the context window focused and reduced "hallucinations" or irrelevant code suggestions from previous steps.
- **Lead Architect Role**: As the lead architect, I learned that AI is best used as a high-speed drafting tool. It provides options, but I must make the final decision on data structures and relationships to ensure the long-term maintainability of the code.

---

## 4. Testing and Verification

**a. What you tested**

I focused on testing the following behaviors:
1. **Task Completion**: Verified that `mark_completed()` correctly updates the task's state.
2. **Pet Management**: Confirmed that adding a task to a pet correctly increments its internal list and assigns the pet's name to the task.
3. **Priority Sorting**: Ensured the `Scheduler` always picks Priority 1 tasks before Priority 2 or 3, regardless of their order in the input list.
4. **Time Constraints**: Validated that the `Scheduler` does not exceed the `available_time` and correctly handles cases where not all tasks can fit.

**b. Confidence**

I am highly confident in the core logic. The `pytest` suite covers the primary scheduling algorithm and the basic class interactions. To further increase confidence, I would test edge cases like negative durations (which should probably be blocked in the UI), zero `available_time`, and handling a large number of tasks (performance testing).

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the transition from UML design to the working Streamlit UI. Using dataclasses made the implementation clean and easy to integrate with Streamlit's session state.

**b. What you would improve**

If I had another iteration, I would add a "Recurring Tasks" feature. Currently, tasks are one-off activities. Adding the ability to schedule a "Daily Feeding" or "Weekly Grooming" would make the app much more useful for real-world pet care.

**c. Key takeaway**

The most important thing I learned is that designing the system's "brain" (the backend logic) first in a standalone script (`main.py`) and verifying it with tests makes the UI integration much smoother. It separates concerns and allows for faster debugging before dealing with the complexities of a web interface.

