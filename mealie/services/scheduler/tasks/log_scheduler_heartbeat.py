import datetime

from mealie.core import root_logger


def log_scheduler_heartbeat() -> None:
    """Emit a heartbeat so operators can confirm the scheduler loop is alive."""
    logger = root_logger.get_logger()
    now = datetime.datetime.now(datetime.UTC).isoformat()
    logger.debug("scheduler heartbeat at %s", now)
    print(f"[scheduler] heartbeat {now}")
