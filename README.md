# Habit-Tracker
This is a python project realised at the finish of my Python Fundamentals course at Tekwill Jr.
It provides utilities to track your daily habits, evolving your discipline and improving your life with small steps every day.

Personal Habit Tracker

A. User Interaction
	•	CLI

B. Data Storage & Retrieval
	•	JSON
	•	API Fetching

C. Functions & Modularity
	•	The code it is be modular, meaning:
	    •	It includes six important functions.
	    •	It is separated into different .py files (modules).

D. Error Handling
	•	The project includes error handling using try-except blocks to prevent crashes due to invalid user input or file errors.

E. External Libraries
	    •	fastapi (for simple web applications)
        •   streamlit (for representing the graph)
        •   matplotlab (for creating the graph)
        •   datetime (to get the real time date)

F. Code Documentation & Readability
	•	The project includes:
	    •	Docstrings and comments to explain important parts of the code.
	    •	Proper variable and function naming for readability.
	    •	Code follows the PEP 8 styling guidelines.


CLI(Terminal) application
 - add habit
 - log the habit daily
 - show a progress graph
 - show daily streak
 - add an ending date
 - delete habit

1. Add new habit:  -a <name> -d <description> -s <start_date>
2. Delete habit:  -d <name>
3. End habit:   -e <name>
4. Show all habits:  -show
5. Log habit:   -l <name>
6. Get streaks:  -streaks
7. Get progress: -p <name>