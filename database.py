"""
Database configuration and initialization for Repair Tracker
"""
import sqlite3
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = "repair_tracker.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with tables and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'USER' CHECK (role IN ('USER', 'ADMIN')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create assets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                owner_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE SET NULL
            )
        """)
        
        # Create repairs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                date DATE NOT NULL,
                description TEXT NOT NULL,
                performed_by TEXT NOT NULL,
                notes TEXT,
                cost_cents INTEGER DEFAULT 0,
                status TEXT DEFAULT 'COMPLETED' CHECK (status IN ('PLANNED', 'COMPLETED')),
                created_by_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES assets (id) ON DELETE CASCADE,
                FOREIGN KEY (created_by_id) REFERENCES users (id) ON DELETE SET NULL
            )
        """)
        
        # Create user_settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency TEXT DEFAULT 'USD',
                language TEXT DEFAULT 'en',
                date_format TEXT DEFAULT 'DD.MM.YYYY',
                theme TEXT DEFAULT 'dark',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Check if we need to insert sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Insert sample users with simple password hashing
            import hashlib
            
            # Simple password hashing for demo purposes
            admin_password = hashlib.sha256("admin123".encode()).hexdigest()
            user_password = hashlib.sha256("user123".encode()).hexdigest()
            
            sample_users = [
                ("admin@example.com", "Admin User", admin_password, "ADMIN"),
                ("user@example.com", "Regular User", user_password, "USER")
            ]
            
            cursor.executemany(
                "INSERT INTO users (email, name, password_hash, role) VALUES (?, ?, ?, ?)",
                sample_users
            )
            
            # Insert sample assets
            sample_assets = [
                ("House", "house", 1),
                ("Garage", "garage", 1),
                ("Apartment", "apartment", 2)
            ]
            
            cursor.executemany(
                "INSERT INTO assets (name, type, owner_id) VALUES (?, ?, ?)",
                sample_assets
            )
            
            # Insert sample repairs
            sample_repairs = [
                (1, "2024-01-15", "Wall painting", "Master", "Completed successfully", 15000, "COMPLETED", 1),
                (2, "2024-02-20", "Door replacement", "Plumber", "Planned for next week", 25000, "PLANNED", 1),
                (3, "2024-01-10", "Kitchen renovation", "Contractor", "Full kitchen update", 50000, "COMPLETED", 2)
            ]
            
            cursor.executemany(
                "INSERT INTO repairs (property_id, date, description, performed_by, notes, cost_cents, status, created_by_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                sample_repairs
            )
            
            # Create default settings for users
            cursor.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cursor.fetchall()]
            
            default_settings = [(user_id, 'USD', 'en', 'DD.MM.YYYY', 'dark') for user_id in user_ids]
            cursor.executemany(
                "INSERT INTO user_settings (user_id, currency, language, date_format, theme) VALUES (?, ?, ?, ?, ?)",
                default_settings
            )
            
            logger.info("Sample data inserted successfully")
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
