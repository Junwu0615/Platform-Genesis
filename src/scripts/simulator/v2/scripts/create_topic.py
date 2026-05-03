# -*- coding: utf-8 -*-
import sys, os; sys.path.insert(0, os.getcwd())

from src.config import *
from src.utils.tools import *
from src.utils.env_config import GET_PATH_ROOT, get_logger_name
from src.modules.log import Logger
from confluent_kafka.admin import (
    AdminClient,
    NewTopic
)


console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)


YAML_VERSION = 'v2'
YAML_PATH = os.path.join('./src/scripts/simulator', f'{YAML_VERSION}', 'factory_config.yaml')
config = get_yaml_config(YAML_PATH)
kafka = config['kafka']


def sync_kafka_infrastructure(config_file):
    # TODO 1. 讀取封裝成類似 Connector 的 JSON 配置文件
    with open(config_file, 'r') as f:
        cfg = json.load(f)

    admin_client = AdminClient({'bootstrap.servers': f'{kafka['host']}:{kafka['port']}'})

    # TODO 2. 取得目前 Kafka 存在的 Topic
    existing_topics = admin_client.list_topics(timeout=5).topics

    new_topics_to_create = []

    for t_cfg in cfg['topics']:
        name = t_cfg['name']
        if name not in existing_topics:
            # TODO 3. 封裝成嚴謹的 NewTopic 對象
            new_topics_to_create.append(NewTopic(
                topic=name,
                num_partitions=t_cfg['partitions'],
                replication_factor=t_cfg['replication_factor'],
                config=t_cfg.get('configs', {})
            ))
            logging.info(f'計畫建立管道: {name}')

    # TODO 4. 執行建立 (類似 Connector 的部署動作)
    if new_topics_to_create:
        fs = admin_client.create_topics(new_topics_to_create)
        for topic, f in fs.items():
            try:
                f.result()
                logging.notice(f'管道 {topic} 部署成功 ...')

            except Exception as e:
                logging.error(f"管道 {topic} 部署失敗", exc_info=True)
    else:
        logging.notice('所有管道已對齊，無需更動 ...')


if __name__ == '__main__':
    try:
        sync_kafka_infrastructure(os.path.join('./src/scripts/simulator', f'{YAML_VERSION}', 'scripts', 'topics_config.json'))
    finally:
        sys.exit(0)