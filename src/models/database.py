import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    domain = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    teams = relationship("Team", back_populates="organization")
    users = relationship("User", back_populates="organization")
    custom_fields = relationship("CustomFieldDefinition", back_populates="organization")

class Team(Base):
    __tablename__ = 'teams'
    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, ForeignKey('organizations.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", back_populates="teams")
    projects = relationship("Project", back_populates="team")
    members = relationship("TeamMembership", back_populates="team")

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, ForeignKey('organizations.id'))
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", back_populates="users")
    memberships = relationship("TeamMembership", back_populates="user")
    tasks = relationship("Task", back_populates="assignee")

class TeamMembership(Base):
    __tablename__ = 'team_memberships'
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'))
    team_id = Column(String, ForeignKey('teams.id'))
    role = Column(String, default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="memberships")
    team = relationship("Team", back_populates="members")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, default=generate_uuid)
    team_id = Column(String, ForeignKey('teams.id'))
    name = Column(String, nullable=False)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    team = relationship("Team", back_populates="projects")
    sections = relationship("Section", back_populates="project")
    tasks = relationship("Task", back_populates="project")

class Section(Base):
    __tablename__ = 'sections'
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey('projects.id'))
    name = Column(String, nullable=False)
    rank = Column(Integer)
    
    project = relationship("Project", back_populates="sections")
    tasks = relationship("Task", back_populates="section")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey('projects.id'))
    section_id = Column(String, ForeignKey('sections.id'))
    assignee_id = Column(String, ForeignKey('users.id'), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    
    project = relationship("Project", back_populates="tasks")
    section = relationship("Section", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
    custom_field_values = relationship("CustomFieldValue", back_populates="task")

class CustomFieldDefinition(Base):
    __tablename__ = 'custom_field_definitions'
    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, ForeignKey('organizations.id'))
    name = Column(String, nullable=False)
    field_type = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", back_populates="custom_fields")
    values = relationship("CustomFieldValue", back_populates="definition")

class CustomFieldValue(Base):
    __tablename__ = 'custom_field_values'
    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey('tasks.id'))
    field_definition_id = Column(String, ForeignKey('custom_field_definitions.id'))
    value_text = Column(String, nullable=True)
    value_number = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    task = relationship("Task", back_populates="custom_field_values")
    definition = relationship("CustomFieldDefinition", back_populates="values")