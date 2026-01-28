from components.storage.battery import Battery
from config import Config


class StorageManager:
    def __init__(self, config: Config):
        self.config = config

        self.battery = Battery(
            capacity_kwh=self.config.BAT_CAPACITY,
            soc_init=self.config.BAT_SOC_INIT,
            soc_min=self.config.BAT_SOC_MIN,
            soc_max=self.config.BAT_SOC_MAX,
            p_charge_nominal_kw=self.config.BAT_P_CHARGE_NOMINAL,
            p_discharge_nominal_kw=self.config.BAT_P_DISCHARGE_NOMINAL,
            p_charge_max_kw=self.config.BAT_P_CHARGE_MAX,
            p_discharge_max_kw=self.config.BAT_P_DISCHARGE_MAX,
            eta_charge=self.config.BAT_ETA_CHARGE,
            eta_discharge=self.config.BAT_ETA_DISCHARGE,
        )

    def step(self, surplus_power_kw: float, dt_hours: float) -> float:
        """
        Gère la batterie pour un pas de temps.
        Retourne la puissance batterie réellement utilisée.
        """
        return self.battery.step(surplus_power_kw, dt_hours)

    def get_soc(self) -> float:
        return self.battery.soc
