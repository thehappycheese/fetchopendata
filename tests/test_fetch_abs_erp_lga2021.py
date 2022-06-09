



def test_fetch_road_network_info():
    import pandas as pd
    from fetchopendata import fetch_abs_erp_lga2021_western_australia
    df = fetch_abs_erp_lga2021_western_australia(startPeriod="2011", endPeriod="2020")
    assert df.columns[2] == "2011"
    assert df.columns[-1] == "2020"
    assert len(df.index)>10
