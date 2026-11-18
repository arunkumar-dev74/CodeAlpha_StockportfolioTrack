import unittest

from portfolio import (
    calculate_investment,
    calculate_current_value,
    calculate_profit_loss,
    calculate_profit_percentage,
    get_portfolio_summary,
    validate_stock
)


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        self.stock = {
            "name": "TCS",
            "quantity": 10,
            "buy_price": 100,
            "current_price": 120
        }

    def test_investment(self):
        self.assertEqual(
            calculate_investment(self.stock), 1000
        )

    def test_current_value(self):
        self.assertEqual(
            calculate_current_value(self.stock), 1200
        )

    def test_profit_loss(self):
        self.assertEqual(
            calculate_profit_loss(self.stock), 200
        )

    def test_profit_percentage(self):
        self.assertEqual(
            calculate_profit_percentage(self.stock), 20
        )

    def test_portfolio_summary(self):
        result = get_portfolio_summary([self.stock])

        self.assertEqual(result["total_investment"], 1000)
        self.assertEqual(result["total_value"], 1200)
        self.assertEqual(result["profit_loss"], 200)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            validate_stock("TCS", 0, 100, 120)


if __name__ == "__main__":
    unittest.main()