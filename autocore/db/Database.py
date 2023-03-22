import mysql.connector
from robot.api import logger


class Database:
    """Closing the created connection will the users' responsibility.
    Suggested usage is to create single instance during the initialization of a global library.
    Then pass the instance only to library components that needs db connection.
    """

    def __init__(self, host: str, user: str, password: str, port: str, database: str):
        self.__connections = []
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port
        self.__database = database

    def execute(self, *args, **kwargs):
        self.__create_connection()

        logger.info(f"Executing query. {args[0]}")
        cursor = self.__connections[0].cursor(dictionary=True)
        cursor.execute(*args, **kwargs)
        result = cursor.fetchall()
        cursor.close()
        logger.info(f"Query Result: {result}")
        return result

    def __create_connection(self):
        if len(self.__connections) == 0:
            logger.info("Creating a new connection.")
            conn = mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password,
                                           port=self.__port, database=self.__database)
            conn.autocommit = True
            self.__connections.append(conn)
        else:
            logger.info(f"Using an existing connection {str(self.__connections[0])}.")

    def close_connections(self):
        for connection in self.__connections:
            logger.info(f"Closing {str(self.__connections[0])}.")
            connection.close()
