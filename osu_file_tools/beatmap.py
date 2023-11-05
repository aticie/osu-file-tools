import hashlib
import typing


class OsuBeatmap:

    def __init__(self, contents):
        self.beatmap_hash = hashlib.md5(contents).hexdigest()
        self.contents = contents
        # Todo: Parse beatmap

    def __repr__(self):
        return f"<OsuBeatmap: {self.beatmap_hash}>"

    @classmethod
    def from_file(cls, file_io: typing.IO):
        contents = file_io.read()
        return cls(contents)
