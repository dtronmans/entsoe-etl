from loaders.base import BaseLoader


class PrintLoader(BaseLoader):
    def load(self, data: list[dict]):
        print(f"\n--- Loaded {len(data)} records ---")
        for item in data[:5]:
            print(item)
        if len(data) > 5:
            print("... (truncated)\n")
