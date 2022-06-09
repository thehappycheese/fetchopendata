import pandas as pd
import pandasdmx as sdmx
from typing import Optional

def fetch_abs_erp_lga2021_western_australia(startPeriod:str="2010", endPeriod:Optional[str]=None) -> pd.DataFrame:
    """
    Fetch dataset avaliable from here : https://explore.data.abs.gov.au/vis?pg=0&tm=ERP%20LGA&hc[dataflowId]=ERP_LGA2021&df[ds]=PEOPLE_TOPICS&df[id]=ERP_LGA2021&df[ag]=ABS&df[vs]=1.0.0&pd=2010%2C&dq=..50080%2B50210%2B50250%2B50280%2B50350%2B50420%2B50490%2B50560%2B50630%2B50770%2B50840%2B50910%2B50980%2B51080%2B51120%2B51190%2B51260%2B51310%2B51330%2B51400%2B51470%2B51540%2B51610%2B51680%2B51750%2B51820%2B51890%2B51960%2B52030%2B52100%2B52170%2B52240%2B52310%2B52380%2B52450%2B52520%2B52590%2B52660%2B52730%2B52800%2B52870%2B52940%2B53010%2B53080%2B53150%2B53220%2B53290%2B53360%2B53430%2B53570%2B53640%2B53710%2B53780%2B53800%2B53920%2B53990%2B54060%2B54130%2B54170%2B54200%2B54280%2B54310%2B54340%2B54410%2B54480%2B54550%2B54620%2B54690%2B54760%2B54830%2B54900%2B54970%2B55040%2B55110%2B55180%2B55250%2B55320%2B55390%2B55460%2B55530%2B55600%2B55670%2B55740%2B55810%2B55880%2B55950%2B56090%2B56160%2B56230%2B56300%2B56370%2B56460%2B56580%2B56620%2B56730%2B56790%2B56860%2B56930%2B57000%2B57080%2B57140%2B57210%2B57280%2B57350%2B57420%2B57490%2B57630%2B57700%2B57770%2B57840%2B57910%2B57980%2B58050%2B58190%2B58260%2B58330%2B58400%2B58470%2B58510%2B58540%2B58570%2B58610%2B58680%2B58760%2B58820%2B58890%2B59030%2B59100%2B59170%2B59250%2B59310%2B59320%2B59330%2B59340%2B59350%2B59360%2B59370%2B5.A&ly[cl]=TIME_PERIOD&ly[rw]=REGION
    """
    ABS = sdmx.Request("ABS_XML")
    meta = ABS.datastructure("ERP_LGA2021")
    # for key,value in meta.codelist.items():
    #     print(f"{' '+key+' ':=^30}")
    #     print(sdmx.to_pandas(value))

    # Get the code list for LGAs. This is an interesting hierarchical key table;
    CL_LGA_2021 = sdmx.to_pandas(meta.codelist["CL_LGA_2021"])
    # Get the index in the table of the row where the `name` column is `Western Australia`
    western_australia_code      = (CL_LGA_2021["name"]=="Western Australia").idxmax()
    # Get the rows of the table where the `parent` column is equal to the `western_australia_code`
    western_australia_lga_codes =  CL_LGA_2021[CL_LGA_2021["parent"] == western_australia_code]
    # Get index of these rows (the list of lga codes) and glue the list 
    # together to get string "50080+50210+50250+50280+50350+50420[...]"
    lga_numbers_key = "+".join(western_australia_lga_codes.index)
    lga_numbers_key
    
    params = {
        "startPeriod":startPeriod,
        "dimensionAtObservation":"AllDimensions",
    }

    if endPeriod is not None:
        params["endPeriod"] = endPeriod
    
    response = ABS.data(
        "ERP_LGA2021",
        key={
            "REGION": lga_numbers_key,#western_australia_lga_codes.index.to_list(),
        },
        dsd=meta.structure["ERP_LGA2021"],
        params=params,
    )
    
    df = response.to_pandas().unstack("TIME_PERIOD").droplevel(["MEASURE","REGION_TYPE"])
    df = df.reset_index(drop=False)
    df["REGION"] = df["REGION"].map(sdmx.to_pandas(meta.codelist["CL_LGA_2021"])["name"])
    df["FREQ"] = df["FREQ"].map(sdmx.to_pandas(meta.codelist["CL_FREQ"])["name"])
    return df