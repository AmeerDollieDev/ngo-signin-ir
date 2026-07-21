import io
import pandas as pd


def build_dataframe(volunteers: list[dict]) -> pd.DataFrame:
    """Turn a list of volunteer dicts into a DataFrame with a fixed column order."""
    columns = ["name", "email", "phone", "signed_in_at"]
    if not volunteers:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(volunteers, columns=columns)


def to_csv_bytes(volunteers: list[dict]) -> bytes:
    df = build_dataframe(volunteers)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def to_xlsx_bytes(volunteers: list[dict]) -> bytes:
    df = build_dataframe(volunteers)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sign-ins")
    buffer.seek(0)
    return buffer.getvalue()
