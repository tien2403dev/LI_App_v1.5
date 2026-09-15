from __future__ import annotations


from pathlib import Path
from typing import Union
from dataclasses import dataclass
from database.connection import create_connection
@dataclass(frozen=True)
class MailHistorySummary:
    id: int
    alarm_date: str
    sent_at: str
    sender: str
    receivers: str
    cc: str
    result: str


@dataclass(frozen=True)
class MailHistoryDetail:
    id: int
    alarm_date: str
    sent_at: str
    sender: str
    receivers: str
    cc: str
    result: str
    subject: str
    html_content: str

class MailSendRepository:
    """Chỉ đọc danh sách và chi tiết lịch sử mail; chưa triển khai gửi mail."""

    def __init__(
        self,
        database_path: Union[str, Path],
    ):
        """Khởi tạo đối tượng và các thành phần liên quan."""
        self.database_path = Path(
            database_path
        )





    def get_mail_history(
            self,
            limit: int = 500,
    ) -> list[MailHistorySummary]:
        """Lấy danh sách email thành công mới nhất."""

        limit = max(
            1,
            int(limit),
        )

        connection = create_connection(
            self.database_path
        )

        try:
            rows = connection.execute(
                """
                SELECT
                    id,
                    alarm_date,
                    sent_at,
                    sender,
                    receivers,
                    cc,
                    result
                FROM mail_send_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            return [
                MailHistorySummary(
                    id=int(row["id"]),
                    alarm_date=str(
                        row["alarm_date"]
                    ),
                    sent_at=str(
                        row["sent_at"]
                    ),
                    sender=str(
                        row["sender"]
                    ),
                    receivers=str(
                        row["receivers"]
                    ),
                    cc=str(
                        row["cc"] or ""
                    ),
                    result=str(
                        row["result"]
                    ),
                )
                for row in rows
            ]

        finally:
            connection.close()

    def get_mail_history_detail(
            self,
            history_id: int,
    ) -> MailHistoryDetail:
        """Lấy snapshot đầy đủ của email đã gửi."""

        connection = create_connection(
            self.database_path
        )

        try:
            row = connection.execute(
                """
                SELECT
                    id,
                    alarm_date,
                    sent_at,
                    sender,
                    receivers,
                    cc,
                    result,
                    subject,
                    html_content
                FROM mail_send_history
                WHERE id = ?
                """,
                (history_id,),
            ).fetchone()

            if row is None:
                raise ValueError(
                    (
                        "Không tìm thấy "
                        "Mail History đã chọn."
                    )
                )

            return MailHistoryDetail(
                id=int(row["id"]),
                alarm_date=str(
                    row["alarm_date"]
                ),
                sent_at=str(
                    row["sent_at"]
                ),
                sender=str(
                    row["sender"]
                ),
                receivers=str(
                    row["receivers"]
                ),
                cc=str(
                    row["cc"] or ""
                ),
                result=str(
                    row["result"]
                ),
                subject=str(
                    row["subject"]
                ),
                html_content=str(
                    row["html_content"]
                ),
            )

        finally:
            connection.close()
