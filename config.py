import json


class Config:
    def __init__(self):
        with open("config.json", "r") as file:

            # SP stands for Solar Panel
            self.config_data = json.load(file)
            self.sp_config_data = self.config_data.get("solar_panel")
            self.SP_P_STC = self.sp_config_data.get("p_stc")
            self.SP_GAMMA = self.sp_config_data.get("gamma")
            self.SP_BETA = self.sp_config_data.get("beta")
            self.SP_NOCT = self.sp_config_data.get("noct")
            self.SP_L_SYST = self.sp_config_data.get("l_syst")
            self.SP_historical_data_path = self.sp_config_data.get(
                "historical_data_path"
            )

            # Site configuration
            self.site_config_data = self.config_data.get("site")
            self.SITE_LATITUDE = self.site_config_data.get("latitude")
            self.SITE_LONGITUDE = self.site_config_data.get("longitude")
