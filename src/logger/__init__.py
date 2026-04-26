import logging
import os
from datetime import datetime

# ──────────────────────────────────────────
# Log file ka naam — date & time ke saath
# ──────────────────────────────────────────
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# ──────────────────────────────────────────
# Logs folder automatically create hoga
# ──────────────────────────────────────────
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# ──────────────────────────────────────────
# Full path of log file
# ──────────────────────────────────────────
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# ──────────────────────────────────────────
# Logger Configuration
# ──────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ──────────────────────────────────────────
# Console par bhi logs dikhenge
# ──────────────────────────────────────────
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger("YT_MLOOPS")
logger.setLevel(logging.INFO)

# Duplicate handlers avoid karo
if not logger.handlers:
    logger.addHandler(console_handler)


# ──────────────────────────────────────────
# Test karo (optional — direct run karne par)
# ──────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Logger successfully initialized!")
    logger.warning("Yeh ek warning hai")
    logger.error("Yeh ek error hai")