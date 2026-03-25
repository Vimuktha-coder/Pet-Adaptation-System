import sys
import os

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace uppercase with lowercase for specific table queries
content = content.replace("supabase.table('SHELTERS')", "supabase.table('shelters')")
content = content.replace("supabase.table('USERS')", "supabase.table('users')")
content = content.replace("supabase.table('PETS')", "supabase.table('pets')")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced table names successfully in app.py")
