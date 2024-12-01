import sys
from pyspark.streaming import kafka
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="StreamingKafka")
ssc = StreamingContext(sc, 2)
brokers, topic = sys.argv[1:]
kafkaStream = kafka.KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":brokers})
kafkaStream.show()

'''
from pyspark.sql import SparkSession

appName = "Kafka to spark"
master = "local"

spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

kafka_servers = "localhost:9092"
print('starting connection')
df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_servers) \
    .option("subscribe", "ValidatedElectionData") \
    .load()
df = df.withColumn('key_str', df['key'].cast('string').alias('key_str')).drop(
    'key').withColumn('value_str', df['value'].cast('string').alias('key_str')).drop('value')
df.show(5)
print('End')
'''