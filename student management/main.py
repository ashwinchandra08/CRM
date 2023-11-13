from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify  
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date,ForeignKey,Float,text
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
from datetime import datetime

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_S_ID):
    return Salesman.query.get(int(user_S_ID))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/project'
db=SQLAlchemy(app)

# here we will create db models that is tables

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

# Create db models (tables) for your CRM project
class Complaint(db.Model):
    Comp_ID = db.Column(db.Integer, primary_key=True)
    Cust_ID = db.Column(db.Integer)
    Details = db.Column(db.String(100))
    Date = db.Column(Date)
    Transaction_ID = db.Column(db.Integer)
    Current_Status = db.Column(db.String(100))
    Prod_ID = db.Column(db.Integer)

class Customer(db.Model):
    Cust_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(100))
    Phone_No = db.Column(db.Integer)

class Product(db.Model):
    Prod_ID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(100))
    Details = db.Column(db.String(100))
    Brand = db.Column(db.String(100))
    Model = db.Column(db.String(100))
    Price = db.Column(db.Float)


class Salesman(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Phone_No = db.Column(db.Integer)
    Email=db.Column(db.String(100),unique=True)
    Position=db.Column(db.String(100))
    Territory=db.Column(db.String(100))
    password=db.Column(db.String(1000))


    # Define other attributes for the Salesman table

class Transaction(db.Model):
    T_ID = db.Column(db.Integer, primary_key=True)
    Prod_ID = db.Column(db.Integer)
    Cust_ID = db.Column(db.Integer)
    Date = db.Column(Date)
    #S_ID = db.Column(db.Integer, ForeignKey('Salesman.S_ID'))
    Quantity = db.Column(db.Integer)
    Amount = db.Column(db.Float)
    # Define attributes for the Transaction table

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))

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

@app.route('/studentdetails')
def studentdetails():
    #query=db.session.execute(text("CALL GetAllCustomers();") )
    query=db.session.execute(text("SELECT * FROM customer_transaction;") )
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



@app.route('/addtransaction',methods=['POST','GET'])
def Transaction_2():
    # query=db.engine.execute(f"SELECT * FROM `student`") 
    query=Customer.query.all()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        attend=request.form.get('attend')
        print(attend,rollno)
        atte=Transaction(rollno=rollno,attendance=attend)
        db.session.add(atte)
        db.session.commit()
        flash("Attendance added","warning")

        
    return render_template('attendance.html',query=query)

@app.route('/search',methods=['POST','GET'])

def search():
    if request.method == "POST":
        Cust_ID = request.form.get('Cust_ID')
        if Cust_ID==0:
            return redirect('/studentdetails')
        try:
            # Use SQLAlchemy Session to execute the stored procedure GetCustomerDetails
            with db.session.begin() as session:
                # Use text construct to represent the SQL expression
                query = db.session.execute(text("CALL GetCustomerDetails(:Cust_ID)"), {"Cust_ID": Cust_ID})

                # Fetch the result set
                customer = query.fetchone()

                if customer is None:
                    flash("No customer found with the provided ID", "warning")
                    return render_template('search.html')

                # Log the result for debugging
                #current_app.logger.info(f"Retrieved customer details: {customer}")

                return render_template('search.html', customer=customer)
        except Exception as e:
            # Log any exceptions for debugging
            #current_app.logger.error(f"Error retrieving customer details: {e}")
            flash("An error occurred while retrieving customer details", "danger")
            raise  # Reraise the exception to see the full traceback in the console

    return render_template('search.html')

@app.route("/delete/<string:Cust_ID>",methods=['POST','GET'])
@login_required
def delete(Cust_ID):
    post=Customer.query.filter_by(Cust_ID=Cust_ID).first()
    post2 = Transaction.query.filter_by(Cust_ID=Cust_ID).first()
    post3 = Complaint.query.filter_by(Cust_ID=Cust_ID).first()
    db.session.delete(post)
    db.session.delete(post2)
    db.session.delete(post3)
    db.session.commit()
    # db.engine.execute(f"DELETE FROM `student` WHERE `student`.`id`={id}")
    flash("Customer Deleted Successfully","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:Cust_ID>",methods=['POST','GET'])
