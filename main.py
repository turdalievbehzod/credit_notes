from core.tables import create_tables
from crud.auth import authorize
from crud.debts import add_debt, show_my_debt, show_history


def print_menu() -> None:
    """
    shows a menu with options
    """
    print("\nMenu:")
    print("1 - add debts")
    print("2 - show my balance")
    print("3 - transaction history")
    print("4 - exit")


def main() -> None:
    """
    collects common functions
    """
    create_tables()

    print("Sign up")
    name = input("Enter your name: ").strip()
    phone = input("phone number: ").strip()

    user_id = authorize(name=name, phone=phone)

    print("\nSuccessfully signed up")

    while True:
        print_menu()
        choice = input("Choose option: ").strip()

        if choice == "1":
            add_debt(user_id)

        elif choice == "2":
            show_my_debt(user_id)

        elif choice == "3":
            show_history(user_id)

        elif choice == "4":
            print(" Goodbye")
            break

        else:
            print("incorrect option")


if __name__ == "__main__":
    # create_tables()
    main()
