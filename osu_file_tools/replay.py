import dataclasses
import lzma
import os
from typing import Union, List, Tuple

from pydantic import BaseModel

from osu_file_tools.utils.file import Reader


class ReplayEvent(BaseModel):
    time_delta: int
    x: float = dataclasses.field()
    y: float = dataclasses.field()
    keys: int = dataclasses.field()


class OsuReplay:
    def __init__(self, replay_file: Union[str, os.PathLike]):
        with open(replay_file, "rb") as replay:
            self._reader = Reader(replay)

            self.game_mode = self._reader.read_ubyte()
            self.version = self._reader.read_uint()
            self.beatmap_md5 = self._reader.read_string()
            self.player_name = self._reader.read_string()
            self.replay_md5 = self._reader.read_string()
            self.count300 = self._reader.read_ushort()
            self.count100 = self._reader.read_ushort()
            self.count50 = self._reader.read_ushort()
            self.count_geki = self._reader.read_ushort()
            self.count_katu = self._reader.read_ushort()
            self.count_miss = self._reader.read_ushort()
            self.score = self._reader.read_uint()
            self.max_combo = self._reader.read_ushort()
            self.perfect = self._reader.read_ubyte()
            self.mods = self._reader.read_uint()
            self.life_bar = self._reader.read_string()
            self.timestamp = self._reader.read_ulong()
            self.compressed_data_length = self._reader.read_uint()
            self._raw_replay_data = replay.read(self.compressed_data_length)
            self.online_play_id = self._reader.read_ulong()

        self.replay_data, self.replay_seed = self.parse_replay(self._raw_replay_data)

    @staticmethod
    def parse_replay(raw_replay_data: bytes) -> Tuple[List[ReplayEvent], int]:
        """Parses raw replay data, returns the replay events and replay seed."""
        decompressed_data = lzma.decompress(raw_replay_data).decode('utf-8')
        raw_replay_events = filter(None, decompressed_data.split(","))
        replay_events = []
        for raw_event in raw_replay_events:
            event = raw_event.split("|")
            event_dict = {
                "time_delta": event[0],
                "x": event[1],
                "y": event[2],
                "keys": event[3]
            }
            replay_event = ReplayEvent.model_validate(event_dict)
            replay_events.append(replay_event)
        seed_event = replay_events.pop()
        replay_seed = seed_event.keys
        return replay_events, replay_seed
