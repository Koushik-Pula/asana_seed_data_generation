import random
import logging
from faker import Faker
from sqlalchemy.orm import Session
from models.database import User, Team, TeamMembership
from utils.constants import DEPARTMENT_ROLES

fake = Faker()
logger = logging.getLogger(__name__)

def generate_users(session: Session, org_id: str, teams: list, count: int):
    logger.info(f"Generating {count} user profiles...")
    
    users = []
    generated_emails = set()
    
    team_has_admin = {team.id: False for team in teams}
    
    for _ in range(count):
        profile = fake.simple_profile()
        email = profile['mail']
        
        while email in generated_emails:
            username = profile['username']
            email = f"{username}{random.randint(100, 999)}@example.com"
        
        generated_emails.add(email)
        
        user = User(
            org_id=org_id,
            full_name=profile['name'],
            email=email,
            is_active=True,
            role="Member"
        )
        
        session.add(user)
        session.flush() 
        
        if teams:
            team = random.choice(teams)
            
            dept_key = next((k for k in DEPARTMENT_ROLES.keys() if k in team.name), "Operations")
            possible_roles = DEPARTMENT_ROLES.get(dept_key, ["Member"])
            user.role = random.choice(possible_roles)

            if not team_has_admin[team.id]:
                role_in_team = "admin"
                team_has_admin[team.id] = True
                user.role = f"{dept_key} Lead" 
            else:
                role_in_team = "member"
            
            membership = TeamMembership(
                user_id=user.id,
                team_id=team.id,
                role=role_in_team
            )
            session.add(membership)
        
        users.append(user)
        
    session.flush()
    logger.info(f"Created {len(users)} users with unique emails.")
    return users