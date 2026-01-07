# Asana Data Generator (Enterprise Scale)

A robust synthetic data generator that simulates a B2B SaaS environment (like Asana or Jira) at scale. It generates a complete SQLite database containing an organizational hierarchy with **5,000+ users**, dynamic team structures, and realistic project workflows.

## Key Features

* **Enterprise Scaling:** Automatically calculates organizational structure (Squads, Departments) based on user count to maintain realistic manager-to-report ratios.
* **AI-Powered Content:** Integrated with **Google Gemini (Flash/Pro Model)** to generate context-aware, unique task titles and descriptions.
* **Robust Fallback:** If no API key is provided, the system seamlessly switches to a high-fidelity **Mock Data** engine, ensuring the simulation always completes successfully.
* **Data Integrity:** Enforces referential integrity, unique email constraints, and strict temporal logic (e.g., tasks cannot be completed before they are created).

## Project Structure

asana-generator/
├── src/
│   ├── generators/       # Logic for creating Users, Projects, and Tasks
│   ├── models/           # SQLAlchemy ORM definitions (Database Schema)
│   ├── scrapers/         # Utility to fetch real company names
│   ├── utils/            # Helper functions and Constants
│   │   └── llm_client.py # Handles Google Gemini connection & Mock fallback
│   └── main.py           # The Orchestrator script
├── output/               # Generated .sqlite files will appear here
├── check_db.py           # Script to verify database integrity
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (API Key) - YOU MUST CREATE THIS

## Setup & Installation

### 1. Prerequisites
* Python 3.8+
* pip

### 2. Install Dependencies
Navigate to the project root and run:
pip install -r requirements.txt

### 3. Configure AI Generation (CRITICAL STEP)
This project uses **Google Gemini** for generating realistic text. While optional (fallback mock data is available), setting this up is highly recommended for realistic output.

**Step A: Get a Free Key**
Visit https://aistudio.google.com/app/apikey and create a new API key.

**Step B: Create the Configuration File**
You must manually create a file named `.env` in the root folder of this project (next to `requirements.txt`).

**Step C: Add Your Key**
Open the `.env` file and add exactly this line (replace with your actual key):

GEMINI_API_KEY=your_google_api_key_here

> **IMPORTANT:** > 1. The file name must be exactly `.env`.
> 2. The variable name must be exactly `GEMINI_API_KEY`.
> 3. Do not use quotes around the key.

## Usage

To start the simulation, run the main script:

python src/main.py

**What happens next?**
1.  **Organization Layer:** Creates a company and fetches real corporate domains.
2.  **Team Scaling:** Dynamically creates ~400+ teams (Engineering, Marketing, Sales) to support the workforce.
3.  **Hiring:** Generates 5,000 unique user profiles and assigns them to teams with correct roles (Admin vs Member).
4.  **Work Generation:** Creates projects and populates them with tasks using AI (if key is valid) or Mock data.
5.  **Output:** Saves the result to `output/asana_simulation.sqlite`.

## Verifying the Data

Once the simulation finishes, you can verify the integrity of the data (5,000 users, team distribution, etc.) by running the included inspection script:

python check_db.py

Alternatively, you can inspect the file using any standard SQL viewer, such as DB Browser for SQLite.

## Database Schema Overview

The generated SQLite database contains the following relational tables:

* **`organizations`**: The root entity.
* **`teams`**: Functional groups linked to the organization.
* **`users`**: Employees with unique emails and specific roles.
* **`team_memberships`**: Junction table linking Users to Teams (Many-to-Many).
* **`projects`**: Work containers owned by teams.
* **`sections`**: Kanban columns (e.g., "To Do", "In Progress").
* **`tasks`**: Individual work items with status, priority, and assignees.