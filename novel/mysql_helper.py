class MysqlHelper:
    def __init__(self, connection):
        """
        Initialize with a MySQL connection.
        :param connection: pymysql connection object
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def upsert_from_object(self, table_name, obj):
        """
        Dynamically generate and execute an UPSERT query from an object's attributes.
        :param table_name: Name of the database table
        :param obj: The object or Scrapy item to process
        """
        # Extract fields and values
        fields = list(obj.keys())
        values = tuple(obj[field] for field in fields)

        # Generate placeholders for the query
        placeholders = ", ".join(["%s"] * len(fields))
        columns = ", ".join(fields)
        updates = ", ".join([f"{field}=VALUES({field})" for field in fields])

        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {updates}
        """
        try:
            # Execute the query
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing query: {e}")
