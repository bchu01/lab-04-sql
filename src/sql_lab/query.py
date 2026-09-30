"""Query the mock table uploaded by process.py."""

import logging
import os
import re

import mysql.connector
import pandas as pd

logger = logging.getLogger(__name__)

# Same credential variables as process.py.
DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")

# Columns in the uploaded mock table. Used to reject unexpected GROUP BY names.
MOCK_COLUMNS = {"id", "group", "last_name", "email", "gender", "ip_address"}


def _require_db_env():
    """Return DB host, name, user, and password, or raise if any are missing."""
    values = {
        "DBHOST": DBHOST,
        "DBNAME": DBNAME,
        "DBUSER": DBUSER,
        "DBPASS": DBPASS,
    }
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(
            "missing environment variables: " + ", ".join(missing)
        )
    return DBHOST, DBNAME, DBUSER, DBPASS


def _connect():
    """Open a MySQL connection from the environment credentials."""
    dbhost, dbname, dbuser, dbpassword = _require_db_env()
    return mysql.connector.connect(
        host=dbhost,
        port=3306,
        user=dbuser,
        password=dbpassword,
        database=dbname,
    )


def _quote_column(name):
    """Backtick-quote a mock column name.

    %s placeholders bind values, not identifiers, so the column is checked
    against the known mock columns and then quoted.
    """
    if name not in MOCK_COLUMNS or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"unknown column: {name}")
    return f"`{name}`"


def get_data_by_group(value):
    """Return mock rows whose group column equals value.

    The filter column is `group`. GROUP is a reserved word in MySQL, so the
    column is backtick-quoted. `value` is bound with a %s placeholder.
    """
    logger.info("fetching rows where group = %s", value)
    # Parameterized filter: the value is not formatted into the SQL string.
    query = "SELECT * FROM mock WHERE `group` = %s"
    connection = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        cursor.execute(query, (value,))
        rows = cursor.fetchall()
        logger.info("found %d rows for group %s", len(rows), value)
        return rows
    except mysql.connector.Error:
        logger.exception("failed to fetch rows for group %s", value)
        raise
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def plot_counts(groupby):
    """Count mock rows for each distinct value of groupby.

    Args:
        groupby: Column to aggregate. One of the mock table columns.

    Returns:
        DataFrame with the column values and a count column.
    """
    column = _quote_column(groupby)
    logger.info("counting rows by %s", groupby)
    # column was validated above; the query has no value parameters.
    query = f"SELECT {column}, COUNT(*) AS row_count FROM mock GROUP BY {column}"
    connection = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        counts = pd.DataFrame(rows, columns=[groupby, "row_count"])
        logger.info("got %d groups for %s", len(counts), groupby)
        return counts
    except mysql.connector.Error:
        logger.exception("failed to count rows by %s", groupby)
        raise
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def main():
    """Show a group filter and row counts for group and gender."""
    print("=== group = notebook ===")
    print(get_data_by_group("notebook"))

    print("=== counts by group ===")
    print(plot_counts("group"))

    print("=== counts by gender ===")
    print(plot_counts("gender"))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    main()
