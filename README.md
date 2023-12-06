# Research Laboratory API Server

Welcome to the Research Laboratory API Server repository! This project provides a RESTful API server tailored for a
research laboratory environment, facilitating the management of various aspects of the lab's activities. The server is
built on Django, a high-level Python web framework.

## Features

### 1. Automatic Publication List Updates

- The API server automatically updates the publication list based on a BibTeX file, ensuring that the latest research
  outputs are always reflected.

### 2. Dynamic Content Management

- The server provides endpoints to publish and manage news, highlights, and vacancies, offering a dynamic platform to
  share updates with the lab community.
- The Django Admin panel is activated, allowing administrators to dynamically manage the database, ensuring flexibility
  in data management.

### 3. Research Topics, Projects, and Collaborators

- Define and retrieve lists of research topics, projects, and collaborator groups and institutes, offering a
  comprehensive overview of the lab's focus areas and ongoing initiatives.

### 4. People and Roles

- Maintain a list of lab members with different roles, making it easy to track and manage personnel within the research
  group.

### 5. Software and Tools

- Define and retrieve lists of software and tools utilized within the lab, providing an organized view of the
  technological landscape.
- Obtain detailed information about software and tools, including relevant authors, based on the list of people
  associated with the lab.

## Example

Currently STAR Research Group is using this server. The website is available
at [https://star.inf.usi.ch](https://star.inf.usi.ch).

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/research-lab-api.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser for accessing the Django Admin panel:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the Django Admin panel at `http://localhost:8000/admin/` to start managing the lab's data.

