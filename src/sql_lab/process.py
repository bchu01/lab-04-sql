"""Read MOCK_DATA, drop incomplete rows, and load the MySQL mock table."""

import logging
import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import Integer, create_engine
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, DOUBLE, TINYINT, VARCHAR

logger = logging.getLogger(__name__)

# Step 3: pandas dtypes from MOCK_DATA.csv mapped to MySQL types.
# id is int64; group, last_name, email, gender, and ip_address are strings.
# pandas 3 prints those string columns as "str".
type_mapping = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",  # safe default varchar length
    "string": "VARCHAR(255)",
    "str": "VARCHAR(255)",
}

# SQLAlchemy types passed to DataFrame.to_sql so the created table uses the mapping.
_sa_types = {
    "int64": BIGINT(),
    "int32": Integer(),
    "float64": DOUBLE(),
    "bool": TINYINT(1),
    "datetime64[ns]": DATETIME(),
    "object": VARCHAR(255),
    "string": VARCHAR(255),
    "str": VARCHAR(255),
}

# Credentials come from the environment (see the lab setup exports).
DBHOST = os.environ.get("DBHOST")
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")


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


def read_data(filename):
    """Load a CSV or Excel file into a pandas DataFrame.

    Args:
        filename: Path to a .csv or .xlsx file.

    Returns:
        DataFrame with the file contents.
    """
    path = Path(filename)
    extension = path.suffix.lower()

    # Branch on the extension so the same function accepts both formats.
    if extension == ".csv":
        data = pd.read_csv(path)
    elif extension == ".xlsx":
        data = pd.read_excel(path, engine="openpyxl")
    else:
        raise ValueError(f"unsupported file type: {extension}")

    logger.info("read %d rows from %s", len(data), filename)
    return data


def clean_data(data):
    """Drop rows with missing values so the frame is ready to upload.

    Args:
        data: DataFrame returned by read_data.

    Returns:
        DataFrame with incomplete rows removed.
    """
    # Mockaroo left some group, last_name, and email cells blank.
    cleaned = data.dropna()
    logger.info(
        "dropped %d rows with missing values; %d rows remain",
        len(data) - len(cleaned),
        len(cleaned),
    )
    return cleaned


def load_data(data, table):
    """Create the destination table and bulk-load the DataFrame into MySQL.

    Args:
        data: Cleaned DataFrame to upload.
        table: Destination table name. Callers should pass "mock".
    """
    dbhost, dbname, dbuser, dbpassword = _require_db_env()

    # Build the per-column SQLAlchemy types from the pandas dtypes.
    dtype = {}
    for column, pandas_dtype in data.dtypes.items():
        key = str(pandas_dtype)
        sql_type = type_mapping.get(key, "VARCHAR(255)")
        dtype[column] = _sa_types.get(key, VARCHAR(255))
        logger.info("column %s: %s -> %s", column, key, sql_type)

    # Connection URL form required by approach B. quote_plus keeps special
    # characters in the password from breaking the URL. This is not SQL text.
    url = (
        f"mysql+mysqlconnector://{quote_plus(dbuser)}:{quote_plus(dbpassword)}"
        f"@{dbhost}:3306/{dbname}"
    )
    engine = create_engine(url)
    try:
        # replace creates mock when it is missing and refreshes it on a re-run,
        # so the table holds this cleaned upload rather than duplicated rows.
        data.to_sql(
            name=table,
            con=engine,
            if_exists="replace",
            index=False,
            dtype=dtype,
        )
        logger.info("loaded %d rows into `%s`", len(data), table)
    except Exception:
        logger.exception("failed to load data into `%s`", table)
        raise
    finally:
        engine.dispose()


def main():
    """Read MOCK_DATA.csv, clean it, and load the mock table."""
    logger.info("starting mock data upload")
    data = read_data("MOCK_DATA.csv")
    cleaned = clean_data(data)
    # Always use the table name "mock" so every database matches.
    load_data(cleaned, "mock")
    logger.info("upload finished")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    main()
