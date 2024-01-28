# Installation

  ## Clone this repository to your local machine:

  ```bash
    git clone https://github.com/vishnuk-24/user-role-management.git
  ```
  ## For latest code
  ```bash
    git pull origin main
  ```

## Creating and Activating a Virtual Environment

Before you start working on this project, it's essential to set up a virtual environment. A virtual environment is a self-contained Python environment that isolates your project's dependencies from the system-wide Python installation. This helps maintain a clean and consistent environment for your project.

To create a virtual environment, open a terminal and navigate to your project directory. Run the following command to create a virtual environment named 'env':

  For Windows:

  ```bash
  virtualenv env
  ```
  For Linux:
  ```bash
  python -m venv .env
  ```
  For activation:
  ```bash
  .\.env\Scripts\activate  #windows
  source .env/bin/activate  #linux
  ```
  To deactivate the virtual environment, simply run the following command in your terminal:
  ```bash
  deactivate
  ```
  To install the project's dependencies from the requirements.txt file within the virtual environment, use the following command

  ```bash
  pip install -r requirements.txt
  ```

## Using Docker for Development

### Creating Docker Files

To containerize your project for development, you'll need to create two essential Docker files:

1. **Dockerfile**: This file contains the necessary instructions to build a Docker image for your Django project.

2. **docker-compose.yml**: This file contains the configuration for your Django application and any related services (e.g., a database).

### Building Docker Images

Install Docker Compose by following the instructions here:

Install Docker Compose.

To build Docker images for your project and its services, use the following command:

```bash
docker compose up -d   # This builds all images configured in the docker-compose.yml file
```
When there is a change only in one of the services, for eg: API code base, run:
```bash
docker compose up -d --no-deps  # This rebuilds only the service in which changes are made.
```
To check logs use the following commands:

```bash
docker logs acedemy -tf  # for app logs
```

Create superuser for admin access
```bash
sudo docker exec -it <container_name_or_id> python manage.py createsuperuser
```

## Example Data Retrieval Using the Django Shell

You can interact with your Django project and its models using the Django shell. To enter the Django shell, follow these steps:

1. Open a terminal.

2. Navigate to your project's root directory if you're not already there. (the directory which have manage.py)

3. Activate your virtual environment if you haven't already done so. You can activate it using the following command:

    For Windows:

    ```bash
    .\.env\Scripts\activate
    ```
    For Linux:
    ```bash
    source .env/bin/activate
    ```
    Enter below command to enter into Django shell:
    ```bash
    python manage.py shell
    ```

## Setting Environment Variables

Use the .env_sample file content to set the .env file while deployment, before the docker run.

The db values needs to be set based on local db user and name.

## Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Creating a Superuser

To create a superuser (admin) account for the Django admin panel, run the following command:

```bash
python manage.py createsuperuser
```

## Usage

To start the development server and make your Django application accessible on a specific IP address, run the following command, replacing `<your-desired-ip>` with the IP address you want to use:

```bash
python manage.py runserver <your-desired-ip>:8000
```
