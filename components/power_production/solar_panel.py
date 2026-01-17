import numpy as np


class SolarPanel:
    def __init__(self, p_stc, gamma, beta, noct, l_syst, albedo):
        self.p_stc = p_stc
        self.gamma = gamma
        self.beta = beta
        self.noct = noct
        self.l_syst = l_syst
        self.p_stc = p_stc
        self.albedo = albedo

    def _compute_bmod(self, bhi, sza, azimuth_sol):
        cos_theta = np.cos(sza) * np.cos(self.beta) + np.sin(sza) * np.sin(
            self.beta
        ) * np.cos(azimuth_sol - 180)
        return bhi * cos_theta / np.cos(sza)

    def _compute_dmod(self, dhi):
        return dhi * (1 + np.cos(self.beta)) / 2

    def _compute_rmod(self, ghi):
        return ghi * self.albedo * (1 - np.cos(self.beta)) / 2

    def _compute_gti(self, ghi, dhi, bhi, sza, azimuth_sol):
        dmod = self._compute_dmod(dhi)
        rmod = self._compute_rmod(ghi)
        bmod = self._compute_bmod(bhi, sza, azimuth_sol)
        return bmod + dmod + rmod

    def _compute_tcell(self, t_amb, gti):
        return t_amb + (self.noct - 20) / 800 * gti

    def _compute_power_output(self, ghi, dhi, bhi, t_amb, sza, azimuth_sol):
        gti = self._compute_gti(ghi, dhi, bhi, sza, azimuth_sol)
        tcell = self._compute_tcell(t_amb, gti)
        p_out = (
            self.p_stc
            * (gti / 1000)
            * (1 + self.gamma * (tcell - 25))
            * (1 - self.l_syst)
        )
        return p_out
