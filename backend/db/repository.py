import re
from typing import Any, Dict, List, Optional

from psycopg2 import sql

from .connection import execute_command, execute_query


def _validate_identifier(name: str) -> bool:
    """Validate that identifier contains only safe characters (alphanumeric and underscore)."""
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))


class Repository:
    def __init__(self, table_name: str):
        if not _validate_identifier(table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        self.table_name = table_name

    def find_all(self, conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find all records

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause

        Returns:
            List of dictionaries representing the records
        """
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name))
        params = []
        
        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                if not _validate_identifier(key):
                    raise ValueError(f"Invalid column name: {key}")
                where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
                params.append(value)
            query = sql.SQL("{} WHERE {}").format(query, sql.SQL(" AND ").join(where_clauses))
        
        return execute_query(query.as_string(None), tuple(params) if params else None)

    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one record

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause

        Returns:
            Dictionary representing the record
        """
        results = self.find_all(conditions)
        return results[0] if results else None

    def find_by_id(self, id_value: Any) -> Optional[Dict[str, Any]]:
        """Find record by ID

        Args:
            id_value: Value of the ID column

        Returns:
            Dictionary representing the record
        """
        return self.find_one({"id": id_value})

    def insert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new record

        Args:
            data: Dictionary of column-value pairs for INSERT

        Returns:
            Dictionary representing the inserted record
        """
        if not data:
            raise ValueError("Cannot insert empty data")
        
        for key in data.keys():
            if not _validate_identifier(key):
                raise ValueError(f"Invalid column name: {key}")
        
        columns = [sql.Identifier(key) for key in data.keys()]
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
            sql.Identifier(self.table_name),
            sql.SQL(", ").join(columns),
            sql.SQL(placeholders)
        )
        results = execute_query(query.as_string(None), values)
        return results[0] if results else None

    def update(self, conditions: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause
            data: Dictionary of column-value pairs for UPDATE

        Returns:
            Dictionary representing the updated record
        """
        if not data:
            raise ValueError("Cannot update with empty data")
        
        set_clauses = []
        params = []
        
        for key, value in data.items():
            if not _validate_identifier(key):
                raise ValueError(f"Invalid column name: {key}")
            set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
            params.append(value)
        
        where_clauses = []
        for key, value in conditions.items():
            if not _validate_identifier(key):
                raise ValueError(f"Invalid column name: {key}")
            where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
            params.append(value)
        
        query = sql.SQL("UPDATE {} SET {} WHERE {} RETURNING *").format(
            sql.Identifier(self.table_name),
            sql.SQL(", ").join(set_clauses),
            sql.SQL(" AND ").join(where_clauses)
        )
        
        results = execute_query(query.as_string(None), tuple(params))
        return results[0] if results else None

    def delete(self, conditions: Dict[str, Any]) -> None:
        """Delete a record

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause
        """
        where_clauses = []
        params = []
        
        for key, value in conditions.items():
            if not _validate_identifier(key):
                raise ValueError(f"Invalid column name: {key}")
            where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
            params.append(value)
        
        query = sql.SQL("DELETE FROM {} WHERE {}").format(
            sql.Identifier(self.table_name),
            sql.SQL(" AND ").join(where_clauses)
        )
        execute_command(query.as_string(None), tuple(params))
