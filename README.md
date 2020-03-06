# Readme
This is a python package for Dspark API. It includes api requests for discrete visit, stay point, link meta, od matrix and od through link.

# Dependency
Python 3.*

# API version
discrete visit: v2

stay point: v2

od matrix: v3

od through link: v1

link meta: v1

# API Basic Element:
please refer to https://dataspark.atlassian.net/wiki/spaces/Peking/pages/777847016/Common+API+Elements

# Usage

## Basic Query
```python
from genome_api.dspark import Dspark

dspark = Dspark()
dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="PT1H")
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique")

## posting request to api and get data
data = dspark.stay_point.request()

## converting data into a pandas DataFrame
dspark.stay_point.to_df(data)

## getting query in json format
dspark.stay_point.json
```

## Multiple aggregations
```python
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
dspark.od_matrix.aggregate(metric="total_stays", typ="doubleSum", described_as="total_stays")
```

## Filter
```python
from genome_api.elements import Filter
filter = Filter()
## normal filter example
dspark.stay_point.filter(filter.in_filter("VIC17483860", "VIC6052402","NSW500187142", dimension="link_id"))

## logic filter exmaple AND
filter = Filter()
and_filter = filter.selector(dimension='agent_gender', value='M') \
    & filter.selector(dimension='agent_home_state', value='1')
dspark.stay_point.filter(and_filter)

## logic filter exmaple OR
filter = Filter()
or_filter = filter.selector(dimension='agent_gender', value='M') \
    | filter.selector(dimension='agent_home_state', value='1')
dspark.stay_point.filter(or_filter)

## logic filter exmaple NOT
filter = Filter()
not_filter = ~filter.selector(dimension='agent_gender', value='M')
dspark.stay_point.filter(not_filter)
```

## Extraction Function
```python
from genome_api.elements import ExtractionFn
## string extraction function example
string_extraction_fn = ExtractionFn(typ='string')

## numeric extraction function example

string_extraction_fn = ExtractionFn(typ='string')
```


# Config
Please put your key and secret into config/genome_api.ini in root directory. Example for genome_api.ini would be:

```
[DEFAULT]
consumer_key = *****************
consumer_secret = ***************
```
