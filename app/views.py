from flask import request, jsonify
from app import create_app, db
from models import Employee, employeeschema
import requests

app = create_app()


@app.route("/syncemployee")
def fetch():
    url = "https://dummy.restapiexample.com/api/v1/employees"
    response = requests.get(url.text)
    datas = response.json()
    for data in datas["data"]:
        new_emp = Employee(
            id=data["id"],
            employee_name=data["employee_name"],
            employee_salary=data["employee_salary"],
            employee_age=data["employee_age"],
        )
        db.session.add(new_emp)

    db.session.commit()
    return "Employee stored successfully"


@app.route("/employees/", methods=["GET"])
@app.route("/employees/<int:id>/", methods=["GET"])
def get_employee(id=None):
    employees = Employee.query
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    search = request.args.get("search")
    employee_age = request.args.get("employee_age", type=int)

    if id:
        employees = Employee.query.filter(Employee.id == id)

    if search:
        search_query = f"%{search}%"
        employees = employees.filter(Employee.name.ilike(search_query))

    if employee_age:
        employees = employees.filter(Employee.employee_age == employee_age)

    employees = employees.order_by(getattr(getattr(Employee, sort), order)())

    return {
        "success": True,
        "pokemons": employeeschema.dump(employees),
        "message": "Pokemon retrieved successfully.",
    }, 200


@app.route("/employees/", methods=["DELETE"])
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id=None):
    if id:
        employee = Employee.query.get(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"success": True, "message": "Record Deleted"})
    deleteEmployee = request.json
    names_to_delete = [name.capitalize() for name in deleteEmployee]
    employees = Employee.query.filter(Employee.name.in_(names_to_delete)).delete()
    db.session.commit()
    return (
        jsonify(
            {"success": True, "message": f"{len(names_to_delete)} records Deleted"}
        ),
        200,
    )
