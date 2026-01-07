import random
import logging
from sqlalchemy.orm import Session
from models.database import Project,Section,Team
from utils.constants import PROJECT_TEMPLATES

logger = logging.getLogger(__name__)

def create_projects_for_team(session:Session, team:Team, num_projects=3):
    dept_name = "Operations" #default
    for key in PROJECT_TEMPLATES.keys():
        if key in team.name:
            dept_name = key
            break

    template = PROJECT_TEMPLATES.get(dept_name)

    created_projects = []

    for _ in range(num_projects):
        project_name = random.choice(template["titles"])
        new_project = Project(
            team_id = team.id,
            name = project_name,
            status=random.choice(["On Track", "At Risk", "Off Track"])
        )

        session.add(new_project)
        session.flush()

        for index,section_name in enumerate(template["sections"]):
            new_section = Section(
                project_id = new_project.id,
                name = section_name,
                rank = index
            )
            session.add(new_section)
        
        created_projects.append(new_project)

    logger.info(f"Created {len(created_projects)} projects for {team.name}")
    return created_projects
