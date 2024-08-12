import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine


class Database:
    def __init__(
        self,
        database: str,
        username: str = "qsamudio",
        password: str = "MhyH3ssKuEll3",
        hostname: str = "127.0.0.1",
    ):
        """
        Initialize the Database connection.

        :param username: MySQL username
        :param password: MySQL password
        :param hostname: MySQL server hostname
        :param database: MySQL database name
        """
        self.engine = create_engine(
            f"mysql+pymysql://{username}:{password}@{hostname}/{database}"
        )
        self.connection = self.engine.connect()
        print("Database connection established.")

    def transform_column_names(self, df):
        # Convert column names from Python timestamps to MySQL-compatible timestamps
        df.columns = [
            (
                self.python_timestamp_to_mysql_timestamp(col)
                if isinstance(col, datetime)
                else col
            )
            for col in df.columns
        ]
        return df

    def python_timestamp_to_mysql_timestamp(self, py_timestamp):
        # Convert Python timestamp to MySQL-compatible timestamp string
        return py_timestamp.strftime("%Y-%m-%d_%H_%M_%S")

    def store_dataframe(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "replace"
    ) -> None:
        """
        Store a pandas DataFrame into a MySQL table.

        :param df: DataFrame to store
        :param table_name: Name of the table in the database
        :param if_exists: Behavior when the table already exists ('replace', 'append', 'fail')
        """
        df = self.transform_column_names(df)
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=True)
        print(f"DataFrame stored in table '{table_name}' with if_exists='{if_exists}'.")

    def retrieve_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Retrieve a pandas DataFrame from a MySQL table.

        :param table_name: Name of the table in the database
        :return: DataFrame with the data from the table
        """
        df = pd.read_sql_table(table_name, self.engine)
        print(f"DataFrame retrieved from table '{table_name}'.")
        return df

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        self.connection.close()
        print("Database connection closed.")


# Usage example
if __name__ == "__main__":
    # Replace with your own credentials
    database = "solar_gain"

    db = Database(database)

    # Example DataFrame
    data = {"column1": [1, 2, 3], "column2": [4, 5, 6]}
    df = pd.DataFrame(data)

    # Store the DataFrame in the database
    db.store_dataframe(df, "example_table")

    # Close the connection
    db.close_connection()
