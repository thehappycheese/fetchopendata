

def test_fetch_road_network_info():
    import pandas as pd
    from fetchopendata import fetch_road_network_info
    df = fetch_road_network_info(additional_params={"where":"ROAD='H001'"})
    assert isinstance(df, pd.DataFrame)
    assert len(df.index)>10
