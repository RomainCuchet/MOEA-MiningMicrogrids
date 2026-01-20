from components.power_production.solar_panel import SolarPanel
from components.power_production.wind_turbine import WindTurbine

from config import Config
import pandas as pd
from utils import compute_solar_azimuth_zenith


class PowerProductionManager:
    def __init__(self, config: Config):
        self.config = config
        self.solar_panel = SolarPanel(
            p_stc=self.config.SP_P_STC,
            gamma=self.config.SP_GAMMA,
            beta=self.config.SP_BETA,
            noct=self.config.SP_NOCT,
            l_syst=self.config.SP_L_SYST,
            albedo=0.2,
        )

        self.wind_turbine = WindTurbine(
            p_nominal=self.config.WT_P_NOMINAL,
            p_max=self.config.WT_P_MAX,
            rotor_diameter=self.config.WT_ROTOR_DIAMETER,
            hub_height=self.config.WT_HUB_HEIGHT,
            v_cut_in=self.config.WT_V_CUT_IN,
            v_rated=self.config.WT_V_RATED,
            v_cut_out=self.config.WT_V_CUT_OUT,
            generator_efficiency=self.config.WT_GENERATOR_EFFICIENCY,
            air_density=self.config.WT_AIR_DENSITY,
            cp=self.config.WT_CP,
            system_losses=self.config.WT_SYSTEM_LOSSES,
        )

    def simulate_historical_power_production(
        self, start_time: pd.Timestamp, end_time: pd.Timestamp
    ):
        df = pd.read_csv(self.config.SP_historical_data_path)
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        df = df[(df.index >= start_time) & (df.index <= end_time)]

        solar_azimuth, sza = compute_solar_azimuth_zenith(
            self.config.SITE_LATITUDE, self.config.SITE_LONGITUDE, df.index
        )

        # TODO: veryfy that sza from utils and from df are the same to validate the library

        df["sp_power"] = self.solar_panel.compute_power_output(
            df["GHI"],
            df["DHI"],
            df["BHI"],
            df["T"],
            df["sza"],
            solar_azimuth,
        )
        return df

    def simulate_historical_wind_power_production(
        self, start_time: pd.Timestamp, end_time: pd.Timestamp
    ):
        df = pd.read_csv(self.config.WT_historical_data_path)
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        df = df[(df.index >= start_time) & (df.index <= end_time)]

        df["wt_power"] = df["wind_speed"].apply(self.wind_turbine.compute_power_output)

        return df
