# Mobility Genome API
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

# Install
please pull the repo by running following command:

```bash
git pull https://github.com/Jingxuan-Wang/DS_genome_api.git
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

# Development Log
## 1.0.10
1. add `period`  function in 'toolkits.api_period' for constructing period string
2. type in aggregation can be matched automatically based on given metric.
3. add `version` parameter for api entry port, so user can select different version of same API
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

# Query Example
## prerequisite code
```python
#import library
from genomeapi.dspark import Dspark
from genomeapi.elements import DimensionFacet, ExtractionFn
from genomeapi.elements import Filter
from genomeapi.toolkits.api_filter import *
from functools import reduce

filter = Filter()
dfacet = DimensionFacet("extraction")
extraction = ExtractionFn("timeFormat")

import pandas as pd
#set showing all column in panda dataframes
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

## Default URL: 'https://apistore.dsparkanalytics.com.au'
dspark = Dspark(token = "your token")
# dspark = Dspark()   # if you have set the consumer key and secret in env setting, use this one
```
## Basic Query
### Query 1: Daily visits/individual/total stay duration in one sa2(117011325) during 2019-06-15 ~ 2019-06-22 (StayPoint)
```python
#Simple Staypoint query, no facet and no filter
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
dspark.stay_point.aggregate(metric="sum_stay_duration", typ="doubleSum",described_as="total_duration") #unit as minute

## posting request to api and get data
sp_example = dspark.stay_point.request()
## converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example)
```

### Query 2: 6 hour interval visits/individual in one sa2(117011325) during 2019-06-15 ~ 2019-06-22 (DisceteVisit)
```python
##Simple discrete visit query, no facet and no filter
dspark.discrete_visit.clear_all()
dspark.discrete_visit.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.discrete_visit.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.discrete_visit.granularity(period="PT6H")  ## 6H granularity
dspark.discrete_visit.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.discrete_visit.aggregate(metric="total_records", typ="doubleSum",described_as="total")
## posting request to api and get data
dv_example = dspark.discrete_visit.request()
## converting data into a pandas DataFrame
df_results= dspark.discrete_visit.to_df(dv_example)
```
### Query 3: Daily trip numbers/sum duration/individuals originating from one sa2(117011325) (OD Matrix)
```python
##Simple od matrix query, no facet and no filter
##od
dspark.od_matrix.clear_all()
dspark.od_matrix.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.od_matrix.location(location_type="locationHierarchyLevel", level_type="origin_sa2", id="117011325")  ##define origin or destination
dspark.od_matrix.granularity(period="P1D")
dspark.od_matrix.time_series_reference("origin")  ## origin or destination
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
dspark.od_matrix.aggregate(metric="total_records", typ="doubleSum", described_as="trips")
dspark.od_matrix.aggregate(metric="sum_duration", typ="doubleSum", described_as="duration")  ##unit as seconds
od_example = dspark.od_matrix.request()
df_results= dspark.od_matrix.to_df(od_example)
```
### Query 4: Daily trip numbers/individuals originating passing through link NSW513043667 during 2019-06-15 ~ 2019-06-22 (OD Through Link)
```python
dspark.od_through_link.clear_all()
dspark.od_through_link.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.od_through_link.time_series_reference("arrival")  #departure or arrival
dspark.od_through_link.granularity(period="P1D")
dspark.od_through_link.link("NSW513043667")
dspark.od_through_link.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
dspark.od_through_link.aggregate(metric="total_records", typ="doubleSum", described_as="trips")
od_link_example = dspark.od_through_link.request()
df_results= dspark.od_through_link.to_df(od_link_example)
```
## Intermediate query
### Query 5: Daily visits/individual/total stay duration/maximum duration among the stays in one sa2(117011325) during 2019-06-15 ~ 2019-06-22, group by home location/gender, also extracting day of week information based on Sydney time zone. (Staypoint)
```python
#intermediate level Staypoint query, multiple facet and time extraction

dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.dimension_facets("agent_home_state_name","agent_gender", #separate dimension by comma
                                   dfacet(dimension="__time",output_name="dow",
                                          extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
                                        ##format EE for Day of Week, change to HH for hour of day
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
dspark.stay_point.aggregate(metric="duration", typ="doubleMax",described_as="Max_duration") #max duration among the stay duration
dspark.stay_point.aggregate(metric="sum_stay_duration", typ="doubleSum",described_as="total_duration") #unit as minute
## posting request to api and get data
sp_example = dspark.stay_point.request()
## converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example)
```
### Query 6: daily mornig and afternoon peak trips to QLD (note: extraction function does NOT work for in_filter. To do this, we need to use a combination of or filter and a select filter) (OD Matrix)
```python
dspark.od_matrix.clear_all()
dspark.od_matrix.dates(begin_date="2020-01-01", end_date="2020-01-31")
dspark.od_matrix.location(location_type="locationHierarchyLevel", level_type="destination_state", id = "3")
dspark.od_matrix.granularity(period="PT12H")
dspark.od_matrix.time_series_reference("destination")
or_filter = filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "06") |\
            filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "07") |\
            filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "08") |\
            filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "16") |\
            filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "17") |\
            filter.selector(dimension="__time", extraction_fn= extraction(format="HH", timezone="Australia/Brisbane"),\
                                 value= "18")

dspark.od_matrix.dimension_facets(dfacet(dimension= "__time", extraction_fn=extraction(format="aa", timezone="Australia/Brisbane"),\
                                  output_name="morningPeak")) # generate a column showing whether it's AM peak or PM peak
dspark.od_matrix.filter(or_filter)
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
data=dspark.od_matrix.request()
df_results= dspark.od_matrix.to_df(data)
```

### Query 7: Trips start and end in the same SA2 (an example of combination of selector filter, and filter, or filter) (OD Matrix)
```python
dspark.od_matrix.clear_all()
## construct filter
listOfSA2 =['305021115', '303021053', '303021055', '303021058']
and_filter_list = list(map(lambda x: (filter.selector(dimension="origin_sa2", value=x) & filter.selector(dimension="destination_sa2", value=x)),listOfSA2))
combine_and_filters = reduce(lambda x, y: x | y, and_filter_list)
dspark.od_matrix.dates(begin_date="2020-03-01")
dspark.od_matrix.filter(combine_and_filters)
dspark.od_matrix.granularity(period="P1D")
dspark.od_matrix.time_series_reference("origin")
dspark.od_matrix.dimension_facets(["origin_sa2", "destination_sa2"])
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_visitors")
data = dspark.od_matrix.request()
df_results= dspark.od_matrix.to_df(data)
```

### Query 8: Trips ended in different SA2 (an example of combination of not filter, selectoer filter ,and filter, or filter) (OD Matrix)
```python
dspark.od_matrix.clear_all()
## construct filter
listOfSA2 =['305021115', '303021053', '303021055', '303021058']
and_filter_list = list(map(lambda x: (~filter.selector(dimension="origin_sa2", value=x) & filter.selector(dimension="destination_sa2", value=x)),listOfSA2))
combine_and_filters = reduce(lambda x, y: x | y, and_filter_list)
dspark.od_matrix.dates(begin_date="2020-03-01")
dspark.od_matrix.filter(combine_and_filters)
dspark.od_matrix.granularity(period="P1D")
dspark.od_matrix.time_series_reference("origin")
dspark.od_matrix.dimension_facets(["origin_sa2", "destination_sa2"])
dspark.od_matrix.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_visitors")
data = dspark.od_matrix.request()
df_results = dspark.od_matrix.to_df(data)
```
## Advanced Query
### Query 9: Visits/individual in one sa4(117) on 2019-06-15 who are NSW/VIC resident, group by home location (Staypoint)
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa4", id="117")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.filter(filter.in_filter("1","2",dimension = "agent_home_state"))  #two values
dspark.stay_point.dimension_facets("agent_home_state","agent_home_state_name")
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
sp_example_filter = dspark.stay_point.request()
df_results= dspark.stay_point.to_df(sp_example_filter)
```

