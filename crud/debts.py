from core.db_settings import execute_query


def add_debt(user_id: int) -> None:
    print("1 - lend money (I gave)")
    print("2 - owe money (I took)")
    choice = input("Choose action: ").strip()

    try:
        amount = int(input("Enter the amount (UZS): "))
        if amount <= 0:
            print("sum should be greater than 0")
            return
    except ValueError:
        print("incorrect sum")
        return

    if choice == "1":
        # история
        execute_query(
            """
            INSERT INTO transactions (user_id, type, amount)
            VALUES (%s, 'gave', %s)
            """,
            (user_id, amount)
        )

        # итог
        execute_query(
            """
            UPDATE debts
            SET i_gave = i_gave + %s
            WHERE user_id = %s
            """,
            (amount, user_id)
        )

    elif choice == "2":
        execute_query(
            """
            INSERT INTO transactions (user_id, type, amount)
            VALUES (%s, 'took', %s)
            """,
            (user_id, amount)
        )

        execute_query(
            """
            UPDATE debts
            SET i_took = i_took + %s
            WHERE user_id = %s
            """,
            (amount, user_id)
        )

    else:
        print("incorrect choice")
        return

    print("transaction saved successfully")

def show_my_debt(user_id: int) -> None:
    row = execute_query(
        """
        SELECT
            u.name,
            u.phone,
            d.i_gave,
            d.i_took,
            (d.i_gave - d.i_took) AS balance
        FROM users u
        JOIN debts d ON u.id = d.user_id
        WHERE u.id = %s
        """,
        (user_id,),
        fetch="one"
    )

    if not row:
        print("values haven't found")
        return

    print(f"\n {row['name']} |  {row['phone']}")
    print(f"lend money (): {row['i_gave']} UZS")
    print(f"owe money: {row['i_took']} UZS")
    print(f"balance: {row['balance']} UZS\n")

def show_history(user_id: int) -> None:
    rows = execute_query(
        """
        SELECT type, amount, created_at
        FROM transactions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
        fetch="all"
    )

    if not rows:
        print("History is empty")
        return

    print("\ntransaction history:")
    for row in rows:
        sign = "+" if row["type"] == "gave" else "-"
        print(f"{row['created_at']} | {sign}{row['amount']} UZS")
