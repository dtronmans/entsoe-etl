class ETLJob:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, **kwargs):
        raw_data = self.extractor.extract(**kwargs)
        parsed_data = self.transformer.transform(raw_data, kwargs["expected_date"])
        self.loader.load(parsed_data)