### Query 10: visits/individual in one sa4(117) on 2019-06-15 during 12:00-12:59, group by home location (Staypoint)
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa4", id="117")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.filter(filter.selector(dimension="__time",value=12,extraction_fn=extraction(format="HH",timezone="Australia/Sydney")))  # Brisbane time stay from 12 o'clock
dspark.stay_point.dimension_facets("agent_home_state","agent_home_state_name")
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
sp_example_filter = dspark.stay_point.request()
df_results= dspark.stay_point.to_df(sp_example_filter)
```

### Query 11: Visits/individual in one sa4(117) on 2019/06/15 who are NOT NSW residents , group by home location (Staypoint)
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa4", id="117")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.filter(~filter.selector(dimension="agent_home_state",value=1))  #Not filter
dspark.stay_point.dimension_facets("agent_home_state","agent_home_state_name")
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
sp_example_filter = dspark.stay_point.request()
df_results= dspark.stay_point.to_df(sp_example_filter)
```

### Query 12: Daily visits/individual in one sa4(117) during 2019/06/15-22, return WEEKEND only , group by home location and day of week information(using OR filter, Sat OR Sun) (StayPoint)
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa4", id="117")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
#weekend filter using OR
dspark.stay_point.filter(filter.selector(dimension="__time",value="Sat",extraction_fn=extraction(format="EE",timezone="Australia/Sydney"))|
                         filter.selector(dimension="__time",value="Sun",extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
dspark.stay_point.dimension_facets("agent_home_state","agent_home_state_name",dfacet(dimension="__time",output_name="dow",
                                          extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")
## posting request to api and get data
sp_example_filter2 = dspark.stay_point.request()
## converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example_filter2)
```

### Query 13: Daily visits/individual in one sa4(117) during 2019/06/15-22, return WEEKDAY only , group by home location and day of week information ( Using AND/NOT filter combined, not Sat AND not Sun) (Staypoint)
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa4", id="117")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
#weekday filter using AND/NOT combined
dspark.stay_point.filter(~filter.selector(dimension="__time",value="Sat",extraction_fn=extraction(format="EE",timezone="Australia/Sydney"))&
                         ~filter.selector(dimension="__time",value="Sun",extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
dspark.stay_point.dimension_facets("agent_home_state","agent_home_state_name",dfacet(dimension="__time",output_name="dow",
                                          extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
dspark.stay_point.aggregate(metric="unique_agents", typ="hyperUnique", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", typ="doubleSum",described_as="visits")

## posting request to api and get data
sp_example_filter2 = dspark.stay_point.request()
## converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example_filter2)
```

### Query 14: number of staypoints in Brisbane Inner City SA4 for at least 2 hours between 9am-5pm 2020-03-03 (The start time of staypoint can be outside the time range, therefore we need to use api_filter_during function). The start hour is set to maximum 3 hours before 2020-03-03 09am. Granularity is set to 15 minutes in order to show when people arrived who met criteria
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2020-03-02", end_date="2020-03-04")
dspark.stay_point.location(location_type= "locationHierarchyLevel",level_type= "sa4",id = "305")
dspark.stay_point.granularity(period= "P31D")
dspark.stay_point.filter(api_filter_during(start = "2020-03-03 09:00:00",\
                                           end = "2020-03-03 17:00:00",\
                                           min_duration = 120,\
                                           starting_within_hr = 3,\
                                           tz="Australia/Brisbane"))
dspark.stay_point.dimension_facets(dfacet(dimension="__time",\
                                          extraction_fn=extraction(format="yyyy-MM-dd HH", timezone="Australia/Brisbane"),\
                                         output_name="Brisbane Time"))
dspark.stay_point.aggregate(metric="unique_agents", typ = "hyperUnique", described_as="unique_agents")
data=dspark.stay_point.request()
df_results= dspark.stay_point.to_df(data)
```




