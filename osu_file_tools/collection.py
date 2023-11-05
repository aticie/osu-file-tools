import datetime
import os
from pathlib import Path
from typing import Union, Dict

from osu_file_tools.utils.file import Reader, WriteBuffer


class OsuCollection:
    def __init__(self, name: str):
        self.name = name
        self.beatmaps = set()

    def add_bmap(self, beatmap_md5: str):
        self.beatmaps.add(beatmap_md5)

    def write(self, fileh):
        buffer = WriteBuffer()
        buffer.write_string(self.name)
        buffer.write_uint(len(self.beatmaps))
        for beatmap in self.beatmaps:
            buffer.write_string(beatmap)
        fileh.write(buffer.data)


class OsuCollectionDB:
    def __init__(self, db_path: Union[str, os.PathLike]):
        if isinstance(db_path, str):
            db_path = Path(db_path)
        self.db_path = db_path
        with open(db_path, 'rb') as f:
            self._reader = Reader(f)
            self.version = self._reader.read_uint()
            self.nr_collections = self._reader.read_uint()

            self.collections: Dict[str, OsuCollection] = {}
            for col_no in range(self.nr_collections):
                collection_name = self._reader.read_string()
                nr_beatmaps = self._reader.read_uint()
                collection = OsuCollection(collection_name)

                for i in range(nr_beatmaps):
                    beatmap_md5 = self._reader.read_string()
                    collection.add_bmap(beatmap_md5)

                self.collections[collection.name] = collection

    def add_collection(self, collection: OsuCollection):
        self.collections[collection.name] = collection
        self.nr_collections += 1

    def save(self):
        now = int(datetime.datetime.now().timestamp())
        self.db_path.replace(self.db_path.with_suffix(f'.bkp').with_stem(f"collection-{now}"))
        with open(self.db_path, 'wb') as f:
            f.write(self.version.to_bytes(length=4, byteorder='little'))
            f.write(self.nr_collections.to_bytes(length=4, byteorder='little'))
            for collection in self.collections.values():
                collection.write(f)
