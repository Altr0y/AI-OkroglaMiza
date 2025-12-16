from typing import Any, Dict, List, Optional

from .connection import execute_command, execute_query


class Repository:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def find_all(self, conditions: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Find all records

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause

        Returns:
            List of dictionaries representing the records
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []
        
        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)
            query += " WHERE " + " AND ".join(where_clauses)
        
        return execute_query(query, tuple(params) if params else None)

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
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
        results = execute_query(query, values)
        return results[0] if results else None

    def update(self, conditions: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause
            data: Dictionary of column-value pairs for UPDATE

        Returns:
            Dictionary representing the updated record
        """
        set_clauses = []
        params = []
        
        for key, value in data.items():
            set_clauses.append(f"{key} = %s")
            params.append(value)
        
        where_clauses = []
        for key, value in conditions.items():
            where_clauses.append(f"{key} = %s")
            params.append(value)
        
        query = (
            f"UPDATE {self.table_name} "
            f"SET {', '.join(set_clauses)} "
            f"WHERE {' AND '.join(where_clauses)} "
            f"RETURNING *"
        )
        
        results = execute_query(query, tuple(params))
        return results[0] if results else None

    def delete(self, conditions: Dict[str, Any]) -> None:
        """Delete a record

        Args:
            conditions: Dictionary of column-value pairs for WHERE clause
        """
        where_clauses = []
        params = []
        
        for key, value in conditions.items():
            where_clauses.append(f"{key} = %s")
            params.append(value)
        
        query = f"DELETE FROM {self.table_name} WHERE {' AND '.join(where_clauses)}"
        execute_command(query, tuple(params))
