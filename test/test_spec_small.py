# lp_spec_model.py  (test version)

power_spec = {
    "domains": [
        {
            "name": "AON",
            "default": True,
            "can_be_switched": False,
            "power_net": "aon_vdd",
            "ground_net": "vss",
            "voltages": ["1.0"],
            "blocks": ["top.u_pmu"],
            "shutoff_cond": None,
        },
        {
            "name": "DMN1",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd1",
            "ground_net": "vss",
            "voltages": ["1.0", "0.0"],
            "blocks": ["top.u_blk1"],
            "shutoff_cond": "top.pmu.dmn1_off_req",
        },
    ],
    "power_states": [
        {"state": "on",
         "value": {"aon_vdd": "1.0", "vdd1": "1.0", "vss": "0.0"}},
        {"state": "dmn1_off",
         "value": {"aon_vdd": "1.0", "vdd1": "0.0", "vss": "0.0"}},
    ],
    "isolations": [
        {"from_domain": "DMN1", "to_domain": "AON"},
    ],
    "level_shifters": [],
}
