from queue import Full, Queue
from threading import Thread

from metrics import pipeline_dropped_messages, pipeline_queue_size


class MessagePipeline:
    def __init__(self, processor, num_workers=2, max_queue_size=10000):
        self.processor = processor
        self.queue = Queue(maxsize=max_queue_size)
        self.num_workers = num_workers
        self.workers = []

        self._start_workers()

    def _start_workers(self):
        for worker_id in range(self.num_workers):
            thread = Thread(
                target=self._worker,
                args=(worker_id,),
                daemon=True,
                name=f"message-worker-{worker_id}",
            )
            thread.start()
            self.workers.append(thread)

        print(
            f"[PIPELINE] Started {self.num_workers} worker(s), "
            f"queue maxsize={self.queue.maxsize}"
        )

    def _worker(self, worker_id):
        while True:
            data = self.queue.get()
            try:
                self.processor.process(data)
            except Exception as exc:
                print(f"[WORKER {worker_id} ERROR] {exc}")
            finally:
                self.queue.task_done()
                pipeline_queue_size.set(self.queue.qsize())

    def submit(self, data):
        try:
            self.queue.put_nowait(data)
            pipeline_queue_size.set(self.queue.qsize())
            return True
        except Full:
            pipeline_dropped_messages.inc()
            print("[PIPELINE] Queue is full. Dropping incoming telemetry message.")
            return False
