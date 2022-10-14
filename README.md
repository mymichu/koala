#Koala

## Use Cases

1. Give me all the tools of a system at a given time.
2. Show me all the Systems which rely on tool Y with version X.
3. Show me all the tools which are under regulation purposes and not.
4. Show me all the changes of tool Y from a given time to a given time. 
5. Show me all the changes of system A from a given time to a given time. 
6. Show me all the changes end of life tools that are used by an SDE.
## Development tools
immuclient login immudb - pw immudb

## SQL

./immuclient query "SELECT peoplenow.id, peoplenow.name, peoplethen.purpose, peoplenow.purpose FROM tool BEFORE now() AS peoplethen INNER JOIN tool AS peoplenow ON peoplenow.id=peoplethen.id;"