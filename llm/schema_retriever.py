from database.service import DatabaseService


class SchemaRetriever:

    def __init__(self):
        self.db = DatabaseService()

    def get_schema_text(self):

        schema = self.db.get_schema()

        output = []

        for table in schema["table_name"].unique():

            output.append(f"Table: {table}")

            cols = schema[schema.table_name == table]

            for _, row in cols.iterrows():
                output.append(
                    f"  - {row.column_name} ({row.data_type})"
                )

            output.append("")

        return "\n".join(output)