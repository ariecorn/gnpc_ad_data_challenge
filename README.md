# GNPC Alzheimer's Proteomics Mock Dataset

This directory contains mock data simulating the structure of the GNPC (Global Neurodegeneration Proteomics Consortium) Alzheimer's disease proteomics dataset. This mock data is designed to help you develop and test your application while awaiting access to the real database.

## Dataset Overview

The GNPC dataset is one of the largest proteomics studies for neurodegenerative diseases, containing:
- Over 18,000 participants from 23 cohorts
- ~31,000 unique biosamples (plasma, serum, CSF)
- ~250 million protein measurements
- 40+ clinical and demographic features
- SomaScan 5k and 7k platform measurements

## Mock Data Structure

### Files Included

#### 1. `participants.csv` (25 mock participants)
Contains demographic and baseline information for study participants.

**Columns:**
- `participant_id`: Unique identifier (e.g., GNPC001)
- `cohort_id`: Associated study cohort
- `age`: Age at enrollment
- `sex`: M/F
- `race`: Racial category
- `ethnicity`: Hispanic/Non-Hispanic
- `education_years`: Years of education completed
- `apoe_genotype`: APOE genetic risk factor (E2/E3/E4 variants)
- `diagnosis`: Healthy Control, MCI (Mild Cognitive Impairment), or AD (Alzheimer's Disease)
- `diagnosis_date`: Date of diagnosis
- `enrollment_date`: Date enrolled in study

#### 2. `clinical_assessments.csv` (30 mock assessments)
Longitudinal clinical assessments and cognitive test scores.

**Columns:**
- `assessment_id`: Unique assessment identifier
- `participant_id`: Links to participants table
- `visit_number`: Visit sequence (1=baseline, 2=6-month, etc.)
- `visit_date`: Assessment date
- `mmse_score`: Mini-Mental State Examination (0-30, higher=better)
- `moca_score`: Montreal Cognitive Assessment (0-30, higher=better)
- `cdr_global`: Clinical Dementia Rating global score (0-3, higher=worse)
- `cdr_sum_boxes`: CDR sum of boxes (0-18, higher=worse)
- `faq_score`: Functional Activities Questionnaire (0-30, higher=worse)
- `npiq_total`: Neuropsychiatric Inventory Questionnaire total
- `bmi`: Body Mass Index
- `systolic_bp`: Systolic blood pressure
- `diastolic_bp`: Diastolic blood pressure
- `notes`: Clinical notes

#### 3. `biosamples.csv` (38 mock samples)
Information about collected biological samples.

**Columns:**
- `sample_id`: Unique sample identifier
- `participant_id`: Links to participants table
- `visit_number`: Visit when sample collected
- `collection_date`: Sample collection date
- `sample_type`: Plasma, Serum, or CSF
- `sample_volume_ml`: Volume in milliliters
- `storage_location`: Freezer location
- `processing_date`: Date sample was processed
- `platform`: Proteomics platform (SomaScan)
- `platform_version`: 5k or 7k
- `batch_id`: Processing batch identifier
- `quality_control_status`: Pass/Borderline/Fail

#### 4. `protein_measurements.csv` (100 mock measurements)
Protein abundance measurements from proteomics assays.

**Columns:**
- `measurement_id`: Unique measurement identifier
- `sample_id`: Links to biosamples table
- `protein_id`: Protein identifier
- `protein_name`: Common protein name
- `uniprot_id`: UniProt database ID
- `gene_symbol`: Gene symbol
- `rfu_value`: Raw Relative Fluorescence Units
- `normalized_value`: Normalized protein abundance
- `z_score`: Standardized z-score
- `detection_status`: Detected/Below Detection Limit

**Key Proteins Included:**
- Amyloid-beta 40/42 (APP): Core AD pathology markers
- Tau protein & Phospho-Tau: Neurodegeneration markers
- Neurofilament light chain (NEFL): Axonal damage marker
- GFAP: Astrocyte activation marker
- YKL-40 (CHI3L1): Neuroinflammation marker
- Neurogranin (NRGN): Synaptic dysfunction marker
- VILIP-1: Neuronal injury marker
- S100B: Brain injury marker

#### 5. `protein_annotations.csv` (10 proteins)
Detailed annotations for proteins measured in the study.

**Columns:**
- `protein_id`: Links to protein_measurements
- `protein_name`: Full protein name
- `uniprot_id`: UniProt database identifier
- `gene_symbol`: Gene symbol
- `protein_class`: Functional classification
- `molecular_weight_kda`: Molecular weight in kDa
- `biological_process`: Primary biological function
- `cellular_component`: Subcellular localization
- `disease_association`: Associated diseases
- `pathway`: Biological pathway involvement

#### 6. `cohort_metadata.csv` (3 cohorts)
Information about the study cohorts.

**Columns:**
- `cohort_id`: Unique cohort identifier
- `cohort_name`: Full cohort name
- `institution`: Research institution
- `country`: Country of study
- `enrollment_start`: Study start date
- `enrollment_end`: Study end date
- `total_participants`: Total enrolled
- `sample_collection_protocol`: Collection method
- `study_design`: Study type
- `primary_objective`: Research goals

## Data Relationships

```
participants (1) ──< (M) clinical_assessments
     │
     └──< (M) biosamples (1) ──< (M) protein_measurements (M) ──> (1) protein_annotations

cohort_metadata (1) ──< (M) participants
```

## Key Features for Analysis

### Longitudinal Data
- Multiple visits per participant (40% of samples)
- Track disease progression over time
- Baseline and follow-up comparisons

### Disease Groups
- **Healthy Controls**: Normal cognitive function
- **MCI (Mild Cognitive Impairment)**: Intermediate stage
- **AD (Alzheimer's Disease)**: Diagnosed dementia

### Biomarker Profiles
- Classic AD biomarkers (Aβ40, Aβ42, tau, p-tau)
- Neuroinflammation markers (GFAP, YKL-40)
- Neurodegeneration markers (NfL, neurogranin)
- Synaptic dysfunction markers

### Risk Factors
- APOE genotype (E4 = risk allele)
- Demographics (age, sex, education)
- Cognitive test scores

## Data Characteristics in Mock Dataset

### Sample Distribution
- **Healthy Controls**: ~32% (8 participants)
- **MCI**: ~32% (8 participants)
- **AD**: ~36% (9 participants)

### Sample Types
- **Plasma**: Most common (~84%)
- **CSF**: Available for some participants (~16%)
- **Serum**: Subset of samples

### Platform Coverage
- **SomaScan 7k**: Primary platform (~87%)
- **SomaScan 5k**: Subset for validation (~13%)

### Protein Expression Patterns
- AD patients show elevated Aβ42, tau, p-tau in CSF
- Controls show normal biomarker ranges
- MCI shows intermediate patterns
- Disease progression reflected in longitudinal samples

## Usage Examples

### Loading Data in Python
```python
import pandas as pd

# Load all datasets
participants = pd.read_csv('mock_data/participants.csv')
assessments = pd.read_csv('mock_data/clinical_assessments.csv')
samples = pd.read_csv('mock_data/biosamples.csv')
measurements = pd.read_csv('mock_data/protein_measurements.csv')
proteins = pd.read_csv('mock_data/protein_annotations.csv')
cohorts = pd.read_csv('mock_data/cohort_metadata.csv')

# Merge for analysis
data = measurements.merge(samples, on='sample_id')
data = data.merge(participants, on='participant_id')
data = data.merge(proteins, on='protein_id')
```

### Example Analyses
1. **Biomarker comparison by diagnosis group**
2. **Longitudinal progression tracking**
3. **APOE genotype associations**
4. **CSF vs Plasma biomarker correlations**
5. **Batch effect correction**
6. **Predictive modeling for diagnosis**
7. **Multi-protein biomarker panels**

## Important Notes

### Limitations of Mock Data
- Real dataset has ~7,000 proteins; mock has 10 key proteins
- Real dataset has 18,645 participants; mock has 25
- Real dataset has 31,083 samples; mock has 38
- Simplified clinical features (40 in real data)
- Synthetic values do not reflect true biological distributions

### When You Get Real Data Access
You'll need to:
1. Adjust for the actual schema (may have additional tables/columns)
2. Handle missing data (real datasets have incomplete records)
3. Implement batch effect correction across cohorts
4. Address platform differences (5k vs 7k normalization)
5. Handle longitudinal data complexity
6. Apply appropriate statistical methods for proteomics
7. Consider cohort-specific effects

## Data Access Information

The real GNPC dataset is available through:
- **AD Data Initiative**: https://www.alzheimersdata.org/gnpc-proteomics-data-challenge
- **AD Workbench**: Cloud-based secure access platform
- Request access through official channels

## References

- [GNPC Nature Medicine Article](https://www.nature.com/articles/s41591-025-03834-0)
- [GNPC Website](https://www.neuroproteome.org/)
- [AD Data Initiative](https://www.alzheimersdata.org/gnpc-proteomics-data-challenge)

## Contact

For questions about the mock data structure or to report issues, please contact your project team.

---

**Generated**: 2025-11-27
**Version**: 1.0
**Purpose**: Development and testing mock data
