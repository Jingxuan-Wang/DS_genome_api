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
### Query 1: Hourly visits/individual/total stay duration in one sa2(305011105) during 2019-06-15 ~ 2019-06-16 (StayPoint)
```python
#Simple Staypoint query, no facet and no filter
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-16")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="PT1H", timezone="Australia/Brisbane")  
# we can use period function to easily specify day, hour, minute
# dspark.stay_point.granularity(period(hour=1), timezone="Australia/Brisbane")
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")
dspark.stay_point.aggregate(metric="sum_stay_duration", described_as="total_duration") # unit as minute

# posting request to api and get data
sp_example = dspark.stay_point.request()
# converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example)
```
### Query 2: 6 hour interval visits/individual in one sa2(117011325) during 2019-06-15 ~ 2019-06-22 (DisceteVisit)
```python
#Simple discrete visit query, no facet and no filter
dspark.discrete_visit.clear_all()
dspark.discrete_visit.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.discrete_visit.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.discrete_visit.granularity(period="PT6H")  ## 6H granularity
dspark.discrete_visit.aggregate(metric="unique_agents", described_as= "agent")
dspark.discrete_visit.aggregate(metric="total_records", described_as="total")
# posting request to api and get data
dv_example = dspark.discrete_visit.request()
# converting data into a pandas DataFrame
df_results= dspark.discrete_visit.to_df(dv_example)
# converting data into a pandas DataFrame
df_results= dspark.stay_point.to_df(sp_example)
```
### Query 3: Daily trip numbers/sum duration/individuals originating from one sa2(117011325) (OD Matrix)
```python
# Simple od matrix query, no facet and no filter (OD Matrix)
dspark.od_matrix.clear_all()
dspark.od_matrix.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.od_matrix.location(location_type="locationHierarchyLevel", level_type="origin_sa2", id="117011325")  ##define origin or destination
dspark.od_matrix.granularity(period="P1D")
dspark.od_matrix.time_series_reference("origin")  ## origin or destination
dspark.od_matrix.aggregate(metric="unique_agents", described_as="unique_agents")
dspark.od_matrix.aggregate(metric="total_records", described_as="trips")
dspark.od_matrix.aggregate(metric="sum_duration",  described_as="duration")  ##unit as seconds
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
dspark.od_through_link.aggregate(metric="unique_agents", described_as="unique_agents")
dspark.od_through_link.aggregate(metric="total_records", described_as="trips")
od_link_example = dspark.od_through_link.request()
df_results= dspark.od_through_link.to_df(od_link_example)
```
## Intermediate query
### Query 5: Daily visits/individual/total stay duration/maximum duration among the stays in one sa2(117011325) during 2019-06-15 ~ 2019-06-22, group by home location/gender, also extracting day of week information based on Sydney time zone. (Staypoint)
#intermediate level Staypoint query, multiple facet and time extraction
```python
dspark.stay_point.clear_all()
dspark.stay_point.dates(begin_date="2019-06-15",end_date="2019-06-22")
dspark.stay_point.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
dspark.stay_point.granularity(period="P1D")  ## 1 day granularity
dspark.stay_point.dimension_facets("agent_home_state_name","agent_gender", #separate dimension by comma
                                   dfacet(dimension="__time",output_name="dow",
                                          extraction_fn=extraction(format="EE",timezone="Australia/Sydney")))
                                        ##format EE for Day of Week, change to HH for hour of day
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")
dspark.stay_point.aggregate(metric="duration", typ="doubleMax",described_as="Max_duration") #max duration among the stay duration
dspark.stay_point.aggregate(metric="sum_stay_duration", described_as="total_duration") #unit as minute
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
dspark.od_matrix.aggregate(metric="unique_agents", described_as="unique_agents")
data=dspark.od_matrix.request()
df_results= dspark.od_matrix.to_df(data)
```

### Query 7: Trips start and end in the same SA2 (an example of combination of selector filter, and filter, or filter) (OD Matrix)
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
dspark.od_matrix.aggregate(metric="unique_agents", described_as="unique_agents")
data=dspark.od_matrix.request()
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
dspark.od_matrix.aggregate(metric="unique_agents", described_as="unique_visitors")
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
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")
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
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")
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
dspark.stay_point.aggregate(metric="unique_agents",  described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")
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
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays",described_as="visits")
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
dspark.stay_point.aggregate(metric="unique_agents", described_as= "agent")
dspark.stay_point.aggregate(metric="total_stays", described_as="visits")

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
dspark.stay_point.aggregate(metric="unique_agents", described_as="unique_agents")
data=dspark.stay_point.request()
df_results= dspark.stay_point.to_df(data)
```
