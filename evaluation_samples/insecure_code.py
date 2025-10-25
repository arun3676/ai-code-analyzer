import sqlite3

def get_user_data(username: str) -> list:
    """
    Retrieves user data from a database.
    This function has a critical security vulnerability.
    """
    # This is insecure! The username is directly concatenated into the query.
    # An attacker could provide a username like: 'admin'; DROP TABLE users; --'
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # In a real scenario, this line would execute the malicious query
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results
