# lp_spec_model.py

power_spec = {
    "domains": [
        {
            "name": "AON",
            "default": True,
            "can_be_switched": False,
            "power_net": "aon_vdd",
            "ground_net": "vss",
            "voltages": ["1.0"],
            "blocks": ["top.u_pmu", "top.u_clk"],
            "shutoff_cond": None,
        },
        {
            "name": "DMN1",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd1",
            "ground_net": "vss",
            "voltages": ["1.0", "0.0"],
            "blocks": ["top.u_blk1", "top.u_blk2"],
            "shutoff_cond": "top.pmu.dmn1_off_req",
        },
        {
            "name": "DMN2",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd2",
            "ground_net": "vss",
            "voltages": ["1.5", "0.0"],
            "blocks": ["top.u_blk3", "top.u_blk4"],
            "shutoff_cond": "top.pmu.dmn2_off_req",
        },
    ],
    "power_states": [
        {
            "state": "on",
            "value": {"aon_vdd": "1.0", "vdd1": "1.0", "vdd2": "1.5", "vss": "0.0"},
        },
        {
            "state": "dmn1_off",
            "value": {"aon_vdd": "1.0", "vdd1": "0.0", "vdd2": "1.5", "vss": "0.0"},
        },
        {
            "state": "dmn2_off",
            "value": {"aon_vdd": "1.0", "vdd1": "1.0", "vdd2": "0.0", "vss": "0.0"},
        },
    ],
    "isolations": [
        {"from_domain": "DMN1", "to_domain": "AON"},
        {"from_domain": "DMN2", "to_domain": "AON"},
    ],
    "level_shifters": [
        {"from_domain": "DMN2", "to_domain": "AON"},
    ],
}
