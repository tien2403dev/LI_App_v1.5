from __future__ import annotations


from dataclasses import dataclass

import requests



BASE_URL = "http://107.11.192.45"

LOGIN_URL = (
    f"{BASE_URL}/DATA/Ajax_UserLoginGet.asp"
)

@dataclass(frozen=True)
class MailLoginInfo:
    """Thông tin trả về sau khi đăng nhập mail."""

    user_id: str
    employee_no: str
    name_en: str
    name_vn: str
    organization_code: str
    organization_en: str
    organization_vn: str


class MailService:
    """Đăng nhập và làm việc với hệ thống mail nội bộ."""

    LOGIN_TIMEOUT_SECONDS = 30

    def __init__(self):
        """Khởi tạo đối tượng và các thành phần liên quan."""
        self.session = None
        self.user_info = None
        self.cookies = {}
        self.is_logged_in = False

    def login(
        self,
        user_id: str,
        password: str,
    ) -> tuple[bool, MailLoginInfo | str]:
        """
        Đăng nhập hệ thống mail nội bộ.

        Kết quả:
        - Thành công: (True, MailLoginInfo)
        - Thất bại: (False, error_message)
        """

        user_id = str(
            user_id or ""
        ).strip()

        password = str(
            password or ""
        )

        if not user_id:
            return (
                False,
                "User ID người gửi đang để trống.",
            )

        if not password:
            return (
                False,
                "Mật khẩu người gửi đang để trống.",
            )

        self.clear_session()

        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"{BASE_URL}/",
            "Origin": BASE_URL,
            "Content-Type": (
                "application/x-www-form-urlencoded"
            ),
        }

        payload = {
            "STR_LAN": "vn",
            "CD_USER": user_id,
            "STR_PASS": password,
        }

        try:
            response = session.post(
                LOGIN_URL,
                data=payload,
                headers=headers,
                timeout=self.LOGIN_TIMEOUT_SECONDS,
            )

        except requests.Timeout:
            session.close()

            return (
                False,
                (
                    "Đăng nhập quá thời gian chờ "
                    f"{self.LOGIN_TIMEOUT_SECONDS} giây."
                ),
            )

        except requests.ConnectionError:
            session.close()

            return (
                False,
                (
                    "Không thể kết nối tới hệ thống "
                    "mail nội bộ."
                ),
            )

        except requests.RequestException as error:
            session.close()

            return (
                False,
                (
                    "Lỗi khi gửi yêu cầu đăng nhập: "
                    f"{error}"
                ),
            )

        if response.status_code != 200:
            session.close()

            return (
                False,
                (
                    "Hệ thống mail trả về HTTP "
                    f"{response.status_code}."
                ),
            )

        response_text = response.content.decode(
            "utf-8",
            errors="ignore",
        )

        lower_text = response_text.lower()

        if (
            "fail" in lower_text
            or "invalid" in lower_text
            or "error" in lower_text
        ):
            session.close()

            return (
                False,
                (
                    "Đăng nhập thất bại. "
                    "User ID hoặc mật khẩu không đúng."
                ),
            )

        info = response_text.split("</>")

        if len(info) < 11:
            session.close()

            return (
                False,
                (
                    "Đăng nhập thất bại: cấu trúc "
                    "phản hồi không hợp lệ "
                    f"({len(info)} trường)."
                ),
            )

        login_user_id = info[0].strip()
        employee_no = info[1].strip()
        name_en = info[2].strip()
        organization_code = info[3].strip()
        organization_en = info[4].strip()
        name_vn = info[9].strip()
        organization_vn = info[10].strip()

        if (
            not login_user_id
            or not employee_no
        ):
            session.close()

            return (
                False,
                (
                    "Đăng nhập thất bại: hệ thống "
                    "không trả về thông tin người dùng."
                ),
            )

        login_info = MailLoginInfo(
            user_id=login_user_id,
            employee_no=employee_no,
            name_en=name_en,
            name_vn=name_vn,
            organization_code=organization_code,
            organization_en=organization_en,
            organization_vn=organization_vn,
        )

        cookies = {
            "ck_Lan": "vn",
            "ck_Pattern": "2U",

            "ck_cdUser": login_user_id,
            "ck_noEmp": employee_no,

            # Cookie/Header chỉ dùng dữ liệu tiếng Anh
            # để tránh lỗi mã hóa latin-1.
            "ck_strName_en": name_en,
            "ck_strName_ko": name_en,
            "ck_strName_vn": name_en,

            "ck_cdOrg": organization_code,

            "ck_strOrg_en": organization_en,
            "ck_strOrg_ko": organization_en,
            "ck_strOrg_vn": organization_en,

            "ck_strTel": "",
            "ck_strHp": "",
            "ck_strEmail": "",

            "ck_Mrp_Lan": "vn",

            "ck_Mrp_cdUser": login_user_id,
            "ck_Mrp_noEmp": employee_no,

            "ck_Mrp_strName_en": name_en,
            "ck_Mrp_strName_ko": name_en,
            "ck_Mrp_strName_vn": name_en,

            "ck_Mrp_cdOrg": organization_code,

            "ck_Mrp_strOrg_en": organization_en,
            "ck_Mrp_strOrg_ko": organization_en,
            "ck_Mrp_strOrg_vn": organization_en,

            "ck_Mrp_strTel": "",
            "ck_Mrp_strHp": "",
            "ck_Mrp_strEmail": "",
        }

        for key, value in cookies.items():
            session.cookies.set(
                key,
                value,
            )

        self.session = session
        self.cookies = cookies
        self.user_info = login_info
        self.is_logged_in = True

        return True, login_info



    def clear_session(self) -> None:
        """Đóng session đăng nhập hiện tại."""

        if self.session is not None:
            self.session.close()

        self.session = None
        self.user_info = None
        self.cookies = {}
        self.is_logged_in = False