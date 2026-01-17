from components.power_production.solar_panel import SolarPanel
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

    def compute_solar_panel_power(self, ghi, dhi, bhi, t_amb, sza, azimuth):

        solar_panel = SolarPanel(
            p_stc=self.config.SP_P_STC,
            gamma=self.config.SP_GAMMA,
            beta=self.config.SP_BETA,
            noct=self.config.SP_NOCT,
            l_syst=self.config.SP_L_SYST,
            albedo=0.2,
        )
        power_output = solar_panel._compute_power_output(
            ghi, dhi, bhi, t_amb, sza, azimuth
        )
        return power_output

    def simmulate_historical_power_production(
        self, start_time: pd.Timestamp, end_time: pd.Timestamp
    ):
        df = pd.read_csv(self.config.SP_historical_data_path)
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        df = df[(df.index >= start_time) & (df.index <= end_time)]
        df["sp_power"] = self.compute_solar_panel_power(
            df["GHI"],
            df["DHI"],
            df["BHI"],
            df["T"],
            df["sza"],
            compute_solar_azimuth_zenith(
                self.config.SITE_LATITUDE, self.config.SITE_LONGITUDE, df.index
            )[0],
        )
        return df
