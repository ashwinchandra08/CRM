-- Create Customer table

create database crmnew;
use crmnew;
CREATE TABLE customer (
    Cust_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Address VARCHAR(100),
    Phone_No INT
);

-- Create Product table
CREATE TABLE product (
    Prod_ID INT PRIMARY KEY,
    Type VARCHAR(100),
    Details VARCHAR(100),
    Brand VARCHAR(100),
    Model VARCHAR(100),
    Price INT
);

-- Create Salesman table
CREATE TABLE salesman (
    S_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Phone_No INT,
    Email VARCHAR(100) UNIQUE,
    Position VARCHAR(100),
    Territory VARCHAR(100),
    password VARCHAR(1000)
);




-- Create Transaction table
CREATE TABLE transaction (
    T_ID INT PRIMARY KEY,
    Prod_ID INT,
    Cust_ID INT,
    Date DATE,
    Quantity INT,
    Amount FLOAT,
    FOREIGN KEY (Prod_ID) REFERENCES product (Prod_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Cust_ID) REFERENCES customer (Cust_ID) ON UPDATE CASCADE ON DELETE CASCADE
    
);
-- Drop the foreign key constraint


ALTER TABLE transaction
MODIFY COLUMN T_ID INT AUTO_INCREMENT;
ALTER TABLE complaint
DROP FOREIGN KEY complaint_ibfk_2;
ALTER TABLE complaint
ADD CONSTRAINT complaint_ibfk_2 FOREIGN KEY (transaction_id) REFERENCES transaction (T_ID);



