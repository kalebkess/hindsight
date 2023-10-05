import os

from dotenv import load_dotenv
import pandas as pd
import yfinance as yf

load_dotenv()



def load_components(INDEX: str="", refresh: bool=False):
    """
    returns list of symbols for a given index.
    stores components for index locally if not already stored or if refresh=True
    """

    ROOT_PATH = os.environ.get("ROOT_PATH")
    INDEX = os.environ.get("INDEX") if INDEX == "" else INDEX
    index_filename = f"{ROOT_PATH}/data/indices/{INDEX}.csv"
    
    # creates indices folder if it does not exist
    if not os.path.exists(f"{ROOT_PATH}/data/indices"):
        print("[*] creating indices folder")
        os.makedirs(f"{ROOT_PATH}/data/indices")
    else:
        print("[*] indices folder exists")

    # Dow Jones Industrial Average (DJIA)
    if INDEX == "DJIA":
        if os.path.exists(index_filename) and refresh is False:
            print(f"[*] loading {INDEX} components from existing csv file")
            components = pd.read_csv(index_filename, header=None)[0].to_list()
        else:
            print(f"[*] csv file for {INDEX} does not exists or refresh=True")
            print(f"[*] downloading components for {INDEX} index")
            components_df = pd.read_html("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")[1]
            components_df.loc[:, "Symbol"].to_csv(index_filename, header=False, index=False)
            print(f"[*] components for {INDEX} stored in indices folder")
            print(f"[*] loading components for {INDEX} from csv stored in indices folder")
            components = pd.read_csv(index_filename, header=None)[0].to_list()

        return components



def download_prices_for_components(INDEX="", START:str = "", END:str = ""):
    """
    downloads prices for index with start and end date
    """

    ROOT_PATH = os.environ.get("ROOT_PATH")
    INDEX = os.environ.get("INDEX") if INDEX == "" else INDEX
    START = os.environ.get("START") if START == "" else START
    END = os.environ.get("END") if END == "" else END
    INDEX_FOLDER = f"{ROOT_PATH}/data/prices/{INDEX}"

    if not os.path.exists(INDEX_FOLDER):
        print(f"[*] creating price folder for {INDEX}")
        os.makedirs(INDEX_FOLDER)
    else:
        print(f"[*] price folder for {INDEX} exists")
    
    components = load_components(INDEX=INDEX)

    
    for component in components:
        print(f"[*] downloading prices for {component}")
        data = yf.download(component, start=START, end=END)
        data.to_csv(f"{INDEX_FOLDER}/{component}.csv")
        print(f"[*] prices for {component} stored")



if __name__ == "__main__":
    components = load_components()
    print(components)
    download_prices_for_components()