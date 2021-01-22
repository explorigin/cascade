from typing import Optional
from hashlib import sha256

from pydantic import BaseSettings
from httpx import Client
from rule_engine import Rule, ast

from ..exceptions import DoesNotExist, ConditionCheckFailed


class Settings(BaseSettings):
    API_KEY: str
    BASE_URL: str
    INITIALIZE: bool = True

    class Config:
        env_prefix = 'KEVALIN_'

#
# def expression_to_condition(expr, key_name: Optional[str] = None):
#     if isinstance(expr, ast.LogicExpression):
#         left = expression_to_condition(expr.left, key_name)
#         right = expression_to_condition(expr.right, key_name)
#         if expr.type == 'and':
#             return left and right
#         if expr.type == 'or':
#             return left or right
#     if isinstance(expr, ast.ComparisonExpression):
#         left = expression_to_condition(expr.left, key_name)
#         right = expression_to_condition(expr.right, key_name)
#         if expr.type == 'eq':
#             return left.eq(right) if right is not None else left.not_exists()
#         if expr.type == 'ne':
#             return left.ne(right) if right is not None else left.exists()
#     if isinstance(expr, ast.SymbolExpression):
#         if expr.name == 'NULL':
#             return None
#         if key_name is not None and expr.name == key_name:
#             return Key(expr.name)
#         return Attr(expr.name)
#     if isinstance(expr, ast.StringExpression):
#         return expr.value
#     if isinstance(expr, ast.ContainsExpression):
#         container = expression_to_condition(expr.container, key_name)
#         member = expression_to_condition(expr.member, key_name)
#         return container.contains(member)
#     raise NotImplementedError


# def rule_to_boto_expression(rule: Rule, key_name: Optional[str] = None):
#     return expression_to_condition(rule.statement.expression, key_name)


class Backend:
    def __init__(self, cls):
        self.settings = Settings()
        self.schema = cls.schema()
        self.hash_key = cls.Config.hash_key
        self.table_name = cls.get_table_name()

        key_hash = sha256()
        key_hash.update(self.settings.API_KEY.encode())
        self.collection_id = f'SERVICE.CASCADE.{key_hash.hexdigest()}'

        self.client = Client(
            base_url=self.settings.BASE_URL,
            headers={
                "Authorization": f"X-API-Key {self.settings.API_KEY}"  # _HB7eEuE04wfXylAQ9FRljH529CqGjxKLOGR
            }
        )

    def create_collection(self, project):
        data = {
            "name": f"cascade_{project.key}",
            "description": f"Cascade Project: {project.key}",
            "users": {},
            "roles": {
                f"{project.key}_reader": {
                    "read": True,
                    "write": False,
                    "admin": False
                },
                f"{project.key}_writer": {
                    "read": True,
                    "write": True,
                    "admin": False
                },
                f"{project.key}_admin": {
                    "read": True,
                    "write": True,
                    "admin": True
                },
            }
        }
        res = self.client.put(f'/collections/{self.collection_id}', json=data)
        res_data = res.json()
        print(f"Creating for {self.collection_id}: {res.status_code}")
        return res.status_code == 200

    def initialize(self):
        data = {
            "name": "cascade",
            "description": "Cascade Project",
            "users": {},
            "roles": {}
        }
        res = self.client.put(f'/collections/{self.collection_id}', json=data)
        print(f"Creating for {self.collection_id}: {res.status_code}")
        return res.status_code == 200

    def exists(self):
        res = self.client.get(f'/collections/{self.collection_id}')
        print(f"Checking for {self.table_name}: {res.status_code}")
        return res.status_code == 200

    def query(self, expression):
        pass
        # # self.client.
        # # fields = tuple(self.sql_field_defs(cls).keys())
        # c = self._conn.cursor()
        # expression, params = rule_to_sqlite_expression(expression)
        # c.execute(f"select * from {self.table_name} where {expression};", params)
        # res = list(c.fetchall())
        # c.close()
        # schema = self.schema['properties']
        # fields = list(schema.keys())
        # return [
        #     {k: DESERIALIZE_MAP[schema[k]['type']](v) for k, v in zip(fields, rec)}
        #     for rec in res
        # ]

    def get(self, item_key):
        pass
        # c = self._conn.cursor()
        # c.execute(f"select * from {self.table_name} where {self.hash_key} = ?;", [item_key])
        # res = c.fetchone()
        # c.close()
        # if not res:
        #     raise DoesNotExist
        # schema = self.schema['properties']
        # fields = list(schema.keys())
        # return {k: DESERIALIZE_MAP[schema[k]['type']](v) for k, v in zip(fields, res)}

    def save(self, item, condition: Optional[Rule] = None) -> bool:
        return True
        # table_name = item.get_table_name()
        # hash_key = item.Config.hash_key
        # key = getattr(item, hash_key)
        # fields_def = self.sql_field_defs(item.__class__)
        # fields = tuple(fields_def.keys())
        #
        # schema = item.schema()['properties']
        # item_data = item.dict()
        # values = tuple([SERIALIZE_MAP[schema[field]['type']](item_data[field]) for field in fields])
        # try:
        #     old_item = self.get(item.__class__, key)
        #     if not condition.matches(old_item):
        #         raise ConditionCheckFailed()
        #
        #     qs = ', '.join(f"{field} = ?" for field in fields)
        #     if condition:
        #         condition_expr, condition_params = rule_to_sqlite_expression(condition)
        #     else:
        #         condition_expr = f"{hash_key} = ?"
        #         condition_params = tuple(key)
        #
        #     self._conn.execute(f"UPDATE {table_name} SET {qs} WHERE {condition_expr};", values + condition_params)
        #     return True
        # except DoesNotExist:
        #     qs = ','.join(['?'] * len(fields))
        #     self._conn.execute(f"insert into {table_name} values ({qs})", values)
        # return True

    def delete(self, item_key: str):
        pass
        # self._conn.execute(f"DELETE FROM {self.table_name} WHERE {self.hash_key} = ?;", [item_key])
