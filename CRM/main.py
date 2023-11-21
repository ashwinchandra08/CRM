from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify  
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date,ForeignKey,Float,text
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
from datetime import datetime
from sqlalchemy.orm import exc

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key=''


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_S_ID):
    return Salesman.query.get(int(user_S_ID))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']=''
db=SQLAlchemy(app)

# here we will create db models that is tables

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

# Create db models (tables) for your CRM project
class Complaint(db.Model):
    Comp_ID = db.Column(db.Integer, primary_key=True)
    Cust_ID = db.Column(db.Integer, ForeignKey('customer.Cust_ID'))
    Details = db.Column(db.String(100))
    Date = db.Column(Date)
    Transaction_ID = db.Column(db.Integer, ForeignKey('transaction.T_ID'))
    Current_Status = db.Column(db.String(100))
    Prod_ID = db.Column(db.Integer,ForeignKey('product.Prod_ID'))

class Customer(db.Model):
    Cust_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name=db.Column(db.String(100))
    Address = db.Column(db.String(100))
    Phone_No = db.Column(db.Integer)
    # Define other attributes for the Customer table (e.g., Name, Email, etc.)

class Product(db.Model):
    Prod_ID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(100))
    Details = db.Column(db.String(100))
    Brand = db.Column(db.String(100))
    Model = db.Column(db.String(100))
    Price = db.Column(db.Float)  # Ensure this is a float column



class Salesman(UserMixin,db.Model):
    S_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))
    Phone_No = db.Column(db.Integer)
    Email=db.Column(db.String(100),unique=True)
    Position=db.Column(db.String(100))
    Territory=db.Column(db.String(100))
    password=db.Column(db.String(1000))
    def get_id(self):
        return str(self.S_ID)


    # Define other attributes for the Salesman table

class Transaction(db.Model):
    T_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Prod_ID = db.Column(db.Integer,ForeignKey('product.Prod_ID'))
    Cust_ID = db.Column(db.Integer, ForeignKey('customer.Cust_ID'))
    Date = db.Column(Date)
    #S_ID = db.Column(db.Integer, ForeignKey('salesman.S_ID'))
    Quantity = db.Column(db.Integer)
    Amount = db.Column(db.Float)
    #product = db.relationship('Product', backref='transactions')
    # Define attributes for the Transaction table
'''
class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))
'''
'''
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
'''



'''
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(50))
    sname=db.Column(db.String(50))
    sem=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    branch=db.Column(db.String(50))
    email=db.Column(db.String(50))
    number=db.Column(db.String(12))
    address=db.Column(db.String(100))
    '''

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/customerdetails')
def studentdetails():
    #query=db.session.execute(text("CALL GetAllCustomers();") )
    query=db.session.execute(text("SELECT * FROM customer_transaction_new Order by Cust_ID;"))
    #query=Customer.query.all() 
    return render_template('studentdetails.html',query=query)

'''
@app.route('/triggers')
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=Trig.query.all()
    return render_template('triggers.html',query=query)
'''
'''
@app.route('/complaints',methods=['POST','GET'])
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=Product.query.filter_by(branch=dept).first()
        if query:
            flash("Product Already Exist","warning")
            return redirect('/complaints')
        dep=Product(branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Product Added","success")
    return render_template('department.html')
'''
@app.route('/complaints',methods=['POST','GET'])
def complaints():
    #query=Complaint.query.all() 
    query = db.session.query(
        Customer.Cust_ID,
        Customer.Name,
        Product.Brand,
        Product.Model,
        Complaint.Details,
        Complaint.Date,
        Complaint.Current_Status
    ) \
        .join(Customer, Complaint.Cust_ID == Customer.Cust_ID) \
        .join(Product, Complaint.Prod_ID == Product.Prod_ID) \
        .all()
    return render_template('complaint.html', query=query)


'''
@app.route('/addtransaction',methods=['POST','GET'])
def Transaction():
    # query=db.engine.execute(f"SELECT * FROM `student`") 
    query=Customer.query.all()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        attend=request.form.get('attend')
        print(attend,rollno)
        atte=Transaction(rollno=rollno,attendance=attend)
        db.session.add(atte)
        db.session.commit()
        flash("Transaction added","warning")

        
    return render_template('attendance.html',query=query)
'''

@app.route('/search',methods=['POST','GET'])


def search():
    if request.method == "POST":
        Brand = request.form.get('Brand')
        try:
            with db.session.begin() as session:
                query = db.session.execute(
                    text("CALL GetProductComplaintByBrand(:Brand)"), {"Brand": Brand}
                )
                products_and_complaints = query.fetchall()
                print("Products and Complaints:", products_and_complaints)
                if not products_and_complaints:
                    flash(f"No complaints found for the brand: {Brand}", "warning")
                return render_template('search.html', products_and_complaints=products_and_complaints)
        except Exception as e:
            print("Error:", e)
            flash("An error occurred while retrieving data", "danger")
    return render_template('search.html')




@app.route("/delete/<string:Cust_ID>",methods=['POST','GET'])
@login_required
def delete_customer_and_transactions(Cust_ID):
    try:
        # Retrieve the customer
        customer = Customer.query.filter_by(Cust_ID=Cust_ID).first()

        if not customer:
            flash("Customer not found", "warning")
            return redirect('/customerdetails')

        # Retrieve related transactions
        transactions = Transaction.query.filter_by(Cust_ID=Cust_ID).all()

        # Now delete the customer and related transactions
        db.session.delete(customer)

        # Delete related transactions
        for transaction in transactions:
            db.session.delete(transaction)

        db.session.commit()

        flash("Customer and related transactions deleted successfully", "danger")

    except exc.NoResultFound:
        flash("Customer not found", "warning")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")

    return redirect('/customerdetails')




