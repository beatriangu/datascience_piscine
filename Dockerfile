FROM python:3.11-slim

# Install PostgreSQL client tools (including psql)
# apt-get update updates the list of available packages
# apt-get install -y postgresql-client installs the client tools without asking for confirmation
# rm -rf /var/lib/apt/lists/* cleans up the apt cache to keep the image size down
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]

