import datetime
from pathlib import Path

from collections import OrderedDict


def get_tsv_line(dictionary):
    return "\t".join([str(v) for v in dictionary.values()]) + "\n"


def get_header_line(dictionary):
    return "\t".join(dictionary.keys()) + "\n"


def ensure_dir(file_path):
    Path.mkdir(Path.absolute(Path(file_path).parent), exist_ok=True)


def dump_data(data, path):
    ensure_dir(path)
    if not Path.exists(path):
        with open(path, "w") as f:
            f.write(get_header_line(data))
            f.write(get_tsv_line(data))
    else:
        with open(path, "a") as f:
            f.write(get_tsv_line(data))


def save_user_stats(self, username, path=""):
    if not username:
        username = self.username
    user_id = self.convert_to_user_id(username)
    infodict = self.get_user_info(user_id)
    if infodict:
        data_to_save = OrderedDict(
            date=str(datetime.datetime.now().replace(microsecond=0)),
            followers=int(infodict["follower_count"]),
            following=int(infodict["following_count"]),
            medias=int(infodict["media_count"])
        )
        file_path = Path(path, "%s.tsv" % username)
        dump_data(data_to_save, file_path)
        self.logger.info("Stats saved at %s." % data_to_save["date"])
    return False
