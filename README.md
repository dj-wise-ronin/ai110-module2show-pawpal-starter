# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

### Smarter Scheduling
The PawPal+ system includes several advanced algorithmic features:
- **Priority-Based Scheduling**: Automatically prioritizes essential care tasks (like medication) to fit within your available time.
- **Time Sorting**: Organizes your daily plan chronologically for easier tracking.
- **Conflict Detection**: Alerts you if multiple tasks for the same pet are scheduled at the same time.
- **Recurring Tasks**: Automatically re-schedules daily tasks once they are marked as complete.
- **Filtering**: Easily filter tasks by pet name or completion status to focus on what matters.

## 📸 Demo

<a href="#"><img src='https://via.placeholder.com/800x400?text=PawPal+App+Screenshot' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Testing PawPal+

To ensure the reliability of the scheduling logic, PawPal+ includes an automated test suite.

### Running Tests
```bash
python3 -m pytest tests/test_pawpal.py
```

### Coverage
The tests verify:
- **Task Recurrence**: Daily tasks correctly generate new instances upon completion.
- **Sorting Accuracy**: Tasks are correctly ordered by time.
- **Conflict Logic**: Scheduler correctly identifies overlapping tasks for the same pet.
- **Priority Logic**: High-priority tasks are correctly scheduled first.
- **Time Constraints**: The scheduler strictly respects the user's available time.

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5) - Core scheduling and data integrity are fully verified by automated tests.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
