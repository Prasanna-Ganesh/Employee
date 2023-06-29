from app import db, create_app
from dataclasses import dataclass
from marshmallow import Schema, fields


@dataclass
class Employee(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_name: str = db.Column(db.Text, nullable=False)
    employee_salary: int = db.Column(db.Integer, nullable=False)
    employee_age: int = db.Column(db.Integer, nullable=False)


class Employeeschema(Schema):
    id = fields.Int(dumps=True)
    employee_name = fields.Str()
    employee_salary = fields.Int()
    employee_age = fields.Int()


employeeschema = Employeeschema(many=True)
