from db.sql_db_handler import sql_db 
from task_bypass.tasktypes.filter import *
from task_bypass.tasktypes.transform import *
from task_bypass.tasktypes.merge import *

def configure():
    # Create your db connection.
    db = sql_db(f'db/outputs/test.db')
    table_structure = """
            'level' TEXT NOT NULL,
            'stage_name' TEXT NOT NULL,
            'task_name' TEXT NOT NULL,
            'date_time' TEXT NOT NULL,
            'error_message' TEXT,
            'other_info' TEXT
            """
    # Drop tables inside test db
    db.dropTable('_log')

    # Create logging table
    db.createTable('_log', table_structure)
    return db
