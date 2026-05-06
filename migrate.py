"""Idempotent schema migration: add new columns/tables without losing data.
Run after pulling new versions: `python migrate.py`."""
from sqlalchemy import inspect, text
from app import app
from models import db


def column_exists(insp, table, column):
    return any(c["name"] == column for c in insp.get_columns(table))


def table_exists(insp, table):
    return table in insp.get_table_names()


ADD_COLUMNS = {
    "project": [
        ("title_ru", "VARCHAR(120) DEFAULT ''"),
        ("description_ru", "TEXT DEFAULT ''"),
        ("cover_image", "VARCHAR(400) DEFAULT ''"),
    ],
    "experience": [
        ("role_ru", "VARCHAR(120) DEFAULT ''"),
        ("company_meta_ru", "VARCHAR(200) DEFAULT ''"),
    ],
    "experience_bullet": [
        ("text_ru", "TEXT DEFAULT ''"),
    ],
    "skill_cluster": [
        ("title_ru", "VARCHAR(120) DEFAULT ''"),
    ],
}


def migrate():
    with app.app_context():
        # create any new tables (HeroRole, ContactSubmission, PageView)
        db.create_all()

        insp = inspect(db.engine)
        with db.engine.begin() as conn:
            for table, cols in ADD_COLUMNS.items():
                if not table_exists(insp, table):
                    print(f"  - skipping {table} (table missing)")
                    continue
                for name, decl in cols:
                    if column_exists(insp, table, name):
                        continue
                    print(f"  + ALTER TABLE {table} ADD COLUMN {name}")
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {decl}"))

        print("Migration done.")


if __name__ == "__main__":
    migrate()
