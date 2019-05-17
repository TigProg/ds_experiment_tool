import hashlib
import inspect
import logging
import os
import pickle
import sqlite3
from typing import Any, Callable, Dict

from experiment_tool.utils import Maybe

log = logging.getLogger(__name__)


class FunctionRunInfo:
    def __init__(self, func: Callable, args: Dict[str, Any]):
        self.code_hash = hashlib.md5(inspect.getsource(func).encode()).hexdigest()
        self.args_hash = hashlib.md5(str(sorted(args.items(), key=lambda x: x[0])).encode()).hexdigest()
        self.path = os.path.join(os.path.split(os.path.dirname(__file__))[0], "results",
                                 hashlib.md5("".join([self.code_hash, self.args_hash]).encode()).hexdigest()
                                 )


class FunctionRunStorage:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._cursor = self.conn.cursor()
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS functions
            (function_code_hash INTEGER, args_hash INTEGER, result_path TEXT,
            UNIQUE(function_code_hash, args_hash))
            """
        )

    def add_function(self, func: Callable, args: Dict[str, Any], result: Any):
        function_run_info = FunctionRunInfo(func, args)
        if self.get_function_result(func, args).is_nothing():
            log.debug('adding function to storage')
            with open(function_run_info.path, 'wb') as f:
                pickle.dump(result, f)
            self._cursor.execute(
                """
                INSERT INTO functions
                VALUES (?, ?, ?)
                """,
                (
                    function_run_info.code_hash,
                    function_run_info.args_hash,
                    function_run_info.path
                )
            )
            self.conn.commit()

    def get_function_result(self, func: Callable, args: Dict[str, Any]) \
            -> Maybe:
        function_run_info = FunctionRunInfo(func, args)
        self._cursor.execute(
            """
            SELECT result_path FROM functions
            WHERE function_code_hash=:code_hash AND args_hash=:args_hash
            """,
            {"code_hash": function_run_info.code_hash, "args_hash": function_run_info.args_hash}
        )
        res = self._cursor.fetchone()
        if res is not None:
            res_path = res[0]
            with open(res_path, 'rb') as f:
                return Maybe(pickle.load(f))
        return Maybe(nothing=True)
