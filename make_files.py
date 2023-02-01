from calcul_equivalent import get_equivalent_data


def replace_apollo_file(thorium, u233, u235, putot, cell_length, coolant_temperature):

    with open("cell-depletion_uo2_iter.d", "r") as file:
        filedata = file.read()

    equivalent_volumic_mass, equivalent_temperature, equivalent_moderator_radius = get_equivalent_data(
        cell_length, coolant_temperature
    )
    cell_length = f"{cell_length:.1f}"
    coolant_temperature = f"{coolant_temperature:.1f}"
    equivalent_volumic_mass = f"{equivalent_volumic_mass:.6f}"
    equivalent_temperature = f"{equivalent_temperature:.6f}"
    equivalent_moderator_radius = f"{equivalent_moderator_radius:.6f}"

    output_name = f"THORIUM={thorium}__U233={u233}__U235={u235}__PUTOT={putot}__CELL_LENGTH={cell_length}__COOLANT_TEMPERATURE={coolant_temperature}__EQUIVALENT_VOLUMIC_MASS={equivalent_volumic_mass}__EQUIVALENT_TEMPERATURE={equivalent_temperature}__EQUIVALENT_MODERATOR_RADIUS={equivalent_moderator_radius}"
    filedata = filedata.replace("TYPE:CHAINE_THORIUM = 'NO';", f"TYPE:CHAINE_THORIUM = '{thorium}';")
    filedata = filedata.replace("TAB:V_U:U233   = INITABLE: 1.E-12;", f"TAB:V_U:U233   = INITABLE: {u233};")
    filedata = filedata.replace("TAB:V_U:U235   = INITABLE: 0.719;", f"TAB:V_U:U235   = INITABLE: {u235};")
    filedata = filedata.replace("TAB:V_PU:PUTOT = INITABLE: 1.E-12;", f"TAB:V_PU:PUTOT = INITABLE: {putot};")
    filedata = filedata.replace(
        "TAB:RADIUS:MODERATOR = INITABLE: 2.5655", f"TAB:RADIUS:MODERATOR = INITABLE: {equivalent_moderator_radius}"
    )
    filedata = filedata.replace("output:directory:name = 'output';", f"output:directory:name = '{output_name}';")
    filedata = filedata.replace(
        "TAB:TEMP:COOLANT = INITABLE: 87.87271554", f"TAB:TEMP:COOLANT = INITABLE: {equivalent_temperature}"
    )
    filedata = filedata.replace(
        "TAB:DENS:COOLANT = INITABLE: 1.066449039", f"TAB:DENS:COOLANT = INITABLE: {equivalent_volumic_mass}"
    )

    # Write the file out again
    with open(f"./all_files/{output_name}.d", "w") as file:
        file.write(filedata)


# Minimum should be greater than 2 * CALANDRIA_RADIUS = 13.2
cell_lengths = [14, 16, 18, 20, 22, 24, 26, 28, 28.6, 30, 32, 34, 36, 38, 40]
enrichments = ["0.719", "1.0", "2.0", "3.0", "4.0", "5.0", "7.5", "10.0", "12.5", "15.0", "17.5", "20.0"]
coolant_temperatures = [300, 305]

# Generation des fichiers
for coolant_temperature in coolant_temperatures:
    for cell_length in cell_lengths:
        for fissile in enrichments:
            replace_apollo_file("NO", "1.E-12", fissile, "1.E-12", cell_length, coolant_temperature)
            replace_apollo_file("NO", "1.E-12", "1.E-12", fissile, cell_length, coolant_temperature)
            replace_apollo_file("YES", "1.E-12", fissile, "1.E-12", cell_length, coolant_temperature)
            replace_apollo_file("YES", fissile, "1.E-12", "1.E-12", cell_length, coolant_temperature)
