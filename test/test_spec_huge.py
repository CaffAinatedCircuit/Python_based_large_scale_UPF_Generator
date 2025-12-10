# test/test_spec_huge.py
# Programmatically build a very large random-style power spec

import random

random.seed(42)  # deterministic for debugging

NUM_DOMAINS = 200
NUM_STATES  = 100

def make_domains():
    domains = []
    for i in range(NUM_DOMAINS):
        name = f"DMN{i}"
        default = (i == 0)
        can_sw = (i != 0)
        power_net = f"vdd{i}"
        ground_net = "vss"
        voltages = ["1.0", "0.0"]
        blocks = [f"top.u_blk{i}_{j}" for j in range(5)]
        shutoff = None if not can_sw else f"top.pmu.{name.lower()}_off_req"
        domains.append(
            {
                "name": name,
                "default": default,
                "can_be_switched": can_sw,
                "power_net": power_net,
                "ground_net": ground_net,
                "voltages": voltages,
                "blocks": blocks,
                "shutoff_cond": shutoff,
            }
        )
    return domains

def make_states(domains):
    states = []
    nets = [d["power_net"] for d in domains] + ["vss"]
    for s in range(NUM_STATES):
        state_name = f"STATE_{s}"
        vals = {}
        for net in nets:
            if net == "vss":
                vals[net] = "0.0"
            else:
                vals[net] = random.choice(["1.0", "0.0"])
        states.append({"state": state_name, "value": vals})
    return states

def make_crossings(domains):
    isolations = []
    level_shifters = []
    names = [d["name"] for d in domains]
    for _ in range(NUM_DOMAINS * 3):
        a, b = random.sample(names, 2)
        isolations.append({"from_domain": a, "to_domain": b})
    for _ in range(NUM_DOMAINS * 3):
        a, b = random.sample(names, 2)
        level_shifters.append({"from_domain": a, "to_domain": b})
    return isolations, level_shifters

_domains = make_domains()
_states  = make_states(_domains)
_isos, _ls = make_crossings(_domains)

power_spec = {
    "domains": _domains,
    "power_states": _states,
    "isolations": _isos,
    "level_shifters": _ls,
}
