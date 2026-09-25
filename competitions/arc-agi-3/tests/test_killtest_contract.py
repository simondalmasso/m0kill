from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HARNESS = Path(__file__).with_name("run_local_eval.py")


def load_harness():
    spec = importlib.util.spec_from_file_location("arc_killtest_harness", HARNESS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {HARNESS}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KilltestContractTests(unittest.TestCase):
    def test_pre_promotion_variants_are_exactly_four_required_lanes(self):
        harness = load_harness()
        labels = [item["label"] for item in harness.variant_specs(False)]
        self.assertEqual(
            labels,
            ["A_BASE_0", "A_BASE_1", "A_BASE_2", "A_CHALLENGER"],
        )

    def test_ablations_are_opt_in_and_only_follow_core_variants(self):
        harness = load_harness()
        core = [item["label"] for item in harness.variant_specs(False)]
        expanded = [item["label"] for item in harness.variant_specs(True)]
        self.assertEqual(expanded[:4], core)
        self.assertEqual(
            expanded[4:],
            [
                "A_CHALLENGER_NO_EFFECT",
                "A_CHALLENGER_NO_INFO",
                "A_CHALLENGER_NO_PLANNER",
            ],
        )

    def test_action_efficiency_without_progress_cannot_promote(self):
        harness = load_harness()
        challenger = {
            "rhae": 0.0,
            "levels_completed": 0.0,
            "games_with_progress": 0.0,
            "actions": 100.0,
        }
        baseline = {
            "rhae": 0.0,
            "levels_completed": 0.0,
            "games_with_progress": 0.0,
            "actions": 200.0,
        }
        decision = harness.promotion_decision(
            challenger,
            baseline,
            delta_ci=(0.0, 0.0),
            repeat_deltas=[0.0, 0.0],
            offline_reproducible=True,
        )
        self.assertEqual(decision["status"], "KILLED_NO_EDGE")
        self.assertFalse(decision["genuine_progress"])

    def test_repeatable_positive_rhae_with_positive_ci_can_promote(self):
        harness = load_harness()
        challenger = {
            "rhae": 12.0,
            "levels_completed": 3.0,
            "games_with_progress": 2.0,
            "actions": 160.0,
        }
        baseline = {
            "rhae": 5.0,
            "levels_completed": 1.0,
            "games_with_progress": 1.0,
            "actions": 170.0,
        }
        decision = harness.promotion_decision(
            challenger,
            baseline,
            delta_ci=(1.5, 10.0),
            repeat_deltas=[6.0, 8.0],
            offline_reproducible=True,
        )
        self.assertEqual(decision["status"], "PROMOTED")
        self.assertTrue(decision["genuine_progress"])


if __name__ == "__main__":
    unittest.main()
