from rabbitmq import start_consumer
from processor import Processor
from metrics import start_metrics_server

if __name__ == "__main__":
    start_metrics_server(8100)

    processor = Processor()
    start_consumer(processor)
