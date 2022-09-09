#!/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
CORE_CTS = [4,8,12,16,17,18,19,20,21,22,23,24,32]
def print_nonparal(files):
    to_print = dict()
    for ANALYSIS_PATH in files:
        df = pd.read_csv(ANALYSIS_PATH)
        for field, vals in df.to_dict().items():
            if field not in to_print:
                to_print[field] = list()
            to_print[field].append(vals[0])

    for field, vals in to_print.items():
        print(field + ":" + str(vals))
def print_paral(files):
    warn_cts = []
    nowarn_cts = []
    by_core = dict()
    for analysis_path in files:
        if "nowarn" in analysis_path:
            warn_type = "nowarn"
        else:
            warn_type = "warn"
        df = pd.read_csv(analysis_path)
        for index, vals in df.iterrows():
            core_ct = int(vals["Cores"])
            if core_ct not in by_core:
                by_core[core_ct] = dict()
            by_core[core_ct][warn_type] = vals.to_dict()
            warn_cts.append(core_ct)
            nowarn_cts.append(core_ct)
    by_core_list = list(by_core.items())
    by_core_list.sort()
    of_interest = dict()
    for core_ct, vals in by_core_list:
        if core_ct not in warn_cts or core_ct not in nowarn_cts:
            continue
        loadstr = "Load: %.2f" % by_core[core_ct]["warn"]["Real Load"] + "%"
        loadstr += "/%.2f" % by_core[core_ct]["nowarn"]["Real Load"] + "%"
        print("Cores: " + str(core_ct) + "| " + loadstr)
        for field in vals["nowarn"].keys():
            res = compare(field,vals["warn"][field],vals["nowarn"][field])
            if res is not None:
                print(("\t %30s" % field) + (": %.2f" % res[1]) + ", " + str(res[2])[:10]+", " + str(res[3])[:10])
                if field not in of_interest:
                    of_interest[field] = dict()
                of_interest[field][core_ct] = res

    print("Fields of interest")
    cores = [int(x) for x in by_core.keys()]
    cores.sort()
    core_hdr = ("\t %30s" % "Cores") + ": "
    for core_ct in cores:
        core_hdr += ("%7s" % str(core_ct)) + "|"
    print(core_hdr + "\n")
    df_dict = {"Loads" : [by_core[x]["warn"]["Real Load"] for x in cores]}
    for field, results in of_interest.items():
        to_print = ("\t %30s" % field) + ": "
        if field not in df_dict:
            df_dict[field] = list()
        for core_ct in cores:
            if core_ct in results:
                to_print += ("%7s" % ("%.2f" % results[core_ct][1])) + "|"
                df_dict[field].append(results[core_ct][1])
            else:
                to_print += ("%7s" % ("")) + "|"
                df_dict[field].append(0)
        print(to_print)

    nrows = int((len(df_dict.keys()) + 3) / 4)
    fig, axes = plt.subplots(nrows=nrows, ncols=4)
    row = 0
    col = 0
    for field in df_dict.keys():
        if field == "Loads":
            continue
        df1 = pd.DataFrame.from_dict(df_dict)
        df1.plot(x='Loads',y=field,ax=axes[row,col])
        col += 1
        if col == 4:
            row += 1
            col = 0
    plt.show()



IGNORE_FIELDS = ["Run ID","Cores","Description"]
def compare(fieldname,warn, nowarn):
    if fieldname in IGNORE_FIELDS or nowarn == 0:
        return None 
    diff = float(warn) - float(nowarn)
    perc_chg = (diff/nowarn) * 100
    if -1 < perc_chg and perc_chg < 1:
        return None 
    return (diff, perc_chg,nowarn,warn)



def main():
    if len(sys.argv) < 4:
        print("Not enough arguments")
    elif sys.argv[1] == "nonparal":
        print_nonparal(sys.argv[2:])
    elif sys.argv[1] == "paral":
        print_paral(sys.argv[2:])
    else:
        print("Invalid Option " + sys.argv[1])
        print("Options: paral or nonparal")
main()
