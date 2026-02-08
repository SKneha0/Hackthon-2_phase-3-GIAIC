#!/usr/bin/env python3
"""
Script to check if tasks are being created in the database
"""
import os
from sqlmodel import SQLModel, Session, select
from models import Task
from db import engine

def check_tasks():
    """Check tasks in the database"""
    # Create a new database session
    with Session(engine) as session:
        # Query all tasks
        tasks = session.exec(select(Task)).all()
        
        print(f"Found {len(tasks)} tasks in the database:")
        for task in tasks:
            print(f"- ID: {task.id}, Title: {task.title}, Completed: {task.completed}, User ID: {task.user_id}")

if __name__ == "__main__":
    check_tasks()