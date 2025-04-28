from uuid import UUID


async def get_uuid_or_str(uuid_or_str: str) -> str | UUID:
    try:
        uuid_str = UUID(uuid_or_str)
    except ValueError:
        if not isinstance(uuid_or_str, str):
            raise TypeError
        return uuid_or_str
    return uuid_str
