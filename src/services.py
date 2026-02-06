import re
from src.database import get_connection
from src.models import URLModel
from src.utils import generate_code

CUSTOM_CODE_REGEX = re.compile(r"^[a-zA-Z0-9_-]{4,20}$")


class URLService:

    def is_code_exists(self, code: str) -> bool:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT 1 FROM urls WHERE code = ?",
                (code,),
            ).fetchone()
            return row is not None

    def create(self, original_url: str, custom_code: str | None = None) -> URLModel:
        if custom_code:
            if not CUSTOM_CODE_REGEX.match(custom_code):
                raise ValueError("Invalid custom code format")

            if self.is_code_exists(custom_code):
                raise KeyError("Custom code already exists")

            code = custom_code
        else:
            code = generate_code()
            while self.is_code_exists(code):
                code = generate_code()

        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO urls (code, original_url) VALUES (?, ?)",
                (code, original_url),
            )
            url_id = cursor.lastrowid

        return URLModel(
            id=url_id,
            code=code,
            original_url=original_url,
        )

    def get_by_code(self, code: str) -> URLModel | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM urls WHERE code = ?",
                (code,),
            ).fetchone()

        if not row:
            return None

        return URLModel(
            id=row["id"],
            code=row["code"],
            original_url=row["original_url"],
        )
