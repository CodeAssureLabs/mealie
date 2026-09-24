from mealie.core import root_logger

logger = root_logger.get_logger()


def log_scheduler_heartbeat():
    """Emit a heartbeat so operators can confirm the scheduler loop is alive"""
    logger.info("scheduler heartbeat")