@login_required
def edit(Cust_ID):
    # dept=db.engine.execute("SELECT * FROM `department`")    
    if request.method=="POST":
        Cust_ID=request.form.get('Cust_ID')
        Name=request.form.get('Name')
        Address=request.form.get('Address')
        Phone_No=request.form.get('Phone_No')
        # query=db.engine.execute(f"UPDATE `student` SET `rollno`='{rollno}',`sname`='{sname}',`sem`='{sem}',`gender`='{gender}',`branch`='{branch}',`email`='{email}',`number`='{num}',`address`='{address}'")
        post=Customer.query.filter_by(Cust_ID=Cust_ID).first()
        post.Cust_ID=Cust_ID
        post.Name=Name
        post.Address=Address
        post.Phone_No=Phone_No
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/studentdetails')
    dept=Product.query.all()
    posts=Customer.query.filter_by(Cust_ID=Cust_ID).first()
    return render_template('edit.html',posts=posts,dept=dept)

@app.route("/editstatus/<string:Cust_ID>", methods=['POST', 'GET'])
@login_required
def editstatus(Cust_ID):
    if request.method == "POST":
        Current_Status = request.form.get('Current_Status')
        
        # Assuming there is a relationship between Customer and Complaint
        customer = Customer.query.filter_by(Cust_ID=Cust_ID).first()
        
        if customer:
            # Assuming there is a relationship between Customer and Complaint
            complaint = Complaint.query.filter_by(Cust_ID=customer.Cust_ID).first()

            if complaint:
                complaint.Current_Status = Current_Status
                db.session.commit()
                flash("Status is updated", "success")
                return redirect('/complaints')

    flash("Unable to update status", "error")
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
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        Email=request.form.get('Email')
        password=request.form.get('password')
        user=Salesman.query.filter_by(Email=Email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash("Logout Successul","warning")
    return redirect(url_for('login'))



@app.route('/addcustomer',methods=['POST','GET'])
@login_required
def add_student():
    # Retrieve the last Cust_ID from the database
    last_customer = Customer.query.order_by(Customer.Cust_ID.desc()).first()
    
    # Set the initial Cust_ID to 1 if there are no existing customers
    if last_customer:
        initial_cust_id = last_customer.Cust_ID + 1
    else:
        initial_cust_id = 1

    if request.method == "POST":
        # Get data from the form
        Cust_ID = initial_cust_id
        #t_ID = initial_cust_id
        name = request.form.get('Name')
        address = request.form.get('Address')
        phone_no = request.form.get('Phone_No')
        type_ = request.form.get('Type')
        brand = request.form.get('Brand')
        model = request.form.get('Model')
        details = request.form.get('Details')
        quantity = int(request.form.get('Quantity'))
        price = float(request.form.get('Price'))
        today_date = datetime.now().date()
        amount = quantity * price

        # Check if the product already exists in the Product table
        existing_product = Product.query.filter_by(Type=type_, Brand=brand, Model=model).first()

        if existing_product:
            # Use the existing Prod_ID if the product already exists
            Prod_ID = existing_product.Prod_ID
        else:
            # Create a new product if it doesn't exist
            new_product = Product(Type=type_, Details=details, Brand=brand, Model=model, Price=price)
            db.session.add(new_product)
            db.session.commit()
            Prod_ID = new_product.Prod_ID

        # Create instances of the Customer and Transaction models
        customer = Customer(Cust_ID=Cust_ID, Name=name, Address=address, Phone_No=phone_no)
        transaction = Transaction(Prod_ID=Prod_ID, Cust_ID=Cust_ID, Date=today_date, Quantity=quantity, Amount=amount)

        try:
            # Add instances to the session and commit changes
            db.session.add(customer)
            db.session.add(transaction)
            db.session.commit()

            flash("Customer and Product Added", "info")
        except Exception as e:
            # Handle exceptions, such as database errors
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")


    return render_template('student.html')
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    