# Plan: Identifying Proteins that Differentiate Fast vs Slow AD Progressors

## Research Question
Which proteins in the dataset delineate fast and slow progressors for Alzheimer's disease, and are there any therapeutic targets we can identify?

## Dataset Summary

### Longitudinal Data Available
From the mock data analysis:
- **Participants with longitudinal data**: 7 participants have 2+ visits
  - GNPC001 (Healthy): 3 visits (baseline, 6-month, 12-month)
  - GNPC002 (MCI): 2 visits (baseline, 6-month)
  - GNPC003 (AD): 2 visits (baseline, 6-month)
  - GNPC004 (Healthy): 2 visits
  - GNPC006 (MCI): 2 visits
  - GNPC009 (Healthy): 2 visits
  - GNPC010 (AD): 2 visits

### Clinical Metrics for Progression
- **MMSE** (Mini-Mental State Exam): 0-30, higher = better cognition
- **MoCA** (Montreal Cognitive Assessment): 0-30, higher = better cognition
- **CDR Global** (Clinical Dementia Rating): 0-3, higher = worse dementia
- **CDR Sum of Boxes**: 0-18, higher = worse dementia
- **FAQ Score** (Functional Activities): 0-30, higher = worse function

### Protein Biomarkers (n=10)
- Amyloid-beta 40/42 (APP pathway)
- Tau & Phospho-Tau (tauopathy markers)
- Neurofilament light chain (neurodegeneration)
- GFAP (astrocyte activation)
- YKL-40 (neuroinflammation)
- Neurogranin (synaptic dysfunction)
- VILIP-1 (neuronal injury)
- S100B (brain injury/glial activation)

## User-Defined Research Strategy

The analysis will follow a drug discovery pipeline:

### Phase 1: Progression Analysis
- **Fast/Slow Progression**: Define using protein levels across cohorts (CN → MCI → AD) and cognitive decline (MMSE/MoCA scores)
- **Correlation Analysis**: Calculate correlation coefficient (r) between cohorts and protein levels to identify top hits

### Phase 2: Therapeutic Target Identification Criteria
Priority targets must show:
1. **Early upregulation**: Protein levels increase in neuroinflammation markers BEFORE cognitive symptoms appear
2. **Stability analysis**: Consistent pattern across cohorts
3. **Hazard ratio**: Statistical significance in disease progression
4. **Fast increase trajectory**: Steep upregulation across CN → MCI → AD stages

### Phase 3: Drug Discovery
1. **Receptor identification**: Identify key receptor for the target protein
2. **Ligand design**: Find/design ligands for the receptor
3. **Molecular docking**: Create analogs and test binding
4. **ADME properties**: Evaluate Absorption, Distribution, Metabolism, Excretion
5. **Best analog selection**: Identify optimal therapeutic candidate

## Implementation Plan

### Overview
A two-part pipeline for Alzheimer's therapeutic target discovery:
- **Part 1**: Statistical analysis to identify proteins showing early neuroinflammation before cognitive decline
- **Part 2**: Drug discovery pipeline from receptor identification to optimized ligand candidates

### Architecture: 11 New Modules

The implementation extends the existing codebase (`src/data_loader.py`, `src/analyzer.py`, `src/visualizer.py`) with:

**Part 1 Modules (Statistical Analysis)**:
1. `src/progression_analyzer.py` - Define fast/slow progressors using longitudinal cognitive decline
2. `src/statistical_analyzer.py` - ANOVA/Kruskal-Wallis tests, effect sizes, trajectory analysis
3. `src/survival_analyzer.py` - Cox proportional hazards for hazard ratios
4. `src/target_prioritization.py` - Multi-criteria scoring system (early upregulation, correlation, hazard ratio, trajectory)
5. `src/visualizer.py` - Extend with 6 new methods (trajectories, forest plots, radar charts)

**Part 2 Modules (Drug Discovery)**:
6. `src/receptor_identification.py` - Query UniProt, STRING, DrugBank for protein-receptor interactions
7. `src/ligand_preparation.py` - Build ligand libraries from PubChem/ChEMBL, generate analogs with RDKit
8. `src/protein_preparation.py` - Retrieve PDB structures, prepare PDBQT files, identify binding sites
9. `src/molecular_docking.py` - AutoDock Vina wrapper for ligand-receptor docking
10. `src/adme_evaluation.py` - Predict BBB permeability, Lipinski Rule of 5, toxicity
11. `src/drug_candidate_selection.py` - Integrate docking + ADME scores, rank candidates

**Orchestration**:
12. `src/pipeline.py` - Master controller coordinating all modules

## Detailed Implementation

### Part 1: Statistical Analysis for Target Identification

#### Step 1: Progression Classification
**Module**: `src/progression_analyzer.py`

