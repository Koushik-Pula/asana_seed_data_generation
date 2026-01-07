import random
import logging
import os
import math
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm 

load_dotenv()

from models.database import Base, Organization, Team, User
from scrapers.company_fetcher import fetch_real_company_names
from generators.users import generate_users
from generators.projects import create_projects_for_team
from generators.tasks import create_tasks_for_project
from utils.constants import DEPARTMENT_ROLES

os.makedirs("output", exist_ok=True)
DB_PATH = "sqlite:///output/asana_simulation.sqlite"

NUM_USERS = 5000 
TARGET_TEAM_SIZE = 12

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def init_db():
    engine = create_engine(DB_PATH)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def main():
    logger.info(f"Starting Production Simulation for {NUM_USERS} Users...")
    
    Session = init_db()
    session = Session()
    
    try:
        logger.info("Stage 1: Creating Organization")
        company_names = fetch_real_company_names(limit=5)
        chosen_name = random.choice(company_names) if company_names else "Globex Corp"
        
        org = Organization(name=chosen_name, domain=f"{chosen_name.lower().replace(' ', '')}.com")
        session.add(org)
        session.flush()
        logger.info(f"   -> Company: {org.name}")

        num_teams_needed = math.ceil(NUM_USERS / TARGET_TEAM_SIZE)
        logger.info(f"Stage 2: Scaling Architecture to {num_teams_needed} Teams")
        
        teams = []
        dept_names = list(DEPARTMENT_ROLES.keys())
        
        for i in range(num_teams_needed):
            dept = dept_names[i % len(dept_names)] 
            team_num = (i // len(dept_names)) + 1
            
            team = Team(
                org_id=org.id, 
                name=f"{dept} - Squad {team_num}", 
                description=f"{dept} Unit {team_num}"
            )
            session.add(team)
            teams.append(team)
            
        session.flush()
        logger.info(f"   -> Created {len(teams)} Teams across {len(dept_names)} Departments.")

        logger.info(f"Stage 3: Mass Hiring {NUM_USERS} Employees")
        all_users = generate_users(session, org.id, teams, NUM_USERS)
        
        logger.info("Stage 4: Generating Enterprise Work History")
        
        total_projects = 0
        total_tasks = 0

        for team in tqdm(teams, desc="Processing Teams"):
            projects = create_projects_for_team(session, team, num_projects=random.randint(1, 4))
            total_projects += len(projects)
            
            for proj in projects:
                team_members = [
                    u for u in all_users 
                    if u.memberships and any(m.team_id == team.id for m in u.memberships)
                ]
                
                if not team_members: 
                    team_members = random.sample(all_users, min(3, len(all_users)))

                tasks = create_tasks_for_project(session, proj, team_members)
                total_tasks += len(tasks)

            if len(teams) > 100 and team.id.endswith("0"): 
                session.commit()

        logger.info("Final Database Commit...")
        session.commit()
        
        file_size_mb = os.path.getsize("output/asana_simulation.sqlite") / (1024 * 1024)

        print("\n" + "="*40)
        print("PRODUCTION BUILD COMPLETE")
        print(f"Company:   {org.name}")
        print(f"Employees: {len(all_users)}")
        print(f"Teams:     {len(teams)}")
        print(f"Projects:  {total_projects}")
        print(f"Tasks:     {total_tasks}")
        print(f"Database:  {DB_PATH} ({file_size_mb:.2f} MB)")
        print("="*40 + "\n")

    except Exception as e:
        logger.error(f"Simulation Failed: {e}")
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    main()