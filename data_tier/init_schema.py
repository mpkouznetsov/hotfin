from data_tier import sql_runner


def init_schema():
    sql_runner.run_sql_file("sql/init.sql")


if __name__ == "__main__":
    init_schema()