import inspect
import logging
import pickle
import sqlite3
from typing import Any, Callable, Dict

log = logging.getLogger(__name__)


class FunctionRunInfo:
    def __init__(self, func: Callable, args: Dict[str, Any], result=None):
        self.code = inspect.getsource(func)
        self.args = str(sorted(args.items(), key=lambda x: x[0]))
        self.result = pickle.dumps(result)


class FunctionRunStorage:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self._cursor = self.conn.cursor()
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS functions
            (function_code, args, result,
            UNIQUE(function_code, args))
            """
        )

    def add_function(self, func: Callable, args: Dict[str, Any], result: Any):
        log.debug('start FunctionRunStorage.add_function')
        function_run_info = FunctionRunInfo(func, args, result)
        self._cursor.execute(
            """
            INSERT OR IGNORE INTO functions
            VALUES (?, ?, ?)
            """,
            (
                function_run_info.code,
                function_run_info.args,
                function_run_info.result
            )
        )
        self.conn.commit()
        log.debug('finish FunctionRunStorage.add_function')

    def get_function_result(self, func: Callable, args: Dict[str, Any]):
        log.debug('start FunctionRunStorage.get_function_result')
        function_run_info = FunctionRunInfo(func, args)
        self._cursor.execute(
            """
            SELECT result FROM functions
            WHERE function_code=:code AND args=:args
            """,
            {"code": function_run_info.code, "args": function_run_info.args}
        )
        res = self._cursor.fetchone()
        log.debug('finish FunctionRunStorage.get_function_result')
        return res
