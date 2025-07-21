class BaseLoader:
    def load(self, data: list[dict]):
        """Load a list of (timestamp, value) dicts into the configured destination."""
        raise NotImplementedError("Each loader must implement the `load` method.")
