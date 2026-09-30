"""Load the cleaned mock data into a local DuckDB file."""

import logging
import re

import duckdb

from process import clean_data, read_data

logger = logging.getLogger(__name__)

DB_FILE = "mock.duckdb"


def load_duckdb(data, table):
    """Create a local DuckDB file and store data in table.

    Args:
        data: Cleaned DataFrame to store.
        table: Destination table name.
    """
    # DuckDB identifiers cannot be bound as parameters, so accept only a plain name.
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table) is None:
        raise ValueError(f"invalid table name: {table}")

    connection = duckdb.connect(DB_FILE)
    try:
        # Register the DataFrame, then copy it into a real table in the file.
        connection.register("cleaned_mock", data)
        connection.execute(
            f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM cleaned_mock"
        )
        count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        logger.info("loaded %d rows into %s table %s", count, DB_FILE, table)
        return count
    except Exception:
        logger.exception("failed to load DuckDB table %s", table)
        raise
    finally:
        connection.close()


def main():
    """Read MOCK_DATA.csv, clean it, and store it in mock.duckdb."""
    logger.info("starting DuckDB load")
    data = read_data("MOCK_DATA.csv")
    cleaned = clean_data(data)
    load_duckdb(cleaned, "mock")
    logger.info("DuckDB load finished")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    main()
