# Database Structure

The following shows the database structure of the backend. 

```mermaid
classDiagram
    entity <|-- entitylinker
    entity <|-- change
    entity <|-- entity_x_document
    entity <|-- entity_ownership
    user <|-- entity_ownership
    document <|-- entity_x_document
    class entity{
        +id (Autoincrement)
        +name
        +version_major
        +purpose
        +changed_at
        +is_system
        +gmp_relevant
    }
    class entitylinker{
        +id (Autoincrement)
        +system_name
        +system_major_version
        +tool_name
        +tool_major_version
        +valid
        +changed_at
    }
    class entity_x_document{
        +id (Autoincrement)
        +entity_id
        +document_id
        +creation_date
    }
    class change{
        +id (Autoincrement)
        +entity_name
        +entity_major_version
        +requester_id
        +reviewer_id
        +change
    }
    class document{
        +id (Autoincrement)
        +name
        +path
        +creation_date
    }
    class entity_ownership{
        +id (Autoincrement)
        +entity_id
        +user_id
        +creation_date
    }
    class user{
        +id (Autoincrement)
        +name
        +first_name
        +active
    }
```


## Explanation

The following section explains the most important points of the database structure.

### entity

The entity table contains all entities. An entity can be a tool or a system. An entity is identified over his purpose, name and version_major. There cannot be a double entry with the same purpose, name, version_major.

### entitylinker

The entitylinker table links a tool to a system or a tool to another tool. This is used to show which system is affected by a tool and which tool is used by a system.


### entitiy_ownership
The entitiy ownership table contains all users that are responsible for an entity (defined ownership). A tool can have multiple owners. 
