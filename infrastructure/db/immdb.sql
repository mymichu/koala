CREATE TABLE IF NOT EXISTS systemToTools(
    system_id INT,
    tool_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (system_id, tool_id)
);

CREATE TABLE IF NOT EXISTS entity(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR,
    version VARCHAR,
    purpose VARCHAR,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_system BOOLEAN,
    PRIMARY KEY id
);

CREATE TABLE IF NOT EXISTS change(
    id INTEGER AUTO_INCREMENT,
    change VARCHAR,
    entity_id INT,
);