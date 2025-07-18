import os
import pickle
import hashlib
from pathlib import Path
from datetime import datetime, timedelta


class Cacher:
    def __init__(self, cache_dir="cache", expiry_hours=72):
        self.cache_dir = Path(cache_dir)
        self.expiry = timedelta(hours=expiry_hours)
        self.cache_dir.mkdir(exist_ok=True)

    def _params_hash(self, params: dict) -> str:
        # Deterministic hash from sorted param key-values
        hash_input = str(sorted(params.items())).encode()
        return hashlib.md5(hash_input).hexdigest()

    def _get_cache_path(self, params: dict) -> Path:
        return self.cache_dir / f"{self._params_hash(params)}.pkl"

    def does_cache_exist(self, params: dict) -> bool:
        path = self._get_cache_path(params)
        if not path.exists():
            return False
        return datetime.now() - datetime.fromtimestamp(path.stat().st_mtime) < self.expiry

    def load_from_cache(self, params: dict):
        path = self._get_cache_path(params)
        with open(path, "rb") as f:
            return pickle.load(f)

    def save_to_cache(self, params: dict, data):
        path = self._get_cache_path(params)
        with open(path, "wb") as f:
            pickle.dump(data, f)
