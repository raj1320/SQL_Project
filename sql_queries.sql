-- ============================================
-- SQL QUERIES - HOSPITAL PATIENT ANALYTICS
-- Intermediate Level - Altera Digital Health
-- ============================================

-- ====================
-- BASIC QUERIES
-- ====================

-- Query 1: List all patients with their contact information
SELECT 
    PatientID,
    CONCAT(FirstName, ' ', LastName) AS PatientName,
    DateOfBirth,
    PhoneNumber,
    EmailAddress,
    RegistrationDate
FROM Patients
ORDER BY RegistrationDate DESC;

-- Query 2: Get all doctors in Cardiology department with their experience
SELECT 
    DoctorID,
    CONCAT(FirstName, ' ', LastName) AS DoctorName,
    Specialization,
    YearsOfExperience,
    ContactNumber
FROM Doctors
WHERE DepartmentID = 1
ORDER BY YearsOfExperience DESC;

-- Query 3: Find all hospital visits from February 2026
SELECT 
    VisitID,
    PatientID,
    DoctorID,
    VisitDate,
    VisitType,
    VisitStatus
FROM HospitalVisits
WHERE MONTH(VisitDate) = 2 AND YEAR(VisitDate) = 2026
ORDER BY VisitDate DESC;

-- ====================
-- JOINS - CRITICAL SKILL
-- ====================

-- Query 4: INNER JOIN - Get patient details with their latest visit information
SELECT 
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    hv.VisitDate,
    hv.DiagnosisCode,
    hv.VisitType,
    d.DepartmentName
FROM Patients p
INNER JOIN HospitalVisits hv ON p.PatientID = hv.PatientID
INNER JOIN Departments d ON hv.DepartmentID = d.DepartmentID
ORDER BY hv.VisitDate DESC;

-- Query 5: LEFT JOIN - Get all patients and their visits (including those with no visits)
SELECT 
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    p.RegistrationDate,
    hv.VisitID,
    hv.VisitDate,
    COALESCE(hv.VisitType, 'No Visit') AS VisitType
FROM Patients p
LEFT JOIN HospitalVisits hv ON p.PatientID = hv.PatientID
ORDER BY p.PatientID, hv.VisitDate DESC;

-- Query 6: INNER JOIN - Doctor with patient details and visit information
SELECT 
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    doc.Specialization,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    hv.VisitDate,
    hv.VisitType,
    dep.DepartmentName
FROM Doctors doc
INNER JOIN HospitalVisits hv ON doc.DoctorID = hv.DoctorID
INNER JOIN Patients p ON hv.PatientID = p.PatientID
INNER JOIN Departments dep ON doc.DepartmentID = dep.DepartmentID
ORDER BY doc.DoctorID, hv.VisitDate DESC;

-- ====================
-- GROUP BY & AGGREGATIONS
-- ====================

-- Query 7: Count total visits per department
SELECT 
    d.DepartmentID,
    d.DepartmentName,
    COUNT(hv.VisitID) AS TotalVisits,
    COUNT(DISTINCT hv.PatientID) AS UniquePatients
FROM Departments d
LEFT JOIN HospitalVisits hv ON d.DepartmentID = hv.DepartmentID
GROUP BY d.DepartmentID, d.DepartmentName
ORDER BY TotalVisits DESC;

-- Query 8: Average billing amount by visit type
SELECT 
    hv.VisitType,
    COUNT(*) AS NumberOfVisits,
    AVG(b.BillingAmount) AS AvgBillingAmount,
    MIN(b.BillingAmount) AS MinAmount,
    MAX(b.BillingAmount) AS MaxAmount,
    SUM(b.BillingAmount) AS TotalRevenue
FROM HospitalVisits hv
INNER JOIN Billing b ON hv.VisitID = b.VisitID
GROUP BY hv.VisitType
ORDER BY TotalRevenue DESC;

-- Query 9: Count visits by doctor and department
SELECT 
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    d.DepartmentName,
    COUNT(hv.VisitID) AS VisitsCompleted
FROM Doctors doc
LEFT JOIN Departments d ON doc.DepartmentID = d.DepartmentID
LEFT JOIN HospitalVisits hv ON doc.DoctorID = hv.DoctorID
GROUP BY doc.DoctorID, CONCAT(doc.FirstName, ' ', doc.LastName), d.DepartmentName
ORDER BY VisitsCompleted DESC;

-- Query 10: Billing summary by payment status
SELECT 
    PaymentStatus,
    COUNT(*) AS NumberOfBills,
    AVG(BillingAmount) AS AvgAmount,
    SUM(BillingAmount) AS TotalAmount
FROM Billing
GROUP BY PaymentStatus
ORDER BY TotalAmount DESC;

-- ====================
-- HAVING CLAUSE (Filtering Groups)
-- ====================

-- Query 11: Departments with more than 2 visits in February 2026
SELECT 
    d.DepartmentName,
    COUNT(hv.VisitID) AS VisitCount
FROM Departments d
LEFT JOIN HospitalVisits hv ON d.DepartmentID = hv.DepartmentID
    AND MONTH(hv.VisitDate) = 2 
    AND YEAR(hv.VisitDate) = 2026
GROUP BY d.DepartmentName
HAVING COUNT(hv.VisitID) > 1
ORDER BY VisitCount DESC;

-- Query 12: Doctors with average visit billing > 2500
SELECT 
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    COUNT(hv.VisitID) AS TotalVisits,
    AVG(b.BillingAmount) AS AvgBillingAmount
