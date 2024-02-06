# FetchOpenData <!-- omit in toc -->

A python package containing tools to download data from various open data portals.

- [1. Installation](#1-installation)
- [2. Usage](#2-usage)
  - [2.1. `fetch_road_network_info()`](#21-fetch_road_network_info)
    - [2.1.1. Parameters](#211-parameters)

## 1. Installation

Please see [Releases](https://github.com/thehappycheese/fetchopendata/releases) for installation instructions.

Or, to install the main branch please use:

```bash
pip install "https://github.com/thehappycheese/fetchopendata/zipball/main/"
```

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
