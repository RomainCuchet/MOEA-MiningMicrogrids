import numpy as np
from pymoo.core.problem import ElementwiseProblem
from SB_My_Fun import MG_Model_rulebased
import pandas as pd


def get_Results_Run(df, DT, P_WT, P_PV, P_bat, E_bat, P_FF):

    MG_Object = MG_Model_rulebased(
        df=df, DT=DT, P_WT=P_WT, P_PV=P_PV, P_bat=P_bat, E_bat=E_bat, P_FF=P_FF
    )

    output = dict()
    output = {"ENS": 0, "ERC": 0, "NPC": 0, "GHE": 0}

    if P_bat == 0:

        Res_MG = MG_Object.get_Result_noBat()  # Scheduling problem for noBAT case
        output["NPC"] = round(Res_MG[0], 4)  ## NPC for DG+Li Million AUD
        output["ERC"] = round(Res_MG[1], 4)  ## RES Curtailment in GWh/yr
        output["ENS"] = round(Res_MG[2], 0)  ## ENergy not served in GWh/yr
        output["GHE"] = round(Res_MG[3], 4)  ## kton/yr CO2-e from DG

    else:

        Res_MG = (
            MG_Object.get_Result_MG_rulebased_Li_BLAST()
        )  # Scheduling problem for Li+DG with BLAST

        output["NPC"] = round(Res_MG[0], 4)  ## NPC for DG+Li Million AUD
        output["ERC"] = round(Res_MG[1], 4)  ## RES Curtailment in GWh/yr
        output["ENS"] = round(Res_MG[2], 0)  ## ENergy not served in GWh/yr
        output["GHE"] = round(Res_MG[3], 4)  ## kton/yr CO2-e from DG

    return output


class MyProblem(ElementwiseProblem):

    def __init__(self, PL, ENL, df, DT):

        super().__init__(
            n_var=5,
            n_obj=3,
            n_ieq_constr=3,
            xl=np.array([0, 0, 0, 0, 0]),
            xu=np.array([3 * PL, 3 * PL, 3 * PL, 3 * PL, PL]),
        )

        self.df = df
        self.DT = DT
        self.ENL = ENL

    def _evaluate(self, x, out, *args, **kwargs):
        P_WT = x[0]
        P_PV = x[1]
        P_bat = x[2]
        E_bat = x[3]
        P_FF = x[4]

        RES = get_Results_Run(self.df, self.DT, P_WT, P_PV, P_bat, E_bat, P_FF)

        g1 = x[3] - 4 * x[2]
        g2 = 0.5 * x[2] - x[3]
        g3 = RES["ENS"] / self.ENL - 0.0  ## ENS should be less than 5%
        # out["F"] = [RES['NPC'], RES['ERC'], RES['ENS'], RES['GHE']]
        out["F"] = [RES["NPC"], RES["GHE"], RES["ERC"]]
        out["G"] = [g3, g2, g1]


class MyProblem_noBAT(ElementwiseProblem):

    def __init__(self, PL, ENL, df, DT):

        super().__init__(
            n_var=3,
            n_obj=3,
            n_ieq_constr=1,
            xl=np.array([0, 0, 0]),
            xu=np.array([3 * PL, 3 * PL, PL]),
        )
        self.df = df
        self.DT = DT
        self.ENL = ENL

    def _evaluate(self, x, out, *args, **kwargs):
        P_WT = x[0]
        P_PV = x[1]
        P_FF = x[2]

        RES = get_Results_Run(self.df, self.DT, P_WT, P_PV, 0, 0, P_FF)

        g3 = RES["ENS"] / self.ENL - 0.0  ## ENS should be less than 0%
        # out["F"] = [RES['NPC'], RES['ERC'], RES['ENS'], RES['GHE']]
        out["F"] = [RES["NPC"], RES["GHE"], RES["ERC"]]
        out["G"] = [g3]
