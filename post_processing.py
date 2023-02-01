import os
import pandas as pd
from columns import output_kinf_columns, output_CR_Mass_columns, output_CR_cr_columns

INPUT_DIR = "./all_results"
res = os.listdir(INPUT_DIR)


def format_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    start_line = next(i for i, line in enumerate(lines) if line.startswith("  0.000000E+00"))
    end_line = next(i for i, line in enumerate(lines) if line.startswith("# FIN_DES_DONNEES"))
    all_lines = [[line for line in lines[i].strip().split(" ") if len(line) > 0] for i in range(start_line, end_line)]
    return pd.DataFrame(all_lines).astype(float)


all_df = []

for dir in res:

    df_output_kinf = format_file(os.path.join(INPUT_DIR, dir, "output_kinf"))
    df_output_kinf.columns = output_kinf_columns

    df_output_CR_cr = format_file(os.path.join(INPUT_DIR, dir, "output_CR_cr"))
    df_output_CR_cr.columns = output_CR_cr_columns

    df_output_CR_Mass = format_file(os.path.join(INPUT_DIR, dir, "output_CR_Mass"))
    df_output_CR_Mass.columns = output_CR_Mass_columns

    assert df_output_kinf["BURNUP (Mwd/t)"].equals(df_output_CR_cr["BURNUP (Mwd/t)"])
    assert df_output_CR_cr[["BURNUP (Mwd/t)", "temps (s)"]].equals(df_output_CR_Mass[["BURNUP (Mwd/t)", "temps (s)"]])

    df = pd.concat(
        [
            df_output_CR_Mass,
            df_output_CR_cr.loc[:, ~df_output_CR_cr.columns.isin(["BURNUP (Mwd/t)", "temps (s)"])],
            df_output_kinf.loc[:, df_output_kinf.columns != "BURNUP (Mwd/t)"],
        ],
        axis=1,
    )

    dict_from_name = dict(elem.split("=") for elem in dir.split("_"))
    df.insert(loc=0, column="Thorium Chain", value=dict_from_name["THORIUM"])
    df.insert(loc=1, column="U233 Input", value=float(dict_from_name["U233"]))
    df.insert(loc=2, column="U235 Input", value=float(dict_from_name["U235"]))
    df.insert(loc=3, column="PUTOT Input", value=float(dict_from_name["PUTOT"]))
    df.insert(loc=4, column="Moderator radius", value=float(dict_from_name["MODERATOR"]))

    all_df.append(df)

final_df = pd.concat(all_df)

final_df.to_csv("all_results.csv", index=False)
