import numpy as np
import pandas as pd


class WindTurbine:
    """Wind Turbine power production model based on the
    aerodynamic power equation with a power coefficient (Cp) approach."""

    def __init__(
        self,
        p_nominal: float,
        p_max: float,
        rotor_diameter: float,
        hub_height: float,
        v_cut_in: float,
        v_rated: float,
        v_cut_out: float,
        generator_efficiency: float = 0.96,
        air_density: float = 1.225,
        cp: float = 0.40,
        system_losses: float = 0.0,
    ):
        self.p_nominal = p_nominal
        self.p_max = p_max
        self.rotor_diameter = rotor_diameter
        self.hub_height = hub_height
        self.v_cut_in = v_cut_in
        self.v_rated = v_rated
        self.v_cut_out = v_cut_out
        self.generator_efficiency = generator_efficiency
        self.air_density = air_density
        self.cp = cp
        self.system_losses = system_losses

        self.rotor_area = np.pi * (self.rotor_diameter / 2) ** 2

    def _compute_power_output(self, wind_speed: float) -> float:
        # Compute electrical power output [W] from wind speed at hub height [m/s]

        # Cut-in / cut-out
        if wind_speed < self.v_cut_in or wind_speed >= self.v_cut_out:
            return 0.0

        # Aerodynamic wind power
        p_wind = 0.5 * self.air_density * self.rotor_area * wind_speed**3

        # Electrical power
        p_elec = self.generator_efficiency * self.cp * p_wind * (1 - self.system_losses)

        # Rated power plateau
        if wind_speed >= self.v_rated:
            p_elec = self.p_nominal

        # Hard limits
        p_elec = np.clip(p_elec, 0, self.p_max)

        return p_elec

    """Wind Turbine power production model based on a power curve approach.
    def __init__(self, power_curve_path: str):
        df = pd.read_csv(power_curve_path)

        self.wind_speeds = df["wind_speed"].values
        self.power_w = df["power_kw"].values * 1000  # kW → W

    def _compute_power_output(self, wind_speed: float) -> float:
        return float(
            np.interp(
                wind_speed,
                self.wind_speeds,
                self.power_w,
                left=0.0,
                right=0.0,
            )
        )
        """