**Approach**:
- Identify 7 participants with longitudinal data (2-3 visits)
- Calculate cognitive decline rate per participant: slope of MMSE/MoCA vs. time (months)
- Classify fast/slow progressors: median split of decline rates
- Calculate protein change rates: slope of protein levels vs. time
- Correlate protein changes with cognitive decline (Pearson/Spearman r)

**Key Method**: `calculate_cognitive_decline_rate()` uses `scipy.stats.linregress`

#### Step 2: Cross-Sectional Statistical Testing
**Module**: `src/statistical_analyzer.py`

**Approach**:
- For each of 10 proteins, compare CN vs. MCI vs. AD groups
- Statistical tests:
  - Shapiro-Wilk normality test
  - Levene's homogeneity of variance
  - One-way ANOVA (parametric) or Kruskal-Wallis (non-parametric)
  - Post-hoc: Tukey HSD or Dunn's test with Bonferroni correction
  - Effect sizes: Cohen's d (pairwise), eta-squared (overall)
- Calculate trajectory slope: linear fit of mean levels across CN → MCI → AD
- Early detection potential: CN vs. MCI comparison (fold change, effect size)

**Libraries**: `scipy.stats`, `statsmodels`, `scikit-posthocs`, `pingouin`

#### Step 3: Hazard Ratio Analysis
**Module**: `src/survival_analyzer.py`

**Approach**:
- Format data for survival analysis:
  - Event = 1 if progressed (CN→MCI/AD or MCI→AD), 0 if stable
  - Time = months from baseline to progression or last visit
  - Covariates = protein level (baseline), age, sex, APOE genotype
- Fit Cox proportional hazards model: h(t) = h₀(t) × exp(β₁×protein + β₂×age + ...)
- Extract hazard ratio: HR = exp(β₁) with 95% CI and p-value
- Interpretation: HR > 1 means higher protein → faster progression

**Library**: `lifelines` (Cox regression, Kaplan-Meier)

#### Step 4: Target Prioritization Scoring
**Module**: `src/target_prioritization.py`

**Composite Score Formula** (normalized 0-100):
```
Target Score = 0.25×Early_Upregulation + 0.20×Disease_Correlation +
               0.20×Trajectory_Steepness + 0.20×Hazard_Ratio +
               0.15×Statistical_Significance
```

**Criteria**:
1. **Early Upregulation** (25%): Cohen's d for CN vs. MCI (larger = earlier change)
2. **Disease Correlation** (20%): Pearson r with disease stage (CN=0, MCI=1, AD=2)
3. **Trajectory Steepness** (20%): Slope magnitude across CN→MCI→AD
4. **Hazard Ratio** (20%): log(HR) from Cox model
5. **Statistical Significance** (15%): Inverse p-value from ANOVA

**Output**: Ranked list of proteins with top 2-3 selected as therapeutic targets
**Filter**: Focus on neuroinflammation markers (GFAP, YKL-40, S100B) - druggable, not disease markers like Aβ

#### Step 5: Visualizations
**Extend**: `src/visualizer.py`

**Add 6 new methods**:
1. `plot_protein_trajectory()` - Box plots (CN/MCI/AD) + longitudinal participant lines
2. `plot_forest_plot_hazard_ratios()` - Forest plot with HR and 95% CI
3. `plot_correlation_matrix_disease_stage()` - Heatmap of protein-disease correlations
4. `plot_progression_scatter()` - Cognitive decline rate vs. protein change rate
5. `plot_target_prioritization_radar()` - Radar chart comparing top 3 targets on 5 criteria
6. `plot_longitudinal_trajectories()` - Spaghetti plots colored by diagnosis

**Output**: 15+ publication-quality figures (300 DPI PNG)

### Part 2: Drug Discovery Pipeline

#### Step 6: Receptor Identification
**Module**: `src/receptor_identification.py`

**Approach**:
- For each top target (e.g., GFAP), query databases:
  - **UniProt API**: Protein-protein interactions
  - **STRING database**: Interaction networks (confidence scores)
  - **DrugBank**: Known drugs targeting the protein
  - **PubMed Entrez**: Literature search for "{protein} receptor"
- Compile receptor profile: primary receptors, binding partners, known modulators
- Output: JSON report per target with druggability assessment

**Note**: Implement local caching and retry logic for API rate limits

#### Step 7: Ligand Library Preparation
**Module**: `src/ligand_preparation.py`

**Approach**:
- Search bioactive compounds:
  - **PubChem**: Search by target name
  - **ChEMBL**: Search by target ID, filter IC50/Ki < 10 μM
- Generate analogs from lead compounds (50 variants per lead):
  - Scaffold hopping
  - R-group enumeration
  - Bioisosteric replacements (RDKit)
- Convert SMILES to 3D structures:
  - RDKit 3D coordinate generation
  - UFF energy minimization
  - Save as PDB files
