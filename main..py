import importlib
import pathlib
import sys

# Make src/ importable
ROOT = pathlib.Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
TEST_DIR = ROOT / "test"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(TEST_DIR))

from lp_checker import run_all_checks
from lp_upf_gen import gen_upf

def run_one_test(module_name: str):
    print(f"\n=== Running low-power test: {module_name} ===")
    mod = importlib.import_module(module_name)
    spec = getattr(mod, "power_spec", None)
    if spec is None:
        print(f"SKIP: {module_name} has no 'power_spec'")
        return
    # Check and generate UPF
    run_all_checks(spec)
    out_name = f"out_{module_name.replace('.', '_')}.upf"
    gen_upf(spec, out_name)
    print(f"OK: Generated {out_name}")

def discover_tests():
    tests = []
    for py in TEST_DIR.glob("test_*.py"):
        tests.append(f"test.{py.stem}")
    return tests

if __name__ == "__main__":
    modules = discover_tests()
    if not modules:
        print("No test specs found in test/ (files must start with test_*.py)")
        sys.exit(1)
    for m in modules:
        run_one_test(m)
