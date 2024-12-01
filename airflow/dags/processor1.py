from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from nifi_processor import getFile, routeOnAttribute, putFile1, \
    updateAttributeTour1, updateAttributeTour2, \
    publishKafkaRecord_2_6Tour1, publishKafkaRecord_2_6Tour2, \
    putFileTour1, putFileTour2

# Define the DAG
# This DAG orchestrates the data pipeline using Airflow, where tasks include downloading files,
# processing them through various transformations, and publishing to Kafka.
with DAG(
    "DAG_ECE_pipeline",  # Name of the DAG
    schedule=timedelta(days=1),  # Schedule to run daily
    start_date=datetime(2022, 1, 1),  # Start date of the DAG
    catchup=False  # Prevent backfilling old runs
) as dag:

    # Task to download the file
    download_file = BashOperator(
        task_id='download_file',  # Unique ID for the task
        bash_command='python3 /scripts/download_file.py'  # Command to execute
    )

    # Task to get the file using NiFi integration
    get_file = PythonOperator(
        task_id="get_file",  # Unique ID for the task
        python_callable=getFile  # Python function to execute
    )

    # Task to route based on specific attributes
    route_on_attribute = PythonOperator(
        task_id="route_on_attribute",  # Unique ID for the task
        python_callable=routeOnAttribute  # Python function to execute
    )

    # Task to put the file in a specific location
    put_file1 = PythonOperator(
        task_id="put_file1",  # Unique ID for the task
        python_callable=putFile1  # Python function to execute
    )

    # Group of tasks for processing and publishing data for Tour 1
    with TaskGroup(group_id="put_and_publish_out_tour1") as put_and_publish_out_tour1:

        # Subgroup for updating attributes for Tour 1
        with TaskGroup(group_id="update_tour1") as update_tour1:
            update_Attribute_Tour1 = PythonOperator(
                task_id="update_Attribute_Tour1",  # Task to update attributes
                python_callable=updateAttributeTour1  # Python function to execute
            )

        # Subgroup for putting files and publishing for Tour 1
        with TaskGroup(group_id="put_and_publish_tour1") as put_and_publish_tour1:
            put_file_tour1 = PythonOperator(
                task_id="put_file_tour1",  # Task to put file
                python_callable=putFileTour1  # Python function to execute
            )

            publish_Kafka_Record_2_6Tour1 = PythonOperator(
                task_id="publish_Kafka_Record_2_6Tour1",  # Task to publish to Kafka
                python_callable=publishKafkaRecord_2_6Tour1  # Python function to execute
            )

            spark_run_tour1 = BashOperator(
                task_id="spark_run_tour1",  # Task to run Spark job
                bash_command='spark-submit /scripts/transformation_tour1.py'  # Command to execute
            )

            # Define task dependencies
            put_file_tour1 >> spark_run_tour1

        # Define subgroup dependencies
        update_tour1 >> put_and_publish_tour1

    # Group of tasks for processing and publishing data for Tour 2
    with TaskGroup(group_id="put_and_publish_out_tour2") as put_and_publish_out_tour2:

        # Subgroup for updating attributes for Tour 2
        with TaskGroup(group_id="update_tour2") as update_tour2:
            update_Attribute_Tour2 = PythonOperator(
                task_id="update_Attribute_Tour2",  # Task to update attributes
                python_callable=updateAttributeTour2  # Python function to execute
            )

        # Subgroup for putting files and publishing for Tour 2
        with TaskGroup(group_id="put_and_publish_tour2") as put_and_publish_tour2:
            put_file_tour2 = PythonOperator(
                task_id="put_file_tour2",  # Task to put file
                python_callable=putFileTour2  # Python function to execute
            )

            publish_Kafka_Record_2_6Tour2 = PythonOperator(
                task_id="publish_Kafka_Record_2_6Tour2",  # Task to publish to Kafka
                python_callable=publishKafkaRecord_2_6Tour2  # Python function to execute
            )

            spark_run_tour2 = BashOperator(
                task_id="spark_run_tour2",  # Task to run Spark job
                bash_command='spark-submit /scripts/transformation_tour2.py'  # Command to execute
            )

            # Define task dependencies
            put_file_tour2 >> spark_run_tour2

        # Define subgroup dependencies
        update_tour2 >> put_and_publish_tour2

    # Define overall task dependencies
    download_file >> get_file >> route_on_attribute >> [put_file1, put_and_publish_out_tour1, put_and_publish_out_tour2]
