import typing


class OsuStoryboard:
    def __init__(self, contents):
        # Todo: Parse storyboard
        self.contents = contents

    @classmethod
    def from_file(cls, file: typing.IO):
        contents = file.read()
        return cls(contents=contents)
