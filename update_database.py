import sqlite3

DATABASE_PATH = "leadflow.db"

new_columns = {
    "ai_classification": "VARCHAR(20)",
    "ai_reason": "TEXT",
    "ai_suggested_action": "TEXT",
}

connection = sqlite3.connect(DATABASE_PATH)

try:
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(leads)")
    existing_columns = {
        row[1] for row in cursor.fetchall()
    }

    if not existing_columns:
        raise RuntimeError(
            "The leads table was not found. "
            "Check that you are running this script "
            "from the LeadFlow project folder."
        )

    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE leads ADD COLUMN "
                f"{column_name} {column_type}"
            )
            print(f"Added column: {column_name}")
        else:
            print(f"Column already exists: {column_name}")

    connection.commit()
    print("\nDatabase update completed successfully!")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()