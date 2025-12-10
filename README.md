## Project overview

This project demonstrates how to:

- Capture low‑power intent (domains, power states, crossings) in a high‑level Python spec.
- Check the spec for common errors (missing shutoff, incomplete state tables, invalid crossings).
- Auto‑generate UPF‑style Tcl for different test designs (small, big, random/huge).
- Reuse Tcl procedures for isolation, level shifters, and retention rules at block and chip level.

It is inspired by industry low‑power automation and DVCon papers on template‑driven UPF generation and verification flows, but all code here is original and simplified for training use.

---

## Directory structure

```text
project_root/
  src/
    lp_spec_model.py   # Example power_spec definition (can be a reference)
    lp_checker.py      # Generic checks on the spec
    lp_upf_gen.py      # UPF generator from the spec
    lp_rules.tcl       # Reusable Tcl procs for isolation/LS/retention
  test/
    test_spec_small.py # Minimal test design
    test_spec_big.py   # Larger SoC-style design
    test_spec_huge.py  # Random large stress test
  main.py              # Test runner: runs checks + generates UPF for all tests
  README.md            # This file

```
One can add more `test/test_*.py` files as new “questions” or training exercises.

---

## src/ components

## lp_spec_model.py

- Contains a `power_spec` Python dictionary describing:
    
    - `domains`: name, default flag, switchable flag, power/ground nets, voltages, blocks, and shutoff condition.
    - `power_states`: named chip‑level states with net→voltage mappings.
    - `isolations`: domain‑to‑domain isolation pairs.
    - `level_shifters`: domain‑to‑domain level shifter pairs.
- Mirrors the idea of a high‑level spec from which a power format file can be auto‑generated, without directly editing UPF.

This file can serve as a template for new specs, but the real test specs live in `test/`.

## lp_checker.py

- Imports a `power_spec` and performs generic validation:
    - Ensures domain names are unique.
    - Checks there is exactly one default domain.
    - For each non‑default, switchable domain, verifies that a shutoff condition is specified.
    - Confirms each power state provides values for all supply nets (including ground).
    - Verifies `isolations` and `level_shifters` refer to existing domain names.
    
- Exposes `run_all_checks(spec)` which raises a custom `SpecError` on problems.
This is the automation layer that catches specification errors early, before running tools.

## lp_upf_gen.py

- Also imports a `power_spec` and assumes it already passed `run_all_checks`.
- Generates a vendor‑neutral, UPF‑style Tcl file:
    - Creates one power domain per entry in `domains`.
    - Emits `create_supply_net`, `create_supply_set`, and `set_domain_supply_net`.
    - Builds a single chip‑level power state table with `create_pst` and `add_pst_state`.
    - Adds template `set_isolation` and `set_level_shifter_strategy` commands per crossing.
        
- Outputs to `auto_low_power_intent.upf` (or a caller‑specified path).

The generated UPF is intentionally generic so it can be adapted to different tools.

## lp_rules.tcl

- Tcl library of reusable procedures, for example:
    
    - `lp_iso_rule from_domain to_domain iso_sig iso_sense clamp nets`
    - `lp_ls_rule from_domain to_domain ls_type nets`
    - `lp_ret_rule domain ret_supply save_sig restore_sig cells`
        
- These procs encapsulate common isolation, level shifter, and retention patterns.
- Can be called from both block‑level and chip‑level UPF scripts with different arguments, demonstrating hierarchical reuse.
    

---

## test/ specs

Each test file defines a `power_spec` object with the same schema used in `src/lp_spec_model.py`. The main runner imports these and produces separate UPF outputs.

## test_spec_small.py

- One always‑on domain and one simple switchable domain.
- Two power states (“on” and one off state).
- Minimal or no crossings.
- Intended as a smoke test to validate that the checker and generator work end‑to‑end.
    

## test_spec_big.py

- More realistic multi‑domain SoC example: AON, CORE, PERI, MEM.
- Multiple power states (FULL_ON, CORE_LPM, PERI_OFF, MEM_RET, CHIP_OFF).
- Several isolation and level‑shifter relations:
    - Core/Peri/Mem to AON.
    - Cross‑domain Core ↔ Peri paths.
- Good for showing understanding of:
    - Multi‑voltage operation (CORE, MEM, PERI rails).
    - Low‑power modes (LPM, retention).
    - Domain crossings that must be guarded.

## test_spec_huge.py

- Auto‑generated “super large random net” style spec:
    - Around 20 domains, each with multiple blocks.
    - 10 random power states with varying on/off combinations.
    - Many random isolation and level‑shifter pairs.
- Designed to stress:
    - Performance of the checker on a large spec.
    - Scalability of the UPF output.
- Illustrates ability to script synthetic stress cases for low‑power flows.
    

---

## main.py (test runner)

`main.py` orchestrates everything:

- Adds `src/` and `test/` to the Python path.
- Discovers all `test/test_*.py` modules.
- For each discovered test:
    - Imports the module, reads its `power_spec`.
    - Runs `run_all_checks(spec)` to validate.
    - Calls `gen_upf(spec, out_name)` to produce a UPF Tcl file named like `out_test_test_spec_big.upf`.
        

Run all tests with:

```bash
python main.py
```

This command effectively runs an “automation regression,” generating UPF for every defined training scenario.

---

## Typical usage flow

1. **Clone / copy the project**  
    Place it on a machine with Python 3.x available.
2. **Create or edit a spec**
    - Copy `test/test_spec_small.py` to a new file like `test/test_spec_usb.py`.
    - Edit the `power_spec` dictionary to match a new low‑power scenario (e.g., USB IP block, DVFS core, mixed‑signal PLL).
3. **Run the framework**
	```bash
	python main.py
	```

4. **Inspect outputs**
    
    - UPF files appear at project root (e.g., `out_test_test_spec_usb.upf`).
    - Check that domains, supply sets, PSTs, and crossings match expectations.
        
5. **Integrate Tcl rules (optional)**
    
    - In a separate UPF or Tcl environment, source `src/lp_rules.tcl`.
    - Use `lp_iso_rule`, `lp_ls_rule`, and `lp_ret_rule` to refine strategy at block/chip level.