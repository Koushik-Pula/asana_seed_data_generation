# Asana Data Generator (Enterprise Scale)

A robust synthetic data generator that simulates a B2B SaaS work-management
platform (similar to Asana or Jira) at enterprise scale.

It generates a fully populated SQLite database containing an organizational
hierarchy with 5,000+ users, dynamic team structures, and realistic project
workflows.


## Key Features

- Enterprise Scaling  
  Automatically derives organizational structure (Departments, Squads)
  based on total user count, maintaining realistic manager-to-report ratios.

- AI-Powered Content Generation  
  Integrated with Google Gemini (Flash / Pro models) to generate
  context-aware, unique project names, task titles, and descriptions.

- Robust Fallback Mode  
  If no API key is provided, the system switches to a high-fidelity
  mock data engine so the simulation always completes.

- Strict Data Integrity  
  Enforces referential integrity, unique corporate email constraints,
  and temporal correctness (tasks cannot be completed before creation).


## Project Structure

asana-generator/
├── src/
│   ├── generators/        # Logic for creating Users, Teams, Projects, Tasks
│   ├── models/            # SQLAlchemy ORM models (database schema)
│   ├── scrapers/          # Utilities for fetching real company names/domains
│   ├── utils/             # Shared helpers and constants
│   │   └── llm_client.py  # Google Gemini client with mock fallback
│   └── main.py            # Orchestrator script
├── output/                # Generated SQLite databases
├── check_db.py            # Database integrity verification script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (must be created manually)


## Setup & Installation

### Prerequisites
- Python 3.8+
- pip


### Install Dependencies

From the project root, run:

pip install -r requirements.txt


## Configure AI Generation (Optional but Recommended)

This project uses Google Gemini for realistic text generation.
If no API key is provided, the system automatically falls back to mock data.


### Step 1: Generate an API Key

Create a free API key at:
https://aistudio.google.com/app/apikey


### Step 2: Create the .env File

In the project root (next to requirements.txt), create a file named:

.env


### Step 3: Add the API Key

Add exactly this line (replace with your key):

GEMINI_API_KEY=your_google_api_key_here


IMPORTANT:
- File name must be exactly .env
- Variable name must be GEMINI_API_KEY
- Do not wrap the key in quotes


## Usage

Run the main orchestrator script:

python src/main.py


### What Happens Internally

1. Organization Layer  
   Creates a company and assigns realistic corporate domains.

2. Team Scaling  
   Dynamically generates 400+ teams
   (Engineering, Sales, Marketing, etc.).

3. User Generation  
   Creates 5,000+ unique users and assigns them to teams
   with correct roles (admin vs member).

4. Work Simulation  
   Generates projects, sections, and tasks using:
   - Google Gemini (if API key is present)
   - Mock data engine (fallback)

5. Output  
   Writes the final database to:

output/asana_simulation.sqlite


## Verifying the Data

To validate row counts, relationships, and constraints, run:

python check_db.py

You can also inspect the database using DB Browser for SQLite.


## Database Schema Overview

The generated SQLite database includes the following tables:

- organizations  
  Root entity representing the customer workspace

- teams  
  Functional groups within the organization

- users  
  Employees with unique corporate emails and roles

- team_memberships  
  Junction table linking users and teams (many-to-many)

- projects  
  Work containers owned by teams

- sections  
  Kanban columns (To Do, In Progress, Done)

- tasks  
  Atomic work items with assignees, priority, and lifecycle timestamps

- custom_field_definitions  
  Metadata describing custom fields (EAV pattern)

- custom_field_values  
  Actual custom field values linked to tasks
