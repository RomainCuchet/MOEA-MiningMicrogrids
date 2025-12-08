import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description="Evo. Multi-Algorithm run")
    parser.add_argument(
        "--alg_flag",
        required=True,
        type=int,
        help="Algorithm flag: a number between 1 and 6",
    )
    parser.add_argument(
        "--seed_no", required=True, type=int, help="Seed No. between 0 and 30"
    )
    parser.add_argument("--n_pop", required=True, type=int)
    parser.add_argument("--n_eval", required=True, type=int)
    parser.add_argument(
        "--der_flag",
        required=True,
        type=int,
        help="DER combination flag-- 1: DG+RES else DG+RES+Li",
        # DER =  Distributed Energy Resources, DG = Distributed Generation, RES = Renewable Energy Sources, Li = Lithium-ion Battery
    )
    return parser


def res_2_dataframe(res, ENL, L_mg, der_flag, n_pop):
    xval = res.X
    fval = res.F
    ENS_val = res.G

    if der_flag == 1:
        sol = pd.DataFrame(
            {
                "PWT (MW)": xval[:, 0],
                "PV (MW)": xval[:, 1],
                "PBAT (MW)": 0,
                "EBAT (MWh)": 0,
                "PDG (MW)": xval[:, 2],
                "NPC ($/kWh)": fval[:, 0] / (ENL * L_mg),
                "GHE (kg CO2/kWh)": fval[:, 1] / ENL,
                "ERC (GWh/yr)": fval[:, 2],
                "ENS (%)": ENS_val[:, 0],
            }
        )
    else:
        sol = pd.DataFrame(
            {
                "PWT (MW)": xval[:, 0],
                "PV (MW)": xval[:, 1],
                "PBAT (MW)": xval[:, 2],
                "EBAT (MWh)": xval[:, 3],
                "PDG (MW)": xval[:, 4],
                "NPC ($/kWh)": fval[:, 0] / (ENL * L_mg),
                "GHE (kg CO2/kWh)": fval[:, 1] / ENL,
                "ERC (GWh/yr)": fval[:, 2],
                "ENS (%)": ENS_val[:, 0],
            }
        )

    hist = res.history

    for ii in range(len(hist)):
        a = hist[ii]
        b = a.pop
        x_vg = b.get("X")
        f_vg = b.get("F")
        g_vg = b.get("G")
        if ii == 0:
            if der_flag == 1:
                sol_g = pd.DataFrame(
                    {
                        "Gen (#)": [ii] * n_pop,
                        "PWT (MW)": x_vg[:, 0],
                        "PV (MW)": x_vg[:, 1],
                        "PBAT (MW)": 0,
                        "EBAT (MWh)": 0,
                        "PDG (MW)": x_vg[:, 2],
                        "NPC ($/kWh)": f_vg[:, 0] / (ENL * L_mg),
                        "GHE (kg CO2/kWh)": f_vg[:, 1] / ENL,
                        "ERC (GWh/yr)": f_vg[:, 2],
                        "ENS (%)": g_vg[:, 0],
                    }
                )
            else:
                sol_g = pd.DataFrame(
                    {
                        "Gen (#)": [ii] * n_pop,
                        "PWT (MW)": x_vg[:, 0],
                        "PV (MW)": x_vg[:, 1],
                        "PBAT (MW)": x_vg[:, 2],
                        "EBAT (MWh)": x_vg[:, 3],
                        "PDG (MW)": x_vg[:, 4],
                        "NPC ($/kWh)": f_vg[:, 0] / (ENL * L_mg),
                        "GHE (kg CO2/kWh)": f_vg[:, 1] / ENL,
                        "ERC (GWh/yr)": f_vg[:, 2],
                        "ENS (%)": g_vg[:, 0],
                    }
                )
        else:
            if der_flag == 1:
                c = pd.DataFrame(
                    {
                        "Gen (#)": [ii] * n_pop,
                        "PWT (MW)": x_vg[:, 0],
                        "PV (MW)": x_vg[:, 1],
                        "PBAT (MW)": 0,
                        "EBAT (MWh)": 0,
                        "PDG (MW)": x_vg[:, 2],
                        "NPC ($/kWh)": f_vg[:, 0] / (ENL * L_mg),
                        "GHE (kg CO2/kWh)": f_vg[:, 1] / ENL,
                        "ERC (GWh/yr)": f_vg[:, 2],
                        "ENS (%)": g_vg[:, 0],
                    }
                )
            else:
                c = pd.DataFrame(
                    {
                        "Gen (#)": [ii] * n_pop,
                        "PWT (MW)": x_vg[:, 0],
                        "PV (MW)": x_vg[:, 1],
                        "PBAT (MW)": x_vg[:, 2],
                        "EBAT (MWh)": x_vg[:, 3],
                        "PDG (MW)": x_vg[:, 4],
                        "NPC ($/kWh)": f_vg[:, 0] / (ENL * L_mg),
                        "GHE (kg CO2/kWh)": f_vg[:, 1] / ENL,
                        "ERC (GWh/yr)": f_vg[:, 2],
                        "ENS (%)": g_vg[:, 0],
                    }
                )

            sol_g = pd.concat([sol_g, c], ignore_index=True)

    return (sol, sol_g)
