# Analytics API with FastAPI and TimescaleDB  
Own your data pipeline with Python and Postgres

<https://www.codingforentrepreneurs.com/courses/analytics-api-with-fastapi-and-timescaledb>  

## 1 UV Python Project Setup   

```bash
python.exe -m pip install --upgrade pip  
pip install -r requirements.txt 
```

<https://blog.pecar.me/uv-with-django>

### 1.Initialize project

uv init .

if toml file available/linux: 
```bash
uv venv
source .venv/bin/activate
uv pip install . --link-mode=copy
```

### 2.Create environment

```bash
uv venv --python 3.13
uv venv envname
uv venv envname --python 3.12
```  

**NB: Check the .python-version file**
Copilot 
I have updated the .python-version file to specify version 3.13. 
The uv command was likely prioritizing the version specified in that file over the one provided in the command-line arguments. 
With this change, uv should now create a virtual environment with Python 3.13 as intended.

You can now try running your command again:
uv venv --python 3.13

### 3.Activate environment
```bash
win
source .venv/Scripts/activate
source env/Scripts/activate
```

linux/mac
```bash
source .venv/bin/activate
```

### 4.Install packages

```bash
uv pip install --upgrade pip
uv pip install -r requirements.txt
```

The quotes around the package specification are important to prevent shell interpretation of the ">" characters
```bash
uv pip install "Django>=5.2,<5.3"
```

### 5.UV Workflow
```bash
uv init .
uv init proj_name
cd proj_name
uv venv --python 3.12
source .venv/Scripts/activate
uv pip install --upgrade pip
uv pip install -r requirements.txt
```

### 6 UV Migrating from Requirements  

Save dependencies to pyproject.toml:

```bash
uv init .
uv init proj_name
cd proj_name
uv venv --python 3.12
source .venv/Scripts/activate
uv add -r requirements.txt
uv lock
```

### 7 UV Docs Links
[Creating a new project](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)

[Managing dependencies](https://docs.astral.sh/uv/guides/projects/#managing-dependencies)

[Docker example](https://docs.astral.sh/uv/guides/integration/docker/#non-editable-installs)  

[Using uv in pre-commit](https://docs.astral.sh/uv/guides/integration/pre-commit/)  

[Building distributions](https://docs.astral.sh/uv/guides/projects/#building-distributions)

## 2 Git  
```bash
echo "# cfe-fastapi-timescaledb" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/todor1/cfe-fastapi-timescaledb.git
git push -u origin main
```  
```bash

# The error "remote origin already exists" means you've already set up a remote repository named "origin" for your local Git repository. You have a few options to resolve this:

# Verify the existing remote:
git remote -v 

# to list the existing remote repositories and their URLs. This will show you what the current "origin" is pointing to.
# If the existing remote is incorrect:
# 1) Remove the existing remote: 

git remote remove origin

# 2) Add the correct remote: 

git remote add origin https://github.com/todor1/cfe-fastapi-timescaledb.git  

git push --set-upstream origin main

# 3) If you want to keep the existing remote and add a new one:
# Use a different name for the new remote: 
# git remote add <new_remote_name> https://github.com/todor1/cfe-fastapi-timescaledb.git 
# e.g.:

git remote add github https://github.com/todor1/cfe-fastapi-timescaledb.git  

git push --set-upstream origin main
```


<https://pypi.org/project/python-decouple/> 

## 4 FastAPI  
### Start command  
uvicorn main:app --reload  

Saving aliases for iterative commands  
```bash
alias dev="uv run uvicorn main:app --reload "
```

#### Toml scripts examples  
<https://github.com/astral-sh/uv/issues/6302>   

## 3 Docker  

### Basic Workflow  

```bash
docker ps
docker compose
docker pull python:3.6.15 
# -> stops immediately
docker run python:3.6.15 
# -> start interactive terminal
docker run -it python:3.6.15 
docker pull python:3.6.15-slim-buster
docker run -it python:3.6.15-slim-buster
```  
1) Search docker hub for python  
2) Search the **tags** tab for specific version (3.13 / 3.6.15)
3) Copy command and paste in terminal (docker pull python:3.6.15-slim-buster)

### Docker file  
```bash
touch Dockerfile
docker pull python:3.13.4-slim-bullseye
...
```
After the commands have been added to the Dockerfile
```bash
mkdir boot && touch boot/docker-run.sh
```
Edit the docker-run file:
```bash
#!/bin/bash

source /opt/venv/bin/activate

cd /code
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app 
```

Add also following row to Dockerfile  

```bash
# make the bash script executable
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh
...
# Add below to the end 
# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/run.sh"]
```

### Run Docker  

Build in the local folder.  
Container not public before pushed to the hub.  


```bash
docker build -t analytics-api -f Dockerfile.web .
docker run analytics-api 

docker build -t analytics-api:v1 -f Dockerfile.web .
docker run analytics-api:v1 

# becomes

docker compose up --watch
docker compose down or docker compose down -v (to remove volumes)
docker compose run app /bin/bash or docker compose run app python
```  

### Stop Running Docker  
```bash
# list running containers
docker ps

docker stop <container_id_or_name>  
docker stop fc3fff834f2a  

# or
docker stop my-app  
docker stop analytics-api  

# or
docker compose down  

# This command stops and removes the containers, networks, and volumes defined in the Docker Compose file. 
# If you want to remove the **volumes** as well, you can use:
# ! docker compose down -v
# !Caution!: docker compose down -v will delete the volumes associated with your services, which can include your database data if the database stores its data in a volume.
```

### Docker Compose  
Create and fill the [compose.yaml](compose.yaml) file

Create an [](.env.compose) file and edit settings. 

Set the arguments for Docker to use in the compose.yaml.

```yaml
    develop:
      watch:
        - action: rebuild
          path: Dockerfile
        - action: rebuild
          path: requirements.txt
        - action: rebuild
          path: compose.yaml
```
watch on changes in above files, then rebuild the entire container.  


```bash
# start
docker compose up
docker compose up --watch
# stop
docker compose down
```

#### Local Start
In VENV -> default port 8000:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
alias dev="cd src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
```
Create nbs folder
Install ipykernel -> only for testing in Jupyter, not for docker container
```bash
uv add ipykernel
(uv add pip)
```

## Data Science Template  
[Cookicutter Data Science](data_science_template.md)

<https://cookiecutter-data-science.drivendata.org/#with-pip> 

<https://github.com/drivendataorg/cookiecutter-data-science/tree/master>

