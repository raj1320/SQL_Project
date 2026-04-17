-- ============================================
-- PROJECT 1: HOSPITAL PATIENT MANAGEMENT SYSTEM
-- SQL Database Schema
-- Altera Digital Health - Healthcare Analytics
-- ============================================

-- Create Patients Table
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    PhoneNumber VARCHAR(15),
    EmailAddress VARCHAR(100),
    RegistrationDate DATE
);

-- Create Departments Table
CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(100),
    Location VARCHAR(100),
    HeadOfDepartment VARCHAR(100),
    BudgetAllocated DECIMAL(12,2)
);

-- Create Doctors Table
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Specialization VARCHAR(100),
    DepartmentID INT,
    ContactNumber VARCHAR(15),
    YearsOfExperience INT,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create Hospital Visits Table
CREATE TABLE HospitalVisits (
    VisitID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    DepartmentID INT,
    VisitDate DATE,
    DiagnosisCode VARCHAR(20),
    VisitType VARCHAR(50), -- 'Consultation', 'Emergency', 'Follow-up'
    TreatmentDescription TEXT,
    VisitStatus VARCHAR(20), -- 'Completed', 'Pending', 'Cancelled'
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Create Billing Table
CREATE TABLE Billing (
    BillingID INT PRIMARY KEY,
    VisitID INT,
    PatientID INT,
    BillingAmount DECIMAL(10,2),
    ConsultationFee DECIMAL(10,2),
    MedicineCharges DECIMAL(10,2),
    LabCharges DECIMAL(10,2),
    OtherCharges DECIMAL(10,2),
    BillingDate DATE,
    PaymentStatus VARCHAR(20), -- 'Paid', 'Pending', 'Partial'
    FOREIGN KEY (VisitID) REFERENCES HospitalVisits(VisitID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- Create Medicines Table
CREATE TABLE Medicines (
    MedicineID INT PRIMARY KEY,
    MedicineName VARCHAR(100),
    Manufacturer VARCHAR(100),
    UnitCost DECIMAL(8,2),
    AvailableQuantity INT,
    ExpiryDate DATE
);

-- Create Prescription Table
CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY,
    VisitID INT,
    PatientID INT,
    MedicineID INT,
    Quantity INT,
    Dosage VARCHAR(50),
    Frequency VARCHAR(50), -- 'Once daily', 'Twice daily', etc.
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (VisitID) REFERENCES HospitalVisits(VisitID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (MedicineID) REFERENCES Medicines(MedicineID)
);

-- Create Bed Management Table
CREATE TABLE Beds (
    BedID INT PRIMARY KEY,
    DepartmentID INT,
    BedType VARCHAR(50), -- 'ICU', 'General', 'Private'
    BedStatus VARCHAR(20), -- 'Available', 'Occupied', 'Under Maintenance'
    PatientID INT,
    AdmissionDate DATE,
    DischargeDate DATE,
    DailyCharge DECIMAL(10,2),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);

-- ============================================
-- SAMPLE DATA INSERTION
-- ============================================

-- Insert Departments
INSERT INTO Departments VALUES 
(1, 'Cardiology', 'Building A, 2nd Floor', 'Dr. Rajesh Kumar', 5000000),
(2, 'Orthopedics', 'Building B, 1st Floor', 'Dr. Priya Singh', 4500000),
(3, 'Neurology', 'Building A, 3rd Floor', 'Dr. Amit Patel', 4800000),
(4, 'Pediatrics', 'Building C, Ground Floor', 'Dr. Neha Sharma', 3500000),
(5, 'Emergency Medicine', 'Building A, 1st Floor', 'Dr. Vikram Verma', 6000000);

-- Insert Doctors
INSERT INTO Doctors VALUES 
(101, 'Rajesh', 'Kumar', 'Cardiologist', 1, '9876543210', 15),
(102, 'Priya', 'Singh', 'Orthopedic Surgeon', 2, '9876543211', 12),
(103, 'Amit', 'Patel', 'Neurologist', 3, '9876543212', 10),
(104, 'Neha', 'Sharma', 'Pediatrician', 4, '9876543213', 8),
(105, 'Vikram', 'Verma', 'Emergency Physician', 5, '9876543214', 7),
(106, 'Deepak', 'Nair', 'Cardiologist', 1, '9876543215', 9),
(107, 'Isha', 'Gupta', 'Orthopedic Surgeon', 2, '9876543216', 6);

-- Insert Patients
INSERT INTO Patients VALUES 
(1001, 'Rahul', 'Sharma', '1980-05-15', 'Male', '9876543217', 'rahul@email.com', '2026-01-10'),
(1002, 'Anjali', 'Verma', '1985-08-20', 'Female', '9876543218', 'anjali@email.com', '2026-01-15'),
(1003, 'Arun', 'Kumar', '1975-03-10', 'Male', '9876543219', 'arun@email.com', '2026-01-20'),
(1004, 'Divya', 'Singh', '1990-11-25', 'Female', '9876543220', 'divya@email.com', '2026-02-01'),
(1005, 'Vikrant', 'Patel', '1988-06-30', 'Male', '9876543221', 'vikrant@email.com', '2026-02-05'),
(1006, 'Priya', 'Nair', '1992-09-12', 'Female', '9876543222', 'priya@email.com', '2026-02-10'),
(1007, 'Manish', 'Gupta', '1978-04-08', 'Male', '9876543223', 'manish@email.com', '2026-02-15'),
(1008, 'Sneha', 'Reddy', '1995-12-03', 'Female', '9876543224', 'sneha@email.com', '2026-02-20');

-- Insert Hospital Visits
INSERT INTO HospitalVisits VALUES 
(501, 1001, 101, 1, '2026-02-15', 'I10.9', 'Consultation', 'Blood pressure monitoring and medication review', 'Completed'),
(502, 1002, 102, 2, '2026-02-14', 'M79.3', 'Consultation', 'Knee pain assessment', 'Completed'),
(503, 1003, 101, 1, '2026-02-13', 'I10.9', 'Follow-up', 'Cardiac follow-up post-procedure', 'Completed'),
(504, 1004, 105, 5, '2026-02-12', 'R05.9', 'Emergency', 'Fever and general weakness', 'Completed'),
(505, 1005, 103, 3, '2026-02-11', 'G89.29', 'Consultation', 'Chronic pain assessment', 'Completed'),
(506, 1006, 104, 4, '2026-02-10', 'Z00.00', 'Consultation', 'Regular health checkup', 'Completed'),
(507, 1007, 102, 2, '2026-02-09', 'M79.3', 'Follow-up', 'Post-treatment follow-up', 'Pending'),
(508, 1008, 106, 1, '2026-02-08', 'I10.9', 'Consultation', 'Heart condition check', 'Completed'),
(509, 1001, 105, 5, '2026-02-07', 'R06.0', 'Emergency', 'Difficulty breathing', 'Completed'),
(510, 1002, 107, 2, '2026-02-06', 'M79.3', 'Consultation', 'Joint pain consultation', 'Completed');

-- Insert Billing
INSERT INTO Billing VALUES 
(601, 501, 1001, 2500.00, 1000.00, 800.00, 500.00, 200.00, '2026-02-15', 'Paid'),
(602, 502, 1002, 3000.00, 1200.00, 1000.00, 600.00, 200.00, '2026-02-14', 'Paid'),
(603, 503, 1003, 4500.00, 1500.00, 1500.00, 1000.00, 500.00, '2026-02-13', 'Partial'),
(604, 504, 1004, 2000.00, 800.00, 700.00, 400.00, 100.00, '2026-02-12', 'Pending'),
(605, 505, 1005, 2800.00, 1000.00, 900.00, 600.00, 300.00, '2026-02-11', 'Paid'),
(606, 506, 1006, 1500.00, 800.00, 400.00, 200.00, 100.00, '2026-02-10', 'Paid'),
(607, 507, 1007, 2200.00, 900.00, 700.00, 400.00, 200.00, '2026-02-09', 'Pending'),
(608, 508, 1008, 3200.00, 1200.00, 1100.00, 700.00, 200.00, '2026-02-08', 'Paid');

-- Insert Medicines
INSERT INTO Medicines VALUES 
(2001, 'Aspirin 500mg', 'Cipla', 10.00, 500, '2027-06-30'),
(2002, 'Lisinopril 10mg', 'Lupin', 15.00, 300, '2027-05-15'),
(2003, 'Ibuprofen 400mg', 'Dr. Reddy', 8.00, 600, '2027-07-20'),
(2004, 'Metformin 1000mg', 'Novartis', 12.00, 400, '2027-04-10'),
(2005, 'Amoxicillin 500mg', 'Alembic', 20.00, 250, '2027-03-25'),
(2006, 'Vitamin D3 1000IU', 'Wyeth', 5.00, 800, '2027-08-30');

-- Insert Prescriptions
INSERT INTO Prescriptions VALUES 
(701, 501, 1001, 2002, 30, '10mg', 'Once daily', '2026-02-15', '2026-04-15'),
(702, 501, 1001, 2001, 30, '500mg', 'Twice daily', '2026-02-15', '2026-03-15'),
(703, 502, 1002, 2003, 20, '400mg', 'Twice daily for pain', '2026-02-14', '2026-02-24'),
(704, 505, 1005, 2004, 60, '1000mg', 'Twice daily', '2026-02-11', '2026-04-11'),
(705, 504, 1004, 2005, 10, '500mg', 'Thrice daily', '2026-02-12', '2026-02-22'),
(706, 506, 1006, 2006, 30, '1000IU', 'Once daily', '2026-02-10', '2026-05-10');

-- Insert Beds
INSERT INTO Beds VALUES 
(3001, 1, 'Private', 'Occupied', 1003, '2026-02-10', NULL, 5000.00),
(3002, 1, 'General', 'Available', NULL, NULL, NULL, 2500.00),
(3003, 2, 'General', 'Occupied', 1002, '2026-02-09', NULL, 2000.00),
(3004, 5, 'ICU', 'Occupied', 1004, '2026-02-12', NULL, 8000.00),
(3005, 3, 'General', 'Available', NULL, NULL, NULL, 2500.00),
(3006, 4, 'General', 'Available', NULL, NULL, NULL, 1500.00),
(3007, 2, 'Private', 'Occupied', 1007, '2026-02-05', NULL, 4000.00),
(3008, 1, 'General', 'Available', NULL, NULL, NULL, 2500.00);

