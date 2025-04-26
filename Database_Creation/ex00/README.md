ex00 – Database Visualization

In this exercise, there are no code files to submit. You only need to verify that the piscineds database is accessible and can be viewed in pgAdmin 4.

Steps to Complete the Exercise

Launch pgAdmin

macOS GUI: Run make pgadmin-native to open the pgAdmin 4 application.

Docker Compose: Run make pgadmin and open http://localhost:8080 in your browser.

Log in to pgAdmin

Email: admin@admin.com

Password: admin

Configure the PostgreSQL Server Connection

Name (Server): piscineds

Host Name/Address: db (or localhost if you are not using Docker)

Port: 5432

Maintenance Database: piscineds

Username: bea

Password: mysecretpassword

Explore the Tables

In the left panel, expand the following tree:

Servers
└─ piscineds
   └─ Databases
      └─ piscineds
         └─ Schemas
            └─ public
               └─ Tables

Confirm that these tables are listed:

data_2022_oct, data_2022_nov, data_2022_dec, data_2023_jan

items

Refresh the Table List

If you have added or removed tables, right-click on Tables and select Refresh.