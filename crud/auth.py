from core.db_settings import execute_query


def authorize(name, phone):
    user = execute_query(
        """
        SELECT id FROM users
        WHERE name = %s AND phone = %s
        """,
        (name, phone),
        fetch="one"
    )

    if user:
        return user["id"]

    new_user = execute_query(
        """
        INSERT INTO users (name, phone)
        VALUES (%s, %s)
        RETURNING id
        """,
        (name, phone),
        fetch="one"
    )

    execute_query(
        "INSERT INTO debts (user_id) VALUES (%s)",
        (new_user["id"],)
    )

    return new_user["id"]
