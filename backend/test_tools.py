#!/usr/bin/env python3
"""
Script to test if tools are working correctly
"""
import asyncio
from src.tools.task_tools import add_task, list_tasks, complete_task

async def test_tools():
    """Test the task tools directly"""
    user_id = "test_user"
    
    print("Testing add_task...")
    result = await add_task(title="Test task from direct tool call", user_id=user_id)
    print(f"Add task result: {result}")
    
    print("\nTesting list_tasks...")
    result = await list_tasks(user_id=user_id)
    print(f"List tasks result: {result}")
    
    # Get the task ID from the result to test completion
    if result["success"] and len(result["tasks"]) > 0:
        task_id = result["tasks"][0]["id"]
        print(f"\nTesting complete_task for task ID {task_id}...")
        result = await complete_task(task_id=task_id, user_id=user_id)
        print(f"Complete task result: {result}")
    
    print("\nTesting list_tasks again to see if task was completed...")
    result = await list_tasks(user_id=user_id)
    print(f"List tasks result after completion: {result}")

if __name__ == "__main__":
    asyncio.run(test_tools())