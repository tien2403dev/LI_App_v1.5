"""Các lựa chọn hiện có trong database LI; không thay đổi dữ liệu gốc."""
from dataclasses import dataclass
from database.connection import connection


@dataclass
class FilterOptionResult:
    eqps: list[str]
    slots: list[int]
    scrap_codes: list[str]
    tiers: list[str]
    models: list[str]


class FilterOptionRepository:
    def __init__(self, database_path):
        self.database_path = database_path

    def load_options(self):
        # Một snapshot cho tất cả danh sách; connection chỉ thuộc worker này.
        with connection(self.database_path, timeout=5) as conn:
            conn.execute("BEGIN")
            def values(sql):
                return [row[0] for row in conn.execute(sql)]
            return FilterOptionResult(
                eqps=values("SELECT DISTINCT EQP FROM prime_data ORDER BY EQP"),
                slots=values("SELECT DISTINCT SLOT FROM prime_data ORDER BY SLOT"),
                # Bộ lọc dùng chung cho PRIME và CUM: không bỏ sót Model chỉ có ở CUM.
                models=values("""SELECT MODEL FROM prime_data
                    UNION SELECT MODEL FROM cum_data ORDER BY MODEL"""),
                tiers=values("""SELECT TIER FROM prime_data WHERE TIER IS NOT NULL
                    UNION SELECT TIER FROM cum_data WHERE TIER IS NOT NULL ORDER BY TIER"""),
                scrap_codes=values("""SELECT SCRAPCODE AS code FROM prime_data
                    WHERE length(SCRAPCODE)=4 AND SCRAPCODE NOT GLOB '*[^0-9]*'
                    UNION SELECT scrap_code FROM cum_scrap_detail ORDER BY code"""),
            )
