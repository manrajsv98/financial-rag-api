
# BUILDS IMAGES ------> BUILDS CONTAINER --------> EVERYTHING YOU DO HERE BUILDS THE CONTAINER

# 1 - BASE IMAGE 
#   - FROM - ALWAYS STARTS WITH THIS

FROM python:3.11-slim 

# 2 - CREATES THIS DIRECTORY IN CONTAINER 
WORKDIR /app

# 3 - COPIES requirements.txt into /app in container
COPY requirements.txt .

# 4 - RUNS the pip install - installs all packages
RUN pip install --no-cache-dir -r requirements.txt

# 5 - . . COPIES EVERYTHING FROM THE DIRECTORY YOUR'RE IN (HOST COMPUTER - CODEBASE) INTO /app
COPY . .

# 6 - PORT 

EXPOSE 8000

# 7 - START COMMAND - Exec Form not Shell 

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]