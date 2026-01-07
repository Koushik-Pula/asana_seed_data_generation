import random
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from models.database import Task, Project, Section
from utils.distributions import get_realistic_task_duration
from utils.llm_client import generate_task_content 

logger = logging.getLogger(__name__)

def create_tasks_for_project(session: Session, project: Project, users: list):
    sections = sorted(project.sections, key=lambda s: s.rank)
    total_sections = len(sections)
    
    if not total_sections:
        return []

    tasks_created = []

    for index, section in enumerate(sections):
        progress_ratio = (index + 1) / total_sections
        completion_prob = progress_ratio ** 2  
        
        name_lower = section.name.lower()
        if any(x in name_lower for x in ['done', 'complete', 'shipped', 'released']):
            completion_prob = 0.98
        elif any(x in name_lower for x in ['backlog', 'todo', 'idea']):
            completion_prob = 0.05

        num_tasks = random.randint(3, 8)
        
        task_contents = generate_task_content(
            dept="General",
            section_name=section.name, 
            count=num_tasks
        )

        for content in task_contents:
            days_ago = random.randint(1, 90)
            created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
            
            duration_days = get_realistic_task_duration()
            due_date = created_at + timedelta(days=duration_days)

            is_completed = random.random() < completion_prob
            completed_at = None

            if is_completed:
                variance_days = random.uniform(-2, 5)
                completion_time = due_date + timedelta(days=variance_days)
                
                if completion_time < created_at:
                    completion_time = created_at + timedelta(hours=random.randint(1, 24))
                
                if completion_time > datetime.now(timezone.utc):
                    completion_time = datetime.now(timezone.utc) - timedelta(minutes=random.randint(10, 1000))

                completed_at = completion_time

            assignee = random.choice(users) if users and random.random() > 0.15 else None

            new_task = Task(
                project_id=project.id,
                section_id=section.id,
                name=content['title'],
                description=content['description'],
                priority=random.choice(["Low", "Medium", "High"]),
                assignee_id=assignee.id if assignee else None,
                created_at=created_at,
                due_date=due_date,
                is_completed=is_completed,
                completed_at=completed_at
            )
            
            session.add(new_task)
            tasks_created.append(new_task)

    logger.info(f" Generated {len(tasks_created)} tasks for project '{project.name}'")
    return tasks_created