import json
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from system.database.database import DataBase

class System:
    def __init__(self) -> None:
        self.allowed_actions = """
        Allowed actions can be found below:
        1. Add new habit:  -a <name> -d <description> -s <start_date>
        2. End habit:   -e <name>
        3. Delete habit:  -d <name>
        4. Show all habits:  -show
        5. Log habit:   -l <name>
        6. Get streaks:  -streaks
        7. Get progress: -p <name>
        8. Help     -help
        9. Exit     -exit
        """
        self.system_active = True
        self.database = DataBase(file_path="D:\CODE\python_curs\HABIT-TRACKER\memory\data_base.json")
    
    def save_database(self):
        """
        Save database
        """
        self.database.save_database_state()

    def run(self):
        """
        Main loop of the system
        """
        while self.system_active:
            user_input = input("Enter action (type <-help> if you want to see the actions available): ")
            if user_input.startswith("-a"):
                self.add_habit(user_input)
            elif user_input.startswith("-d"):
                self.delete_habit(user_input)
            elif user_input.startswith("-e"):
                self.end_habit(user_input)
            elif user_input.startswith("-show"):
                self.show_all_habits()
            elif user_input.startswith("-l"):
                self.log_habit(user_input)
            elif user_input.startswith("-streaks"):
                self.get_streaks()
            elif user_input.startswith("-p"):
                self.get_progress_graph(user_input)
            elif user_input.startswith("-help"):
                print(self.allowed_actions)
            elif user_input.startswith("-exit"):
                self.system_active = False
            else:
                print("Invalid action. Please type <-help> to see the actions available")
    
    def process_user_input(self, user_input: str, allowed_action: str):
        """
        Process user input and return a dictionary with the parameters

        Args:
            user_input (str): The user's input string
            allowed_action (str): The allowed action to be processed

        Returns:
            dict: Dictionary with the parameters
        """

        if not user_input.startswith(allowed_action):
            raise ValueError(f"Invalid action: {user_input}")
        
        parameters = user_input[:]

        parameters_dict = {}
        for parameter in parameters.split("-")[1:]:
            parameters_dict[f"-{parameter[0]}"] = parameter[2:-1]
        
        return parameters_dict

    def add_habit(self, user_input: str):
        """
        Add new habit based on the user input

        Args:
            user_input (str): The user's input string
        """
        print("Adding new habit")
        
        try:
            user_parameters_dict = self.process_user_input(user_input, allowed_action="-a ")
            today_date = datetime.now().strftime("%Y-%m-%d")

            self.database.database["habits"].append(
                {
                    "name": user_parameters_dict["-a"],
                    "description": user_parameters_dict["-d"],
                    "start_date": user_parameters_dict["-s"],
                    "end_date": None,
                    "streak": 1,
                    "logs": [{"date": today_date}]
                }
            )
            self.save_database()
            print("New habit added successfully")
        except KeyError:
            print("Invalid parameters. Please type <-help> to see the actions available")

    def delete_habit(self, user_input: str):
        """
        Delete a certain habit

        Args:
            user_input (str): The user's input string
        """
        user_parameters_dict = self.process_user_input(user_input, allowed_action="-d ")

        for habit in self.database.database["habits"]:
            if habit["name"] == user_parameters_dict["-d"]:
                self.database.database["habits"].remove(habit)
                self.save_database()
                print(f"Habit {habit['name']} deleted successfully")
                return
        print("Habit not found")
        return

    def end_habit(self, user_input: str):
        """
        Ending habit today

        Args:
            user_input (str): The user's input string
        """

        user_parameters_dict = self.process_user_input(user_input, allowed_action="-e ")
        today_date = datetime.now().strftime("%Y-%m-%d")

        for habit in self.database.database["habits"]:
            if habit["name"] == user_parameters_dict["-e"] and habit["end_date"] == None:
                habit["end_date"] = today_date
                self.save_database()
                print(f"Habit {habit['name']} ended successfully")
                return
        print("Habit not found")
        return
    
    def show_all_habits(self):
        """
        Show all habits
        """
        print("Showing all habits")
        for habit in self.database["habits"]:
            print(f"{habit['name']} - {habit['description']} (Streak: {habit['streak']})")
    
    def get_streaks(self, habit):
        """
        Get streaks

        Args:
            habit (str): The user's input string
        """
        print("Getting streaks")
        for habit in self.database.database["habits"]:
            if habit["name"] == habit:
                return f"{habit['name']}: {habit['streak']} days"
        return f"There is no streak for this habit"

    def get_progress_graph(self, user_input: str):
        """
        Shows the progress for a habit through a graph, to see the streaks evolution.

        Args:
            user_input (str): The user's input string
        """

        try:
            user_parameters_dict = self.process_user_input(user_input, allowed_action="-p ")
            habit_name = user_parameters_dict["-p"]

            for habit in self.database.database["habits"]:
                if habit["name"] == habit_name:
                    dates = sorted([datetime.strptime(log["date"], "%Y-%m-%d") for log in habit["logs"]])

                    fig, ax = plt.subplots(figsize=(9, 3))
                    ax.plot(dates, range(1, len(dates) + 1), marker='o', linestyle='-', color='g')
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Streak Length")
                    ax.set_title(f"Habit Streak Progress: {habit['name']}")
                    st.pyplot(fig)

                    break
                else:
                    print("No progress data avilable for this habit")
        except KeyError:
            print("Invalid parameters. Please type <-help> to see the actions available.")  

    def log_habit(self, user_input: str):
        """
        Log daily progress for a habit, updating its streak.

        Args:
            user_input (str): The user's input string
        """

        try:
            user_parameters_dict = self.process_user_input(user_input, allowed_action="-l ")

            habit_name = user_parameters_dict["-l"]
            today_date = datetime.now().strftime("%Y-%m-%d")

            for habit in self.database.database["habits"]:
                if habit["name"] == habit_name  and habit["end_date"] == None:
                    if any(log["date"] == today_date for log in habit["logs"]):
                        print(f"Habit '{habit_name}' is already logged today!")
                        return
                    habit["logs"].append({"date": today_date})
                    habit["logs"].sort(key=lambda log: log["date"])

                    if len(habit["logs"]) > 1:
                        prev_date = datetime.strptime(habit["logs"][-2]["date"], "%Y-%m-%d")
                        curr_date = datetime.strptime(today_date, "%Y-%m-%d")
                        if (curr_date - prev_date).days == 1:
                            habit["streak"] += 1
                        else:
                            habit["streak"] = 1
                        
                        self.save_database()
                        print(f"Habit '{habit_name}' logged successfully today! Keep going!")
                        return

            print("Habit not found or ended already!")
        except KeyError:
            print("Invalid parameters. Please type <-help> to see the actions available.")