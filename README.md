# 💼 Global Salary & Compensation Analysis

An end-to-end data analysis project exploring salary trends, workforce demographics, and compensation equity across industries, countries, and demographics — using a real-world salary survey dataset of **28,149 responses**.

---

## 📌 Business Problem

This project was designed to answer key questions that matter to HR professionals, job seekers, and organizations focused on pay equity:

### 💰 Salary & Compensation
- What is the salary distribution across industries?
- Which job titles pay the most globally?
- Which countries or states pay above the global/US median for the same role?

### 👩‍💼 Workforce Demographics
- Does age correlate with higher salaries? (youth vs. senior pay gap)
- Do younger professionals in tech earn more than older professionals in non-tech?
- Are certain ethnicities underpaid compared to others, controlling for experience?
- Does education level (Bachelor's, Master's, PhD) justify the pay difference?

### 📈 Career Growth
- How much does pay grow after X years in a domain?
- At what experience level do salaries plateau in certain industries?

### 🔎 Job Market Strategy
- Which industries overpay for entry-level roles?
- Which industries have the smallest gender/ethnic pay gaps?
- Which job titles are most consistent in pay across locations?
- What job/industry combinations have the best bonus structures?
- Where are salaries most volatile for the same role?

> **Who benefits from this analysis?**
> - **HR / Recruiters** → to set competitive pay bands
> - **Employees / Job Seekers** → to know where to maximize earning potential
> - **Companies** → to track inclusivity, fairness, and ROI of education & experience

---

## 🗂️ Dataset Overview

The dataset is a global salary survey with **28,149 entries** and **18 columns**, including:

| Column | Description |
|---|---|
| `survey_time` | Timestamp of survey submission |
| `age` | Age bracket of the respondent |
| `industry` | Industry sector |
| `job_title` | Self-reported job title |
| `annual_salary` | Annual salary (standardized to integer) |
| `currency` | Currency of reported salary |
| `work_country` | Country of work |
| `state(only_USA)` | US state (for US respondents) |
| `work_city` | City of work |
| `overall_work_experience` | Total years of professional experience |
| `domain_work_experience` | Years in current domain/field |
| `education_level` | Highest level of education completed |
| `gender` | Gender identity |
| `ethnicity` | Ethnicity (simplified from free-text) |

---

## ⚙️ Pipeline Overview

The project follows a structured 3-stage pipeline:

```
Raw CSV  ──▶  file_cleaning.py  ──▶  data_ingestion.py  ──▶  MySQL DB  ──▶  EDA Notebook
```

### Stage 1 — File Cleaning (`src/file_cleaing.py`)

The raw survey CSV has extremely verbose, messy column names (full question text as headers). This script:

- Reads the raw `.csv` file
- Renames all 18 columns from their original survey question text to clean snake_case names
- Saves the cleaned file as `fixed_salary_survey.csv` in the `fixed_data/` directory
- Uses a custom logger throughout for traceability

**Column rename mapping (sample):**

| Original Header | Cleaned Name |
|---|---|
| `Timestamp` | `survey_time` |
| `age?` | `age` |
| `What country do you work in?` | `work_country` |
| `What is your gender?` | `gender` |
| `What is your race? (Choose all that apply.)` | `ethnicity` |
| `How many years of professional work experience do you have overall?` | `overall_work_experience` |

---

### Stage 2 — Data Ingestion (`src/data_ingestion.py`)

Once cleaned, the data is loaded into a **MySQL database** for structured querying:

- Scans the `fixed_data/` directory for all `.csv` files
- Uses `pandas.to_sql()` with SQLAlchemy to push each file into MySQL as a table
- Replaces the table on each run (`if_exists='replace'`) to keep the DB fresh
- Logs each step using the custom logger

**Database:** `DATA_Korty` on `localhost:3306`  
**Table:** `fixed_salary_survey`

---

### Stage 3 — EDA & Transformation (`src/Notebook/data_transformation_and_eda.ipynb`)

The main analysis notebook connects directly to MySQL and performs:

**Data Type Fixes:**
- `annual_salary` → stripped of commas, cast to `int`
- `survey_time` → parsed to `datetime`

**Null Value Handling:**

| Column | Null % | Action |
|---|---|---|
| `expected_pay(40hrs)` | 74.1% | Dropped |
| `other_currency` | 99.2% | Dropped |
| `income_context` | 89.2% | Dropped |
| `bonuses` | 26.1% | Dropped |
| `industry`, `job_title`, `gender`, `education_level` | < 1% | Filled with mode |
| `ethnicity` | 0.65% | Filled as `Other/Unknown` |

**Experience Labels — Standardized:**

| Original | Cleaned |
|---|---|
| `1 year or less` | `0-1` |
| `2 - 4 years` | `2-4` |
| `5-7 years` | `5-7` |
| `8 - 10 years` | `8-10` |
| `11 - 20 years` | `11-20` |
| `21 - 30 years` | `21-30` |
| `31 - 40 years` | `31-40` |
| `41 years or more` | `45+` |

**Gender — Simplified:**  
`"Other or prefer not to answer"` and `"Prefer not to answer"` → merged into `"Others"`

**Ethnicity — Reduced from 51 → 7 categories:**  
Free-text responses mapped to: `White`, `Asian`, `Black`, `Hispanic/Latino`, `Middle Eastern`, `Native American`, `Multiracial`, `Other/Unknown`

**Work Country — Standardized from 386 → 93 clean names:**  
All variations of `"US"`, `"U.S.A."`, `"United states"`, `"America"` etc. → `"USA"` (and similarly for all other countries)

---

## 📊 Demographic Snapshot (Post-Cleaning)

**Gender Distribution:**

| Gender | Count |
|---|---|
| Woman | 21,411 |
| Man | 5,518 |
| Non-binary | 747 |
| Others | 299 |

**Ethnicity Distribution:**

| Ethnicity | Count |
|---|---|
| White | 23,249 |
| Multiracial | 1,760 |
| Asian | 1,416 |
| Other/Unknown | 913 |
| Black | 696 |
| Middle Eastern | 72 |
| Native American | 43 |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core analysis language |
| **Pandas** | Data manipulation & cleaning |
| **MySQL** | Data storage (`DATA_Korty` database) |
| **SQLAlchemy + PyMySQL** | Database connection & ORM |
| **mysql-connector-python** | MySQL driver |
| **Seaborn + Matplotlib** | Data visualization |
| **NumPy** | Numerical operations |
| **Jupyter Notebook** | Interactive analysis environment |
| **Custom Logger** | Pipeline traceability (`src/logger.py`) |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/BhaskarMishra05/Data.git
cd Data
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your MySQL database
Create a MySQL database and update the connection string in both `data_ingestion.py` and the notebook:
```python
engine = create_engine('mysql+mysqlconnector://your_user:your_password@localhost:3306/your_database')
```

### 4. Run the pipeline

**Step 1 — Clean the raw file:**
```python
from src.file_cleaing import cleaning_raw_file
df = cleaning_raw_file('path/to/raw_survey.csv')
```

**Step 2 — Ingest into MySQL:**
```bash
python src/data_ingestion.py
```

**Step 3 — Open the notebook:**
```bash
jupyter notebook src/Notebook/data_transformation_and_eda.ipynb
```

---

## 👤 Author

**Bhaskar Mishra**  
[GitHub: @BhaskarMishra05](https://github.com/BhaskarMishra05)
