import pandas as pd

# List of column names
column_names = ['Column1', 'Column2', 'Column3']

# Create an empty DataFrame with these column names
df = pd.DataFrame(columns=column_names)

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

print("Excel file created successfully!")
