import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation


class ChaseBrokerageCsvParser:
    CASH_ASSET_CLASS = "Cash & Money Market Funds"

    def __init__(self, file):
        self.file = file

    def parse(self) -> list[dict]:
        rows = []
        for row in self._read_rows():
            holding = self._parse_row(row)
            if holding is not None:
                rows.append(holding)
        return rows

    def _read_rows(self) -> csv.DictReader:
        content = self.file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")
        return csv.DictReader(io.StringIO(content))

    def _parse_row(self, row: dict) -> dict | None:
        ticker = (row.get("Ticker") or "").strip()
        if not ticker or (row.get("Asset Class") or "").strip() == self.CASH_ASSET_CLASS:
            return None

        try:
            return {
                "ticker": ticker,
                "quantity": Decimal(row["Quantity"]),
                "cost_per_share": Decimal(row["Unit Cost"].replace(",", "")),
                "date_purchased": datetime.strptime(row["Acquisition Date"], "%m/%d/%Y").date(),
            }
        except (KeyError, InvalidOperation, ValueError):
            return None


class CsvImportService:
    PARSERS = {
        "chase_brokerage": ChaseBrokerageCsvParser,
    }

    def __init__(self, source: str, file):
        self.source = source
        self.file = file

    def is_supported(self) -> bool:
        return self.source in self.PARSERS

    def parse(self) -> list[dict]:
        parser_cls = self.PARSERS[self.source]
        return parser_cls(self.file).parse()
