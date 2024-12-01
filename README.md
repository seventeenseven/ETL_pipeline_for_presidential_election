# Pipeline de Traitement des Données pour l'élection présidentielle française 2021

Ce projet implémente un pipeline de traitement des données pour analyser les résultats des élections présidentielles françaises. Il utilise des outils modernes comme Python, PySpark, Airflow, NiFi et Kafka pour collecter, transformer et publier les données.

## Fonctionnalités principales
- **Extraction de données** : Collecte des résultats électoraux à partir de fichiers CSV publiés sur [data.gouv.fr](https://www.data.gouv.fr).
- **Traitement des données** : Nettoyage, transformation et validation des données.
- **Publication et diffusion** : Transmission des données traitées à un serveur Kafka pour une consommation ultérieure.

## Architecture du Projet
![Pipeline Architecture](/img/airflow.png)

### Technologies Utilisées
- **Python** : Pour le scripting et les transformations de données.
- **PySpark** : Pour le traitement parallèle et l'analyse des données volumineuses.
- **Airflow** : Pour l'orchestration et l'automatisation des tâches.
- **NiFi** : Pour la construction de pipelines de flux de données.
- **Kafka** : Pour la diffusion des données traitées.

## Organisation des Fichiers

- **`/scripts`** : Contient les scripts Python pour télécharger, nettoyer et transformer les données.
- **`/airflow`** : Contient les DAGs pour orchestrer les étapes du pipeline.
- **`/nifi`** : Contient les fichiers XML de configuration pour les pipelines NiFi.

## Détails des Pipelines

### Airflow
Les DAGs orchestrent les étapes du pipeline, incluant :
1. **Téléchargement des fichiers CSV** via des scripts Bash.
2. **Traitement des données** avec des fonctions Python et Spark.
3. **Publication des résultats** sur Kafka.

Exemple de DAG :
```python
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('example_dag', schedule_interval='@daily') as dag:
    task = PythonOperator(
        task_id='example_task',
        python_callable=my_function
    )
```

### PySpark
- Renommage des colonnes pour des noms compréhensibles.
- Suppression des doublons et des valeurs nulles.
- Publication des données nettoyées vers Kafka.

### NiFi
- Utilisé pour orchestrer le flux initial des données brutes et les connecter au serveur Kafka.

![NIFI flow](/img/nifi.png)


## Instructions pour l’Exécution

### Prérequis
- Python 3.8+
- Apache Spark
- Apache Airflow
- Apache NiFi
- Apache Kafka

### Exécution
1. Démarrez le serveur Kafka :
   ```bash
   kafka-server-start.sh config/server.properties
   ```
2. Démarrez Airflow :
   ```bash
   airflow webserver &
   airflow scheduler &
   ```
3. Exécutez les DAGs via l’interface Airflow.

## Résultats
Les données traitées seront publiées dans les topics Kafka pour une consommation éventuelle par d'autres systèmes.

## Contributions
Les contributions sont les bienvenues ! Veuillez soumettre vos propositions via des pull requests.


