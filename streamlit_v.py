import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

# -----------------------------------
# MySQL Configuration
# -----------------------------------

DB_USER = "spark"
DB_PASSWORD = "spark"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "taxi_db"

# -----------------------------------
# Create Database Connection
# -----------------------------------

@st.cache_resource
def get_engine():

    connection_url = (
        f"mysql+pymysql://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    return create_engine(connection_url)


# -----------------------------------
# Get Available Tables
# -----------------------------------

def get_tables(engine):

    inspector = inspect(engine)

    return inspector.get_table_names()


# -----------------------------------
# Load Table Data
# -----------------------------------

def load_table(engine, table_name, limit=100):

    # Quote the identifier using MySQL backticks.
    # The table name comes from inspect(), not user input.
    quoted_table = f"`{table_name.replace('`', '``')}`"

    query = text(
        f"SELECT * FROM {quoted_table} LIMIT :limit"
    )

    return pd.read_sql(
        query,
        engine,
        params={"limit": limit}
    )


# -----------------------------------
# Streamlit Interface
# -----------------------------------

st.set_page_config(
    page_title="TLC Trip Record Data",
    layout="wide"
)

st.title("TLC Trip Record Data")
st.write(
    "Explore the data stored in your MySQL database."
)

try:

    engine = get_engine()

    # Test connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    st.success("Connected to MySQL successfully!")

    # Get tables
    tables = get_tables(engine)

    if not tables:

        st.warning("No tables found in the database.")

    else:

        st.sidebar.header("Database Tables")

        selected_table = st.sidebar.selectbox(
            "Select a table",
            tables
        )

        row_limit = st.sidebar.slider(
            "Number of rows",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )

        st.header(f"Table: {selected_table}")

        # Load data
        df = load_table(
            engine,
            selected_table,
            row_limit
        )

        # Display information
        st.subheader("Table Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows Loaded", len(df))

        with col2:
            st.metric("Columns", len(df.columns))

        # Display dataframe
        st.subheader("Data")

        st.dataframe(
            df,
            use_container_width=True
        )

        # Display data types
        st.subheader("Column Data Types")

        st.dataframe(
            pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str).values
            }),
            use_container_width=True
        )

except SQLAlchemyError as e:

    st.error("Database connection or query failed.")

    st.exception(e)

except Exception as e:

    st.error("An unexpected error occurred.")

    st.exception(e)