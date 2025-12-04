
# =========================
#  State Machine simplă
# =========================
def state_machine(row):
    """
    Decide culoarea semaforului pe baza datelor.
    """
    if row["vehicul_urgenta"]:
        return "PRIORITY_GREEN"   # vehicul de urgență are prioritate
    elif row["numar_pietoni"] > 15:
        return "PEDESTRIAN_GREEN" # mulți pietoni → verde pietoni
    elif row["numar_vehicule"] > 20:
        return "VEHICLE_GREEN"    # trafic intens → verde vehicule
    else:
        return "RED"              # default → roșu
