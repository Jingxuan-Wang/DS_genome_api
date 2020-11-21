# Mobility Genome API
This is a python package for Dspark API. It includes api requests for discrete visit, stay point, link meta, od matrix and od through link.

# Dependency
Python 3.*

# API version by default
discrete visit: v2

stay point: v2

od matrix: v3

od through link: v1

link meta: v1

# API Basic Element:
please refer to https://dataspark.atlassian.net/wiki/spaces/Peking/pages/777847016/Common+API+Elements

# Install
please pull the repo by running following command:

```bash
git pull https://github.com/SingTel-DataCo/DS_genome_api.git
```

check into the package folder and run:

```bash
python3 setup.py build

python3 setup.py install
```

or using whl file to install:

```bash
pip install *.whl
```

# Usage

## Latest Change

### Mapping of values
#### A dict can be used to map between values in the underlying data and a desired dimension or filter value
```python
from genomeapi.dspark import Dspark
from genomeapi.elements import Filter, ValueMap

dspark = Dspark()
f = Filter()
dspark.od_matrix.dates(begin_date="2020-09-29")
dspark.od_matrix.filter(f.selector("origin_state","3"))
dspark.od_matrix.granularity(period="P1D")
dspark.od_matrix.time_series_reference("origin")
vmap = ValueMap("group")
transportmap = vmap(dimension="dominant_mode",
                           output_name="main_mode",
                           show_nulls=True,
                           map={
                               'Public Transport': ['BUS','RAIL','SUBWAY','TRAM','FERRY'],
                               'Car': ['CAR'],
                               'Walk': ['WALK']
                           })
rmap = ValueMap("range")
agegrpmap = rmap(dimension="agent_year_of_birth",
                 output_name="age_group",
                 show_nulls=True,
                 map={
                   "20-24": [2020-24,2020-20],
                   "25-29": [2020-29,2020-25],
                   "30-34": [2020-34,2020-30],
                   "35-39": [2020-39,2020-35],
                   "40-44": [2020-44,2020-40],
                   "45-49": [2020-49,2020-45],
                   "50-54": [2020-54,2020-50],
                   "55-59": [2020-59,2020-55],
                   "60-64": [2020-64,2020-60],
                   "65-69": [2020-69,2020-65],
                   "70+": [2020-999,2020-70]
                 })

dspark.od_matrix.maps(transportmap, agegrpmap)
dspark.od_matrix.aggregate(metric="unique_agents",typ="hyperUnique",described_as="unique_people")
dspark.od_matrix.aggregate(metric="total_records",typ="longSum",described_as="total_trips")
dspark.od_matrix.dimension_facets("main_mode","age_group")
qldtripsbymainmode = dspark.od_matrix.request(version="4")
```

### URL parameter
```python
from genomeapi.dspark import Dspark

url = 'https://staging-presto.dsparkanalytics.com.au'
dspark = Dspark(URL = url)

## Default URL: 'https://apistore.dsparkanalytics.com.au'
dspark = Dspark()
```

### For Extraction Fn
```python
from genomeapi.elements import ExtractionFn
## string extraction function example
string_extraction_fn = ExtractionFn(typ='substring') # not 'string' as type
string_extraction_fn(index=1, length=4)

## time format extraction function example

time_format_extraction_fn = ExtractionFn(typ='timeFormat') # not 'time' as type
time_format_extraction_fn(format='EEEE', timezone='Australia/Sydney')
```

## Basic Query
```python
from genomeapi.dspark import Dspark
from genomeapi.toolkits import *

## proxies(optional)
proxies = {'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080',}
## with proxies
dspark = Dspark(proxies=proxies)

## without proxies
dspark = Dspark()

dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period=period(day=1))
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique")

## posting request to api and get data
data = dspark.stay_point.request()

## Query new API endpoint
data = dspark.stay_point.request(version= "4")

## converting data into a pandas DataFrame
dspark.stay_point.to_df(data)

## getting query in json format
dspark.stay_point.json
```

## Switch endpoint
```python
dspark.stay_point ## endpoint for stay point v2
dspark.od_matrix ## endpoint for od matrix v3
dspark.discrete_vist ## endpoint for discrete visit v2
dspark.od_through_link ## endpoint for od through link v1
dspark.link_meta ## endpoint for link meta v1
```

## API endpoint version
#### To use new features including timezone, we need to set the API version as "4"
```python
dspark.stay_point.request(version = "4") ## endpoint for stay point v4
dspark.od_matrix.request(version = "4") ## endpoint for od matrix v4
dspark.discrete_vist.request(version = "4") ## endpoint for discrete visit v4
dspark.od_through_link.request(version = "4") ## endpoint for od through link v4
```

