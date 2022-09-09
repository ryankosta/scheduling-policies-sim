#!/bin/env python3
import pandas as pd
import sys
import matplotlib.pyplot as plt

lat_fields = ["99.9% Tail Latency","99% Tail Latency","95% Tail Latency"]
fields = lat_fields.copy()
fields.append("Cores")
df1 = pd.read_csv(sys.argv[1])[fields]
df2 = pd.read_csv(sys.argv[2])[fields]
df1_rename = dict()
df2_rename = dict()
for field in lat_fields:
    df1_rename[field] = "No Warn: " + field
    df2_rename[field] = "Warn: " + field
df1 = df1.rename(columns=df1_rename)
df2 = df2.rename(columns=df2_rename)
merge_df = pd.merge(df1,df2)
for field in lat_fields:
    graph_df = merge_df[["Cores","Warn: " + field, "No Warn: " + field]]
    graph_df = graph_df[graph_df["Cores"] != 16]
    graph_df = graph_df.sort_values("Cores")
    graph_df = graph_df.set_index("Cores")
    print(graph_df)
    graph_df.plot(y=["Warn: " + field,"No Warn: " + field],ylabel=(field +" (ns)"))
    plt.savefig(field +"-graph.pdf")
