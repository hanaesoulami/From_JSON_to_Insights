
# **From JSON to Insights** – ETL & Data Modeling for a Music App

This project demonstrates how I designed a **PostgreSQL database** and built an **end-to-end ETL pipeline using Python** to help a music streaming startup analyze user activity and song plays. I worked on transforming raw JSON data into a structured, queryable format so insights could be easily generated.

---

### **What I Did**
- Explored and cleaned raw datasets (song metadata and user activity logs).  
- Designed a **star schema**: fact table (`songplays`) and dimension tables (`users`, `songs`, `artists`, `time`).  
- Built an **ETL pipeline in Python** to extract, transform, and load data into PostgreSQL.  
- Validated the data to ensure consistency and correct relationships between tables.  

---

### **Datasets**
- **Songs dataset**: Metadata for songs and artists (subset of Million Song Dataset).  
- **Logs dataset**: Simulated user activity including song plays, sessions, and page visits.  

---

### **Database Design**
The database uses a **star schema** to make analytics queries efficient:  

- **Fact table**: `songplays` – stores song play events.  
- **Dimension tables**:  
  - `users` – user info (name, gender, level).  
  - `songs` – song info (title, duration, year).  
  - `artists` – artist info (name, location, coordinates).  
  - `time` – timestamps broken down into hour, day, week, month, year, weekday.  

This schema allows the team to quickly answer questions like:  
- What songs are most popular?  
- Who are the most active users?  
- Which artists are trending over time?  

---

### **Project Structure**
| File | Description |
|------|-------------|
| `sql_queries.py` | SQL statements for creating, dropping, and inserting tables |
| `create_tables.py` | Sets up PostgreSQL database and tables |
| `etl.py` | Python script to extract, transform, and load JSON data |
| `etl.ipynb` | Jupyter Notebook to explore and understand datasets |
| `test.ipynb` | Notebook to validate the loaded data |

---

### **Technologies**
- Python 3.6+  
- PostgreSQL 9.5+  
- `psycopg2` for connecting Python to PostgreSQL  
- Jupyter Notebook for exploration and testing  

---

### **How to Run**
1. Run the main program:  
```bash
python main.py
