import io
from datetime import date
from decimal import Decimal

from django.test import SimpleTestCase

from simulations.services.csv_import_service import ChaseBrokerageCsvParser, CsvImportService

CHASE_HEADER = "Ticker,Asset Class,Quantity,Unit Cost,Acquisition Date\n"


def make_file(content: str) -> io.BytesIO:
    return io.BytesIO(content.encode("utf-8-sig"))


class ChaseBrokerageCsvParserTests(SimpleTestCase):
    def test_parses_valid_rows(self):
        csv_content = CHASE_HEADER + "AAPL,Equity,10,150.25,01/15/2024\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(
            rows,
            [
                {
                    "ticker": "AAPL",
                    "quantity": Decimal("10"),
                    "cost_per_share": Decimal("150.25"),
                    "date_purchased": date(2024, 1, 15),
                }
            ],
        )

    def test_parses_comma_separated_unit_cost(self):
        csv_content = CHASE_HEADER + 'AAPL,Equity,10,"1,250.25",01/15/2024\n'

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows[0]["cost_per_share"], Decimal("1250.25"))

    def test_skips_cash_and_money_market_rows(self):
        csv_content = CHASE_HEADER + "SWVXX,Cash & Money Market Funds,100,1.00,01/15/2024\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows, [])

    def test_skips_rows_without_ticker(self):
        csv_content = CHASE_HEADER + ",Equity,10,150.25,01/15/2024\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows, [])

    def test_skips_rows_with_invalid_quantity(self):
        csv_content = CHASE_HEADER + "AAPL,Equity,not-a-number,150.25,01/15/2024\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows, [])

    def test_skips_rows_with_invalid_date(self):
        csv_content = CHASE_HEADER + "AAPL,Equity,10,150.25,not-a-date\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows, [])

    def test_skips_rows_missing_columns(self):
        csv_content = "Ticker,Asset Class\nAAPL,Equity\n"

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual(rows, [])

    def test_parses_multiple_valid_rows(self):
        csv_content = (
            CHASE_HEADER
            + "AAPL,Equity,10,150.25,01/15/2024\n"
            + "MSFT,Equity,5,300.00,02/01/2024\n"
        )

        rows = ChaseBrokerageCsvParser(make_file(csv_content)).parse()

        self.assertEqual([row["ticker"] for row in rows], ["AAPL", "MSFT"])


class CsvImportServiceTests(SimpleTestCase):
    def test_is_supported_for_known_source(self):
        service = CsvImportService("chase_brokerage", make_file(CHASE_HEADER))

        self.assertTrue(service.is_supported())

    def test_is_not_supported_for_unknown_source(self):
        service = CsvImportService("unknown_source", make_file(CHASE_HEADER))

        self.assertFalse(service.is_supported())

    def test_parse_delegates_to_matching_parser(self):
        csv_content = CHASE_HEADER + "AAPL,Equity,10,150.25,01/15/2024\n"
        service = CsvImportService("chase_brokerage", make_file(csv_content))

        rows = service.parse()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["ticker"], "AAPL")
