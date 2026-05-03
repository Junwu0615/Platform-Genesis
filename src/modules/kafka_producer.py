# -*- coding: utf-8 -*-
from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from src.config import *
from src.modules.log import Logger
from src.utils.env_config import GET_PATH_ROOT, get_logger_name


console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)


class KafkaProducerManager:
    def __init__(self, bootstrap_servers, sr_url, schemas_list: list):
        # 建立 Schema Registry 客戶端
        sr_conf = {'url': sr_url}
        self.sr_client = SchemaRegistryClient(sr_conf)

        # 基礎 Producer 設定
        _config = {
            'bootstrap.servers': bootstrap_servers,
            'queue.buffering.max.messages': 100000,
            'linger.ms': 50,
            'compression.type': 'lz4',  # gzip / lz4[*] / snappy[*]
            # 'key.serializer': StringSerializer('utf_8'),
            # 'value.serializer': avro_serializer  # TODO 自動處理序列化與註冊
        }
        self.producer = Producer(_config)
        # self.producer = SerializingProducer(_config)

        # 快取 Serializers，避免重複向 SR 註冊
        self.serializers = {}
        for schemas in schemas_list:
            self.serializers[schemas['topic']] = AvroSerializer(self.sr_client, schemas['content'])

        # self.serializers = {
        #     "inst.status-logs": AvroSerializer(self.sr_client, schemas.MACHINE_STATUS_SCHEMA),
        #     "inst.prod-records": AvroSerializer(self.sr_client, schemas.PROD_RECORD_SCHEMA)
        # }


    def send_message(self, topic, key, payload):
        serializer = self.serializers.get(topic)
        if not serializer:
            logging.error(f"[Topic: {topic}] 尚未定義 Schema", exc_info=False)
            return

        # 將 dict 序列化為 Avro 二進制格式 => JDBC Sink
        ctx = SerializationContext(topic, MessageField.VALUE)
        value_bytes = serializer(payload, ctx)

        self.producer.produce(
            topic=topic,
            key=str(key).encode('utf-8'),
            value=value_bytes,
            on_delivery=self.delivery_report
        )


    def flush(self):
        self.producer.flush()


    def delivery_report(self, err, msg):
        if err:
            logging.error(f'訊息推送失敗: {err}', exc_info=False)
        else:
            # logging.info(f"訊息成功推送到 {msg.topic()} [{msg.partition()}]")
            pass