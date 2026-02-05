# ex00 – Database Visualization for Data Warehouse

In this exercise (Ex00) of the **Data Warehouse** module, you will verify that the `piscineds` database is accessible and explore its tables in pgAdmin 4.

## Steps

1. **Launch pgAdmin**
   - Via Docker Compose:
     ```bash
     make pgadmin
     ```
   - Or on macOS GUI:
     ```bash
     make pgadmin-native
     ```

2. **Open pgAdmin in your browser**
   ```
   http://localhost:8080
   ```

3. **Log in**
   - **Email:** `admin@admin.com`
   - **Password:** `admin`

4. **Create/Select the Server Connection**
   - **Name:** `piscineds`
   - **Host:** `db` (or `localhost` if not using Docker)
   - **Port:** `5432`
   - **Maintenance DB:** `piscineds`
   - **User:** `bea`
   - **Password:** `mysecretpassword`

5. **Explore the `public` schema**
   - In the left panel, expand:
     ```
     Servers → piscineds → Databases → piscineds → Schemas → public → Tables
     ```
   - Confirm that the following tables exist:
     - `data_2022_oct`, `data_2022_nov`, `data_2022_dec`, `data_2023_jan`, `data_2023_feb`
     - `items` (if loaded)
     - `customers`, `customers_distinct`, `customers_dedup`, `customers_full`

6. **Refresh if needed**
   - Right-click on **Tables** and select **Refresh** to reload the list.





