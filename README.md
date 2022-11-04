#Koala

## Use Cases

1. Give me all the tools of a system at a given time.
2. Show me all the Systems which rely on tool Y with version X.
3. Show me all the tools which are under regulation purposes and not.
4. Show me all the changes of tool Y from a given time to a given time. 
5. Show me all the changes of system A from a given time to a given time. 
6. Show me all the changes end of life tools that are used by an SDE.
7. Show all related documents to tool and system.
8. Optional: Generate Reports out of information.
9. All information system data classifications are within the database.
## Development tools
immuclient login immudb - pw immudb

## SQL

./immuclient query "SELECT peoplenow.id, peoplenow.name, peoplethen.purpose, peoplenow.purpose FROM tool BEFORE now() AS peoplethen INNER JOIN tool AS peoplenow ON peoplenow.id=peoplethen.id;"


 ## Instal Docker-Compose without docker desktop on Ubuntu 20.04

Instal docker compose to a running docker engine. Therefore execute the following commands:

```bash	
curl -SL https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose                                                                                                                                                               
docker compose version 
```