# FetchOpenData <!-- omit in toc -->

A python package containing tools to download data from various open data portals.

- [1. Installation](#1-installation)
- [2. Usage](#2-usage)
  - [2.1. `fetch_road_network_info()`](#21-fetch_road_network_info)
    - [2.1.1. Parameters](#211-parameters)
  - [2.2. `fetch_abs_erp_lga2021_western_australia()`](#22-fetch_abs_erp_lga2021_western_australia)
    - [2.2.1. Usage](#221-usage)

## 1. Installation

Please see [Releases](https://github.com/thehappycheese/fetchopendata/releases) for installation instructions.

## 2. Usage

### 2.1. `fetch_road_network_info()`

Fetches road network data data and returns a `pandas.DataFrame`.

The default source can be found in data portals 
- here: https://portal-mainroads.opendata.arcgis.com/datasets/mainroads::road-network/about
- here: https://data.gov.au/dataset/ds-wa-31cc90e7-2b25-48b7-b855-0ed41996ff50/details?q=
- and here: https://catalogue.data.wa.gov.au/dataset/mrwa-road-network

#### 2.1.1. Parameters

- `url`: str
  - optional
  - specify to override the default
  - default: "https://mrgis.mainroads.wa.gov.au/arcgis/rest/services/OpenData/RoadAssets_DataPortal/MapServer/17/query"
- `chunk_limit`: Optional[int] = None
  - Specify if you wish to limit the number of chunks requested. This can prevent an infinite loop if something goes wrong. Typically the server will respond with chunks of up to 1000 records at a time. Repeated requests are made until all chunks are received.
- `query_params`:Optional[Dict[str, Any]] = None
  - Specify to entirely replace the default query parameters
  - (see more detail at https://developers.arcgis.com/rest/services-reference/enterprise/map-service.htm)
- `additional_query_params`:Optional[Dict[str, Any]] = None
  - Specify to replace only some of the default query parameters
  
```python
# default query parameters if `query_params` is not specified
{
  "where":"1=1",
  "outFields":["ROAD", "START_SLK", "END_SLK", "CWY", "NETWORK_TYPE", "START_TRUE_DIST", "END_TRUE_DIST", "RA_NO"],
  "outSR":4326,
  "f":"json",
  "returnGeometry":False,
}
```

call with default query parameters:

```python
from fetchopendata import fetch_road_network_info
df = fetch_road_network_info()
```

Specify `query_params` to replace all default query parameters:

```python
# this will not use any of the defaults above. This query will fetch all data including geometry; it is not recommended that you do this.
# (I think `"where":"1=1"` is required on all queries?)
df = fetch_road_network_info(
  query_params={
    "where":"1=1",
  }
)
```

Specify `additional_query_params` to replace only some of the default query parameters

```python
df = fetch_road_network_info(
  additional_params={
    "where":"ROAD='H001'",
  }
)
```

### 2.2. `fetch_abs_erp_lga2021_western_australia()`

Fetch Estimated Residential Population from Australian Bureau of Statistics.

Publicly avaliable from ABS here [ERP by LGA (ASGS 2021), 2001 to 2021](https://explore.data.abs.gov.au/vis?pg=0&tm=ERP%20LGA&hc[dataflowId]=ERP_LGA2021&df[ds]=PEOPLE_TOPICS&df[id]=ERP_LGA2021&df[ag]=ABS&df[vs]=1.0.0&pd=2010%2C&dq=..50080%2B50210%2B50250%2B50280%2B50350%2B50420%2B50490%2B50560%2B50630%2B50770%2B50840%2B50910%2B50980%2B51080%2B51120%2B51190%2B51260%2B51310%2B51330%2B51400%2B51470%2B51540%2B51610%2B51680%2B51750%2B51820%2B51890%2B51960%2B52030%2B52100%2B52170%2B52240%2B52310%2B52380%2B52450%2B52520%2B52590%2B52660%2B52730%2B52800%2B52870%2B52940%2B53010%2B53080%2B53150%2B53220%2B53290%2B53360%2B53430%2B53570%2B53640%2B53710%2B53780%2B53800%2B53920%2B53990%2B54060%2B54130%2B54170%2B54200%2B54280%2B54310%2B54340%2B54410%2B54480%2B54550%2B54620%2B54690%2B54760%2B54830%2B54900%2B54970%2B55040%2B55110%2B55180%2B55250%2B55320%2B55390%2B55460%2B55530%2B55600%2B55670%2B55740%2B55810%2B55880%2B55950%2B56090%2B56160%2B56230%2B56300%2B56370%2B56460%2B56580%2B56620%2B56730%2B56790%2B56860%2B56930%2B57000%2B57080%2B57140%2B57210%2B57280%2B57350%2B57420%2B57490%2B57630%2B57700%2B57770%2B57840%2B57910%2B57980%2B58050%2B58190%2B58260%2B58330%2B58400%2B58470%2B58510%2B58540%2B58570%2B58610%2B58680%2B58760%2B58820%2B58890%2B59030%2B59100%2B59170%2B59250%2B59310%2B59320%2B59330%2B59340%2B59350%2B59360%2B59370%2B5.A&ly[cl]=TIME_PERIOD&ly[rw]=REGION)

This function demonstrates the use the SDMX rest interface used by the ABS
website. It is included in this python package as the source code may serve as a
useful example for future uses of the SDMX format for other purposes.

#### 2.2.1. Usage

```python
import pandas as pd
from fetchopendata import fetch_abs_erp_lga2021_western_australia
df = fetch_abs_erp_lga2021_western_australia(startPeriod="2011", endPeriod="2020")
```
