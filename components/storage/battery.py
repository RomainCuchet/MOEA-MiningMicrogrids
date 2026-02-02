class Battery:
    def __init__(
        self,
        capacity_kwh: float,
        soc_init: float,
        soc_min: float,
        soc_max: float,
        p_charge_nominal_kw: float,
        p_discharge_nominal_kw: float,
        p_charge_max_kw: float,
        p_discharge_max_kw: float,
        eta_charge: float,
        eta_discharge: float,
    ):
        self.capacity = capacity_kwh
        self.soc = soc_init

        self.soc_min = soc_min
        self.soc_max = soc_max

        self.p_charge_nominal = p_charge_nominal_kw
        self.p_discharge_nominal = p_discharge_nominal_kw

        self.p_charge_max = p_charge_max_kw
        self.p_discharge_max = p_discharge_max_kw

        self.eta_charge = eta_charge
        self.eta_discharge = eta_discharge

    def step(self, surplus_power_kw: float, dt_hours: float) -> float:
        """
        surplus_power_kw > 0  -> charge
        surplus_power_kw < 0  -> discharge

        Returns battery power (kW) actually used.
        """

        if surplus_power_kw > 0:
            # CHARGE
            power = min(surplus_power_kw, self.p_charge_max)
            energy = power * dt_hours * self.eta_charge

            max_storable = (self.soc_max - self.soc) * self.capacity
            energy = min(energy, max_storable)

            self.soc += energy / self.capacity
            return energy / dt_hours

        else:
            # DISCHARGE
            power = min(-surplus_power_kw, self.p_discharge_max)
            energy = power * dt_hours / self.eta_discharge

            max_available = (self.soc - self.soc_min) * self.capacity
            energy = min(energy, max_available)

            self.soc -= energy / self.capacity
            return -energy / dt_hours
