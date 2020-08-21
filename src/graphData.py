import pandas as pd
from dataLogger import load_json_file

def produce_instapygram_report():
    raw_data = load_json_file("instagramStats.json")
    df = pd.DataFrame(raw_data)
    print ("\n############## InstaPYgram Report ##############\n")
    print (df)
