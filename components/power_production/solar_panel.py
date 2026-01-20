import numpy as np


class SolarPanel:
    def __init__(
        self,
        p_stc: float,
        gamma: float,
        beta: float,
        noct: float,
        l_syst: float,
        albedo: float,
        surface_azimuth: float = 180,
    ):
        self.p_stc = p_stc
        self.gamma = gamma
        self.beta = np.radians(beta)
        self.noct = noct
        self.l_syst = l_syst
        self.albedo = albedo
        self.surface_azimuth = np.radians(surface_azimuth)

    def compute_power_output(
        self,
        ghi: float,
        dhi: float,
        bhi: float,
        t_amb: float,
        sza: float,
        solar_azimuth: float,
    ) -> float:
        sza_rad = np.radians(sza)
        solar_azimuth_rad = np.radians(solar_azimuth)

        cos_theta = np.cos(sza_rad) * np.cos(self.beta) + np.sin(sza_rad) * np.sin(
            self.beta
        ) * np.cos(solar_azimuth_rad - self.surface_azimuth)
        cos_theta = np.clip(cos_theta, 0, 1)

        cos_sza = np.cos(sza_rad)

        with np.errstate(divide="ignore", invalid="ignore"):
            b_mod = np.where(cos_sza > 0.05, bhi * cos_theta / cos_sza, 0)
        b_mod = np.clip(b_mod, 0, bhi * 1.5)

        d_mod = dhi * (1 + np.cos(self.beta)) / 2
        r_mod = ghi * self.albedo * (1 - np.cos(self.beta)) / 2

        gti = np.maximum(b_mod + d_mod + r_mod, 0)

        t_cell = t_amb + (self.noct - 20) / 800 * gti

        power_output = (
            self.p_stc
            * (gti / 1000)
            * (1 + self.gamma * (t_cell - 25))
            * (1 - self.l_syst)
        )

        return np.maximum(power_output, 0)
