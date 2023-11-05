import os
import zipfile
from typing import Union

from osu_file_tools.beatmap import OsuBeatmap


class Osz:
    def __init__(self, file_path: Union[str, os.PathLike]):
        self.beatmaps = []
        with zipfile.ZipFile(file_path) as osz:
            for file in osz.namelist():
                if file.endswith(".osu"):
                    with osz.open(file) as osu_beatmap_file:
                        self.beatmaps.append(OsuBeatmap.from_file(osu_beatmap_file))

        print(self.beatmaps)
