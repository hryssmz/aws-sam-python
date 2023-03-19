# s3_app/schemas.py
EMPTY_OBJECT = {
    "type": "object",
    "properties": {},
}

CLIENT_ERROR = {
    "type": "object",
    "required": ["code", "message"],
    "properties": {"code": {"type": "string"}, "message": {"type": "string"}},
}

LIST_OBJECTS_RESPONSE = {
    "type": "object",
    "required": ["objects"],
    "properties": {"objects": {"type": "array", "items": {"type": "string"}}},
}

GET_OBJECT_RESPONSE = {
    "type": "object",
    "required": ["content"],
    "properties": {"content": {"type": "string"}},
}