- Library size: 50-100 compounds per target

**Library**: `rdkit`, `chembl_webresource_client`

#### Step 8: Protein Structure Preparation
**Module**: `src/protein_preparation.py`

**Approach**:
- Retrieve receptor structures:
  - Query RCSB PDB for crystal structures (prioritize high resolution)
  - Fallback: AlphaFold predicted structures
- Prepare for docking:
  - Remove water molecules
  - Remove heteroatoms (unless co-crystallized ligand)
  - Add hydrogens
  - Convert to PDBQT format (AutoDock Vina)
- Identify binding site:
  - Co-crystallized ligand position (if available)
  - Cavity detection (Fpocket or literature)
  - Output: center coordinates (x, y, z) and box size (20×20×20 Å)

**Tools**: RDKit/BioPython for parsing, MGLTools/Open Babel for PDBQT conversion

#### Step 9: Molecular Docking
**Module**: `src/molecular_docking.py`

**Approach**:
- Prepare ligands: Convert PDB → PDBQT
- Run AutoDock Vina:
  - Input: receptor PDBQT, ligand PDBQT, binding site coordinates
  - Parameters: exhaustiveness=8, n_poses=9
  - Output: Binding affinity (kcal/mol), 9 poses ranked by score
- Parallel docking: Process library with multiprocessing (n_jobs=4)
- Extract top pose for each compound

**Software**: AutoDock Vina (install via conda)
**Scoring**: More negative affinity = stronger binding (typical range: -4 to -12 kcal/mol)
**Threshold**: Filter compounds with affinity < -7.0 kcal/mol

#### Step 10: ADME Property Evaluation
**Module**: `src/adme_evaluation.py`

**Approach**:
- **Lipinski Rule of 5** (drug-likeness):
  - MW ≤ 500 Da
  - LogP ≤ 5
  - H-bond donors ≤ 5
  - H-bond acceptors ≤ 10

- **BBB Permeability** (CRITICAL for AD drugs):
  - TPSA < 90 Ų
  - MW < 450 Da
  - 1 < LogP < 3
  - H-bond donors ≤ 3
  - Predicted with RDKit descriptors + pkCSM API

- **ADME Predictions**:
  - Absorption: Caco-2 permeability, human absorption %
  - Distribution: Volume of distribution, plasma protein binding
  - Metabolism: CYP450 substrate/inhibitor profile
  - Toxicity: Ames mutagenicity, hepatotoxicity, cardiotoxicity

**Tools**: RDKit (primary), pkCSM API (validation), ADMETlab 2.0 (alternative)

**Output**: Filter to BBB-permeant, Lipinski-compliant, non-toxic compounds

#### Step 11: Drug Candidate Selection
**Module**: `src/drug_candidate_selection.py`

**Drug Score Formula** (0-100):
```
Drug Score = 0.30×Binding_Affinity + 0.25×BBB_Permeability +
             0.15×Lipinski_Compliance + 0.15×Metabolic_Stability +
             0.15×Toxicity_Inverse
```

**Weights optimized for CNS drugs** (BBB permeability is critical)

**Filtering Cascade**:
1. Docking affinity < -7.0 kcal/mol
2. Lipinski Rule of 5: pass
3. BBB permeant: yes
4. Ames test: negative
5. Hepatotoxicity: low
6. CYP3A4 inhibition: not strong

**Output**: Top 5 drug candidates per target with comprehensive reports (structure, scores, binding pose visualization)

### Pipeline Orchestration

**Module**: `src/pipeline.py`

**Master Class**: `TherapeuticTargetPipeline`

**Methods**:
- `run_part1_statistical_analysis()` → Returns top 2-3 targets
- `run_part2_drug_discovery(targets)` → Returns top 5 candidates per target
- `run_complete_pipeline()` → End-to-end execution

**CLI Interface** (update `main.py`):
```bash
python main.py --mode all          # Full pipeline
python main.py --mode part1        # Statistical analysis only
python main.py --mode part2 --targets outputs/results/top_therapeutic_targets.csv
```

## Configuration Updates

**File**: `config.py`

**Add**:
```python
# New directories
STRUCTURES_DIR = BASE_DIR / "structures"
DOCKING_DIR = BASE_DIR / "docking_results"
CACHE_DIR = BASE_DIR / "cache"

# Statistical parameters
PROGRESSOR_PERCENTILE = 50.0
SCORING_WEIGHTS = {
    'early_upregulation': 0.25,
    'disease_correlation': 0.20,
    'trajectory_steepness': 0.20,
    'hazard_ratio': 0.20,
    'statistical_significance': 0.15
}

# Docking parameters
VINA_EXHAUSTIVENESS = 8
DOCKING_AFFINITY_CUTOFF = -7.0
BBB_REQUIRED = True
```