-- Create Complaint table
CREATE TABLE complaint (
    Comp_ID INT PRIMARY KEY,
    Cust_ID INT,
    Details VARCHAR(100),
    Date DATE,
    Transaction_ID INT,
    Current_Status VARCHAR(100),
    FOREIGN KEY (Cust_ID) REFERENCES customer (Cust_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Transaction_ID) REFERENCES transaction (T_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create Trig table
CREATE TABLE trig (
    tid INT PRIMARY KEY,
    rollno VARCHAR(100),
    action VARCHAR(100),
    timestamp VARCHAR(100)
);


-- Insert statements for Customer table
INSERT INTO customer (Cust_ID, Name, Address, Phone_No) VALUES
(1, 'John Doe', '123 Main St', '5551234'),
(2, 'Jane Smith', '456 Oak St', '5555678'),
(3, 'Bob Johnson', '789 Pine St', '5559012'),
(4, 'Alice Williams', '101 Maple St', '5553456'),
(5, 'Charlie Brown', '202 Birch St', '5557890');

-- Insert statements for Product table
INSERT INTO product (Prod_ID, Name, Details, Brand, Model, Price) VALUES
(1, 'Laptop', 'High-performance laptop', 'Dell', 'XPS 13', 1200.00),
(2, 'Smartphone', 'Latest smartphone', 'Samsung', 'Galaxy S21', 900.00),
(3, 'TV', '4K Ultra HD TV', 'Sony', 'Bravia OLED', 1500.00),
(4, 'Headphones', 'Noise-canceling headphones', 'Bose', 'QuietComfort 35 II', 300.00),
(5, 'Camera', 'Mirrorless camera', 'Canon', 'EOS R5', 2500.00);

-- Insert statements for Salesman table
INSERT INTO salesman (S_ID, Name, Phone_No, Email, Position, Territory, password) VALUES
(1, 'Salesman1', '5551111', 'salesman1@example.com', 'Senior Sales', 'North', 'password1'),
(2, 'Salesman2', '5552222', 'salesman2@example.com', 'Junior Sales', 'South', 'password2'),
(3, 'Salesman3', '5553333', 'salesman3@example.com', 'Senior Sales', 'East', 'password3'),
(4, 'Salesman4', '5554444', 'salesman4@example.com', 'Junior Sales', 'West', 'password4'),
(5, 'Salesman5', '5555555', 'salesman5@example.com', 'Senior Sales', 'Central', 'password5');

-- Insert statements for Transaction table
INSERT INTO transaction (T_ID, Prod_ID, Cust_ID, Date, S_ID, Quantity, Amount) VALUES
(1, 1, 1, '2023-11-01',  2, 2400.00),
(2, 2, 2, '2023-11-02',  1, 900.00),
(3, 3, 3, '2023-11-03',  3, 4500.00),
(4, 4, 4, '2023-11-04',  1, 300.00),
(5, 5, 5, '2023-11-05',  2, 5000.00);

-- Insert statements for Complaint table
INSERT INTO complaint (Comp_ID, Cust_ID, Details, Date, Transaction_ID, Current_Status) VALUES
(1, 1, 'Defective product', '2023-11-01', 1, 'Pending'),
(2, 2, 'Late delivery', '2023-11-02', 2, 'Pending'),
(3, 3, 'Missing accessories', '2023-11-03', 3, 'Pending'),
(4, 4, 'Product not as described', '2023-11-04', 4, 'Pending'),
(5, 5, 'Refund request', '2023-11-05', 5, 'Pending');
DELIMITER //
CREATE PROCEDURE GetCustomerDetails(IN custID INT)
BEGIN
    SELECT * FROM Customer WHERE Cust_ID = custID;
END //
DELIMITER ;

DELIMITER //
CALL GetCustomerDetails(0);
CREATE PROCEDURE GetAllCustomers()
BEGIN
    SELECT * FROM Customer;
END //

DELIMITER ;




CREATE VIEW customer_transaction_new AS
SELECT
    c.Cust_ID,
    c.Name AS Customer_Name,
    c.Address AS Customer_Address,
    c.Phone_No AS Customer_Phone_No,
    p.Type AS Purchased_Product_Type,
    p.Brand AS Brand,
    p.Model AS Model
FROM
    customer c
JOIN
    transaction t ON c.Cust_ID = t.Cust_ID
JOIN
    product p ON t.Prod_ID = p.Prod_ID;
    

DELIMITER //
CREATE TRIGGER before_transaction_insert
BEFORE INSERT ON transaction
FOR EACH ROW
BEGIN
    -- Your trigger logic here
    -- For example, you can update the Date field before inserting a new transaction

    -- Retrieve the Price from the product table based on the Prod_ID
    SET NEW.Amount = (
        SELECT product.Price
        FROM product
        WHERE product.Prod_ID = NEW.Prod_ID
    ) * NEW.Quantity;
    
    SET NEW.Date = NOW();

    -- Increment the T_ID based on the previous one
    SET NEW.T_ID = (
        SELECT MAX(T_ID) + 1
        FROM transaction
    );

    -- If there is no previous T_ID, set it to 1
    IF NEW.T_ID IS NULL THEN
        SET NEW.T_ID = 1;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_customer_delete
BEFORE DELETE ON customer
FOR EACH ROW
BEGIN
    -- Delete related transactions when a customer is deleted
    DELETE FROM transaction WHERE Cust_ID = OLD.Cust_ID;
END;
//
DELIMITER ;





--  this is for displaying all products that have compaints registered against them--
DELIMITER //
CREATE PROCEDURE GetProductDetails(IN productBrand VARCHAR(100))
BEGIN
    SELECT * FROM product WHERE Brand = productBrand;
END //
DELIMITER ;
CALL GetProductDetails('Dell');
-- ok--
drop procedure GetProductComplaints;
drop procedure GetProductComplaintByBrand;
DELIMITER //
CREATE PROCEDURE GetProductComplaintByBrand(IN brandName VARCHAR(100))
BEGIN
    SELECT p.*, c.Details,c.Date,C.Current_Status
    FROM product p
    JOIN transaction t ON p.Prod_ID = t.Prod_ID
    JOIN complaint c ON t.T_ID = c.Transaction_ID
    WHERE p.Brand = brandName ;
END //

DELIMITER ;

CALL GetProductComplaintByBrand('Dell');






