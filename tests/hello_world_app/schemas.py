# hello_world_app/schemas.py
HELLO_WORLD_RESPONSE = {
    "type": "object",
    "required": ["message"],
    "properties": {"message": {"type": "string"}},
}
