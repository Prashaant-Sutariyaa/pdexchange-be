import logging
import os
from datetime import datetime


os.makedirs("logs", exist_ok=True)


log_filename = datetime.now().strftime(
    "logs/sync_%Y%m%d_%H%M%S.log"
)


logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger("sync_logger")