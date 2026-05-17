import asyncio
import json
import logging
import threading
from typing import Any

from aiokafka import AIOKafkaProducer

from game.game_app import Main
from game.queue_wrapper import DefaultBufferQueue
from config.settings import settings, producer_kafka_settings
from kafka.schemes.kafka_schemes import PlayerTopicScheme

logger = logging.getLogger("app")


class AIOGameMapKafkaProducer:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    _is_running = False
    _kafka_config = {}
    _player_updates_topic: str
    _location_updates_topic: str
    _game_updates_topic: str

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, output_queue: DefaultBufferQueue, game: Main, tick: int):
        if not self._initialized:
            self.game = game
            self.tick = tick
            self.producer = None
            self._output_queue = output_queue
            self._initialized = True
            self._player_updates_topic = settings.topic.player_update_kafka_topic
            self._location_updates_topic = settings.topic.location_update_kafka_topic
            self._game_updates_topic = settings.topic.game_update_kafka_topic

    async def start(self):
        if not self._is_running:
            try:
                self.producer = AIOKafkaProducer(**producer_kafka_settings.get_config())
                await self.producer.start()
            except Exception as err:
                logger.error(f"Producer Kafka error: {err}", err)
                return
            self._is_running = True

    async def run(self, stop_event: asyncio.Event):
        if self.producer is None:
            await self.start()
        try:
            while not stop_event.is_set():
                await asyncio.sleep(self.tick / 1000)
                buffer = await self._output_queue.drain_buffer()

                try:
                    for topic, data in buffer.items():
                        if topic == self._player_updates_topic:
                            await self._send_player_updates(data)
                        elif topic == self._location_updates_topic:
                            await self._send_location_updates(data)
                        elif topic == self._game_updates_topic:
                            await self._send_game_updates(data)
                    self.game.unlock_all_users()
                except Exception as err:
                    logger.error(f"Kafka producer error sending message: {err}", err)
                    # raise

        except asyncio.CancelledError:
            logger.info("Producer task cancelled.")
        finally:
            await self.close()
            self._is_running = False

    async def close(self):
        if self.producer:
            await self.producer.stop()

    async def _send_game_updates(self, data):
        for key, value in data.items():
            logger.info(f"PRODUCER - Send game updates: {key} : {value}")
            await self._send_message(self._game_updates_topic, key, value)

    async def _send_location_updates(self, data):
        for key, value in data.items():
            logger.info(f"PRODUCER - Send location updates: {key} : {value}")
            await self._send_message(self._location_updates_topic, key, value)

    async def _send_player_updates(self, data: dict[str, dict[str, Any]]):
        for user, controller in list(self.game.users_player_controllers.items()):
            user_params = data.get(user, None)
            if user_params is None:
                await controller.skip_turn()
                continue
            user_params["message"] = controller.get_player().messages
            payload = PlayerTopicScheme(**user_params)
            logger.info(f"PRODUCER - Send user updates: {user} : {user_params}")
            await self._send_message(self._player_updates_topic, user, payload.model_dump())
            controller.get_player().messages = []
        for controller in self.game.character_player_controllers.values():
            await controller.skip_turn()

    async def _send_message(self, topic, key, value):
        logger.info(f"SEND TO WS SERVER - TOPIC: {topic}, KEY: {key}, VALUE: {value}")
        encoded_message = self._ecode_message(key, value)
        metadata = await self.producer.send_and_wait(topic=topic,
                                                     key=encoded_message.get("key"),
                                                     value=encoded_message.get("value"))

    def _ecode_message(self, key: str, value: dict) -> dict:
        return {
            "key": key.encode("utf-8"),
            "value": json.dumps(value).encode("utf-8"),
        }
