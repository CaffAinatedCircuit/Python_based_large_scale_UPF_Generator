# lp_upf_gen.py
from src.lp_spec_model import power_spec
from src.lp_checker import run_all_checks

OUT_UPF = "auto_low_power_intent.upf"

def gen_upf(spec, out_path):
    doms = spec["domains"]
    states = spec["power_states"]

    lines = []
    lines.append("# Auto-generated low-power UPF (intent)")

    # Create domains and supply sets
    for d in doms:
        name = d["name"]
        pnet = d["power_net"]
        gnet = d["ground_net"]
        blocks = " ".join(d.get("blocks", []))

        lines.append(f"\n# Domain {name}")
        lines.append(f"create_power_domain {name} -elements {{{blocks}}}")
        lines.append(f"create_supply_net {pnet}")
        lines.append(f"create_supply_net {gnet}")
        lines.append(f"create_supply_set SS_{name} -primary {{{pnet} {gnet}}}")
        lines.append(
            f"set_domain_supply_net {name} "
            f"-primary_power_net {pnet} -primary_ground_net {gnet}"
        )

        # Optional: mark default domain via comment or attribute
        if d.get("default"):
            lines.append(f"# {name} is default domain")

        # If switchable, note shutoff condition
        if d.get("can_be_switched"):
            lines.append(
                f"# Shut-off condition for {name}: {d.get('shutoff_cond', '<missing>')}"
            )

    # Build unified PST
    all_nets = sorted({d["power_net"] for d in doms} | {doms[0]["ground_net"]})
    lines.append("\n# Chip-level Power State Table")
    lines.append(f"create_pst PST_CHIP -supplies {{{' '.join(all_nets)}}}")

    for ps in states:
        state = ps["state"]
        values = ps["value"]
        value_str = " ".join(f"{net} {val}" for net, val in values.items())
        lines.append(
            f"add_pst_state {state} -pst PST_CHIP -state {{{value_str}}}"
        )

    # Generic isolation / LS strategies using domain names
    lines.append("\n# Isolation strategies")
    for iso in spec.get("isolations", []):
        from_d = iso["from_domain"]
        to_d = iso["to_domain"]
        iso_name = f"ISO_{from_d}_TO_{to_d}"
        lines.append(
            f"set_isolation {iso_name} "
            f"-domain {from_d} "
            f"-applies_to outputs "
            f"-isolation_signal <FILL_ME_{from_d}_ISO_SIG> "
            f"-isolation_sense low "
            f"-clamp_value 0 "
            f"-location parent"
        )

    lines.append("\n# Level shifter strategies")
    for ls in spec.get("level_shifters", []):
        from_d = ls["from_domain"]
        to_d = ls["to_domain"]
        ls_name = f"LS_{from_d}_TO_{to_d}"
        lines.append(
            f"set_level_shifter_strategy {ls_name} "
            f"-from {from_d} -to {to_d} "
            f"-ls_type both "
            f"-location parent"
        )

    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"INFO: Wrote UPF to {out_path}")

if __name__ == "__main__":
    run_all_checks(power_spec)
    gen_upf(power_spec, OUT_UPF)
