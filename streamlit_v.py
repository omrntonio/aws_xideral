import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import plotly.express as px

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
    "Datos extraidos de https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
)

try:

    engine = get_engine()

    # Test connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    st.success("Conectado a MySQL exitosamente!")

    # Get tables
    tables = get_tables(engine)

    if not tables:

        st.warning("No se pudieron encontrar tablas en la base de datos.")

    else:
        tab1, tab2, tab3 = st.tabs([
            "Tabla",
            "Grafica",
            "Columnas Yellow Taxi"
        ])
        with tab1:

            st.sidebar.header("Tabla de la base de datos (⌐■_■)")

            selected_table = st.sidebar.selectbox(
                "Selecciona una tabla",
                tables
            )

            row_limit = st.sidebar.slider(
                "Numero de datos a cargar",
                min_value=10,
                max_value=1000,
                value=100,
                step=10
            )

            st.header(f"Tabla: {selected_table}")

            # Load data
            df = load_table(
                engine,
                selected_table,
                row_limit
            )

            # Display information
            st.subheader("Información de la Tabla")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Datos Cargados", len(df))

            with col2:
                st.metric("Columnas", len(df.columns))

            # Display dataframe
            st.subheader("Datos")

            st.dataframe(
                df,
                use_container_width=True
            )

        with tab2:

            columns = df.columns.tolist()

            chart_type = st.selectbox(
            "Selecciona tipo de gráfica",
            [
                "Scatter Plot",
                "Line Chart",
                "Bar Chart",
                "Histogram",
                "Heatmap"
            ]
        )

            # Select X-axis
            x_column = st.selectbox(
                "Selecciona columna del eje X",
                columns
            )

            # Select Y-axis when required
            if chart_type != "Histograma":

                y_column = st.selectbox(
                    "Selecciona columna del eje Y",
                    columns
                )

            # Generate chart
            if st.button("Generar Gráfica"):

                try:

                    if chart_type == "Scatter Plot":

                        fig = px.scatter(
                            df,
                            x=x_column,
                            y=y_column,
                            title=f"{y_column} vs {x_column}"
                        )

                    elif chart_type == "Line Chart":

                        fig = px.line(
                            df,
                            x=x_column,
                            y=y_column,
                            title=f"{y_column} over {x_column}"
                        )

                    elif chart_type == "Bar Chart":

                        fig = px.bar(
                            df,
                            x=x_column,
                            y=y_column,
                            title=f"{y_column} by {x_column}"
                        )

                    elif chart_type == "Histogram":

                        fig = px.histogram(
                            df,
                            x=x_column,
                            title=f"Distribution of {x_column}"
                        )

                    elif chart_type == "Heatmap":

                        fig = px.density_heatmap(
                            df,
                            x=x_column,
                            y=y_column,
                            title=f"Heatmap: {x_column} vs {y_column}"
                        )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(f"Unable to create chart: {e}")

        with tab3:
            pdf_url = "https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf"

            st.subheader("Yellow Taxi Data Dictionary")

            st.markdown(
                f"""
                <iframe
                    src="{pdf_url}"
                    width="100%"
                    height="700"
                    style="border: none;">
                </iframe>
                """,
                unsafe_allow_html=True
            )

        
            

except SQLAlchemyError as e:

    st.error("Conexión a la base de datos fallida.")

    st.exception(e)

except Exception as e:

    st.error("Error.")

    st.exception(e)