from typing import Any, Optional, Dict
import requests
from urllib.parse import urlencode
import pandas as pd

DATA_SOURCE_URL = "https://mrgis.mainroads.wa.gov.au/arcgis/rest/services/OpenData/RoadAssets_DataPortal/MapServer/17/query"

DEFAULT_PARAMETERS = {
    "where":"1=1",
    "outFields":",".join(["ROAD", "START_SLK", "END_SLK", "CWY", "NETWORK_TYPE", "START_TRUE_DIST", "END_TRUE_DIST", "RA_NO"]),
    "outSR":4326,
    "f":"json",
    "returnGeometry":False,
}

def fetch_road_network_info(
        url:str=DATA_SOURCE_URL,
        chunk_limit:Optional[int]=None,
        query_params:Optional[Dict[str, Any]]=None,
        additional_params:Optional[Dict[str, Any]]=None,
    ) -> pd.DataFrame:
    """
    
    Fetches data from the specified `url` and returns a `pandas.DataFrame`.
    
    The default source can be found in data portals 
    - here: https://portal-mainroads.opendata.arcgis.com/datasets/mainroads::road-network/about
    - here: https://data.gov.au/dataset/ds-wa-31cc90e7-2b25-48b7-b855-0ed41996ff50/details?q=
    - and here: https://catalogue.data.wa.gov.au/dataset/mrwa-road-network
    
    Specify a `chunk_limit` to limit the number of chunks requested. This can prevent an infinite loop if something goes wrong. Default is None.
    
    Specify `query_params` to entirely replace the default query parameters:
    (see more detail at https://developers.arcgis.com/rest/services-reference/enterprise/map-service.htm)

    ```python
    # default query parameters if `query_params` is not specified
    {
        "where":"1=1",
        "outFields":["ROAD", "START_SLK", "END_SLK", "CWY", "NETWORK_TYPE", "START_TRUE_DIST", "END_TRUE_DIST", "RA_NO"],
        "outSR":4326,
        "f":"json",
        "returnGeometry":False,
    }

    # call with non-default query parameters
    # this will not use any of the defaults above. This query will fetch all data including geometry; it is not recommended that you do this.
    # (I think `"where":"1=1"` is required on all queries?)
    fetch_road_network_info(
        query_params={
            "where":"1=1",
        }
    )
    ```

    Specify `additional_query_params` to replace only some of the default query parameters

    ```python
    fetch_road_network_info(
        additional_params={
            "where":"ROAD='H001'",
        }
    )
    ```

    ARGS:
        url: str = "https://mrgis.mainroads.wa.gov.au/arcgis/rest/services/OpenData/RoadAssets_DataPortal/MapServer/17/query"
        chunk_limit: Optional[int] = None
        query_params:Optional[Dict[str, Any]] = None
    """

    if query_params is None:
        query_params = DEFAULT_PARAMETERS
    
    if additional_params is None:
        additional_params = {}

    query_params |= additional_params

    response = requests.request("GET", f"{url}?" + urlencode(query_params | {"returnCountOnly":True}))
    try:
        record_count = response.json()["count"]
    except KeyError:
        raise Exception(
            f"could not get record count from {url} \n\n"
            "This is likely due to a problem with the query:\n"
            "?{urlencode(query_params | {'returnCountOnly':True})}\n\n"
            "The raw response follows:\n{response.text}"
        )

    print(f"Downloading {record_count} records" + (":" if chunk_limit is None else f", chunk_limit={chunk_limit}:"))

    # ASSUMED_CHUNK_SIZE = 1000
    # if chunk_limit is not None:
    # 		print("." * min(chunk_limit, math.floor(record_count/ASSUMED_CHUNK_SIZE)))
    # else:
    # 		print("." * math.floor(record_count/ASSUMED_CHUNK_SIZE))

    output=[]
    offset = 0
    chunk_counter = 0

    while True:

        if chunk_limit is not None and chunk_counter >= chunk_limit:
            break

        chunk_counter += 1

        response = requests.request(
            "GET",
                f"{url}?"
            + urlencode(
                {"resultOffset":offset} | query_params
            )
        )

        json = response.json()
        
        offset += len(json["features"])
        output.extend(json["features"])

        if "exceededTransferLimit" not in json or not json["exceededTransferLimit"]:
            break
        # print(".", end="")

    print(f"\nDownload Completed. received {len(output)} records")
    json["features"] = output

    result = pd.json_normalize(json, record_path="features")
    result.columns = [c.replace("attributes.", "") for c in result.columns]

    return result