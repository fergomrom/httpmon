from time import time


class Counter(object):
    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    @property
    def remaining_time(self):
        return self.target - time()

    @property
    def has_finished(self):
        return time() > self.target


def truncate_text(text, max_len):
    if len(text) > max_len:
        return f'{text[:max_len]}...'
    return text
