# ex00 — Data Warehouse Verification

This exercise focuses on **verifying accessibility and structure of the data warehouse**
after the initial ingestion and table creation steps.

The goal is to ensure that the database is reachable and that the expected warehouse
tables are present and correctly exposed for querying and downstream processing.

---

## Objective

- Verify connectivity to the data warehouse
- Inspect the database schemas and tables
- Confirm that ingestion and table creation steps completed successfully
- Validate the warehouse layer before applying transformations or analytics

---

## What Is Being Verified

The following aspects are checked:

- Database availability
- Correct database and active schema
- Presence of expected warehouse tables
- Structural consistency of ingested data

This step acts as a **sanity check** for the data warehouse layer.

---

## Warehouse Exploration

Using a PostgreSQL-compatible client (such as a database administration tool or CLI),
navigate through the database structure:

```text
Databases
└── <warehouse_database>
    └── Schemas
        └── public
            └── Tables
Confirm that the warehouse exposes tables corresponding to:

Ingested customer datasets (e.g. monthly partitions)

Reference or lookup tables (such as items)

Derived or consolidated customer tables produced by previous steps

Exact table names may vary depending on the ingestion and transformation configuration.

Notes
No credentials or connection parameters are hard-coded in this repository

Access details depend on the local or containerized environment

This exercise does not generate outputs or persisted artifacts

Context
This verification step ensures that the data warehouse layer is consistent and queryable
before proceeding to data cleaning, deduplication, or dataset fusion.

All subsequent data warehouse exercises assume that this layer is correctly initialized.







