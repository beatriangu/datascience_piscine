# ex00 — Database Verification

This exercise focuses on **verifying database accessibility and structural integrity**
after the initial data engineering setup has been completed.

No application code is implemented at this stage.  
The goal is to confirm that the database is correctly initialized, reachable,
and populated with the expected tables.

---

## Objective

- Verify connectivity to the PostgreSQL database
- Inspect schemas and table structures
- Ensure ingested data is visible and consistent
- Validate the data foundation before downstream processing

---

## What Is Verified

The following aspects are checked:

- Database availability
- Correct database name and active schema
- Presence of expected tables
- Successful data ingestion from previous steps

This step acts as a **sanity check** for the data engineering layer.

---

## Database Exploration

Using a PostgreSQL client (such as `psql` or a database administration tool),
navigate through the following structure:

```text
Databases
└── <database_name>
    └── Schemas
        └── public
            └── Tables
Confirm that the expected tables are present, including:

Customer-related tables (e.g. monthly datasets)

Items or reference tables

Exact table names may vary depending on the ingestion configuration.

Notes
No credentials or connection details are hard-coded in this repository

Database access parameters depend on the local or containerized environment

This exercise does not generate outputs or artifacts

Context
This verification step ensures that the data engineering foundation is solid
before proceeding to data warehousing, analysis, or modeling stages.

All subsequent modules assume that this database layer is accessible and consistent.
