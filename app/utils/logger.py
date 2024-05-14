import loguru
import sys

logger = loguru.logger
logger.remove()
logger.add(sys.stdout, format="{time} - {level} - ({extra[request_id]}) {message} ", level="DEBUG")