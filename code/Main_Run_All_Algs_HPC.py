"""
The Multi-objective main code for MG optimization using BLAST_lite

"""

import pandas as pd
import numpy as np
import os

from input_data.MG_Input_Data import L_mg

from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning

from algorithm import *

import warnings

from problem import MyProblem, MyProblem_noBAT

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)


from utils import get_parser

parser = get_parser()
args = parser.parse_args()

alg_flag = args.alg_flag  # Algorithm flag: a number between 1 and 6
seed_no = args.seed_no  # seed number to be used
n_pop = args.n_pop  # population size
n_eval = args.n_eval  # number of function evaluations
der_flag = args.der_flag  # whether battery is used or not

df = pd.read_csv("input_data//RES_Power_hourly.csv")

t1 = pd.to_datetime(df.loc[0, "timestamp"])
t2 = pd.to_datetime(df.loc[1, "timestamp"])

DT = pd.Timedelta(t2 - t1).seconds / 3600
PL = np.ceil(df["PD"].max())
ENL = DT * df["PD"].sum() / 1e3  ## Total annual load energy GWh/yr

seed_vect = [
    4,
    34,
    42,
    76,
    87,
    121,
    146,
    170,
    200,
    240,
    270,
    319,
    344,
    542,
    617,
    625,
    706,
    814,
    938,
    1281,
    1748,
    1846,
    2206,
    3065,
    3383,
    3742,
    7253,
    12697,
    13391,
    15760,
    128765,
]

RESULTS_DIR = "./Results/"
RESULTS_DIR_BAT = "./Results_BAT/"

VERBOSE = False
SAVE_HISTORY = True

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR_BAT, exist_ok=True)

problem = (
    MyProblem_noBAT(PL, ENL, df, DT) if der_flag == 1 else MyProblem(PL, ENL, df, DT)
)

params = (
    n_pop,
    n_eval,
    der_flag,
    seed_vect[seed_no],
    ENL,
    L_mg,
    problem,
)
kwargs = {"verbose": VERBOSE, "save_history": SAVE_HISTORY}

# NSGAII: 1, AGE-MOEA: 2, SMS-EMOA: 3, AGE-MOEA2: 4, NSGA-III: 5, UNSGAIII: 6, C-TAEA: 7

match alg_flag:
    case 1:
        name = "NSGA-II"
        print(f"Running {name}")

        Solution = NSGAII_run(*params, **kwargs)
    case 2:
        name = "AGE-MOEA"
        print(f"Running {name}")
        Solution = AGEMOEA_runSolution = AGEMOEA_run(*params, **kwargs)
    case 3:
        name = "SMS-EMOA"
        print(f"Running {name}")
        Solution = SMSEMOA_runSolution = SMSEMOA_run(*params, **kwargs)
    case 4:
        name = "AGE-MOEA2"
        print(f"Running {name}")
        Solution = AGEMOEA2_runSolution = AGEMOEA2_run(*params, **kwargs)
    case 5:
        name = "NSGA-III"
        print(f"Running {name}")
        Solution = NSGA3_runSolution = NSGA3_run(*params, **kwargs)
    case 6:
        name = "UNSGA-III"
        print(f"Running {name}")
        Solution = UNSGA3_runSolution = UNSGA3_run(*params, **kwargs)
    case 7:
        name = "C-TAEA"
        print(f"Running {name}")
        Solution = CTAEA_runSolution = CTAEA_run(*params, **kwargs)
    case _:
        print("Invalid Algorithm Flag")

pareto_sol = Solution[0]
gen_sol = Solution[1]

pareto_sol_path = f"{RESULTS_DIR if der_flag == 1 else RESULTS_DIR_BAT}Pareto_{name}_{"no" if der_flag == 1 else ""}BAT_seedno_{seed_no}.csv"
gen_sol_path = f"{RESULTS_DIR if der_flag == 1 else RESULTS_DIR_BAT}AllPop_{name}_{"no" if der_flag == 1 else ""}BAT_seedno_{seed_no}.csv"

pareto_sol.to_csv(pareto_sol_path)
gen_sol.to_csv(gen_sol_path)

print(f"Results saved to {pareto_sol_path} and {gen_sol_path}")
