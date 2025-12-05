# 🏭 Warehouse Intelligence & Analytics Platform (WIAP)

This project mirrors a **real enterprise warehouse data platform** and showcases depth across,


```
* Data Engineering/ Data analytics (DE/DA)
* Data Modeling & Power BI Development
* Operational KPI/ SLA Frameworks
* End-to-end FMCG, Warehouse, Logistics and QC Domain Knowledge 
```

Click here to interact with the [Online **Dashboard**](https://app.powerbi.com/view?r=eyJrIjoiODYzM2RmOWMtYzA5Yi00MzQzLTkyYTEtODMxNWJmOTQ2M2FhIiwidCI6ImM0ZGRhYWFjLTQ4OWItNGQ1Zi1hMzVjLWFhODVlNmVkZjhkOCJ9)

![cover image](images\cover_image.png)

**WIAP** is a full-stack **data engineering + analytics + warehouse operations intelligence platform** designed to simulate and analyze real FMCG/3PL warehouse environments.

This project is basically a **warehouse digital twin**:

* Generates complex synthetic operational data (Inbound, Outbound, Inventory, Transport, Quality, HR).
* Loads everything into a **PostgreSQL warehouse** with a fully normalized schema.
* Creates **views powered by heavy SQL**, data cleaning, imputations, and logic transformations.
* Builds an analytic semantic layer in **Power BI** with M-ETL pipelines and optimized schemas.
* Delivers **70+ operational KPIs** used in real warehouse management.

Everything mirrors **real industry workflow** learned from *9+ years* working in food FMCG QA, warehousing, and logistics.

---

## 📋 Project Planning & Scoping

### **Goals**

* Build a *realistic*, scalable warehouse data ecosystem.
* Showcase **analytics engineering** + **data engineering** workflow end-to-end.
* Create a modular platform that supports future ML and forecasting.
* Demonstrate strong BI concepts: modeling, KPI governance, DAX standards.
* Highlight my operational intelligence from QA + FMCG + logistics.

### **Objectives**

* Design enterprise-grade schema (normalized + views).
* Create multi-domain synthetic data with natural randomness.
* Build reproducible ETL logic.
* Develop BI dashboards that mimic real 3PL/WH KPIs/ SLAs.
* Create documented KPI dictionary for governance.
---
## ♻️ Basic Warehouse Operation Flow

![WH operation](images\wh_process.png)
</br>
*`End-to-end WH operation`*

---

## 🗂️ GitHub Projects Board

A **Kanban board** is included to track:

* Data generation tasks
* Schema iterations
* Loader fixes
* View redesigns
* Power BI modeling
* KPI validation
* Future roadmap (Phase II Ops)

![GitHub Projects](images\github_projects.png)
</br>`Progress tracking with GitHub Projects - Kanban board`*

---

## 🛠️ Tech Stack

### **Data Engineering & Analytics Stack**

| Category | Tools |
|---------|-------|
| **Python & Data Generation** | ![Python](https://img.shields.io/badge/Python_3.11-Data_Generation-3776AB.svg?logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg?logo=pandas&logoColor=white) ![Random](https://img.shields.io/badge/Random-Randomization-3776AB.svg?logo=python&logoColor=white) ![OS](https://img.shields.io/badge/OS-System_Ops-3776AB.svg?logo=python&logoColor=white) ![DateTime](https://img.shields.io/badge/Datetime-Time_Handling-3776AB.svg?logo=python&logoColor=white) ![Logging](https://img.shields.io/badge/Logging-Debugging-3776AB.svg?logo=python&logoColor=white) ![Time](https://img.shields.io/badge/Time-Timing-3776AB.svg?logo=python&logoColor=white) ![IDE](https://img.shields.io/badge/VS_Code-IDE-007ACC.svg?logo=visualstudiocode&logoColor=white) |
| **LLM Integration** | ![Ollama](https://img.shields.io/badge/Ollama-LLM_Framework-7C3AED.svg?logo=ollama&logoColor=white) ![Mistral](https://img.shields.io/badge/Mistral_1.5B-Local_LLM-5E17EB.svg?logo=ai&logoColor=white) |
| **Database Connectivity** | ![Psycopg2](https://img.shields.io/badge/psycopg2-Database_Driver-336791.svg?logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-EE0000.svg?logo=sqlalchemy&logoColor=white) |
| **SQL Database Management** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DBMS-336791.svg?logo=postgresql&logoColor=white) ![DBeaver](https://img.shields.io/badge/DBeaver-DB_Client-372923.svg?logo=dbeaver&logoColor=white) |

---

### **BI & Analytics Engineering**

| Category | Tools |
|---------|--------|
| **Power Platform & Visualization** | ![Power BI](https://img.shields.io/badge/Power_BI-Analytics-F2C811.svg?logo=powerbi&logoColor=black) |

---

### **Development & Workflow**

| Category | Tools |
|---------|--------|
| **Version Control, Project Tracking & Documentation** | ![Git](https://img.shields.io/badge/Git-Version_Control-F05032.svg?logo=git&logoColor=white) ![GitHub and GitHub Projects](https://img.shields.io/badge/GitHub_&_GitHub_Projects-Progress_Tracking_&_Portfolio-181717.svg?logo=github&logoColor=white) ![MD](https://img.shields.io/badge/Markdown-Documentation-000000.svg?logo=markdown&logoColor=white) |

---

### **AI & Productivity Tools**

| Category | Tools |
|---------|--------|
| **AI Assistance & Creative Tools** | ![AI](https://img.shields.io/badge/Grok,_ChatGPT,_DeepSeek-AI_Assistance-8B3DFF.svg?logo=ai&logoColor=white) ![UI](https://img.shields.io/badge/Adobe_Photoshop-UI_Design-31A8FF.svg?logo=adobephotoshop&logoColor=white) ![Project Walk-through](https://img.shields.io/badge/CapCut-Project_walk_through-000000.svg?logo=capcut&logoColor=white)![Gemini nano banana](https://img.shields.io/badge/Gemini_Nano_Banana-Multimodal_AI-4285F4.svg?logo=googlegemini&logoColor=white) ![draw.io](https://img.shields.io/badge/diagrams.net-Diagramming-087CFA.svg?logo=diagramsdotnet&logoColor=white) |


---

## 📂 Project Folder
```bash
Data_Analytics_Projects_Warehouse_Process_Analysis_Pipeline/
├── data/
│   └── raw/                           # Raw data generated (Python Libraries + LLM)
│    
├── src/                               # Production-ready Python codes
│   ├── data_generator.py              # LLM functions and DataFrame creation logic
│   └── data_loader.py                 # Logic for loading data from CSVs into the PostgreSQL database.
|
├── sql/                               # PSQL scripts
│   └── schema.sql                     # CREATE TABLE statements for the database schema
|
├── KPI_docs/                          # Extensions to the main README.md to expand KPIs
│   ├── KPI_COO.md                     # KPIs in COO's view
│   ├── KPI_Inbound.md                 # KPIs in Inbounds & Returns Page
│   └── KPI_Outbound.md                # KPIs in Outbounds Page
│
├── reports/                           # Final reports and visualizations
│   ├── project_doc.docx.py            # Project Report 
│   ├── project_video.mp4              # Dashboard/ Report walkthrough
│   └── Operations_Dashboard_P01.pbix  # Data cleaning, data modeling, data analysis, visualization and publish
│
├── images/                            # All relevant image files
|
├── LICENSE.md                         # MIT License
├── .gitignore                         # Files and folders to ignore in Git.
└── README.md                          # Project documentation
```
---
## Data Pipeline - *from mid to matrix*</br><font size=2>🧠 Idea → 🎨 Design → 🔁 ETL → 📊 Analyze → 🎛️ Dashboard → 📈 Results</font>
![Data Pipeline](images\data_pipeline.png)

## 🏗️ Data Architecture
*Python + VS Code - [`data_generator.py`](src\data_generator.py)*
- Python-generated synthetic datasets  
- SQL-first normalized schema (PK/FK, indexes)  
- Data cleaning via SQL views  
- ETL pipeline using SQLAlchemy  
- Power BI data modeling & measure tables  
- Department-wise KPI models  

---

## 🧱 Schema Design
*PostgreSQL + VS Code - [`schema.sql`](sql\schema.sql)*
- 4 standalone dimension tables  
- 10 dependent operational tables  
- 2 monitoring/incident tables  
- 16 analytics-ready views  
- Full PK/FK relationships  
- Indexes for query performance  

The schema follows a **Raw → Clean Views → PBI ETL → BI Model** architecture.

---

## 🔄 ETL & Loading
*Python + VS Code - [`data_loader.py`](src\data_loader.py)*
- FK-safe load sequence  
- UPSERT logic (`ON CONFLICT`)  
- Automated logging  
- Idempotent reruns  
---

## 🧹 View Layer (Advanced SQL)
*PostgreSQL + DBeaver - [`views.sql`](sql\views.sql)*
- LLM hallucination corrections
- Missing value imputation
- NaN → TRUE logic conversions
- Dimensional transformations
- Standardized naming conventions
- RegEx cleanup
- Time-casting, type standardization  
- Derived KPIs (cycle times, severities, statuses)  
- Normalization of messy logs  
---

## 🔧 ETL in Power BI

**Power Query Editor**:

* Data profiling
* Quality checks
* Column-level lineage
* Conditional transformations
* Metadata management
* Governance patterns
* Versioned query groups
* Staging → Clean → Fact → Dim layering

---

## 📊 Data Modeling (Power BI)

Model highlights:

* Complex-schema with clean relationship directions 
* Row-level granularity by operation
* Model optimization:
  * Field parameter grouping
  * Surrogate keys
  * Removing high-cardinality clutter
  * Merged fact tables
* Department-wise measure tables
* KPI folders for governance

![Data Model](images\wh_data_model.png)</br>
*`Data model`*

---

## 📈 Analytics Delivered (Phase I)

Each KPI includes:
1. Business Question  
2. Formula
3. Importance  
4. Operational Meaning (High vs Low)    
5. How to Improve  

### 📙 COO's Dashboard (section wise) - [*COO's  KPI Dictionary 🔍*](KPI_doc\KPI_COO.md)
✔ Revenue, Profit, CBM flows  
✔ Workforce demographics  
✔ Warehouse utilization  
✔ All operational KPIs summarized  

![COO's view](images\coo_dashboard.png)</br>
*`COO's UI`*

### 📗 Inbound/ Retunrs KPIs - [*Inbound/ Returns KPI Dictionary 🔍*](KPI_doc\KPI_Inbound.md)
✔ Labour efficiency  
✔ Shift productivity (Inbound, Returns)  
✔ Operational Cycle times (Picking, Loading, Return handling)  
✔ On-time put-away %  
✔ Rejection % analyses  
✔ Supplier performance  
✔ Return behaviors   
✔ Incident reporting

![Inbounds](images\inbound_dashboard.png)</br>
*`Inbounds UI`*

![Returns](images\retunrs_dashboard.png)</br>
*`Returns UI`*


### 📘 Outbound KPIs - [*Outbound KPI Dictionary 🔍*](KPI_doc\KPI_Outbound.md)
✔ Labour efficiency  
✔ Shift productivity  
✔ Order fulfillment %   
✔ Operational cycle time  
✔ WH Throughput (Cartons, CBM, Pallet)  
✔ Failed-pick product analysis   
✔ Lost GP due to failed-picks  
✔ Vehicle utilization  
✔ On-Time-Dispatch (OTD) %  

![Outbound](images\outbound_dashboard.png)</br>
*`Outbounds UI`*

---

## 🧭 Roadmap (Phase II)
- Inventory Control analytics
- Quality Control analytics   
- Transport/ Logistics analytics   
---

## 🧭 Future Enhancements
* Integrate Sales data model to perform a financial analysis
* Predictive analysis with Machine Learnig models


---
## 👷 How to Run WIAP
<details>
<summary><strong>📘 Shall we explore how to run the WIAP 🔍 ..?</strong></summary>

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/wiap.git
cd wiap

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL (Docker)
docker-compose up -d

# 4. Generate synthetic datasets
python data_generation/data_generator.py

# 5. Load data into the DW
python etl/data_loader.py

# 6. Open Power BI Desktop and proceed with your own analysis and visualization
.pbix file is not inluded
```
</details>

## 📝 Commit Message Convention
<details>
<summary><strong>📘 Want to commit 🔍 ..?</strong></summary>

```
feat: added supplier rejection logic  
fix: corrected on-time putaway calculation  
docs: updated KPI dictionary  
refactor: optimized SQL view joins  
test: added loader unit tests  
chore: updated requirements.txt  
```
</details>

## 🔧 How to Contribute
<details>
<summary><strong>📘 Want to explore how you can contribute 🔍 ..?</strong></summary>

```
1. Fork the repo
2. Create a feature branch
3. Follow commit conventions
4. Ensure tests pass
5. Submit PR with:
  * What changed
  * Why it was needed
  * Any dependencies
  * Screenshots (if Power BI)
```
</details>

## 🧪 Testing Strategy
<details>
<summary><strong>📘 Would you like test it 🔍 ..?</strong></summary>

#### ✔ Data Gen Tests

* Column issues
* Null handling
* Pattern consistency
* Business rule checks

#### ✔ ETL Tests

* PK/FK constraints
* UPSERT validation
* Row counts
* Error handling

#### ✔ SQL View Tests

* Data cleaning logic
* COALESCE strategy
* Cycle time calculations
* SLA logic correctness
</details>

---
## 🏁 Final Thoughts

WIAP isn’t a toy project. It’s a **full-fledged warehouse intelligence platform** demonstrating,
- Data engineering abilities  
- Analytics engineering discipline  
- Business logic modeling  
- Dashboard design  
- KPI governance  
- Operational domain knowledge 

---


## 🙏 Heartfelt Thanks & High-Fives All Around..!

- Learning from YouTube communities: *Exploring best practices in KPI representation and user interface design inspiration*.  
- Leveraging AI assistants (Grok, ChatGPT, DeepSeek): *For researching concepts, validating ideas, developing KPI/SLA frameworks, and debugging and optimizing codes*.


---

## 👨‍💻 Author
**Thilina Perera | Data with TP**
```
📌 Data Science/ Data Analytics D-Technosavant
📌 Machine Learning, Deep Learning, LLM/LMM, NLP, and Automated Data Pipelines Inquisitive
``` 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/thilina-perera-148aa934/)  [![TikTok](https://img.shields.io/badge/TikTok-%23000000.svg?logo=TikTok&logoColor=white)](https://tiktok.com/@data_with_tp) [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://youtube.com/@Data_with_TP) [![email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:kgttpereraqatar2022@gmail.com) 

## 🏆 License
    This project is licensed under the MIT License.
    Free to use and extend.