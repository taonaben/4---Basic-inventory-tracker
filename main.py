import psycopg2
import db_details


def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=db_details.db_name,
            user=db_details.db_user,
            password=db_details.db_password,
            host=db_details.db_host,
            port=db_details.db_port,
        )
        print("Connection to database established successfully.")
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None


def run_a_query(conn):
    cur = conn.cursor()
    cur.execute("ALTER TABLE inventory ADD COLUMN id SERIAL PRIMARY KEY")
    print("Query executed successfully.")


def print_table(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    rows = cur.fetchall()
    print(f"{len(rows)} rows found.\n")
    print("{:<20}\t{:<10}\t{:<10}\t{:<10}".format("Item Name", "Stock", "Price", "ID"))
    print("-" * 50)
    for row in rows:
        print(
            "{:<20}\t{:<10}\t{:<10.2f}\t{:<10}".format(row[0], row[1], row[2], row[3])
        )
    cur.close()


def add_item_to_db(conn):
    item_name = input("Enter item name: ")
    stock = int(input("Enter stock: "))
    price = float(input("Enter price: "))

    if conn is None:
        print("Database connection is not established.")
        return

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO inventory (item_name, stock, price) VALUES (%s, %s, %s)",
        (item_name, stock, price),
    )
    conn.commit()
    cur.close()

    print("Item added successfully.")

    print_table(conn)


def delete_item_from_db(conn):
    item_id = input("ID of item to delete: ")

    if conn is None:
        print("Database connection is not established.")
        return

    cur = conn.cursor()

    cur.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()

    print("Item deleted successfully.")


def main():
    conn = connect_to_db()
    while True:
        print("\n\nSelect an option:")
        print("1. Add item to database")
        print("2. View items in database")
        print("3. Delete item from database")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_item_to_db(conn)
        elif choice == "2":
            print_table(conn)
        elif choice == "3":
            delete_item_from_db(conn)
        elif choice == "4":
            break


if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        main()
