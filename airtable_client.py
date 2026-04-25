import os
from pyairtable import Api
from pyairtable.formulas import match
from functools import wraps
import traceback

# ─── Config ───────────────────────────────────────────────────────────────────
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "")
BASE_ID = "app77CdzKEqLlhZ8d"

# ─── Table IDs ────────────────────────────────────────────────────────────────
TABLES = {
    "customers":           "tbl3ZGvwQ5cLigpFM",
    "tasks":               "tblsodUowDPPiOcCk",
    "quotes":              "tblJTBG0o9jhcs522",
    "orders":              "tblJYbxBXWUkAoI7m",
    "order_lines":         "tbliWBlXR7HdaZms5",
    "inventory_movements": "tblS074Z1pDNpEVWO",
    "inventory_by_location": "tbl6HhpUq3cTba1RB",
    "measurements":        "tblOBD9ctlmESWA2x",
    "approvals":           "tbl6z2mmkNpEFI6jx",
    "installers":          "tblNj2W8WJWbeG1sl",
    "cancellations":       "tblATBHZSrauLczV9",
    "team":                "tblOVdS88j37ydSQm",
    "factory_orders":      "tblgNNGPAk4sSADlq",
    "suppliers":           "tblPVjHSRx6T6f8jj",
    "daily_log":           "tblgBFxsESiqesTNY",
    "rates":               "tbl4guJMDoluPnHLD",
    "projects":            "tblXRD8ZN1twkFbjh",
    "installations":       "tblndyBo0AqfNm3l3",
    "products":            "tbl9DI5ogG6HkbsOo",
}


class AirtableClient:
    def __init__(self):
        self.api = Api(AIRTABLE_API_KEY)
        self.base = self.api.base(BASE_ID)
        self._tables = {}

    def table(self, name: str):
        if name not in self._tables:
            self._tables[name] = self.base.table(TABLES[name])
        return self._tables[name]

    # ── Generic CRUD ──────────────────────────────────────────────────────────

    def get_all(self, table_name: str, formula: str = None, sort=None, fields=None) -> list:
        """Return all records from a table."""
        try:
            kwargs = {}
            if formula:
                kwargs["formula"] = formula
            if sort:
                kwargs["sort"] = sort
            if fields:
                kwargs["fields"] = fields
            records = self.table(table_name).all(**kwargs)
            return [{"id": r["id"], **r["fields"]} for r in records]
        except Exception as e:
            print(f"[AirtableClient] get_all({table_name}) error: {e}")
            traceback.print_exc()
            return []

    def get_one(self, table_name: str, record_id: str) -> dict | None:
        """Return a single record by ID."""
        try:
            r = self.table(table_name).get(record_id)
            return {"id": r["id"], **r["fields"]}
        except Exception as e:
            print(f"[AirtableClient] get_one({table_name}, {record_id}) error: {e}")
            return None

    def create(self, table_name: str, fields: dict) -> dict | None:
        """Create a new record."""
        try:
            r = self.table(table_name).create(fields)
            return {"id": r["id"], **r["fields"]}
        except Exception as e:
            print(f"[AirtableClient] create({table_name}) error: {e}")
            traceback.print_exc()
            return None

    def update(self, table_name: str, record_id: str, fields: dict) -> dict | None:
        """Update an existing record."""
        try:
            r = self.table(table_name).update(record_id, fields)
            return {"id": r["id"], **r["fields"]}
        except Exception as e:
            print(f"[AirtableClient] update({table_name}, {record_id}) error: {e}")
            traceback.print_exc()
            return None

    def delete(self, table_name: str, record_id: str) -> bool:
        """Delete a record (use sparingly – prefer soft-delete)."""
        try:
            self.table(table_name).delete(record_id)
            return True
        except Exception as e:
            print(f"[AirtableClient] delete({table_name}, {record_id}) error: {e}")
            return False

    # ── Domain helpers ────────────────────────────────────────────────────────

    def get_customers(self, search: str = None) -> list:
        formula = None
        if search:
            formula = f"OR(FIND('{search}', {{שם}}), FIND('{search}', {{טלפון}}))"
        return self.get_all("customers", formula=formula, sort=["שם"])

    def get_orders(self, status: str = None, customer_id: str = None) -> list:
        parts = []
        if status:
            parts.append(f"{{סטטוס}}='{status}'")
        if customer_id:
            parts.append(f"FIND('{customer_id}', ARRAYJOIN({{לקוח}}))")
        formula = f"AND({', '.join(parts)})" if parts else None
        return self.get_all("orders", formula=formula)

    def get_inventory(self) -> list:
        return self.get_all("inventory_by_location")

    def get_installers(self) -> list:
        return self.get_all("installers", sort=["Name"])

    def get_tasks(self, status: str = None) -> list:
        formula = f"{{סטטוס}}='{status}'" if status else None
        return self.get_all("tasks", formula=formula)

    def get_quotes(self, status: str = None) -> list:
        formula = f"{{סטטוס}}='{status}'" if status else None
        return self.get_all("quotes", formula=formula)

    def get_products(self) -> list:
        return self.get_all("products", sort=["שם מוצר מלא"], fields=["שם מוצר מלא", "מידה", "סוג זכוכית", "גוון פרזול", "גובה", "תמונה"])

    def create_product(self, fields: dict) -> dict | None:
        return self.create("products", fields)

    def get_product(self, record_id: str) -> dict | None:
        return self.get_one("products", record_id)

    def get_order_lines(self, order_id: str) -> list:
        formula = f"FIND('{order_id}', ARRAYJOIN({{הזמנה}}))"
        return self.get_all("order_lines", formula=formula)


# ── Singleton ─────────────────────────────────────────────────────────────────
_client: AirtableClient | None = None


def get_client() -> AirtableClient:
    global _client
    if _client is None:
        _client = AirtableClient()
    return _client
