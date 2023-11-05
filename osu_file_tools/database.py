import datetime
import logging
import os
from typing import Union

from osu_file_tools.utils.file import Reader

logger = logging.getLogger(__name__)


class OsuDB:
    def __init__(self, db_path: Union[str, os.PathLike]):
        with open(db_path, "rb") as db:
            reader = Reader(db)
            self.version = reader.read_uint()
            self.folder_count = reader.read_uint()
            self.account_unlocked = reader.read_bool()
            self.account_unlock_date = self.parse_datetime(reader.read_ulong())
            self.name = reader.read_string()
            self.num_beatmaps = reader.read_uint()
            self.beatmaps = [OsuDBBeatmap(reader=reader) for _ in range(self.num_beatmaps)]

        logger.info(f"Ended reading osu!.db. You have {len(self.beatmaps)} beatmaps!")

    @staticmethod
    def parse_datetime(ticks: int):
        return datetime.datetime(1, 1, 1) + \
            datetime.timedelta(microseconds=ticks // 10)


class OsuDBBeatmap:
    def __init__(self, reader: Reader):
        self._reader = reader
        self.artist = reader.read_string()
        self.artist_unicode = reader.read_string()
        self.song_title = reader.read_string()
        self.song_title_unicode = reader.read_string()
        self.mapper = reader.read_string()
        self.difficulty = reader.read_string()
        self.audio_file = reader.read_string()
        self.md5_hash = reader.read_string()
        self.map_file = reader.read_string()
        self.ranked_status = reader.read_ubyte()
        self.num_hitcircles = reader.read_ushort()
        self.num_sliders = reader.read_ushort()
        self.num_spinners = reader.read_ushort()
        self.last_modified = reader.read_ulong()
        self.approach_rate = reader.read_float()
        self.circle_size = reader.read_float()
        self.hp_drain = reader.read_float()
        self.overall_difficulty = reader.read_float()
        self.slider_velocity = reader.read_double()
        self.std_star_rating = self.read_star_rating()
        self.taiko_star_rating = self.read_star_rating()
        self.ctb_star_rating = self.read_star_rating()
        self.mania_star_rating = self.read_star_rating()
        self.drain_time = reader.read_uint()
        self.total_time = reader.read_uint()
        self.preview_time = reader.read_uint()
        self.timing_points = self.read_timing_point()
        self.beatmap_id = reader.read_uint()
        self.beatmap_set_id = reader.read_uint()
        self.thread_id = reader.read_uint()
        self.grade_standard = reader.read_ubyte()
        self.grade_taiko = reader.read_ubyte()
        self.grade_ctb = reader.read_ubyte()
        self.grade_mania = reader.read_ubyte()
        self.local_offset = reader.read_ushort()
        self.stack_leniency = reader.read_float()
        self.gameplay_mode = reader.read_ubyte()
        self.song_source = reader.read_string()
        self.song_tags = reader.read_string()
        self.online_offset = reader.read_ushort()
        self.title_font = reader.read_string()
        self.is_unplayed = reader.read_bool()
        self.last_played = reader.read_ulong()
        self.is_osz2 = reader.read_bool()
        self.folder_name = reader.read_string()
        self.last_checked = reader.read_ulong()
        self.ignore_sounds = reader.read_bool()
        self.ignore_skin = reader.read_bool()
        self.disable_storyboard = reader.read_bool()
        self.disable_video = reader.read_bool()
        self.visual_override = reader.read_bool()
        self.last_modified2 = reader.read_uint()
        self.scroll_speed = reader.read_ubyte()

    def read_star_rating(self):
        num_star_ratings = self._reader.read_uint()
        sr_dict = dict()

        for _ in range(num_star_ratings):
            mod, sr = self._reader.read_int_double()
            sr_dict[mod] = sr

        return sr_dict

    def read_timing_point(self):
        return [self._reader.read_timing_point() for _ in range(self._reader.read_uint())]

    def __hash__(self):
        return self.md5_hash
