# Analytics API with FastAPI and TimescaleDB  
Own your data pipeline with Python and Postgres

<https://www.codingforentrepreneurs.com/courses/analytics-api-with-fastapi-and-timescaledb>  

## UV Python Project Setup   

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

<https://pypi.org/project/python-decouple/> 

## FastAPI  
### Start command  
uvicorn main:app --reload  

Saving aliases for iterative commands  
```bash
alias dev="uv run uvicorn main:app --reload "
```

#### Toml scripts examples  
<https://github.com/astral-sh/uv/issues/6302>   

### Docker  

#### Basic Workflow  

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

#### Docker file  
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

## Git  
```bash
echo "# cfe-fastapi-timescaledb" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/todor1/cfe-fastapi-timescaledb.git
git push -u origin main
```