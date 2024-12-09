from typing import Any, Dict


class QueryValidator:
    def __init__(self, query: Dict[str, Any], schema: Dict[str, Any]):
        self.query = query
        self.schema = schema

    def validate(self) -> None:
        for key, value in self.query.items():
            if key not in self.schema:
                raise QueryValidationError(f"Invalid query key: {key}")
            if not isinstance(value, self.schema[key]):
                raise QueryValidationError(
                    f"Invalid query value for key {key}: {value}"
                )


class QueryValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
