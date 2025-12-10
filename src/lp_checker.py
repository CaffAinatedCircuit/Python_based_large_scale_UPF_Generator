# lp_checker.py
from src.lp_spec_model import power_spec

class SpecError(Exception):
    pass

def check_domains(domains):
    seen_names = set()
    default_count = 0

    for d in domains:
        name = d["name"]

        # Unique domain names
        if name in seen_names:
            raise SpecError(f"Duplicate domain name: {name}")
        seen_names.add(name)

        # Count defaults
        if d.get("default"):
            default_count += 1

        # Basic fields present
        for key in ["power_net", "ground_net", "voltages"]:
            if key not in d or not d[key]:
                raise SpecError(f"Domain {name} missing '{key}'")

        # If switchable, must have shutoff condition
        if (not d.get("default", False)
                and d.get("can_be_switched", False)
                and not d.get("shutoff_cond")):
            raise SpecError(
                f"No shut-off condition specified for switched domain {name}"
            )

    if default_count == 0:
        raise SpecError("No default domain specified")
    if default_count > 1:
        raise SpecError("More than one default domain specified")

def check_power_states(power_states, domains):
    # Build set of all power nets from domains
    nets = {d["power_net"] for d in domains}
    nets.add(domains[0]["ground_net"])  # assume common ground name for simplicity

    for ps in power_states:
        state_name = ps["state"]
        values = ps["value"]

        # All nets must be covered in each state
        missing = nets - set(values.keys())
        if missing:
            raise SpecError(
                f"Power state '{state_name}' missing values for nets: {sorted(missing)}"
            )

        # Voltage strings must be non-empty
        for net, val in values.items():
            if val is None or val == "":
                raise SpecError(
                    f"Empty voltage value in state '{state_name}' for net {net}"
                )

def check_crossings(spec):
    domain_names = {d["name"] for d in spec["domains"]}

    for iso in spec.get("isolations", []):
        if iso["from_domain"] not in domain_names:
            raise SpecError(f"Isolation 'from_domain' unknown: {iso['from_domain']}")
        if iso["to_domain"] not in domain_names:
            raise SpecError(f"Isolation 'to_domain' unknown: {iso['to_domain']}")

    for ls in spec.get("level_shifters", []):
        if ls["from_domain"] not in domain_names:
            raise SpecError(f"LS 'from_domain' unknown: {ls['from_domain']}")
        if ls["to_domain"] not in domain_names:
            raise SpecError(f"LS 'to_domain' unknown: {ls['to_domain']}")

def run_all_checks(spec):
    check_domains(spec["domains"])
    check_power_states(spec["power_states"], spec["domains"])
    check_crossings(spec)
    print("INFO: Low-power specification passed all checks.")

if __name__ == "__main__":
    try:
        run_all_checks(power_spec)
    except SpecError as e:
        print("ERROR:", e)
        raise SystemExit(1)