## Multiple aggregations
```python
dspark.od_matrix.aggregate(metric="unique_agents", described_as="unique_agents")
dspark.od_matrix.aggregate(metric="total_records", described_as="total_stays")
```

## Stackable Dimension Facets
```python
from genomeapi.elements import DimensionFacet, ExtractionFn
dfacet = DimensionFacet("extraction")
extraction = ExtractionFn("timeFormat")
dfacets = ["origin_sa4","origin_sa3", dfacet(dimension="__time",output_name="hour",extraction_fn=extraction(format="HH",timezone="Australia/Brisbane"))]
dspark.od_matrix.dimension_facets(dfacets)
```
## Query granularity
Method 1: use ISO 8601 duration format
```python
dspark.stay_point.granularity(period="PT1H")
# we can put timezone in granularity element, the default timezone is Australia/Sydney time
dspark.stay_point.granularity(period="PT1H", timezone="Australia/Brisbane")  
```
Method 2: set day/hour/minute, and period function will convert it into ISO 8601 duration format
```python
from genomeapi.toolkits.api_period import *
dspark.stay_point.granularity(period(hour=1), timezone="Australia/Brisbane") 

# we can mix day/hour/minute together
dspark.stay_point.granularity(period(day = 1,hour=1, minute=15), timezone="Australia/Brisbane")
```

## Filter
```python
from genomeapi.elements import Filter
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

## Maps
### Simple Maps
```python
from genomeapi.elements import ValueMap
simple_map = ValueMap("simple")
simple_map.map(BOY="M", GIRL="F")
maps = simple_map(dimension="agent_gender", output_name="gender")
dspark.stay_point.maps(maps)
```

### Group Maps
```python
from genomeapi.elements import ValueMap
group_map = ValueMap("group")
group_map.map(public_transport=["BUS", "TRAM", "FERRY"])
maps = group_map(dimension="dominant_mode", output_name="transport")
dspark.stay_point.maps(maps)
```

### Range Maps
```python
from genomeapi.elements import ValueMap
range_map = ValueMap("range")
range_map.map(Morning=["00", "11"], Afternoon=["12","23"], Full_Day=["00", "23"])
maps = range_map(dimension="__time", output_name="timeperiod", show_nulls=True)
dspark.stay_point.maps(maps)
```

### Multiple Maps
```python
from genomeapi.elements import ValueMap
range_map = ValueMap("range")
range_map.map(Morning=["00", "11"], Afternoon=["12","23"], Full_Day=["00", "23"])
group_map = ValueMap("group")
group_map.map(public_transport=["BUS", "TRAM", "FERRY"])
maps = range_map(dimension="__time", output_name="timeperiod", show_nulls=True) + group_map(dimension="dominant_mode", output_name="transport")
dspark.stay_point.maps(maps)
```

## Clear out previous query
```python
dspark.stay_point.clear_all()
```

# Authorize
Method 1:
Please put your key and secret into config/genome_api.ini in root directory. Example for genome_api.ini would be:

```
[DEFAULT]
consumer_key = *****************
consumer_secret = ***************
```

Method 2:
set 'consumer_key' and 'consumer_secret' as environment variable

```python
## setting envior in jupyter
%env consumer_key = *********
%env consumer_secret = *********
``` 

Method 3:
provide 'token' as a string variable
```python
token = *********
from genomeapi.dspark import Dspark
dspark = Dspark(token=token)
```

# Query Example
For query examples, please refer to [sample query](sample_query.md)

# Development Log
## 1.0.12
1. add `maps` as part of elements in package

## 1.0.11
1. make `filter` obj be able to reused after calling to_dict function

## 1.0.10
1. add `period`  function in 'toolkits.api_period' for constructing period string
2. type in aggregation can be matched automatically based on given metric.
3. add `version` parameter in api 'request' function, so user can select different version of same API
4. add `timezone` parameter for granularity function, default value is 'Australia/Sydney'

## 1.0.9
1. Add a new section 'toolkits' which includes useful advance features regarding to specific user cases and some common 
functions such as functions related to timestamp manipulation

## 1.0.8
1. Workaround for API limitation of multiple extraction functions on same dimension
2. Fix a issue that cause or operation not working for a list of and filter and vice versa 
3. User can give a path of config file which contains the key and secret for authorization

## 1.0.7
1. Allow multiple extraction dimensions as both list or multiple unnamed parameters

## 1.0.6
1. Make LinkMeta API functional
2. Make dimension facets stackable.

## 1.0.5
1. Add proxies(optional) for api request

## 1.0.4
1. Fix the issue that filter doesn't allow multiple layers of logical operations

## 1.0.3
1. Change response error from RequestException to ResponseException in order to show more detailed error return from API
2. Add RequestException message when api return is empty

