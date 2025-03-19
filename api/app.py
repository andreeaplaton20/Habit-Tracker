from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi.responses import Response
import matplotlib.pyplot as plt
import streamlit as st
import sys
import os
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from system.system import System
from system.database.database import DataBase

app = FastAPI(
    title='Personal Habit Tracker API',
    description="Some API for managing my daily",
    version="0.0.1"
)

database = DataBase(file_path="D:\CODE\python_curs\HABIT-TRACKER\memory\data_base.json")

class AddHabit(BaseModel):
    name: str
    description: str
    start_date: str

class DeleteHabit(BaseModel):
    name: str

class LogHabit(BaseModel):
    name: str

class Progress(BaseModel):
    name: str

class Habit(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: Optional[str] = None  
    streak: int
    logs: List[dict]

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello from the Habit Tracker API"}

@app.get("/habits", response_model=List[Habit], tags=["Habits"])
def get_all_habits():
    """Get all habits"""
    return database.database.get("habits", [])

@app.post("/habits", response_model = Habit, tags = ["Habits"])
def add_habit(habit: AddHabit):
    """Adding a new habit"""
    for existing_habit in database.database["habits"]:
        if existing_habit["name"] == habit.name:
            raise HTTPException (
                status_code=400,
                detail="This habit was already added!"
            )
    today_date = datetime.now().strftime("%Y-%m-%d")
    new_habit = {
        "name": habit.name,
        "description": habit.description,
        "start_date": habit.start_date,
        "end_date": None,
        "streak": 1,
        "logs": [{"date": today_date}]
    }
    database.database["habits"].append(new_habit)
    database.save_database_state()

    return new_habit

@app.post("/habits/{name}", tags=["Habits"])
def delete_habit(habit: str):
    """Deleting a certain habit, meaning that we set and ending date for that habit"""
    today_date = datetime.now().strftime("%Y-%m-%d")
    for existing_habit in database.database["habits"]:
            if existing_habit["name"] == habit:
                if existing_habit["end_date"] is None:
                    existing_habit["end_date"] = today_date
                    database.save_database_state()
                    return f"The {habit} habit was ended successfully!"
                else:
                    raise HTTPException (
                        status_code=400,
                        detail="This habit was already ended or hasn't ever existed!"
                    )
    raise HTTPException (
        status_code=404,
        detail="This habit doesn't exist!"
    )

@app.post("/habits/{name}/log", tags=["Habits"])
def log_habit(habit: str):
    """Logging the habit daily to create a streak or not"""
    today_date = datetime.now().strftime("%Y-%m-%d")
    for existing_habit in database.database["habits"]:
        if existing_habit["name"] == habit and existing_habit["end_date"] == None:
            if any(log["date"] == today_date for log in existing_habit["logs"]):
                raise HTTPException (
                    status_code=400,
                    detail="This habit was already logged for today!"
                )
            existing_habit["logs"].append({"date": today_date})
            existing_habit["logs"].sort(key=lambda log: log["date"])

            if len(existing_habit["logs"]) > 1:
                prev_date = datetime.strptime(existing_habit["logs"][-2]["date"], "%Y-%m-%d")
                curr_date = datetime.strptime(today_date, "%Y-%m-%d")
                if (curr_date - prev_date).days == 1:
                    existing_habit["streak"] += 1
                else:
                    existing_habit["streak"] = 1
                        
            database.save_database_state()
            return f"Habit '{habit}' logged successfully today! Keep going!"

    raise HTTPException (
        status_code=404,
        detail="This habit doesn't exist!"
    )
        
@app.get("/habits/{name}/progress", tags=["Habits"])
def get_progress_graph(habit: str):
    """
    Shows the progress for a habit through a graph, to see the streaks evolution.
    """  
    for existing_habit in database.database["habits"]:
        if existing_habit["name"] == habit:
            if not existing_habit["logs"]:
                raise HTTPException (
                    status_code=400,
                    detail="No progress data avilable for this habit!"
                )
            dates = sorted([datetime.strptime(log["date"], "%Y-%m-%d") for log in existing_habit["logs"]])

            fig, ax = plt.subplots(figsize=(9, 3))
            ax.plot(dates, range(1, len(dates) + 1), marker='o', linestyle='-', color='g')
            ax.set_xlabel("Date")
            ax.set_ylabel("Streak Length")
            ax.set_title(f"Habit Streak Progress: {existing_habit['name']}")
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            return Response(buf.getvalue(), media_type="image/png")
    raise HTTPException (
        status_code=404,
        detail="This habit doesn't exist!"
    )

@app.get("/habits/{name}/streak", tags=["Habits"])
def get_streak(habit: str):
    """
    Returns the current streak of a specific habit.
    """
    for existing_habit in database.database["habits"]:
        if existing_habit["name"] == habit:
            return {"habit": habit, "streak": existing_habit["streak"]}
    raise HTTPException (
        status_code = 404,
        detail = "This habit doesn't exist or has been ended so far!"
    )