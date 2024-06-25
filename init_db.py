import sqlite3

# Define database name and CSV filenames (modify as needed)
db_name = "fantasyFootball.db"
csv_files = ["season_summary.csv", "simulated_season_seed.csv", "simulated_season_summary.csv", 'summary_sim.csv', 'summary_weekly.csv']

# Connect to the database
conn = sqlite3.connect(db_name)


def create_table(table_name, csv_file):
  """
  Creates a table in the database based on the schema of the CSV file.
  """
  with open(csv_file, 'r') as f:
      first_line = f.readline().strip().split(',')
      columns = ','.join([f'"{col}"' for col in first_line])

  # Modify data types based on your data
  create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
      {columns}
  )"""
  conn.execute(create_table_query)


def insert_data(table_name, csv_file):
    """
    Inserts data from the CSV file into the specified table.
    """
    with open(csv_file, 'r') as f:
        first_line = f.readline().strip().split(',')
        columns = ','.join([f'"{col}"' for col in first_line])
        placeholders = ','.join(['?'] * len(first_line)) 
        data = [line.strip().split(',') for line in f]

    # Modify insert query based on column count
    insert_query = f"""INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"""

    conn.executemany(insert_query, data)


# Create tables based on CSV schema (optional)
for filename in csv_files:
  table_name = filename.split('.')[0]  # Extract table name from filename (modify if needed)
  create_table(table_name, filename)

# Insert data into tables
for filename, table_name in zip(csv_files, [t.split('.')[0] for t in csv_files]):
  insert_data(table_name, filename)


# Commit changes and close connection
conn.commit()
conn.close()

print("Data imported successfully!")
