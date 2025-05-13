# Piscine Data Science

⚠️ This project has not undergone a formal review—there may be typos, bugs, or inconsistencies. Use at your own risk.

This repository contains the solutions for the **Piscine Data Science** program at 42, organized by day and module.

## 📂 Project Structure
```
.
├── Data_Warehouse/            # Day 1: SQL / ETL
│   ├── ex01/                  # Create customers table
│   ├── ex02/                  # Remove duplicate entries
│   └── ex03/                  # Merge tables
├── Data_viz/                  # Day 2: Data Visualization
│   ├── ex00/                  # Pie chart
│   ├── ex01/                  # Time-series charts
│   ├── ex02/                  # Boxplots (“Mustache”)
│   ├── ex03/                  # Histograms (orders & spending)
│   ├── ex04/                  # Elbow Method
│   └── ex05/                  # K-Means clustering
├── Data_scientist_1/          # Day 3: Statistics & Preprocessing
│   ├── ex00/                  # Knights’ skills histograms
│   ├── ex01/                  # Correlation analysis
│   ├── ex02/                  # Scatter plots
│   ├── ex03/                  # Standardization (Z-score)
│   ├── ex04/                  # Normalization (Min–Max)
│   └── ex05/                  # Train/Validation split
├── Data_scientist_2/          # Day 4: Modeling & Prediction
│   ├── ex00/                  # Confusion matrix
│   ├── ex01/                  # Correlation heatmap
│   ├── ex02/                  # PCA scree plot
│   ├── ex03/                  # Feature selection (VIF)
│   ├── ex04/                  # Decision tree & random forest
│   ├── ex05/                  # KNN (optimal k search)
│   └── ex06/                  # Voting classifier
├── docker-compose.yml         # Docker compose configuration
├── Dockerfile                 # Docker image build instructions
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files and directories to ignore in Git
└── README.md                  # Project overview (this file)
```

## 🛠 Prerequisites
- Docker & Docker Compose
- Python 3.9 or higher
- (Optional) Virtual environment

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

1. **Start Docker services**
   ```bash
docker-compose up -d --build
```

2. **Initialize the Data Warehouse**
   ```bash
docker-compose exec db psql -U bea -d piscineds \
  -f Data_Warehouse/ex01/create_customers.sql \
  -f Data_Warehouse/ex02/remove_duplicates.sql \
  -f Data_Warehouse/ex03/fusion.sql
```
   Access pgAdmin at http://localhost:8081 (user: admin@admin.com / pass: admin)

3. **Run Day 2 Visualization Scripts**
   ```bash
cd Data_viz
python ex00/pie.py --input_folder /data/customer --output ./ex00/output/pie.png
python ex01/chart.py --outdir ./ex01/output
# Repeat for ex02–ex05
```

4. **Run Day 3 Preprocessing Scripts**
   ```bash
cd ../Data_scientist_1/ex00
python histogram.py --train Train_knight.csv --test Test_knight.csv --output Histogram.png
# Repeat for ex01–ex05
```

5. **Run Day 4 Modeling Scripts**
   ```bash
cd ../../Data_scientist_2
python ex00/Confusion_Matrix.py predictions.txt truth.txt
python ex01/Heatmap.py --input data.csv --output heatmap.png
python ex02/variances.py --input Train_knight.csv --output variances.png
python ex03/Feature_Selection.py --train Train_knight.csv --test Test_knight.csv
python ex04/Tree.py Train_knight.csv Test_knight.csv --output Tree.txt
python ex05/KNN.py Train_knight.csv Test_knight.csv --output KNN.txt
python ex06/democracy.py Train_knight.csv Test_knight.csv --output Voting.txt
```