FROM Doctors doc
LEFT JOIN HospitalVisits hv ON doc.DoctorID = hv.DoctorID
LEFT JOIN Billing b ON hv.VisitID = b.VisitID
GROUP BY doc.DoctorID, CONCAT(doc.FirstName, ' ', doc.LastName)
HAVING AVG(b.BillingAmount) > 2500
ORDER BY AvgBillingAmount DESC;

-- ====================
-- SUBQUERIES
-- ====================

-- Query 13: Find patients who have had more visits than the average
SELECT 
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    COUNT(hv.VisitID) AS VisitCount
FROM Patients p
INNER JOIN HospitalVisits hv ON p.PatientID = hv.PatientID
GROUP BY p.PatientID, CONCAT(p.FirstName, ' ', p.LastName)
HAVING COUNT(hv.VisitID) > (
    SELECT AVG(VisitCount)
    FROM (
        SELECT COUNT(*) AS VisitCount
        FROM HospitalVisits
        GROUP BY PatientID
    ) AS avg_visits
)
ORDER BY VisitCount DESC;

-- Query 14: Find departments with total billing above average
SELECT 
    d.DepartmentID,
    d.DepartmentName,
    SUM(b.BillingAmount) AS TotalBilling
FROM Departments d
LEFT JOIN HospitalVisits hv ON d.DepartmentID = hv.DepartmentID
LEFT JOIN Billing b ON hv.VisitID = b.VisitID
GROUP BY d.DepartmentID, d.DepartmentName
HAVING SUM(b.BillingAmount) > (
    SELECT AVG(TotalAmount)
    FROM (
        SELECT SUM(BillingAmount) AS TotalAmount
        FROM Billing
        GROUP BY (SELECT DepartmentID FROM HospitalVisits hv2 WHERE hv2.VisitID = Billing.VisitID)
    ) AS dept_avg
)
ORDER BY TotalBilling DESC;

-- Query 15: Get patients with pending visits
SELECT 
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    hv.VisitID,
    hv.VisitDate,
    hv.VisitStatus
FROM Patients p
WHERE p.PatientID IN (
    SELECT DISTINCT PatientID 
    FROM HospitalVisits 
    WHERE VisitStatus = 'Pending'
)
ORDER BY hv.VisitDate;

-- ====================
-- ADVANCED QUERIES - WINDOW FUNCTIONS
-- ====================

-- Query 16: Rank doctors by number of visits
SELECT 
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    doc.Specialization,
    COUNT(hv.VisitID) AS TotalVisits,
    RANK() OVER (ORDER BY COUNT(hv.VisitID) DESC) AS VisitRank
FROM Doctors doc
LEFT JOIN HospitalVisits hv ON doc.DoctorID = hv.DoctorID
GROUP BY doc.DoctorID, CONCAT(doc.FirstName, ' ', doc.LastName), doc.Specialization
ORDER BY VisitRank;

-- Query 17: Running total of billing amount by date
SELECT 
    BillingDate,
    SUM(BillingAmount) AS DailyTotal,
    SUM(SUM(BillingAmount)) OVER (ORDER BY BillingDate) AS RunningTotal
FROM Billing
GROUP BY BillingDate
ORDER BY BillingDate;

-- ====================
-- MULTI-TABLE ANALYTICS
-- ====================

-- Query 18: Patient billing history with visit details
SELECT 
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    hv.VisitDate,
    hv.VisitType,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    b.BillingAmount,
    b.PaymentStatus,
    b.BillingDate
FROM Patients p
INNER JOIN HospitalVisits hv ON p.PatientID = hv.PatientID
INNER JOIN Doctors doc ON hv.DoctorID = doc.DoctorID
INNER JOIN Billing b ON hv.VisitID = b.VisitID
ORDER BY p.PatientID, hv.VisitDate DESC;

-- Query 19: Medicine usage report with prescription details
SELECT 
    m.MedicineName,
    m.Manufacturer,
    COUNT(DISTINCT pr.PrescriptionID) AS PrescribedCount,
    SUM(pr.Quantity) AS TotalQuantityPrescribed,
    m.AvailableQuantity,
    m.UnitCost,
    (SUM(pr.Quantity) * m.UnitCost) AS EstimatedCost
FROM Medicines m
LEFT JOIN Prescriptions pr ON m.MedicineID = pr.MedicineID
GROUP BY m.MedicineID, m.MedicineName, m.Manufacturer, m.AvailableQuantity, m.UnitCost
ORDER BY PrescribedCount DESC;

-- Query 20: Bed utilization report by department
SELECT 
    d.DepartmentName,
    COUNT(*) AS TotalBeds,
    SUM(CASE WHEN b.BedStatus = 'Occupied' THEN 1 ELSE 0 END) AS OccupiedBeds,
    SUM(CASE WHEN b.BedStatus = 'Available' THEN 1 ELSE 0 END) AS AvailableBeds,
    SUM(CASE WHEN b.BedStatus = 'Under Maintenance' THEN 1 ELSE 0 END) AS MaintenanceBeds,
    ROUND(
        (SUM(CASE WHEN b.BedStatus = 'Occupied' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 
        2
    ) AS OccupancyPercentage
FROM Departments d
LEFT JOIN Beds b ON d.DepartmentID = b.DepartmentID
GROUP BY d.DepartmentID, d.DepartmentName
ORDER BY OccupancyPercentage DESC;

