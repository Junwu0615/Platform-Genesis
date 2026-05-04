# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-05-04
    Description:
    Notice:
        FIXME : 明文傳送應加密 + 安全性須提升 ( 認證 ... etc. )
"""
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
        sr_conf = {'url': sr_url}
        self.sr_client = SchemaRegistryClient(sr_conf)

        _config = {
            'bootstrap.servers': bootstrap_servers,
            'queue.buffering.max.messages': 100000,
            'linger.ms': 50,
            'compression.type': 'lz4', # gzip / lz4[*] / snappy[*]
            # 'key.serializer': StringSerializer('utf_8'),
            # 'value.serializer': avro_serializer  # TODO 自動處理序列化與註冊
        }
        self.producer = Producer(_config)
        # self.producer = SerializingProducer(_config)

        self.serializers = {}
        for schemas in schemas_list:
            self.serializers[schemas['topic']] = AvroSerializer(self.sr_client, schemas['content'])


    def send_message(self, topic, key, payload):
        try:
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

            # 高併發環境，在外部 loop 每 N 筆呼叫一次
            # self.poll(0)

        # 緩衝區滿了 queue.buffering.max.messages 的限制，無法接受更多訊息
        except BufferError:
            logging.warning(f'Local producer queue is full ({len(producer)} messages awaiting delivery), waiting ...')
            self.poll(1) # 阻塞 1 秒等待緩衝釋放
            self.send_message(topic, key, payload) # 重試

        except Exception as e:
            logging.error(f'Failed to produce message to {topic} [KEY: {key}]', exc_info=True)


    def poll(self, sec=None):
        if sec:
            self.producer.poll(sec)


    def flush(self, sec=None):
        if sec:
            self.producer.flush(sec)


    def delivery_report(self, err, msg):
        if err:
            logging.error(f'訊息推送失敗: {err}', exc_info=False)
        else:
            # logging.info(f"訊息成功推送到 {msg.topic()} [{msg.partition()}]")
            pass