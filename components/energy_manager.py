from power_production.power_production_manager import PowerProductionManager
from storage.storage_manager import StorageManager
import pandas as pd


class EnergyManager:
    def __init__(self, config):
        self.ppm = PowerProductionManager(config)
        self.sm = StorageManager(config)

    def simulate(self, df: pd.DataFrame, load_kw: float):
        df["pv_power_kw"] = self.ppm.compute_power_timeseries(df)

        dt_hours = (df.index[1] - df.index[0]).total_seconds() / 3600

        soc_list = []
        battery_power_list = []

        for p in df["pv_power_kw"]:
            surplus = p - load_kw
            b_power = self.sm.step(surplus, dt_hours)

            soc_list.append(self.sm.get_soc())
            battery_power_list.append(b_power)

        df["battery_power_kw"] = battery_power_list
        df["battery_soc"] = soc_list

        return df
