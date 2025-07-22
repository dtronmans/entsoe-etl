
# Extensible ENTSOE ETL

The ENTSOE API returns raw XML, making it difficult to use the returned data Python-usable and work with it directly

This repository defines an extensible Extract, Transform and Load (ETL) framework that makes the ENTSOE data easily retrievable, transformable, and storable.

Some example use cases:

* Visualization of variables like actual and forecasted load, demand and prices.
* Database storage (InfluxDB, TimeScaleDB, PostGreSQL, etc...)
* Forecasting using machine learning

Each part of the ETL pipeline is modular:
- **Extractors**: Query and fetch XML data from ENTSOE
- **Transformers**: Convert raw XML into timestamped, structured data
- **Loaders**: Send the processed data to a CSV, database, visualizer, etc.
- **Jobs**: Perform a series of custom Extract, Transform and Load operations


## Example

Code:

```
job = NetherlandsActualLoad(
    extractor=LoadForecastExtractor(),
    transformer=LoadTransformer(),
    loader=VisualizeLoader()
)

job.run(
    bidding_zone="10YNL----------L",
    load_type=LoadType.FORECAST,
    target_date="2025-07-07",
    n_days=1
)
```

Result:

In the above code snippet, custom-defined extract, transform, and load operations are combined to build and run a full pipeline.

In this case, the loader visualizes the result using Matplotlib. However, loaders can be swapped out to write to:

* CSV files
* SQL databases
* Time-series stores like TimeScaleDB or InfluxDB
* Any other destination

Result of the ETL job:

![alt text](etl_actual.png "An image showing the actual ETL load over time for the Netherlands")


# Usage

An ENTSOE API key needs to be featured in your .env for the repository to function:

```
API_KEY=<entsoe_api_key>
```

## Data structure

The output of the extract and load operations should be a list of dicts, in the form:

```
{'timestamp': 'str_timestamp', 'variable': value}
```

For example:

```
[
    {'timestamp': '2025-07-07T00:00:00+02:00', 'load_mw': 10409.0},
    {'timestamp': '2025-07-07T00:15:00+02:00', 'load_mw': 10232.5},
    ...
]
```

## Extractors

To define a new extractor, subclass BaseExtractor and implement the extract() method. This method must build the appropriate query parameters and call:

```
self.call_entsoe(params)
```
This ensures a consistent XML output across all extractors.

Example: extractors/load_forecast.py

## Transformers

Transformers receive the raw XML (from the extractor) and parse it into structured Python data.

To define one, subclass BaseTransformer and implement:

```
def transform(self, root: Element, expected_date: date) -> list[dict]:
```

This method should:

* Parse the XML Element
* Extract the relevant points (e.g., quantity, timestamp)
* Convert timestamps to the desired timezone
* Return a list of dicts with the data structure format mentioned above

Example: transformers/load_transformer.py

## Loaders

Loaders take the transformed data and send it to a destination.

All loaders subclass BaseLoader and implement:

```
def load(self, data: list[dict]):
```

Examples:

* PrintLoader: just prints the output to console
* VisualizeLoader: plots data using Matplotlib

## Jobs

Jobs are the glue between extract, transform, and load steps. The base job is ETLJob, which can run one or more days of data:

```
class ETLJob:
    def __init__(self, extractor, transformer, loader):
        ...

    def run(self, target_date, n_days=1, **extract_kwargs):
        ...
```

You can also define custom jobs for specific countries or use cases by subclassing ETLJob. For example:

```
class NetherlandsActualLoad(ETLJob):
    def run(self, target_date, n_days=1):
        ...
```