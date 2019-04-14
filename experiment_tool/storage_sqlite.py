import logging
import pickle
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Set

from experiment_tool.storage import ExperimentStorage


log = logging.getLogger(__name__)


class SQLiteExpStorage(ExperimentStorage):
    def __init__(self, *, path: str) -> None:
        self.path = path
        self.conn = sqlite3.connect(path)
        self._init_tables()

    @contextmanager
    def _cursor(self):
        cursor = self.conn.cursor()
        try:
            yield cursor
        except sqlite3.Error:
            # TODO: add error handling
            log.error('some problem with connection to database ')
            raise
        finally:
            self.conn.commit()
            cursor.close()

    def _get_all_tables(self) -> Set[str]:
        with self._cursor() as cursor:
            result = cursor.execute(
                'SELECT name FROM sqlite_master'
            ).fetchall()
        if result:
            result = {res[0] for res in result}
        else:
            result = set()
        return result

    def _init_tables(self) -> None:
        existing_table = self._get_all_tables()
        requiring_tables = {
            'experiments': 'id INTEGER, name TEXT, structure TEXT',
            'functions': 'exp_id INTEGER, name TEXT, func_code TEXT',
            'arguments': 'exp_id INTEGER, name TEXT, arg_value BLOB',
        }
        for table_name, table_schema in requiring_tables.items():
            if table_name not in existing_table:
                # using str.format() only for creating tables by schemes
                with self._cursor() as cursor:
                    cursor.execute(
                        'CREATE TABLE {name} ({schema})'.format(
                            name=table_name, schema=table_schema
                        )
                    )

    def get_experiment_ids(self, exp_name: str, structure: str) -> List[int]:
        with self._cursor() as cursor:
            result = cursor.execute(
                """
                SELECT id FROM experiments
                WHERE name = :name AND structure = :structure
                """,
                {'name': exp_name, 'structure': structure}
            ).fetchall()
        if result:
            result = [res[0] for res in result]
        else:
            result = []
        return result

    def add_experiment(self, exp_name: str, structure: str) -> int:
        with self._cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO experiments
                VALUES (
                    (SELECT IFNULL(MAX(id), -1) + 1 FROM experiments),
                    :name, :structure)
                """,
                {'name': exp_name, 'structure': structure}
            )
        return max(self.get_experiment_ids(exp_name, structure))

    def get_functions(self, exp_id: int) -> Dict[str, str]:
        with self._cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name, func_code
                FROM functions
                WHERE exp_id = :id
                """,
                {'id': exp_id}
            ).fetchall()
        if result:
            result = {item[0]: item[1] for item in result}
        else:
            result = {}
        return result

    def add_functions(self, exp_id: int, funcs: Dict[str, str]) -> None:
        func_records = [
            (exp_id, name, code)
            for name, code in funcs.items()
        ]
        with self._cursor() as cursor:
            cursor.executemany(
                'INSERT INTO functions VALUES (?, ?, ?)',
                func_records
            )

    def get_arguments(self, exp_id: int) -> Dict[str, Any]:
        with self._cursor() as cursor:
            result = cursor.execute(
                """
                SELECT name, arg_value
                FROM arguments
                WHERE exp_id = :id
                """,
                {'id': exp_id}
            ).fetchall()
        if result:
            result = {item[0]: pickle.loads(item[1]) for item in result}
        else:
            result = {}
        return result

    def add_arguments(self, exp_id: int, args: Dict[str, Any]) -> None:
        arg_records = [
            (exp_id, name, pickle.dumps(arg_value))
            for name, arg_value in args.items()
        ]
        with self._cursor() as cursor:
            cursor.executemany(
                'INSERT INTO arguments VALUES (?, ?, ?)',
                arg_records
            )


if __name__ == '__main__':
    storage = SQLiteExpStorage(path='test.db')
