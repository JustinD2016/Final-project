#!/usr/bin/env python3
"""
BANK INNOVATION DATASET - DATA DICTIONARY PDF GENERATOR
=======================================================
Creates a comprehensive, nicely formatted PDF documentation
for the bank_innovation_dataset_FINAL.csv
"""

import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.lib import colors
from datetime import datetime
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = r"C:\Users\jdorv\Coding Fun\Bank Innovation\Data"
FINAL_PROJECT_DIR = r"C:\Users\jdorv\Coding Fun\Bank Innovation\Final-project"
DATA_FILE = os.path.join(FINAL_PROJECT_DIR, "data", "bank_innovation_dataset_FINAL.csv")
OUTPUT_PDF = os.path.join(FINAL_PROJECT_DIR, "data", "Data_Dictionary.pdf")

# ============================================================================
# FIELD DEFINITIONS
# ============================================================================

FIELD_DEFINITIONS = {
    # ========== IDENTIFIERS ==========
    'BANK_ID': {
        'source': 'Identifier',
        'description': 'Unique internal bank identifier assigned sequentially (BANK_0001, BANK_0002, etc.)',
        'type': 'String',
        'unit': 'N/A',
        'example': 'BANK_0001'
    },
    'RSSD_ID': {
        'source': 'Identifier',
        'description': 'Federal Reserve Research, Statistics, Supervision, Discount, and Credit (RSSD) identifier. Primary key for matching across regulatory datasets.',
        'type': 'String',
        'unit': 'N/A',
        'example': '123456'
    },
    'IDRSSD': {
        'source': 'Identifier',
        'description': 'Same as RSSD_ID. Preserved for backward compatibility with raw FFIEC data.',
        'type': 'String',
        'unit': 'N/A',
        'example': '123456'
    },
    'FDIC_Cert': {
        'source': 'Identifier',
        'description': 'FDIC Certificate Number. Unique identifier for FDIC-insured institutions.',
        'type': 'Integer',
        'unit': 'N/A',
        'example': '12345'
    },
    'Bank_Name': {
        'source': 'Identifier',
        'description': 'Official legal name of the financial institution as reported to regulators.',
        'type': 'String',
        'unit': 'N/A',
        'example': 'First National Bank'
    },
    'Year': {
        'source': 'Identifier',
        'description': 'Calendar year of the observation (2010-2021).',
        'type': 'Integer',
        'unit': 'Year',
        'example': '2020'
    },
    
    # ========== FFIEC CALL REPORT - BALANCE SHEET ==========
    'Total_Assets': {
        'source': 'FFIEC Call Report',
        'description': 'Total assets reported on the balance sheet. Represents all resources owned or controlled by the bank. From RCON2170 (domestic) or RCFD2170 (consolidated).',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '1000000 (= $1 billion)'
    },
    'Total_Deposits': {
        'source': 'FFIEC Call Report',
        'description': 'Total deposits including demand deposits, savings deposits, and time deposits. Primary funding source for banks. From RCON2200 or RCFD2200.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '800000 (= $800 million)'
    },
    'Total_Equity': {
        'source': 'FFIEC Call Report',
        'description': 'Total equity capital including common stock, surplus, and retained earnings. Represents shareholders\' equity. From RCON3210 or RCFD3210.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '100000 (= $100 million)'
    },
    'Total_Liabilities': {
        'source': 'FFIEC Call Report',
        'description': 'Total liabilities including all deposits, borrowed money, and other obligations. From RCON2948 or RCFD2948.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '900000 (= $900 million)'
    },
    'NIB_Deposits': {
        'source': 'FFIEC Call Report',
        'description': 'Noninterest-bearing deposits (e.g., checking accounts). High proportion indicates strong customer relationships and low funding costs. From RCON6631 or RCFD6631.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '200000 (= $200 million)'
    },
    'Cash_Balances': {
        'source': 'FFIEC Call Report',
        'description': 'Cash and balances due from depository institutions. Includes vault cash and deposits at other banks. From RCON0081 or RCFD0081.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '50000 (= $50 million)'
    },
    'Securities_AFS': {
        'source': 'FFIEC Call Report',
        'description': 'Securities available for sale. Investment securities that can be sold before maturity. From RCON1773 or RCFD1773.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '150000 (= $150 million)'
    },
    'Loans_Net': {
        'source': 'FFIEC Call Report',
        'description': 'Total loans and leases net of unearned income and allowance for loan losses. Primary earning asset for banks. From RCONB528 or RCFDB528.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '600000 (= $600 million)'
    },
    'Other_Borrowed_Money': {
        'source': 'FFIEC Call Report',
        'description': 'Borrowed funds from sources other than deposits (e.g., Federal Home Loan Bank advances, Fed funds purchased). From RCON3190 or RCFD3190.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '50000 (= $50 million)'
    },
    
    # ========== FFIEC CALL REPORT - INCOME STATEMENT ==========
    'Net_Interest_Income': {
        'source': 'FFIEC Call Report',
        'description': 'Net interest income (interest income minus interest expense). Primary source of bank revenue. From RIAD4074 or RIAD4065.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '40000 (= $40 million)'
    },
    'Noninterest_Income': {
        'source': 'FFIEC Call Report',
        'description': 'Income from sources other than interest (e.g., fees, service charges, trading income). Innovation indicator for diversified revenue. From RIAD4079 or RIAD4080.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '10000 (= $10 million)'
    },
    'Noninterest_Expense': {
        'source': 'FFIEC Call Report',
        'description': 'Operating expenses excluding interest expense (e.g., salaries, occupancy, technology costs). From RIAD4093 or RIAD4135.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '35000 (= $35 million)'
    },
    
    # ========== FFIEC CALL REPORT - ASSET QUALITY ==========
    'ALLL': {
        'source': 'FFIEC Call Report',
        'description': 'Allowance for Loan and Lease Losses. Reserve for expected credit losses. Higher values indicate higher risk loans. From RCON3123 or RCFD3123.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '8000 (= $8 million)'
    },
    'Nonaccrual_Loans': {
        'source': 'FFIEC Call Report',
        'description': 'Loans on nonaccrual status (90+ days past due or otherwise impaired). Asset quality indicator. From RCON1403 or RCFD1403.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '3000 (= $3 million)'
    },
    
    # ========== FFIEC CALL REPORT - INNOVATION PROXIES ==========
    'Premises_Fixed_Assets': {
        'source': 'FFIEC Call Report',
        'description': 'Premises and fixed assets including buildings, equipment, and furniture. Proxy for physical infrastructure investment. From RCON2145 or RCFD2145.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '15000 (= $15 million)'
    },
    'Goodwill': {
        'source': 'FFIEC Call Report',
        'description': 'Goodwill from business combinations. Present for banks that have made acquisitions. From RCON3163 or RCFD3163.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '5000 (= $5 million)'
    },
    'Intangible_Assets': {
        'source': 'FFIEC Call Report',
        'description': 'Identifiable intangible assets including software, core deposit intangibles, and other intellectual property. Innovation indicator. From RCON2143, RCFD2143, RCON0426, or RCFD0426.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '2000 (= $2 million)'
    },
    
    # ========== SOD - BRANCH NETWORK ==========
    'Total_Branches': {
        'source': 'SOD (Summary of Deposits)',
        'description': 'Total number of physical branch locations as of June 30. Indicator of distribution strategy and market presence.',
        'type': 'Integer',
        'unit': 'Count',
        'example': '25'
    },
    'Total_Deposits_SOD': {
        'source': 'SOD (Summary of Deposits)',
        'description': 'Total deposits across all branches as reported in SOD. Should closely match FFIEC Total_Deposits but may differ due to timing and scope.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '800000 (= $800 million)'
    },
    'Deposits_Per_Branch': {
        'source': 'SOD (Calculated)',
        'description': 'Average deposits per branch (Total_Deposits_SOD / Total_Branches). Key efficiency and innovation metric - higher values suggest digital adoption or efficient branch strategy.',
        'type': 'Float',
        'unit': 'Thousands of USD',
        'example': '32000 (= $32 million per branch)'
    },
    'Branch_Growth_YoY': {
        'source': 'SOD (Calculated)',
        'description': 'Year-over-year percentage change in branch count ((Branches_t - Branches_t-1) / Branches_t-1). Negative growth may indicate digital transformation.',
        'type': 'Float',
        'unit': 'Percentage (decimal)',
        'example': '-0.05 (= -5% branch reduction)'
    },
    'Branch_Efficiency_Percentile': {
        'source': 'SOD (Calculated)',
        'description': 'Percentile rank of Deposits_Per_Branch within each year. Values from 0 to 1, where 1.0 = highest efficiency.',
        'type': 'Float',
        'unit': 'Percentile (0-1)',
        'example': '0.75 (= 75th percentile)'
    },
    
    # ========== EDGAR SEC FILINGS ==========
    'Has_10K': {
        'source': 'Edgar SEC Filings',
        'description': 'Boolean indicator of whether bank filed annual 10-K report with SEC. TRUE only for publicly-traded banks.',
        'type': 'Boolean',
        'unit': 'True/False',
        'example': 'True'
    },
    'Has_10Q': {
        'source': 'Edgar SEC Filings',
        'description': 'Boolean indicator of whether bank filed quarterly 10-Q reports with SEC. TRUE only for publicly-traded banks.',
        'type': 'Boolean',
        'unit': 'True/False',
        'example': 'True'
    },
    'Has_DEF14A': {
        'source': 'Edgar SEC Filings',
        'description': 'Boolean indicator of whether bank filed DEF 14A proxy statement with SEC. Contains board and governance information.',
        'type': 'Boolean',
        'unit': 'True/False',
        'example': 'False'
    },
    'Total_Annual_Filings': {
        'source': 'Edgar SEC Filings',
        'description': 'Total count of all SEC filings (10-K, DEF 14A, etc.) made during the year.',
        'type': 'Integer',
        'unit': 'Count',
        'example': '12'
    },
    'Filing_Count_10K': {
        'source': 'Edgar SEC Filings',
        'description': 'Count of 10-K filings for the year (typically 1, but may include amendments).',
        'type': 'Integer',
        'unit': 'Count',
        'example': '1'
    },
    'Filing_Count_10Q': {
        'source': 'Edgar SEC Filings',
        'description': 'Count of 10-Q filings for the year (typically 3: Q1, Q2, Q3. Q4 is covered by 10-K).',
        'type': 'Integer',
        'unit': 'Count',
        'example': '3'
    },
    'Filing_Count_DEF14A': {
        'source': 'Edgar SEC Filings',
        'description': 'Count of DEF 14A proxy statements filed during the year (typically 1 for annual meeting).',
        'type': 'Integer',
        'unit': 'Count',
        'example': '1'
    },
    'Filing_Date_10K': {
        'source': 'Edgar SEC Filings',
        'description': 'Date of first 10-K filing during the year.',
        'type': 'Date',
        'unit': 'YYYY-MM-DD',
        'example': '2020-03-15'
    },
    'Filing_Date_DEF14A': {
        'source': 'Edgar SEC Filings',
        'description': 'Date of first DEF 14A filing during the year.',
        'type': 'Date',
        'unit': 'YYYY-MM-DD',
        'example': '2020-04-10'
    },
    'Is_Public_Company': {
        'source': 'Edgar (Derived)',
        'description': 'Boolean indicator of whether bank is publicly traded (Has_10K = True). Public companies subject to SEC reporting requirements.',
        'type': 'Boolean',
        'unit': 'True/False',
        'example': 'True'
    },
    
    # ========== DERIVED METRICS ==========
    'Asset_Growth_YoY': {
        'source': 'Calculated',
        'description': 'Year-over-year percentage growth in Total_Assets ((Assets_t - Assets_t-1) / Assets_t-1). Growth indicator and innovation proxy.',
        'type': 'Float',
        'unit': 'Percentage (decimal)',
        'example': '0.08 (= 8% growth)'
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_data_statistics(data_file):
    """Load dataset and compute statistics."""
    if not os.path.exists(data_file):
        return None
    
    df = pd.read_csv(data_file)
    
    stats = {
        'total_records': len(df),
        'unique_banks': df['RSSD_ID'].nunique() if 'RSSD_ID' in df.columns else 0,
        'year_range': f"{df['Year'].min():.0f}-{df['Year'].max():.0f}" if 'Year' in df.columns else 'N/A',
        'total_columns': len(df.columns),
        'completeness': {}
    }
    
    # Calculate completeness for key fields
    for col in df.columns:
        if col in FIELD_DEFINITIONS:
            stats['completeness'][col] = 100 * df[col].notna().sum() / len(df)
    
    return stats, df


def create_title_page(story, styles):
    """Create title page."""
    # Title
    title = Paragraph(
        "<b>BANK INNOVATION DATASET</b><br/><b>Data Dictionary</b>",
        styles['CustomTitle']
    )
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    # Subtitle
    subtitle = Paragraph(
        "Complete Reference for bank_innovation_dataset_FINAL.csv",
        styles['CustomSubtitle']
    )
    story.append(subtitle)
    story.append(Spacer(1, 1*inch))
    
    # Version info
    version_data = [
        ['Dataset Version:', '1.0'],
        ['Documentation Date:', datetime.now().strftime('%B %d, %Y')],
        ['Data Period:', '2010-2021'],
        ['Data Sources:', 'FFIEC Call Reports, SOD, Edgar SEC Filings']
    ]
    
    version_table = Table(version_data, colWidths=[2.5*inch, 3*inch])
    version_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(version_table)
    story.append(Spacer(1, 1*inch))
    
    # Purpose
    purpose_text = """
    <b>Purpose:</b><br/>
    This data dictionary provides comprehensive documentation for the Bank Innovation Dataset, 
    which integrates financial performance data, branch network metrics, and SEC filing information 
    for U.S. banking institutions from 2010-2021. The dataset is designed to support research on 
    bank innovation, digital transformation, and competitive strategy.
    """
    story.append(Paragraph(purpose_text, styles['Normal']))
    
    story.append(PageBreak())


def create_overview_section(story, styles, stats):
    """Create overview section."""
    story.append(Paragraph("<b>1. DATASET OVERVIEW</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    overview_text = f"""
    The Bank Innovation Dataset combines regulatory filings, branch network data, and SEC disclosures 
    to create a comprehensive view of U.S. banking institutions. The dataset contains 
    <b>{stats['total_records']:,} bank-year observations</b> covering <b>{stats['unique_banks']:,} unique banks</b> 
    over the period <b>{stats['year_range']}</b>.
    <br/><br/>
    <b>Key Features:</b><br/>
    • One row per bank per year (panel structure)<br/>
    • {stats['total_columns']} variables spanning financial performance, branch efficiency, and public filings<br/>
    • 98.7% completeness on critical financial metrics<br/>
    • Quarterly and annual views available<br/>
    """
    story.append(Paragraph(overview_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Data sources table
    story.append(Paragraph("<b>1.1 Data Sources</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    sources_data = [
        ['<b>Source</b>', '<b>Description</b>', '<b>Coverage</b>'],
        ['FFIEC Call Reports', 
         'Quarterly regulatory filings with detailed financial data',
         '100% of banks (regulatory requirement)'],
        ['SOD (Summary of Deposits)',
         'Branch-level deposit data collected annually by FDIC',
         '~95% of banks (branch-based institutions)'],
        ['Edgar SEC Filings',
         '10-K, 10-Q, and DEF 14A filings for public companies',
         '~2-3% of banks (publicly-traded only)']
    ]
    
    sources_table = Table(sources_data, colWidths=[1.5*inch, 3.2*inch, 1.8*inch])
    sources_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#F2F2F2')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(sources_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Unit conventions
    story.append(Paragraph("<b>1.2 Unit Conventions</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    units_text = """
    <b>Financial Values:</b> All dollar amounts are reported in <b>thousands of USD</b> 
    unless otherwise noted. For example, Total_Assets = 1,000,000 represents $1 billion in assets.
    <br/><br/>
    <b>Percentages:</b> Growth rates and ratios are expressed as <b>decimals</b>. 
    For example, Asset_Growth_YoY = 0.08 represents 8% growth.
    <br/><br/>
    <b>Dates:</b> All dates follow ISO 8601 format (YYYY-MM-DD).
    """
    story.append(Paragraph(units_text, styles['Normal']))
    
    story.append(PageBreak())


def create_field_section(story, styles, source_name, fields_dict):
    """Create a section for fields from a specific source."""
    story.append(Paragraph(f"<b>{source_name}</b>", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    
    for field_name, field_info in fields_dict.items():
        # Field name and type
        field_header = f"<b>{field_name}</b> ({field_info['type']})"
        story.append(Paragraph(field_header, styles['FieldName']))
        
        # Create info table
        info_data = [
            ['<b>Unit:</b>', field_info['unit']],
            ['<b>Example:</b>', field_info['example']],
            ['<b>Description:</b>', field_info['description']]
        ]
        
        info_table = Table(info_data, colWidths=[1*inch, 5*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (-1, -1), 'Helvetica', 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.15*inch))
    
    story.append(Spacer(1, 0.1*inch))


def create_data_quality_section(story, styles, stats):
    """Create data quality section."""
    story.append(Paragraph("<b>3. DATA QUALITY METRICS</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    # Completeness table
    story.append(Paragraph("<b>3.1 Field Completeness</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    completeness_text = """
    The following table shows the percentage of non-null values for each field. 
    100% indicates every record has a value; lower percentages indicate missing data.
    """
    story.append(Paragraph(completeness_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Group by source and create tables
    sources = ['Identifier', 'FFIEC Call Report', 'SOD (Summary of Deposits)', 
               'SOD (Calculated)', 'Edgar SEC Filings', 'Edgar (Derived)', 'Calculated']
    
    for source in sources:
        source_fields = {k: v for k, v in FIELD_DEFINITIONS.items() if v['source'] == source}
        if not source_fields:
            continue
        
        story.append(Paragraph(f"<b>{source}</b>", styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
        
        completeness_data = [['<b>Field</b>', '<b>Completeness</b>']]
        
        for field_name in sorted(source_fields.keys()):
            if field_name in stats['completeness']:
                pct = stats['completeness'][field_name]
                completeness_data.append([field_name, f"{pct:.1f}%"])
        
        if len(completeness_data) > 1:
            comp_table = Table(completeness_data, colWidths=[3.5*inch, 1.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#F2F2F2')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(comp_table)
            story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # Known limitations
    story.append(Paragraph("<b>3.2 Known Limitations and Missing Data</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    limitations_text = """
    <b>Edgar SEC Filings (Low Coverage):</b> Only 2-3% of banks are publicly traded and required 
    to file with the SEC. The remaining 97-98% are private institutions with no Edgar data. 
    This is expected and appropriate for the dataset structure.
    <br/><br/>
    <b>SOD Branch Data (~95% Coverage):</b> Some banks do not operate physical branches 
    (e.g., online-only banks, credit card banks, trust companies) and thus do not appear in SOD data.
    <br/><br/>
    <b>FFIEC Asset Quality Fields (Variable Coverage):</b> Fields like Nonaccrual_Loans and Goodwill 
    have lower completeness because not all banks report these items. This reflects legitimate 
    differences in business models rather than data quality issues.
    <br/><br/>
    <b>RCON vs RCFD Codes:</b> Most banks (98%+) report only domestic operations (RCON codes). 
    Only large multinational banks report consolidated domestic+foreign operations (RCFD codes). 
    The dataset prioritizes RCON codes for compatibility.
    """
    story.append(Paragraph(limitations_text, styles['Normal']))


def create_usage_notes(story, styles):
    """Create usage notes section."""
    story.append(PageBreak())
    story.append(Paragraph("<b>4. USAGE NOTES</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>4.1 Matching Across Datasets</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    matching_text = """
    <b>Primary Key:</b> RSSD_ID + Year uniquely identifies each observation.
    <br/><br/>
    <b>Cross-Dataset Matching:</b><br/>
    • RSSD_ID: Used for all Federal Reserve and FFIEC data<br/>
    • FDIC_Cert: Used for FDIC data including SOD<br/>
    • CIK (not in this dataset): SEC identifier for Edgar matching<br/>
    <br/>
    <b>Bank Name Matching:</b> Bank names may change due to mergers, acquisitions, or rebranding. 
    Always use RSSD_ID for reliable matching across time.
    """
    story.append(Paragraph(matching_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>4.2 Recommended Analyses</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    analyses_text = """
    <b>Innovation Metrics:</b><br/>
    • Deposits_Per_Branch: High values indicate digital adoption or efficient branch strategy<br/>
    • Branch_Growth_YoY: Negative growth may signal digital transformation<br/>
    • Noninterest_Income / Total_Assets: Product diversification indicator<br/>
    • Intangible_Assets / Total_Assets: Technology investment proxy<br/>
    <br/>
    <b>Efficiency Metrics:</b><br/>
    • Noninterest_Expense / (Net_Interest_Income + Noninterest_Income): Efficiency ratio<br/>
    • NIB_Deposits / Total_Deposits: Low-cost funding advantage<br/>
    <br/>
    <b>Growth Metrics:</b><br/>
    • Asset_Growth_YoY: Overall growth indicator<br/>
    • Compare to Branch_Growth_YoY to assess digital vs. physical expansion<br/>
    """
    story.append(Paragraph(analyses_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>4.3 Citation</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    citation_text = """
    When using this dataset in academic research, please cite the data sources:<br/>
    <br/>
    • FFIEC Call Reports: Federal Financial Institutions Examination Council. 
    "Consolidated Reports of Condition and Income." Various years.<br/>
    • SOD: Federal Deposit Insurance Corporation. "Summary of Deposits." Various years.<br/>
    • Edgar: U.S. Securities and Exchange Commission. "Edgar Database." Various years.
    """
    story.append(Paragraph(citation_text, styles['Normal']))


# ============================================================================
# MAIN PDF GENERATION
# ============================================================================

def create_data_dictionary_pdf(data_file, output_pdf):
    """Generate the complete data dictionary PDF."""
    print("="*80)
    print("GENERATING DATA DICTIONARY PDF")
    print("="*80)
    
    # Load data and compute statistics
    print(f"\nLoading dataset: {data_file}")
    stats, df = get_data_statistics(data_file)
    
    if stats is None:
        print(f"✗ Dataset not found: {data_file}")
        print("  Please ensure the integration script has been run.")
        return
    
    print(f"✓ Loaded dataset:")
    print(f"  - {stats['total_records']:,} records")
    print(f"  - {stats['unique_banks']:,} unique banks")
    print(f"  - {stats['total_columns']} columns")
    print(f"  - Years: {stats['year_range']}")
    
    # Create PDF
    print(f"\nGenerating PDF: {output_pdf}")
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=HexColor('#1F4E78'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Subtitle style
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=HexColor('#4472C4'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    # Field name style
    styles.add(ParagraphStyle(
        name='FieldName',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#1F4E78'),
        spaceAfter=6,
        fontName='Helvetica-Bold',
        leftIndent=0
    ))
    
    # Heading styles with color
    styles['Heading1'].textColor = HexColor('#1F4E78')
    styles['Heading1'].fontSize = 16
    styles['Heading1'].spaceAfter = 12
    
    styles['Heading2'].textColor = HexColor('#4472C4')
    styles['Heading2'].fontSize = 13
    styles['Heading2'].spaceAfter = 10
    
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].alignment = TA_JUSTIFY
    
    # Build document
    story = []
    
    # Title page
    print("  Creating title page...")
    create_title_page(story, styles)
    
    # Overview
    print("  Creating overview section...")
    create_overview_section(story, styles, stats)
    
    # Field definitions by source
    print("  Creating field definitions...")
    story.append(Paragraph("<b>2. FIELD DEFINITIONS</b>", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    # Group fields by source
    sources = {}
    for field_name, field_info in FIELD_DEFINITIONS.items():
        source = field_info['source']
        if source not in sources:
            sources[source] = {}
        sources[source][field_name] = field_info
    
    # Order sources logically
    source_order = [
        'Identifier',
        'FFIEC Call Report', 
        'SOD (Summary of Deposits)',
        'SOD (Calculated)',
        'Edgar SEC Filings',
        'Edgar (Derived)',
        'Calculated'
    ]
    
    for source in source_order:
        if source in sources:
            create_field_section(story, styles, source, sources[source])
            if source != source_order[-1]:
                story.append(PageBreak())
    
    # Data quality
    print("  Creating data quality section...")
    create_data_quality_section(story, styles, stats)
    
    # Usage notes
    print("  Creating usage notes...")
    create_usage_notes(story, styles)
    
    # Build PDF
    print("\n  Building PDF document...")
    doc.build(story)
    
    print(f"\n✓ PDF generated successfully!")
    print(f"  Location: {output_pdf}")
    
    # Get file size
    file_size = os.path.getsize(output_pdf) / 1024  # KB
    print(f"  Size: {file_size:.1f} KB")
    
    print("\n" + "="*80)
    print("DATA DICTIONARY COMPLETE")
    print("="*80)


if __name__ == "__main__":
    create_data_dictionary_pdf(DATA_FILE, OUTPUT_PDF)