# test/test_spec_big.py
# Larger low-power spec to stress-check the generator

power_spec = {
    "domains": [
        {
            "name": "AON",
            "default": True,
            "can_be_switched": False,
            "power_net": "aon_vdd",
            "ground_net": "vss",
            "voltages": ["1.0"],
            "blocks": ["top.u_pmu", "top.u_clk", "top.u_reset"],
            "shutoff_cond": None,
        },
        {
            "name": "CORE",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd_core",
            "ground_net": "vss",
            "voltages": ["1.0", "0.8", "0.0"],
            "blocks": ["top.u_core", "top.u_alu", "top.u_icache"],
            "shutoff_cond": "top.pmu.core_off_req",
        },
        {
            "name": "PERI",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd_peri",
            "ground_net": "vss",
            "voltages": ["1.8", "0.0"],
            "blocks": ["top.u_uart", "top.u_spi", "top.u_gpio"],
            "shutoff_cond": "top.pmu.peri_off_req",
        },
        {
            "name": "MEM",
            "default": False,
            "can_be_switched": True,
            "power_net": "vdd_mem",
            "ground_net": "vss",
            "voltages": ["1.0", "0.6", "0.0"],
            "blocks": ["top.u_sram0", "top.u_sram1"],
            "shutoff_cond": "top.pmu.mem_off_req",
        },
    ],

    # Chip-level power states (simple examples)
    "power_states": [
        {
            "state": "FULL_ON",
            "value": {
                "aon_vdd": "1.0",
                "vdd_core": "1.0",
                "vdd_peri": "1.8",
                "vdd_mem": "1.0",
                "vss": "0.0",
            },
        },
        {
            "state": "CORE_LPM",
            "value": {
                "aon_vdd": "1.0",
                "vdd_core": "0.8",
                "vdd_peri": "1.8",
                "vdd_mem": "1.0",
                "vss": "0.0",
            },
        },
        {
            "state": "PERI_OFF",
            "value": {
                "aon_vdd": "1.0",
                "vdd_core": "1.0",
                "vdd_peri": "0.0",
                "vdd_mem": "1.0",
                "vss": "0.0",
            },
        },
        {
            "state": "MEM_RET",
            "value": {
                "aon_vdd": "1.0",
                "vdd_core": "0.0",
                "vdd_peri": "0.0",
                "vdd_mem": "0.6",
                "vss": "0.0",
            },
        },
        {
            "state": "CHIP_OFF",
            "value": {
                "aon_vdd": "0.0",
                "vdd_core": "0.0",
                "vdd_peri": "0.0",
                "vdd_mem": "0.0",
                "vss": "0.0",
            },
        },
    ],

    # Which domain crossings need isolation
    "isolations": [
        {"from_domain": "CORE", "to_domain": "AON"},
        {"from_domain": "PERI", "to_domain": "AON"},
        {"from_domain": "MEM",  "to_domain": "AON"},
        {"from_domain": "CORE", "to_domain": "PERI"},
    ],

    # Which domain crossings need level shifters
    "level_shifters": [
        {"from_domain": "CORE", "to_domain": "AON"},
        {"from_domain": "AON",  "to_domain": "PERI"},
        {"from_domain": "CORE", "to_domain": "PERI"},
        {"from_domain": "PERI", "to_domain": "CORE"},
    ],
}
