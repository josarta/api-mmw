from datetime import timedelta
from aiobreaker import CircuitBreaker, CircuitBreakerListener
from fastapi import logger


circuit_breaker = CircuitBreaker(fail_max=5, timeout_duration=timedelta(seconds=60))


class LogListener(CircuitBreakerListener):

    def state_change(self, breaker, old, new):
        logger.info(f"{old.state} -> {new.state}")

breaker = CircuitBreaker(listeners=[LogListener()])