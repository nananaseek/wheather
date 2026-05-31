import asyncio
from celery import Task


class AsyncTask(Task):
    _loop = None

    @property
    def loop(self):
        if self._loop is None:
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop

    def __call__(self, *args, **kwargs):
        return self.loop.run_until_complete(self.run(*args, **kwargs))


