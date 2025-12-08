
# MOEA-MiningMicrogrids


This repository contain code on "Optimal Planning of Renewable-Based Mining Microgrids: A Comparative Study of Multi-Objective Evolutionary Algorithms". The main directory include the code, results and the manuscript of the following paper.

  

## Python Virtual Environment Setup
It is highly recommended to use a Python virtual environment (`venv`) to **avoid conflicts with existing libraries**.

### 1. Create a virtual environment

Run the following command in your project folder:

```bash
$ py -m venv your_venv_name

```

### 2. Activate the virtual environment

**Windows:**

```bash
$ your_venv_name\Scripts\activate

```

**Linux / macOS:**

```bash
$ source your_venv_name/bin/activate

```

### 3. Install dependencies

Navigate to the folder containing `requirements.txt` and run:

```bash
$ pip install -r requirements.txt

```

### 4. Updating dependencies

If you add new libraries to the project, first install them in your virtual environment:

```bash
$ pip install <library_name>

```

Then update `requirements.txt`:

```bash
$ pip freeze > requirements.txt

```

## Tip

Always activate your virtual environment before running scripts or installing new packages to ensure all dependencies are correctly isolated.

## Usage

  

Main_Run_All_Algs_HPC.py". It takes 5 input variables as follows.

  

* `--n_pop`: population size for MOEA

* `--n_eval`: number of function evaluation

* `--seed_no`: Seed number, int number between 0 and 30, pre-assigned for our experiments.

* `--der_flag`: DER combination flag, 1 for no battery (DG+RES) else battery case (DG+RES+LI).

* `--alg_flag`: Algorithm flag, int number between 1 and 6, these algorithms are from Pymoo.

  

> DER (Distributed Energy Resources) , DG (Distributed Generation) , RES (Renewable Energy Sources), Li (Lithium-ion Battery)

Example:

```

py Main_Run_All_Algs_HPC.py --alg_flag=1 --seed_no=0 --n_pop=100 --n_eval=10000 --der_flag=1

```

## Results

The results can be found on [Figshare](https://figshare.com/articles/dataset/Results/27347496) with the identifier 10.25909/27347496 .

- Gen: generation index
- PWT (MW): Wind Turbine Installed Power Capacity (in megawatts)
- PV (MW): Photovoltaic Installed Power Capacity (in megawatts)
- PBAT (MW): Battery Power Capacity (in megawatts)
- EBAT (MWh): Battery Energy Capacity (in megawatt-hours)
- PDG (MW): Diesel Generator Installed Power Capacity (in megawatts)
- NPC ($/kWh): Net Present Cost per Delivered Energy Unit
- GHE (kg CO2/kWh): Greenhouse Gas Emissions per kWh Delivered
- ERC (GWh/yr): Energy Renewable Curtailment per Year (in gigawatt-hours per year).
Amount of potential renewable energy (PV + wind) that could not be used or stored and was therefore wasted.
- ENS (%):Energy-Not-Served Ratio (percentage). Reliability indicator: percentage of load demand that is not met during the year.
    - ENS = 0 % → perfect reliability
    - ENS > 0 % → there are shortages or blackouts


## License

  

[MIT](https://choosealicense.com/licenses/mit/)