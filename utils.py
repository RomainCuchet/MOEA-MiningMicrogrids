import pvlib


def compute_solar_azimuth_zenith(latitude, longitude, times):
    site = pvlib.location.Location(latitude, longitude)
    solar_position = site.get_solarposition(times)
    return solar_position["azimuth"], solar_position["zenith"]
