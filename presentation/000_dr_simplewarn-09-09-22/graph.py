#!/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt

lat_fields = ["99.9% Tail Latency","99% Tail Latency","95% Tail Latency"]
files = ["dr-nowarn-varyload-manycores-fromdr.out",  "dr-warn-varyload-manycores-7ms.out"]
fields = lat_fields.copy()
fields.append("Cores")
nowarn_df = pd.read_csv(files[0])[fields]
warn_df = pd.read_csv(files[1])[fields]
nowarn_df_rename = dict()
warn_df_rename = dict()
for field in lat_fields:
    nowarn_df_rename[field] = "No Warn: " + field
    warn_df_rename[field] = "Warn: " + field
nowarn_df = nowarn_df.rename(columns=nowarn_df_rename)
warn_df = warn_df.rename(columns=warn_df_rename)
merge_df = pd.merge(nowarn_df,warn_df)
for field in lat_fields:
    graph_df = merge_df[["Cores","Warn: " + field, "No Warn: " + field]]
    graph_df = graph_df[graph_df["Cores"] != 16]
    graph_df = graph_df.sort_values("Cores")
    graph_df = graph_df.set_index("Cores")
    print(graph_df)
    graph_df.plot(y=["Warn: " + field,"No Warn: " + field],ylabel=(field +" (ns)"))
    plt.savefig(field +"-graph.pdf")
