================================================================================
PROJECT 3: PATIENT DATA PROCESSING PIPELINE
Python Data Cleaning & Analysis
Altera Digital Health - Healthcare Analytics
================================================================================

FILE: patient_data_cleaning.py

OVERVIEW:
This script demonstrates data cleaning techniques for a real healthcare dataset.
It handles common data quality issues found in hospital information systems.

================================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PatientDataCleaner:
    """
    Healthcare Patient Data Cleaning Pipeline
    Handles common data quality issues in hospital databases
    """
    
    def __init__(self, filepath):
        """Initialize with raw data file"""
        logger.info(f"Loading data from {filepath}")
        self.raw_data = pd.read_csv(filepath)
        self.cleaned_data = None
        self.data_quality_report = {}
        
    def load_and_inspect(self):
        """Inspect raw data structure and quality"""
        logger.info("=== DATA INSPECTION ===")
        
        print(f"\nDataset shape: {self.raw_data.shape}")
        print(f"Columns: {list(self.raw_data.columns)}")
        print(f"\nData types:\n{self.raw_data.dtypes}")
        print(f"\nFirst 5 rows:\n{self.raw_data.head()}")
        
        # Missing value analysis
        missing = self.raw_data.isnull().sum()
        missing_pct = (missing / len(self.raw_data)) * 100
        print(f"\nMissing values:\n{pd.DataFrame({'Count': missing, 'Percentage': missing_pct})}")
        
        return self
    
    # ====================
    # CLEANING FUNCTIONS
    # ====================
    
    def clean_patient_names(self):
        """
        Standardize patient names
        Issues: Extra spaces, inconsistent casing
        """
        logger.info("Cleaning patient names...")
        
        # Remove leading/trailing whitespace
        self.raw_data['PatientName'] = self.raw_data['PatientName'].str.strip()
        
        # Remove extra internal spaces
        self.raw_data['PatientName'] = self.raw_data['PatientName'].apply(
            lambda x: ' '.join(x.split()) if pd.notna(x) else x
        )
        
        # Standardize to Title Case
        self.raw_data['PatientName'] = self.raw_data['PatientName'].str.title()
        
        logger.info("✓ Patient names cleaned")
        return self
    
    def clean_dates(self):
        """
        Standardize date formats
        Issues: Multiple date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)
        """
        logger.info("Cleaning date fields...")
        
        def parse_date(date_str):
            """Parse multiple date formats"""
            if pd.isna(date_str):
                return pd.NaT
            
            date_str = str(date_str).strip()
            
            # Try common formats
            formats = [
                '%Y-%m-%d',    # 1980-05-15
                '%Y/%m/%d',    # 1980/05/15
                '%m/%d/%Y',    # 05/15/1980
                '%d/%m/%Y',    # 15/05/1980
                '%m-%d-%Y',    # 05-15-1980
            ]
            
            for fmt in formats:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except ValueError:
                    continue
            
            # If all formats fail, log and return NaT
            logger.warning(f"Could not parse date: {date_str}")
            return pd.NaT
        
        # Apply date parsing
        self.raw_data['DateOfBirth'] = self.raw_data['DateOfBirth'].apply(parse_date)
        self.raw_data['RegistrationDate'] = self.raw_data['RegistrationDate'].apply(parse_date)
        
        # Validate reasonable age range (0-150 years)
        today = pd.Timestamp.now()
        valid_dob = (today.year - self.raw_data['DateOfBirth'].dt.year >= 0) & \
                    (today.year - self.raw_data['DateOfBirth'].dt.year <= 150)
        
        invalid_count = (~valid_dob).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} invalid DOBs. Setting to NaT")
            self.raw_data.loc[~valid_dob, 'DateOfBirth'] = pd.NaT
        
        logger.info("✓ Dates standardized")
        return self
    
    def clean_gender(self):
        """
        Standardize gender values
        Issues: M/F, Male/Female, male/female inconsistency
        """
        logger.info("Cleaning gender field...")
        
        gender_mapping = {
            'M': 'Male',
            'F': 'Female',
            'MALE': 'Male',
            'FEMALE': 'Female',
            'Male': 'Male',
            'Female': 'Female',
        }
        
        self.raw_data['Gender'] = self.raw_data['Gender'].str.strip().str.upper()
        self.raw_data['Gender'] = self.raw_data['Gender'].map(gender_mapping)
        
        # Log invalid values
        invalid_gender = self.raw_data['Gender'].isnull().sum()
        if invalid_gender > 0:
            logger.warning(f"Found {invalid_gender} invalid gender values. Set to 'Unknown'")
            self.raw_data['Gender'].fillna('Unknown', inplace=True)
        
        logger.info("✓ Gender standardized")
        return self
    
    def clean_phone_numbers(self):
        """
        Standardize phone numbers
        Issues: Different formats, spaces, missing values
        """
        logger.info("Cleaning phone numbers...")
        
        def standardize_phone(phone):
            """Remove non-numeric characters and validate"""
            if pd.isna(phone) or phone == '':
                return np.nan
            
            # Convert to string and remove non-numeric
            phone_str = str(phone)
            digits_only = ''.join(filter(str.isdigit, phone_str))
            
            # Validate: Indian mobile is 10 digits
            if len(digits_only) == 10:
                return digits_only
            elif len(digits_only) == 12 and digits_only.startswith('91'):
                # Remove country code
                return digits_only[2:]
            else:
                logger.warning(f"Invalid phone format: {phone}")
                return np.nan
        
        self.raw_data['PhoneNumber'] = self.raw_data['PhoneNumber'].apply(standardize_phone)
        
        logger.info("✓ Phone numbers standardized")
        return self
    
    def clean_diagnosis_codes(self):
        """
        Standardize ICD-10 diagnosis codes
        Issues: Case sensitivity, extra spaces
        """
        logger.info("Cleaning diagnosis codes...")
        
        self.raw_data['DiagnosisCode'] = self.raw_data['DiagnosisCode'].str.strip()
        self.raw_data['DiagnosisCode'] = self.raw_data['DiagnosisCode'].str.upper()
        
        # Validate ICD-10 format (Letter followed by 2 digits, optional decimal, 2 digits)
        # Example: I10.9, M79.3
        valid_icd = self.raw_data['DiagnosisCode'].str.match(r'^[A-Z]\d{2}(\.\d{1,2})?$', na=False)
        
        invalid_count = (~valid_icd).sum()
        if invalid_count > 0:
            logger.warning(f"Found {invalid_count} invalid ICD-10 codes. Setting to 'UNKNOWN'")
            self.raw_data.loc[~valid_icd, 'DiagnosisCode'] = 'UNKNOWN'
        
        logger.info("✓ Diagnosis codes standardized")
        return self
    
    def clean_billing_amount(self):
        """
        Standardize billing amounts
        Issues: Missing values, non-numeric
        """
        logger.info("Cleaning billing amounts...")
        
        # Convert to numeric, coerce errors to NaN
        self.raw_data['BillingAmount'] = pd.to_numeric(
            self.raw_data['BillingAmount'], 
            errors='coerce'
        )
        
        # Validate positive amounts
        invalid_amounts = self.raw_data['BillingAmount'] < 0
        if invalid_amounts.sum() > 0:
            logger.warning(f"Found {invalid_amounts.sum()} negative billing amounts. Setting to NaN")
            self.raw_data.loc[invalid_amounts, 'BillingAmount'] = np.nan
        
        # Fill missing with median (healthcare context - typical visit cost)
        median_billing = self.raw_data['BillingAmount'].median()
        self.raw_data['BillingAmount'].fillna(median_billing, inplace=True)
        
        logger.info(f"✓ Billing amounts cleaned. Median amount: ₹{median_billing:.2f}")
        return self
    
    def clean_payment_status(self):
        """
        Standardize payment status values
        Issues: Case sensitivity, typos, invalid values
        """
        logger.info("Cleaning payment status...")
        
        payment_mapping = {
            'PAID': 'Paid',
            'Paid': 'Paid',
            'paid': 'Paid',
            'PENDING': 'Pending',
            'Pending': 'Pending',
            'pending': 'Pending',
            'PARTIAL': 'Partial',
            'Partial': 'Partial',
            'partial': 'Partial',
        }
        
        self.raw_data['PaymentStatus'] = self.raw_data['PaymentStatus'].str.strip()
        self.raw_data['PaymentStatus'] = self.raw_data['PaymentStatus'].map(payment_mapping)
        
        # Handle invalid values
        invalid_status = self.raw_data['PaymentStatus'].isnull().sum()
        if invalid_status > 0:
            logger.warning(f"Found {invalid_status} invalid payment statuses. Set to 'Unknown'")
            self.raw_data['PaymentStatus'].fillna('Unknown', inplace=True)
        
        logger.info("✓ Payment status standardized")
        return self
    
    def clean_doctor_names(self):
        """
        Standardize doctor names
        Issues: Case inconsistency, title inconsistency
        """
        logger.info("Cleaning doctor names...")
        
        # Standardize title format
        self.raw_data['DoctorName'] = self.raw_data['DoctorName'].str.strip()
        self.raw_data['DoctorName'] = self.raw_data['DoctorName'].str.title()
        
        # Remove extra spaces
        self.raw_data['DoctorName'] = self.raw_data['DoctorName'].apply(
            lambda x: ' '.join(x.split()) if pd.notna(x) else x
        )
        
        logger.info("✓ Doctor names standardized")
        return self
    
    def clean_department(self):
        """
        Standardize department names
        Issues: Case sensitivity, extra spaces
        """
        logger.info("Cleaning department names...")
        
        # Standard department names
        department_mapping = {
            'CARDIOLOGY': 'Cardiology',
            'Cardiology': 'Cardiology',
            'cardiology': 'Cardiology',
            'ORTHOPEDICS': 'Orthopedics',
            'Orthopedics': 'Orthopedics',
            'orthopedics': 'Orthopedics',
            'NEUROLOGY': 'Neurology',
            'Neurology': 'Neurology',
            'neurology': 'Neurology',
            'PEDIATRICS': 'Pediatrics',
            'Pediatrics': 'Pediatrics',
            'pediatrics': 'Pediatrics',
            'EMERGENCY MEDICINE': 'Emergency Medicine',
            'Emergency Medicine': 'Emergency Medicine',
            'EMERGENCY': 'Emergency Medicine',
            'Emergency': 'Emergency Medicine',
        }
        
        self.raw_data['Department'] = self.raw_data['Department'].str.strip()
        self.raw_data['Department'] = self.raw_data['Department'].map(department_mapping)
        
        invalid_dept = self.raw_data['Department'].isnull().sum()
        if invalid_dept > 0:
            logger.warning(f"Found {invalid_dept} invalid departments. Set to 'General'")
            self.raw_data['Department'].fillna('General', inplace=True)
        
        logger.info("✓ Departments standardized")
        return self
    
    def handle_duplicates(self):
        """
        Identify and handle duplicate records
        In healthcare: Same patient visiting multiple times (valid)
        But same visit recorded twice (invalid)
        """
        logger.info("Checking for duplicates...")
        
        # Create composite key (patient + date + doctor)
        # If these three match, likely duplicate
        duplicate_columns = ['PatientID', 'DateOfBirth', 'DoctorName', 'RegistrationDate']
        
        duplicates = self.raw_data.duplicated(subset=duplicate_columns, keep='first')
        duplicate_count = duplicates.sum()
        
        if duplicate_count > 0:
            logger.warning(f"Found {duplicate_count} duplicate records. Removing...")
            self.raw_data = self.raw_data[~duplicates]
            self.data_quality_report['duplicates_removed'] = duplicate_count
        else:
            logger.info("✓ No duplicates found")
        
        return self
    
    def create_calculated_fields(self):
        """Create useful calculated fields"""
        logger.info("Creating calculated fields...")
        
        # Age calculation
        today = pd.Timestamp.now()
        self.raw_data['Age'] = (today.year - self.raw_data['DateOfBirth'].dt.year)
        
        # Days since registration
        self.raw_data['DaysSinceRegistration'] = (today - self.raw_data['RegistrationDate']).dt.days
        
        # Visit month/year
        self.raw_data['VisitMonth'] = self.raw_data['RegistrationDate'].dt.to_period('M')
        
        logger.info("✓ Calculated fields created")
        return self
    
    def generate_quality_report(self):
        """Generate data quality report"""
        logger.info("\n=== DATA QUALITY REPORT ===")
        
        print(f"\nOriginal records: {len(self.raw_data)}")
        print(f"Duplicates removed: {self.data_quality_report.get('duplicates_removed', 0)}")
        print(f"Final records: {len(self.raw_data)}")
        
        # Missing values after cleaning
        missing = self.raw_data.isnull().sum()
        if missing.sum() > 0:
            print(f"\nRemaining missing values:\n{missing[missing > 0]}")
        
        # Data type summary
        print(f"\nFinal data types:\n{self.raw_data.dtypes}")
        
        return self
    
    def clean_pipeline(self):
        """
        Execute complete cleaning pipeline
        Order matters - dependencies between cleaning steps
        """
        logger.info("\n" + "="*70)
        logger.info("STARTING DATA CLEANING PIPELINE")
        logger.info("="*70 + "\n")
        
        self.load_and_inspect()
        self.clean_patient_names()
        self.clean_dates()
        self.clean_gender()
        self.clean_phone_numbers()
        self.clean_diagnosis_codes()
        self.clean_billing_amount()
        self.clean_payment_status()
        self.clean_doctor_names()
        self.clean_department()
        self.handle_duplicates()
        self.create_calculated_fields()
        self.generate_quality_report()
        
        self.cleaned_data = self.raw_data
        
        logger.info("\n" + "="*70)
        logger.info("DATA CLEANING COMPLETED SUCCESSFULLY")
        logger.info("="*70 + "\n")
        
        return self
    
    def save_cleaned_data(self, output_path):
        """Save cleaned data to CSV"""
        if self.cleaned_data is not None:
            self.cleaned_data.to_csv(output_path, index=False)
            logger.info(f"✓ Cleaned data saved to {output_path}")
        else:
            logger.error("No cleaned data to save. Run clean_pipeline() first.")
    
    def get_cleaned_data(self):
        """Return cleaned dataframe"""
        return self.cleaned_data


# ====================
# EXECUTION
# ====================

if __name__ == "__main__":
    # Initialize cleaner
    cleaner = PatientDataCleaner('messy_patient_data.csv')
    
    # Run cleaning pipeline
    cleaner.clean_pipeline()
    
    # Save cleaned data
    cleaner.save_cleaned_data('cleaned_patient_data.csv')
    
    # Get cleaned data for further analysis
    cleaned_df = cleaner.get_cleaned_data()
    print("\nCleaned data sample:")
    print(cleaned_df.head())