@app.route("/edit/<string:Cust_ID>",methods=['POST','GET'])
@login_required
def edit(Cust_ID):
    if request.method == "POST":
        #Cust_ID = request.form.get('Cust_ID')
        Name = request.form.get('Name')
        Address = request.form.get('Address')
        Phone_No = request.form.get('Phone_No')

        # Check if the record exists
        post = Customer.query.filter_by(Cust_ID=Cust_ID).first()
        if post:
            # Update the record if it exists
            post.Cust_ID = Cust_ID
            post.Name = Name
            post.Address = Address
            post.Phone_No = Phone_No
            db.session.commit()
            flash("Slot is Updated", "success")
            return redirect('/customerdetails')
        else:
            flash("Record not found", "error")
            return redirect('/customerdetails')

    dept = Product.query.all()
    posts = Customer.query.filter_by(Cust_ID=Cust_ID).first()
    return render_template('edit.html', posts=posts, dept=dept)


@app.route("/editstatus/<string:Cust_ID>",methods=['POST','GET'])
@login_required
def editstatus(Cust_ID):
    if request.method == "POST":
        Current_Status = request.form.get('Current_Status')
        post = Complaint.query.filter_by(Cust_ID=Cust_ID).first()
        post.Current_Status = Current_Status
        db.session.commit()
        flash("Status is updated", "success")
        return redirect('/complaints')
        # Send the updated status back to the clien

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        Name=request.form.get('Name')
        Email=request.form.get('Email')
        Phone_No = request.form.get("Phone_No")
        Position = request.form.get("Position")
        Territory = request.form.get("Territory")
        password=request.form.get('password')
        encpassword=generate_password_hash(password)

        user=Salesman.query.filter_by(Email=Email).first()
        if user:
            flash("Email Already Exists","warning")
            return render_template('/signup.html')

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=Salesman(Name=Name,Phone_No = Phone_No,Email=Email,Position=Position,Territory=Territory, password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Success Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        Email=request.form.get('Email')
        password=request.form.get('password')
        user=Salesman.query.filter_by(Email=Email).first()

        if user and password:
            login_user(user)
            flash("Login Success", "primary")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
            return render_template('login.html')
 

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash("Logout Successul","warning")
    return redirect(url_for('login'))


'''
@app.route('/addcustomer',methods=['POST','GET'])
@login_required
def addstudent():
    # dept=db.engine.execute("SELECT * FROM `department`")
    dept=Product.query.all()
    if request.method=="POST":
        Cust_ID=request.form.get('Cust_ID')
        Name=request.form.get('Name')
        Address=request.form.get('Address')
        Phone_No=request.form.get('Phone_No')
        # query=db.engine.execute(f"INSERT INTO `student` (`rollno`,`sname`,`sem`,`gender`,`branch`,`email`,`number`,`address`) VALUES ('{rollno}','{sname}','{sem}','{gender}','{branch}','{email}','{num}','{address}')")
        query=Customer(Cust_ID = Cust_ID,Name = Name,Address=Address,Phone_No=Phone_No)
        db.session.add(query)
        db.session.commit()

        flash("Customer Added","info")


    return render_template('student.html',dept=dept)

'''
'''
@app.route('/addcustomer', methods=['POST', 'GET'])
@login_required
def addstudent():
    # Retrieve the last Cust_ID from the database
    last_customer = Customer.query.order_by(Customer.Cust_ID.desc()).first()
    # Set the initial Cust_ID to 1 if there are no existing customers
    if last_customer:
        initial_cust_id = last_customer.Cust_ID + 1
    else:
        initial_cust_id = 1
    dept = Product.query.all()
    if request.method == "POST":
        # Increment the Cust_ID for the new customer
        Cust_ID = initial_cust_id
        Name = request.form.get('Name')
        Address = request.form.get('Address')
        Phone_No = request.form.get('Phone_No')
        # Create and add the new customer to the database
        new_customer = Customer(Cust_ID=Cust_ID, Name=Name, Address=Address, Phone_No=Phone_No)
        db.session.add(new_customer)
        db.session.commit()
        flash("Customer Added", "info")
    return render_template('student.html', dept=dept)

'''


@app.route('/addcustomer', methods=['POST', 'GET'])
@login_required
def add_customer():
    if request.method == "POST":
        try:
            # Retrieve customer details from the form
            name = request.form.get('Name')
            address = request.form.get('Address')
            phone_no = request.form.get('Phone_No')

            # Check if a customer with the same name and phone number already exists
            existing_customer = Customer.query.filter_by(Name=name, Phone_No=phone_no).first()

            if existing_customer:
                # If the customer already exists, retrieve the existing customer's Cust_ID
                cust_id = existing_customer.Cust_ID
            else:
                # If the customer doesn't exist, create and add the new customer to the database
                new_customer = Customer(Name=name, Address=address, Phone_No=phone_no)
                db.session.add(new_customer)
                db.session.commit()

                # Fetch the newly added customer from the database to get the updated Cust_ID
                new_customer = Customer.query.filter_by(Name=name, Phone_No=phone_no).first()
                cust_id = new_customer.Cust_ID

            # Retrieve product details from the form
            prod_id = int(request.form.get('existing_product'))

            # Retrieve additional transaction details from the form
            quantity = int(request.form.get('Quantity'))

            # Create and add the new transaction to the database
            new_transaction = Transaction(Prod_ID=prod_id, Cust_ID=cust_id, Quantity=quantity)
            db.session.add(new_transaction)
            db.session.commit()

            flash("Customer and Transaction Added", "info")

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect('/addcustomer')

    # Retrieve the products for rendering the template
    products = Product.query.all()
    return render_template('student.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html', user=current_user)  # Pass the user variable if using Flask-Login

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    