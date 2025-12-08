from pymoo.algorithms.moo.sms import SMSEMOA
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.age2 import AGEMOEA2
from pymoo.algorithms.moo.ctaea import CTAEA
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from utils import res_2_dataframe


def NSGAII_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    algorithm = NSGA2(pop_size=n_pop)
    termination = get_termination("n_eval", n_eval)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def AGEMOEA_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    algorithm = AGEMOEA(pop_size=n_pop)
    termination = get_termination("n_eval", n_eval)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def SMSEMOA_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    algorithm = SMSEMOA(pop_size=n_pop)
    termination = get_termination("n_eval", n_eval)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def AGEMOEA2_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    algorithm = AGEMOEA2(pop_size=n_pop)
    termination = get_termination("n_eval", n_eval)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def CTAEA_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    termination = get_termination("n_eval", n_eval)
    ref_dirs = get_reference_directions(
        "das-dennis", problem.n_obj, n_partitions=n_pop, n_points=n_pop
    )
    algorithm = CTAEA(ref_dirs=ref_dirs)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def NSGA3_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    termination = get_termination("n_eval", n_eval)

    ref_dirs = get_reference_directions("energy", problem.n_obj, n_points=n_pop)
    algorithm = NSGA3(ref_dirs=ref_dirs, pop_size=n_pop)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol


def UNSGA3_run(
    n_pop,
    n_eval,
    der_flag,
    seed_no,
    ENL,
    L_mg,
    problem,
    verbose=False,
    save_history=True,
):
    termination = get_termination("n_eval", n_eval)

    ref_dirs = get_reference_directions("energy", problem.n_obj, n_points=n_pop)
    algorithm = UNSGA3(ref_dirs=ref_dirs, pop_size=n_pop)

    res = minimize(
        problem,
        algorithm,
        termination,
        verbose=verbose,
        save_history=save_history,
        seed=seed_no,
    )

    sol = res_2_dataframe(res=res, ENL=ENL, L_mg=L_mg, der_flag=der_flag, n_pop=n_pop)

    return sol
