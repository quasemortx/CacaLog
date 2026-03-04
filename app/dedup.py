from __future__ import annotations

import time
from collections import deque

from redis.asyncio import Redis

# Fallback em memória
_mem: deque[str] = deque(maxlen=5000)
_mem_set: set[str] = set()


class Deduper:
    def __init__(self, redis: Redis | None, ttl_seconds: int = 7 * 24 * 3600):
        self.redis = redis
        self.ttl_seconds = ttl_seconds

    async def is_duplicate(self, msg_id: str) -> bool:
        global _mem_set
        if not msg_id:
            return False

        # 1) Redis (preferencial)
        if self.redis is not None:
            key = f"cacalogs:msg:{msg_id}"
            try:
                # SET key value NX EX ttl  -> retorna True se setou (novo), None se já existia
                ok = await self.redis.set(
                    name=key, value=str(int(time.time())), nx=True, ex=self.ttl_seconds
                )
                return ok is None
            except Exception:
                # Se Redis cair, cai pro fallback
                pass

        # 2) Fallback em memória
        if msg_id in _mem_set:
            return True
        _mem.append(msg_id)
        _mem_set.add(msg_id)
        # manter set em sincronia com deque
        while len(_mem_set) > len(_mem):
            _mem_set = set(_mem)
        return False