## Dependencies

**Add to `requirements.txt`**:
```
# Part 1: Statistical Analysis
lifelines>=0.28.0
scikit-posthocs>=0.8.0
pingouin>=0.5.3

# Part 2: Drug Discovery
rdkit>=2023.9.1
chembl-webresource-client>=0.10.8
biopython>=1.81
py3Dmol>=2.0.3
```

**External Software**:
```bash
conda install -c conda-forge autodock-vina
```

## Implementation Sequence

### Phase 1: Statistical Foundation (Priority 1)
1. Install dependencies, update `config.py`
2. Create `progression_analyzer.py` - progression classification
3. Create `statistical_analyzer.py` - ANOVA/KW tests, trajectories
4. Create `survival_analyzer.py` - Cox regression
5. Create `target_prioritization.py` - composite scoring
6. Extend `visualizer.py` - 6 new plot methods
7. **Validate**: Run Part 1, generate all figures/results

### Phase 2: Drug Discovery Setup (Priority 2)
8. Create `receptor_identification.py` - API integrations
9. Create `ligand_preparation.py` - RDKit workflows
10. Create `protein_preparation.py` - PDB handling
11. **Validate**: Test structure retrieval and preparation

### Phase 3: Docking & ADME (Priority 3)
12. Install AutoDock Vina, test basic docking
13. Create `molecular_docking.py` - Vina wrapper
14. Create `adme_evaluation.py` - property predictions
15. **Validate**: Dock 5-10 test compounds, check ADME

### Phase 4: Integration (Priority 4)
16. Create `drug_candidate_selection.py` - final scoring
17. Create `pipeline.py` - orchestration
18. Update `main.py` - CLI interface
19. **Validate**: Run complete pipeline on mock data

### Phase 5: Documentation & Testing (Priority 5)
20. Write unit tests (target 80% coverage)
21. Validate results against literature
22. Document all functions/classes
23. Create usage README

**Timeline**: 12 days full-time or 3-4 weeks part-time

## Expected Outputs

### Part 1: Statistical Analysis
**Files**:
- `progressor_classification.csv` (7 participants)
- `statistical_tests_all_proteins.csv` (10 proteins)
- `hazard_ratios.csv` (10 proteins)
- `target_prioritization_scores.csv` (10 proteins ranked)
- `top_therapeutic_targets.csv` (top 2-3)
- 15+ figures (trajectories, forest plots, radar charts)

**Key Finding**: 2-3 neuroinflammation proteins (likely GFAP, YKL-40) showing early upregulation before cognitive decline

### Part 2: Drug Discovery
**Files**:
- `receptor_profiles/*.json` (2-3 targets)
- `ligand_library_*.csv` (50-100 compounds per target)
- `docking_scores.csv` (all docking results)
- `adme_properties.csv` (all compounds)
- `final_drug_candidates.csv` (top 5 per target)
- `drug_candidate_reports/*.json` (detailed profiles)
- 300+ structure files (proteins, ligands, docked poses)
- 5-10 figures (binding poses, ADME distributions)

**Key Finding**: 5-10 BBB-permeant compounds with strong binding affinity and favorable ADME profiles

## Critical Files to Implement

1. **`src/target_prioritization.py`** - Bridges Part 1 and Part 2, determines which proteins become therapeutic targets
2. **`src/molecular_docking.py`** - Core of Part 2, most technically complex (Vina integration)
3. **`src/statistical_analyzer.py`** - Foundation of Part 1, establishes statistical significance
4. **`src/adme_evaluation.py`** - Critical BBB filter for CNS drugs
5. **`src/pipeline.py`** - Orchestrates entire workflow

## Risk Mitigation

**Challenge**: Limited longitudinal data (7 participants)
**Solution**: Supplement with cross-sectional analysis, use effect sizes, bootstrap CIs

**Challenge**: Mock data statistical power
**Solution**: Focus on effect sizes > p-values, report biological plausibility, acknowledge limitations

**Challenge**: AutoDock Vina setup
**Solution**: Detailed conda instructions, test on multiple platforms, document troubleshooting

**Challenge**: ADME prediction accuracy
**Solution**: Consensus of multiple methods, conservative BBB filters, validate against literature

**Challenge**: API rate limits
**Solution**: Local caching, retry logic, exponential backoff, offline fallbacks

## Success Criteria

✓ Identified 2-3 proteins with early upregulation (Cohen's d > 0.5)
✓ Significant disease correlation (|r| > 0.5, p < 0.05)
✓ Hazard ratio > 1.5 for top targets
✓ Retrieved structures for all targets
✓ 50-100 ligands docked per target
✓ 5-10 BBB-permeant candidates with affinity < -7 kcal/mol
✓ All outputs generated with comprehensive reports
✓ Complete pipeline execution in < 4 hours
