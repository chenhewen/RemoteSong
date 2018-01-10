import threading
import subprocess
import time
import re
from pathlib import Path
from wing_girl import *

wait = 0


class MyClass(threading.Thread):
    def __init__(self, file, length):
        threading.Thread.__init__(self)
        self.file = "mp3/" + file + ".mp3"
        global wait
        self.length = length
        wait += float(length)
        # print(wait)

    def run(self):
        rate = song_rate
        # print("wait before call------: " + str(wait - self.length))
        time.sleep(rate * (wait - self.length))
        if Path(self.file).exists():
            subprocess.call(["afplay", self.file])


def cal_length(length_str):
    count_half = length_str.count('_')
    count_dot = length_str.count('.')
    count_full = length_str.count('-')
    half = pow(0.5, count_half)
    dot = pow(1.5, count_dot)
    full = count_full + 1
      # print("length_str: {}, half: {}, dot: {}, full: {}".format(length_str, half, dot, full))
    return full * dot * half


if __name__ == '__main__':
    song = song_score
    rec_name = re.compile("[-|+|++]?[0-7]")
    rec_length = re.compile("(?<=[0-7])[_|.|\-|]*")
    for scale in song:
        name = rec_name.search(scale).group(0)
        rec_length_groups = rec_length.findall(scale)
        length = 0
        for length_str in rec_length_groups:
            length += cal_length(length_str)
        print("name: {}, length: {}".format(name, length))
        MyClass(name, length).start()
