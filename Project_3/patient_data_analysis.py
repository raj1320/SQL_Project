================================================================================
FILE: patient_data_analysis.py
Healthcare Data Analysis - Key Insights and Visualizations
================================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class PatientDataAnalyzer:
    """
    Analyze cleaned healthcare patient data for business insights
    """
    
    def __init__(self, cleaned_data_path):
        """Initialize with cleaned data"""
        self.df = pd.read_csv(cleaned_data_path)
        self.df['RegistrationDate'] = pd.to_datetime(self.df['RegistrationDate'])
        self.df['DateOfBirth'] = pd.to_datetime(self.df['DateOfBirth'])
        
    # ====================
    # BASIC STATISTICS
    # ====================
    
    def patient_demographics(self):
        """Analyze patient demographics"""
        print("\n=== PATIENT DEMOGRAPHICS ===")
        
        # Age statistics
        valid_ages = self.df['Age'].dropna()
        print(f"\nAge Statistics:")
        print(f"  Average age: {valid_ages.mean():.1f} years")
        print(f"  Median age: {valid_ages.median():.0f} years")
        print(f"  Age range: {valid_ages.min():.0f} - {valid_ages.max():.0f} years")
        
        # Gender distribution
        print(f"\nGender Distribution:")
        print(self.df['Gender'].value_counts())
        print(f"Female %: {(self.df['Gender'] == 'Female').sum() / len(self.df) * 100:.1f}%")
        
    def billing_analysis(self):
        """Analyze billing patterns"""
        print("\n=== BILLING ANALYSIS ===")
        
        total_revenue = self.df['BillingAmount'].sum()
        avg_billing = self.df['BillingAmount'].mean()
        
        print(f"\nTotal Revenue: ₹{total_revenue:,.2f}")
        print(f"Average billing per visit: ₹{avg_billing:.2f}")
        print(f"Median billing: ₹{self.df['BillingAmount'].median():.2f}")
        
        # Payment status analysis
        print(f"\nPayment Status Distribution:")
        payment_dist = self.df['PaymentStatus'].value_counts()
        print(payment_dist)
        
        collection_rate = (self.df['PaymentStatus'] == 'Paid').sum() / len(self.df) * 100
        print(f"\nCollection Rate: {collection_rate:.1f}%")
        
    def department_analysis(self):
        """Analyze department performance"""
        print("\n=== DEPARTMENT ANALYSIS ===")
        
        dept_stats = self.df.groupby('Department').agg({
            'PatientID': 'count',
            'BillingAmount': ['sum', 'mean'],
            'Age': 'mean'
        }).round(2)
        
        dept_stats.columns = ['Visit Count', 'Total Revenue', 'Avg Billing', 'Avg Patient Age']
        print("\nDepartment Performance:")
        print(dept_stats.sort_values('Total Revenue', ascending=False))
        
    def doctor_analysis(self):
        """Analyze doctor productivity"""
        print("\n=== DOCTOR PRODUCTIVITY ===")
        
        doc_stats = self.df.groupby('DoctorName').agg({
            'PatientID': 'count',
            'BillingAmount': ['sum', 'mean']
        }).round(2)
        
        doc_stats.columns = ['Patient Count', 'Total Revenue', 'Avg Billing']
        print("\nTop 5 Doctors by Patient Count:")
        print(doc_stats.sort_values('Patient Count', ascending=False).head())
        
    # ====================
    # ADVANCED ANALYSIS
    # ====================
    
    def patient_age_groups(self):
        """Analyze billing by age groups"""
        print("\n=== BILLING BY AGE GROUP ===")
        
        # Create age groups
        age_bins = [0, 25, 35, 50, 65, 150]
        age_labels = ['<25', '25-35', '35-50', '50-65', '65+']
        self.df['AgeGroup'] = pd.cut(self.df['Age'], bins=age_bins, labels=age_labels)
        
        age_analysis = self.df.groupby('AgeGroup').agg({
            'PatientID': 'count',
            'BillingAmount': ['sum', 'mean'],
            'Age': 'mean'
        }).round(2)
        
        age_analysis.columns = ['Patient Count', 'Total Revenue', 'Avg Billing', 'Avg Age']
        print(age_analysis)
        
        return age_analysis
    
    def payment_aging(self):
        """Identify overdue payments"""
        print("\n=== PAYMENT AGING ANALYSIS ===")
        
        today = pd.Timestamp.now()
        self.df['DaysSinceVisit'] = (today - self.df['RegistrationDate']).dt.days
        
        # Outstanding bills
        outstanding = self.df[self.df['PaymentStatus'].isin(['Pending', 'Partial'])]
        
        print(f"\nOutstanding Bills: {len(outstanding)}")
        print(f"Outstanding Amount: ₹{outstanding['BillingAmount'].sum():,.2f}")
        
        if len(outstanding) > 0:
            print(f"\nDays Pending (Statistics):")
            print(f"  Average: {outstanding['DaysSinceVisit'].mean():.0f} days")
            print(f"  Maximum: {outstanding['DaysSinceVisit'].max():.0f} days")
            print(f"  Minimum: {outstanding['DaysSinceVisit'].min():.0f} days")
    
    def diagnosis_pattern_analysis(self):
        """Analyze diagnosis patterns"""
        print("\n=== DIAGNOSIS PATTERNS ===")
        
        diagnosis_dist = self.df['DiagnosisCode'].value_counts().head(10)
        print("\nTop 10 Diagnosis Codes:")
        print(diagnosis_dist)
        
        # Billing by diagnosis
        diagnosis_billing = self.df.groupby('DiagnosisCode').agg({
            'BillingAmount': ['sum', 'mean', 'count']
        }).round(2)
        diagnosis_billing.columns = ['Total Revenue', 'Avg Cost', 'Patient Count']
        print("\nTop 10 Diagnoses by Revenue:")
        print(diagnosis_billing.sort_values('Total Revenue', ascending=False).head())
    
    # ====================
    # TREND ANALYSIS
    # ====================
    
    def monthly_trends(self):
        """Analyze monthly trends"""
        print("\n=== MONTHLY TRENDS ===")
        
        self.df['Month'] = self.df['RegistrationDate'].dt.to_period('M')
        
        monthly_stats = self.df.groupby('Month').agg({
            'PatientID': 'count',
            'BillingAmount': ['sum', 'mean']
        }).round(2)
        
        monthly_stats.columns = ['Visit Count', 'Total Revenue', 'Avg Billing']
        print(monthly_stats)
        
        return monthly_stats
    
    def registration_trend(self):
        """Analyze new patient registration trend"""
        print("\n=== NEW PATIENT REGISTRATIONS ===")
        
        # Group by registration month
        reg_trend = self.df.groupby(self.df['RegistrationDate'].dt.to_period('M')).size()
        
        print("\nNew Patients by Month:")
        print(reg_trend)
        
        # Calculate growth rate
        if len(reg_trend) > 1:
            growth_rate = ((reg_trend.iloc[-1] - reg_trend.iloc[-2]) / reg_trend.iloc[-2] * 100)
            print(f"\nLatest Month Growth: {growth_rate:+.1f}%")
    
    # ====================
    # DATA QUALITY CHECKS
    # ====================
    
    def data_quality_summary(self):
        """Summary of data quality"""
        print("\n=== DATA QUALITY SUMMARY ===")
        
        print(f"\nTotal Records: {len(self.df)}")
        print(f"Complete Records: {len(self.df.dropna())} ({len(self.df.dropna())/len(self.df)*100:.1f}%)")
        
        print(f"\nMissing Values:")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("  None")
        
        print(f"\nData Completeness by Column:")
        for col in self.df.columns:
            pct = (1 - self.df[col].isnull().sum() / len(self.df)) * 100
            print(f"  {col}: {pct:.1f}%")
    
    # ====================
    # KEY INSIGHTS
    # ====================
    
    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        print("\n" + "="*70)
        print("PATIENT DATA ANALYSIS - COMPREHENSIVE REPORT")
        print("="*70)
        
        self.data_quality_summary()
        self.patient_demographics()
        self.billing_analysis()
        self.department_analysis()
        self.doctor_analysis()
        self.patient_age_groups()
        self.payment_aging()
        self.diagnosis_pattern_analysis()
        self.monthly_trends()
        self.registration_trend()
        
        print("\n" + "="*70)
        print("REPORT COMPLETED")
        print("="*70)
    
    # ====================
    # EXPORT FUNCTIONS
    # ====================
    
    def export_summary_metrics(self, output_file):
        """Export key metrics to CSV"""
        metrics = {
            'Total Revenue': [self.df['BillingAmount'].sum()],
            'Average Billing': [self.df['BillingAmount'].mean()],
            'Total Visits': [len(self.df)],
            'Unique Patients': [self.df['PatientID'].nunique()],
            'Collection Rate %': [(self.df['PaymentStatus'] == 'Paid').sum() / len(self.df) * 100],
            'Average Patient Age': [self.df['Age'].mean()],
        }
        
        metrics_df = pd.DataFrame(metrics)
        metrics_df.to_csv(output_file, index=False)
        print(f"✓ Summary metrics exported to {output_file}")


