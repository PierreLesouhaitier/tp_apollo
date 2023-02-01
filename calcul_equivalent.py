import math

# All length are in centimeters
FUEL_RADIUS = 0.614
CLADDING_RADIUS = 0.654

NUMBER_RODS = 37
CALANDRIA_RADIUS = 6.6
COOLANT_RADIUS = 5.17

# Moderator
MODERATOR_TEMPERATURE = 80
MODERATOR_TEMPERATURE_K = MODERATOR_TEMPERATURE + 273.16
MODERATOR_VOLUMIC_MASS = 1.0782

# Valeur intermediaire
FUEL_SURFACE = NUMBER_RODS * math.pi * FUEL_RADIUS**2
COOLANT_SURFACE = math.pi * (COOLANT_RADIUS**2 - NUMBER_RODS * CLADDING_RADIUS**2)


# Coolant pressure is supposed to be 11 MPa
def get_coolant_volumic_mass(coolant_temperature, is_empty):
    if is_empty:
        return 0

    if coolant_temperature == 300:
        return 0.79041
    elif coolant_temperature == 305:
        return 0.77718
    else:
        raise "Not allowed coolant temperature."


def get_equivalent_data(cell_length, coolant_temperature, is_empty=False):
    coolant_temperature_K = coolant_temperature + 273.16
    coolant_volumic_mass = get_coolant_volumic_mass(coolant_temperature, is_empty)

    total_surface = cell_length**2
    moderator_surface = total_surface - math.pi * CALANDRIA_RADIUS**2

    volumic_mass = (moderator_surface * MODERATOR_VOLUMIC_MASS + COOLANT_SURFACE * coolant_volumic_mass) / (
        moderator_surface + COOLANT_SURFACE
    )
    temperature = (
        moderator_surface * MODERATOR_VOLUMIC_MASS * MODERATOR_TEMPERATURE_K
        + COOLANT_SURFACE * coolant_volumic_mass * coolant_temperature_K
    ) / (moderator_surface * MODERATOR_VOLUMIC_MASS + COOLANT_SURFACE * coolant_volumic_mass) - 273.16
    moderation_ratio = (COOLANT_SURFACE + moderator_surface) / FUEL_SURFACE
    equivalent_moderator_radius = math.sqrt(moderation_ratio * FUEL_RADIUS**2 + CLADDING_RADIUS**2)

    return volumic_mass, temperature, equivalent_moderator_radius


if __name__ == "__main__":
    initial_cell_length = 28.6
    minimum_cell_length = CALANDRIA_RADIUS * 2  # cannot be less than 2 * CALANDRIA_RADIUS
    initial_temperature = 300
    print(get_equivalent_data(initial_cell_length, initial_temperature, is_empty=False))
    # Should return (1.0644196780570827, 87.82250549484638, 2.5655390588023335)
