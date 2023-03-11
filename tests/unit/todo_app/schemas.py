# unit/todo_app/schemas.py
EMPTY_OBJECT = {
    "type": "object",
    "properties": {},
}

CLIENT_ERROR = {
    "type": "object",
    "required": ["code", "message"],
    "properties": {"code": {"type": "string"}, "message": {"type": "string"}},
}

TODO_ITEM = {
    "type": "object",
    "required": [
        "id",
        "name",
        "description",
        "priority",
        "createdAt",
        "updatedAt",
    ],
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "priority": {"type": "integer", "minimum": 1, "maximum": 3},
        "createdAt": {"type": "string", "format": "date-time"},
        "updatedAt": {"type": "string", "format": "date-time"},
    },
}

LIST_TODOS_RESPONSE = {
    "type": "object",
    "required": ["todos"],
    "properties": {"todos": {"type": "array", "items": TODO_ITEM}},
}

CREATE_TODO_RESPONSE = {
    "type": "object",
    "required": ["todo"],
    "properties": {"todo": TODO_ITEM},
}

UPDATE_TODO_RESPONSE = {
    "type": "object",
    "required": ["todo"],
    "properties": {"todo": TODO_ITEM},
}

GET_TODO_RESPONSE = {
    "type": "object",
    "required": ["todo"],
    "properties": {"todo": TODO_ITEM},
}
