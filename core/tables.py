from core.db_settings import execute_query


def create_tables() -> None:
    
    execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        CONSTRAINT unique_user UNIQUE (name, phone)
    );
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS debts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL UNIQUE
            REFERENCES users(id) ON DELETE CASCADE,
        i_gave BIGINT DEFAULT 0 CHECK (i_gave >= 0),
        i_took BIGINT DEFAULT 0 CHECK (i_took >= 0)
    );
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL
            REFERENCES users(id) ON DELETE CASCADE,
        type VARCHAR(10) NOT NULL
            CHECK (type IN ('gave', 'took')),
        amount BIGINT NOT NULL CHECK (amount > 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
