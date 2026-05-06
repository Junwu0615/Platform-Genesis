# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-05-04
    Description:
    Notice:
        FIXME : 明文傳送應加密 + 安全性須提升 ( 認證 ...etc. )
"""
from shared.config import *
from shared.utils.kafka_tools import get_partition_id
from confluent_kafka import (
    Consumer,
    TopicPartition,
    KafkaError
)


class KafkaConsumerManager:
    def __init__(self, logging, log_main_name: str,
                 config: dict, topic: str, topic_key: str):

        self.logging = logging
        self.main_name = log_main_name

        _config = {
            'bootstrap.servers': '127.0.0.1:9092',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        }
        config = {**_config, **config}
        self.consumer = Consumer(config)

        target_partition = get_partition_id(
            self.consumer,
            topic,
            topic_key,
        )
        tp = TopicPartition(topic, target_partition)
        self.consumer.assign([tp])


    def get(self):
        return self.consumer


    def poll(self, timeout: float=1.0):
        """
        Poll for messages from the Kafka topic.
        :param timeout: Time in seconds to wait for a message before returning None.
        :return: The message value if a message is received, otherwise None.
        """
        msg = self.consumer.poll(timeout)
        if msg is None:
            return None

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # 當前消費完畢 => 目前沒新訊息，繼續等待 ...
                logging.info(f"[{self.main_name}] topic: {msg.topic()} | partition: {msg.partition()}")
                return None

            else:
                # 其他錯誤: Broker 斷線、認證失敗 ...etc.
                logging.error(f"[{self.main_name}] kafka consumer error: {msg.error()}", exc_info=False)
                raise

        return msg.value()


    def commit(self, asynchronous=False):
        self.consumer.commit(asynchronous=asynchronous)


    def close(self):
        self.consumer.close()
        logging.notice(f'[{self.main_name}] 已安全關閉 kafka consumer 連線 ...')