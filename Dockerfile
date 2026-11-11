# Airflow 3.x image + Providers & custom deps from requirements.txt + dbt venv.
# Bump the tag to the newest 3.x if you like (e.g. 3.0.4 / 3.1.x).
FROM apache/airflow:3.0.3

# Copy and install python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# dbt in its own venv so it never clashes with Airflow's deps. DAG calls /opt/airflow/dbt_venv/bin/dbt
RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir "dbt-snowflake==1.8.*"