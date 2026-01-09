from django.db import connection
try:
    with connection.cursor() as cursor:
        # Check if using PostgreSQL
        if connection.vendor == 'postgresql':
            print("Detected PostgreSQL. synchronizing sequence...")
            cursor.execute("SELECT setval(pg_get_serial_sequence('t_crm_prospets', 'id'), coalesce(max(id), 0) + 1, false) FROM t_crm_prospets;")
            print("Sequence 't_crm_prospets_id_seq' reset successfully.")
        else:
            print(f"Database vendor is {connection.vendor}, skipping Postgres sequence reset.")
except Exception as e:
    print(f"Error resetting sequence: {e}")
