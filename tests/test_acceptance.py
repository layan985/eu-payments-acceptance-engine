import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


experiment = load_module("experiment", ROOT / "experiment.py")
generator = load_module("generator", ROOT / "generate_data.py")


class AcceptanceTests(unittest.TestCase):
    def test_experiment_recovers_positive_treatment_effect(self):
        result = experiment.run_experiment(n=100_000, seed=11)
        self.assertGreater(result["treatment_rate"], result["control_rate"])
        self.assertLess(result["p_value"], 0.05)

    def test_known_germany_pspb_penalty(self):
        p_a = generator.approval_probability("DE", "PSP_A", "visa", "desktop", False)
        p_b = generator.approval_probability("DE", "PSP_B", "visa", "desktop", False)
        self.assertGreater(p_a, p_b)
        self.assertAlmostEqual(p_a - p_b, 0.035, places=6)

    def test_generator_respects_n_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a.csv"
            b = Path(td) / "b.csv"
            generator.generate(a, n=25, seed=123)
            generator.generate(b, n=25, seed=123)
            self.assertEqual(a.read_text(), b.read_text())
            with a.open(encoding="utf-8") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 25)


if __name__ == "__main__":
    unittest.main()
