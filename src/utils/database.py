"""
Database initialization and management utilities for SQLite.
"""
import sqlite3
import os
from datetime import datetime
from typing import Optional


class Database:
    """Manages SQLite database connection and schema initialization."""
    
    def __init__(self, db_path: str = "data/financial_research.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        return self.conn
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            
    def initialize_schema(self):
        """Create all database tables if they don't exist."""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Companies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Companies (
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL UNIQUE,
                company_name TEXT NOT NULL,
                exchange TEXT,
                sector TEXT,
                industry TEXT,
                market_cap REAL,
                currency TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # MarketIndices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MarketIndices (
                index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                index_name TEXT NOT NULL,
                description TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # StockPrices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS StockPrices (
                price_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                adjusted_close REAL,
                FOREIGN KEY (company_id) REFERENCES Companies(company_id),
                UNIQUE(company_id, timestamp)
            )
        """)
        
        # IndexPrices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS IndexPrices (
                price_id INTEGER PRIMARY KEY AUTOINCREMENT,
                index_id INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                FOREIGN KEY (index_id) REFERENCES MarketIndices(index_id),
                UNIQUE(index_id, timestamp)
            )
        """)
        
        # NewsArticles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NewsArticles (
                article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT,
                publish_date TIMESTAMP NOT NULL,
                source TEXT,
                url TEXT UNIQUE,
                related_ticker TEXT,
                sentiment_score REAL
            )
        """)
        
        # Watchlists table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Watchlists (
                watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                watchlist_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                UNIQUE(user_id, watchlist_name)
            )
        """)
        
        # WatchlistItems table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WatchlistItems (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                watchlist_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (watchlist_id) REFERENCES Watchlists(watchlist_id),
                FOREIGN KEY (company_id) REFERENCES Companies(company_id),
                UNIQUE(watchlist_id, company_id)
            )
        """)
        
        # Portfolios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Portfolios (
                portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                portfolio_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                UNIQUE(user_id, portfolio_name)
            )
        """)
        
        # Holdings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Holdings (
                holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                average_cost_basis REAL,
                purchase_date DATE,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (portfolio_id) REFERENCES Portfolios(portfolio_id),
                FOREIGN KEY (company_id) REFERENCES Companies(company_id),
                UNIQUE(portfolio_id, company_id)
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company_id INTEGER,
                index_id INTEGER,
                alert_type TEXT NOT NULL,
                threshold_value REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                triggered_at TIMESTAMP,
                message TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (company_id) REFERENCES Companies(company_id),
                FOREIGN KEY (index_id) REFERENCES MarketIndices(index_id),
                CHECK ((company_id IS NOT NULL AND index_id IS NULL) OR 
                       (company_id IS NULL AND index_id IS NOT NULL))
            )
        """)
        
        # AnalysisTemplates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AnalysisTemplates (
                template_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                template_name TEXT NOT NULL,
                configuration_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                UNIQUE(user_id, template_name)
            )
        """)
        
        # MarketSentiment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MarketSentiment (
                sentiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL UNIQUE,
                overall_market_sentiment REAL,
                source TEXT,
                category TEXT
            )
        """)
        
        self.conn.commit()
        print("Database schema initialized successfully!")
        
    def create_demo_user(self):
        """Create a default demo user if none exists."""
        if not self.conn:
            self.connect()
            
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username = 'demo_user'")
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO Users (username, email) 
                VALUES ('demo_user', 'demo@example.com')
            """)
            self.conn.commit()
            print("Demo user created successfully!")
        else:
            print("Demo user already exists.")
            
        return cursor.lastrowid if cursor.lastrowid else 1


def initialize_database():
    """Initialize the database with schema and demo user."""
    db = Database()
    db.connect()
    db.initialize_schema()
    db.create_demo_user()
    db.close()
    print("Database initialization complete!")


if __name__ == "__main__":
    initialize_database()


