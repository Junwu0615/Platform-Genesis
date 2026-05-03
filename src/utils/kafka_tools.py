# -*- coding: utf-8 -*-
import json

from src.config import *
from src.modules.log import Logger
from src.utils.env_config import GET_PATH_ROOT, get_logger_name


console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)


def kafka_murmur2(data: bytes):
    """Kafka 官方 Java 版 Murmur2 的 Python 實作"""
    length = len(data)
    seed = 0x9747b28c
    # 'm' and 'r' are mixing constants generated offline.
    # They're not so unique, so they don't have to be random.
    m = 0x5bd1e995
    r = 24

    # Initialize the hash to a 'random' value
    h = seed ^ length
    length_4 = length // 4

    for i in range(length_4):
        i_4 = i * 4
        k = struct.unpack('<I', data[i_4:i_4 + 4])[0]
        k = (k * m) & 0xffffffff
        k ^= (k >> r) & 0xffffffff
        k = (k * m) & 0xffffffff
        h = (h * m) & 0xffffffff
        h ^= k

    # Handle the last few bytes of the input array
    extra_bytes = length % 4
    if extra_bytes == 3:
        h ^= (data[(length & ~3) + 2] << 16) & 0xffffffff
    if extra_bytes >= 2:
        h ^= (data[(length & ~3) + 1] << 8) & 0xffffffff
    if extra_bytes >= 1:
        h ^= (data[length & ~3]) & 0xffffffff
        h = (h * m) & 0xffffffff

    h ^= (h >> 13) & 0xffffffff
    h = (h * m) & 0xffffffff
    h ^= (h >> 15) & 0xffffffff
    return h


def get_partition_id(consumer, topic_name: str, topic_key: str) -> int:
    """根據 Kafka 的分區邏輯，計算出給定 topic_key 對應的 Partition ID"""

    # 取得分區總數
    cluster_metadata = consumer.list_topics(topic=topic_name)
    partitions = cluster_metadata.topics[topic_name].partitions
    num_partitions = len(partitions)

    # 計算 Partition ID
    target_partition = (kafka_murmur2(topic_key.encode('utf-8')) & 0x7fffffff) % num_partitions

    logging.info(f"[{topic_key}] 對應 Partition 分區 ID 為: [{target_partition}]")
    return target_partition


def producer_on_message(err, msg):
    if err is not None:
        logging.error(f'訊息推送失敗: {err}', exc_info=False)
    else:
        # logging.info(f"訊息成功推送到 {msg.topic()} [{msg.partition()}]")
        pass


def add_message(producer, topic, key, payload):
    """使用 producer 發送訊息"""
    try:
        # 確保資料格式正確
        payload = payload.encode('utf-8') if isinstance(payload, str) else payload
        payload = json.dumps(payload) if isinstance(payload, dict) else payload

        # 發送訊息
        producer.produce(
            topic=topic,
            key=str(key),  # 確保 key 是字串或 bytes
            value=payload,
            callback=producer_on_message
        )

        # 高併發環境，在外部 loop 每 N 筆呼叫一次
        # producer.poll(0)

    # 緩衝區滿了 queue.buffering.max.messages 的限制，無法接受更多訊息
    except BufferError:
        logging.warning(f'Local producer queue is full ({len(producer)} messages awaiting delivery), waiting ...')
        producer.poll(1) # 阻塞 1 秒等待緩衝釋放
        add_message(producer, topic, key, data) # 重試

    except Exception as e:
        logging.error(f'Failed to produce message to {topic} [KEY: {key}]', exc_info=True)