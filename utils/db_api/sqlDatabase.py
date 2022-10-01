import sqlite3

from sqlite3 import Error


class Database:

    def __init__(self, path_to_db="Users.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):

        if not parameters:
            parameters = tuple()

        connection = self.connection
        cursor = connection.cursor()
        connection.set_trace_callback(logger)
        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        ids str NOT NULL,
        created varchar(255) NOT NULL,
        name varchar(255),
        username varchar(255),
        time int(255),
        tokenA varchar(255),
        tokenB varchar(255),
        dollarAmount varchar(255),
        crossExchange varchar(255),
        adminRights int(255),
        PRIMARY KEY (ids)
        );"""
        self.execute(sql, commit=True)

    def add_user(self, ids: str,
                 created: str,
                 name: str = None,
                 username: str = None,
                 time: int = None,
                 tokenA: str = None,
                 tokenB: str = None,
                 dollarAmount: float = None,
                 crossExchange: str = None,
                 adminRights: int = 0):

        SQL_COMMAND = "INSERT INTO Users(ids, created, name, username, time, tokenA, tokenB, " \
                      "dollarAmount, crossExchange,adminRights ) VALUES(?,?,?,?,?,?,?,?,?,?) "

        parameters = (ids,
                      created,
                      name,
                      username,
                      time,
                      tokenA,
                      tokenB,
                      dollarAmount,
                      crossExchange,
                      adminRights)

        self.execute(SQL_COMMAND, parameters=parameters, commit=True)

    def select_all_users(self):
        SQL_COMMAND = "SELECT * FROM Users"
        return self.execute(SQL_COMMAND, fetchall=True)

    @staticmethod
    def format_args(SQL_COMMAND, parameters: dict):

        SQL_COMMAND += " AND ".join([
            f" {item} = ?" for item in parameters
        ])

        return SQL_COMMAND, tuple(parameters.values())

    def select_user(self, **kwargs):
        SQL_COMMAND = "SELECT * FROM Users WHERE"
        SQL_COMMAND, parameters = self.format_args(SQL_COMMAND, kwargs)
        return self.execute(SQL_COMMAND, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_Time(self, time, user_ids):
        SQL_COMMAND = "UPDATE Users SET Time=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(time, user_ids), commit=True)

    def update_TokenA(self, TokenA, user_ids):
        SQL_COMMAND = "UPDATE Users SET TokenA=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(TokenA, user_ids), commit=True)

    def update_TokenB(self, TokenB, user_ids):
        SQL_COMMAND = "UPDATE Users SET TokenB=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(TokenB, user_ids), commit=True)

    def update_DollarAmount(self, DollarAmount, user_ids):
        SQL_COMMAND = "UPDATE Users SET DollarAmount=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(DollarAmount, user_ids), commit=True)

    def update_CrossExchange(self, CrossExchange, user_ids):
        SQL_COMMAND = "UPDATE Users SET CrossExchange=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(CrossExchange, user_ids), commit=True)

    def delete_user(self, user_ids):
        SQL_COMMAND = "DELETE FROM Users WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(user_ids,), commit=True)

    def update_user(self, user_ids, time, TokenA, TokenB, DollarAmount):
        SQL_COMMAND = "UPDATE Users SET time=? , TokenA=? , TokenB=? , DollarAmount=?  WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(time, TokenA, TokenB, DollarAmount, user_ids), commit=True)

    def makeAdmin(self, adminRights, user_ids):
        SQL_COMMAND = "UPDATE Users SET adminRights=? WHERE ids=?"
        return self.execute(SQL_COMMAND, parameters=(adminRights, user_ids), commit=True)

    def delete_all_users(self):
        return self.execute("DELETE FROM Users WHERE True", commit=True)


def logger(statement):
    print(f"""
------------------------------------
Executing:
{statement}
------------------------------------
""")
