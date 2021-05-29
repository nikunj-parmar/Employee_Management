from flask import Flask, render_template, flash, url_for, redirect, request
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/nikunj'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    emp = db.relationship('Employeesalary', backref='author', lazy=True)

    def __repr__(self):
        return f"Employee('{self.name}','{self.department}','{self.emp}')"


class Employeesalary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Empid = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return ('Salary : ' + str(self.salary))


@app.route("/")
@app.route("/home")
def home():
    empls = Employee.query.all()

    return render_template('index.html', title='Home', empls=empls)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Employee(name=form.name.data, department=form.department.data)
        db.session.add(user)
        db.session.commit()
        emp = Employeesalary(Empid=user.id, salary=form.salary.data)
        db.session.add(emp)
        db.session.commit()
        flash('Employee added successfully !!', category='success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form, legend = 'join Today')


@app.route("/employee/<int:employee_id>")
def employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee.html', employee=employee)


@app.route("/employee/<int:employee_id>/update", methods=["POST", "GET"])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    emp = Employeesalary.query.get_or_404(employee_id)

    form = RegistrationForm()
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.department = form.department.data
        emp.salary = form.salary.data
        db.session.commit()
        flash('Your Post has been updated!!', 'success')
        return redirect(url_for('employee', employee_id=employee.id))
    elif request.method == 'GET':
        form.name.data = employee.name
        form.department.data = employee.department
        form.salary.data = emp.salary

    return render_template('register.html', form=form, legend = 'Update Now')

@app.route("/employee/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    emp = Employeesalary.query.get_or_404(employee_id)


    db.session.delete(employee)
    db.session.delete(emp)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/servicedepartment")
def servicedepartment():
    emp = Employee.query.filter_by(department='The Service Department')
    return render_template('services.html', emp=emp)


@app.route("/managementdepartment")
def managementdepartment():
    emp = Employee.query.filter_by(department='Management Department')
    return render_template('management.html', emp=emp)


@app.route("/productiondepartment")
def productiondepartment():
    emp = Employee.query.filter_by(department='Production Department')
    return render_template('production.html', emp=emp)


@app.route("/financedepartment")
def financedepartment():
    emp = Employee.query.filter_by(department='Finance Department')
    return render_template('finance.html', emp=emp)


@app.route("/itdepartment")
def itdepartment():
    emp = Employee.query.filter_by(department='IT Department')
    return render_template('it.html', emp=emp)


if __name__ == '__main__':
    app.run(debug=True)