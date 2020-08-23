"""
Unit tests for eoq_calculator.py
"""

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

import eoq_calculator

class TestEoqFunctions(unittest.TestCase):
    """
    Test cases.
    """
    # Define sample data
    sample_forecast = pd.DataFrame({
        'days': [0, 33, 33, 66, 66, 99, 99, 132, 132, 165, 165, 198],
        'inventory': [90, 0, 90, 0, 90, 0, 90, 0, 90, 0, 90, 0]
    })

    # Tests
    def test_calc_order_size(self):
        """
        Test order size calculation.
        """
        self.assertEqual(
            eoq_calculator.calc_order_size(
                year_demand=1000,
                order_cost=10,
                unit_storage_cost=2.5
            ),
            90
        )
    def test_calc_reorder_point(self):
        """
        Test reorder point calculation.
        """
        self.assertEqual(
            eoq_calculator.calc_reorder_point(
                year_demand=1000,
                order_delay=7
            ),
            (2.73972602739726, 20)
        )
    def test_calc_order_lifetime(self):
        """
        Test order lifetime calculation.
        """
        self.assertEqual(
            eoq_calculator.calc_order_lifetime(
                day_demand=2.73972602739726,
                order_size=90
            ),
            33
        )
    def test_calc_inventory_forecast(self):
        """
        Test inventory forecast calculation.
        """
        assert_frame_equal(
            eoq_calculator.calc_inventory_forecast(
                forecast_size=180,
                order_size=90,
                order_lifetime=33
            ),
            self.sample_forecast
        )

if __name__ == '__main__':
    unittest.main()
