import sqlite3
from typing import List, Optional, Tuple


class ExperimentsStorage:
    def __init__(self, path: str) -> None:
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self) -> None:
        tables = self._get_all_tables()
        if ('experiments',) not in tables:
            self.cursor.execute(
                """
                CREATE TABLE experiments
                  (id integer, name text, structure text)
                """
            )
        if ('arguments',) not in tables:
            self.cursor.execute(
                """
                CREATE TABLE arguments
                  (exp_id integer, name text, arg_list text)
                """
            )
        if ('functions',) not in tables:
            self.cursor.execute(
                """
                CREATE TABLE functions
                  (exp_id integer, name text, func_code text)
                """
            )
        self._commit()

    def get_experiment_id(self, exp_name: str, json: str) -> Optional[int]:
        result = self.cursor.execute(
            """
            SELECT id FROM experiments 
            WHERE name = ? AND structure = ?
            """,
            (exp_name, json)
        ).fetchall()
        if result:
            return result[0][0]
        return None

    def add_experiment(self, exp_name: str, json: str) -> int:
        last_id = self.cursor.execute(
            'SELECT max(id) FROM experiments'
        ).fetchone()[0]
        new_id = 0 if last_id is None else last_id + 1
        self.cursor.execute(
            """
            INSERT INTO experiments
            VALUES (?, ?, ?)
            """,
            (new_id, exp_name, json)
        )
        self._commit()
        return new_id

    def get_functions(self, exp_id: int) #-> Optional[int]:
        return self.cursor.execute(
            """
            SELECT * FROM functions 
            WHERE exp_id = ?
            """,
            (exp_id,)
        ).fetchall()

    def _get_all_tables(self) -> List[Tuple[str]]:
        self.cursor.execute('SELECT name FROM sqlite_master')
        return self.cursor.fetchall()

    def _commit(self) -> None:
        self.conn.commit()

    def _close(self) -> None:
        self.conn.close()