# ====================
# VISUALIZATION FUNCTIONS
# ====================

def create_visualizations(df):
    """Create key visualizations"""
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Revenue by Department
    dept_revenue = df.groupby('Department')['BillingAmount'].sum().sort_values(ascending=False)
    dept_revenue.plot(kind='bar', ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title('Revenue by Department')
    axes[0, 0].set_xlabel('Department')
    axes[0, 0].set_ylabel('Revenue (₹)')
    
    # 2. Payment Status Distribution
    payment_counts = df['PaymentStatus'].value_counts()
    payment_counts.plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%', colors=['green', 'orange', 'red'])
    axes[0, 1].set_title('Payment Status Distribution')
    
    # 3. Billing Amount Distribution
    axes[1, 0].hist(df['BillingAmount'], bins=20, color='skyblue', edgecolor='black')
    axes[1, 0].set_title('Distribution of Billing Amounts')
    axes[1, 0].set_xlabel('Billing Amount (₹)')
    axes[1, 0].set_ylabel('Frequency')
    
    # 4. Age Distribution
    axes[1, 1].hist(df['Age'].dropna(), bins=15, color='lightcoral', edgecolor='black')
    axes[1, 1].set_title('Patient Age Distribution')
    axes[1, 1].set_xlabel('Age (years)')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('healthcare_analysis_visualizations.png', dpi=300, bbox_inches='tight')
    print("✓ Visualizations saved to healthcare_analysis_visualizations.png")
    plt.show()


# ====================
# EXECUTION
# ====================

if __name__ == "__main__":
    # Initialize analyzer
    analyzer = PatientDataAnalyzer('cleaned_patient_data.csv')
    
    # Generate comprehensive report
    analyzer.generate_insights_report()
    
    # Export summary metrics
    analyzer.export_summary_metrics('key_metrics_summary.csv')
    
    # Create visualizations
    create_visualizations(analyzer.df)

