# Financial research tool demo

## Project Description
I would like to retrieve financial data and information into an csv file, then using the data to create a dashboard showing the graph to do the data analysis. Also, giving an overview of the stock market at a glance

## Product Requirements Document
Product Name: Financial Research Tool Demo
Version: 1.0
Date: 2023-10-27

1.0 Introduction

1.1 Purpose
The purpose of this Product Requirements Document (PRD) is to outline the requirements for a demonstration financial research tool. This tool aims to assist individual investors by providing consolidated financial data, analysis capabilities, and a market overview, ultimately shortening the time required for market analysis and enabling data personalization.

1.2 Scope
This initial demo project will focus on core functionalities including data retrieval from free APIs, CSV export, an interactive dashboard for data analysis using Streamlit, and a summary market overview. The deployment will be local for personal use, prioritizing rapid development within a week and a zero-budget constraint.

2.0 Goals & Objectives

2.1 Business Goals (Implicit for Demo)
*   Demonstrate the feasibility of a financial research tool.
*   Validate core concepts for future potential development.

2.2 User Goals
*   **Shorten Analysis Time:** Reduce the effort and time individual investors spend on market analysis.
*   **Personalized Data Access:** Allow users to retrieve and analyze data relevant to their specific interests.
*   **Market at a Glance:** Provide a quick, comprehensive overview of the stock market status.
*   **Efficient Data Export:** Enable users to export financial data for further offline processing.

3.0 Target Audience

The primary target audience for this demo tool is individual investors who seek to perform their own financial analysis. They require a tool that can consolidate various financial data points, present them in an understandable format, and offer analytical features to aid investment decisions.

4.0 Features & Functionality

4.1 Data Retrieval & CSV Export
*   **Data Sourcing:** Ability to retrieve financial data and information from free APIs.
*   **CSV Export:** Functionality to export retrieved data into a CSV file. The export should be flexible enough to include both raw and/or processed data, depending on the user's specific analysis needs once data structures are observed.
*   **Portability:** The data retrieval and processing code should be designed with portability in mind to accommodate future expansion of data sources and types.

4.2 Interactive Dashboard
*   **Technology:** Built using Python and Streamlit.
*   **Data Visualization:** Display graphs for data analysis.
*   **Core Features:**
    *   **Watchlists:** Users can create and manage lists of stocks they are monitoring.
    *   **Alerts:** Basic alerts based on pre-defined conditions (e.g., price thresholds).
    *   **Portfolio Tracking:** Allow users to input and track their investment portfolio performance.
    *   **Pre-defined Analysis Templates:** Offer ready-to-use templates for common financial analyses.
    *   **Historical Performance Analysis:** Visualize and analyze historical data for selected assets.
    *   **Sentiment Analysis:** Integrate basic sentiment indicators where available from data sources.

4.3 Market Overview
*   **Key Indicators:** Display an at-a-glance overview of the stock market.
    *   Major Index Performance (e.g., S&P 500, Dow Jones, NASDAQ).
    *   Top Gainers/Losers for a selected period.
    *   Sector Performance across various industries.
    *   Important Economic News headlines.
    *   Overall Market Sentiment Indicators.
*   **Update Frequency:** Data for the market overview does not need to be real-time. It can be updated hourly or at a slower interval, as resources allow for this demo phase.

5.0 Data Requirements

5.1 Data Sources
*   Free APIs for financial data (specific APIs to be identified during development).

5.2 Data Types
*   Stock Prices (historical and current where available)
*   Company Fundamentals (e.g., P/E ratio, market cap, dividend yield)
*   Market Indices (e.g., S&P 500, Dow Jones)
*   News Headlines (relevant to financial markets)
*   Potentially more data types in the future, necessitating a flexible data handling architecture.

5.3 Data Volatility & Update Frequency
*   Historical data for up to 10 years for analysis.
*   Market overview data updated hourly or slower.
*   Specific stock data update frequency to be determined by API capabilities and demo needs.

5.4 Data Portability
*   The system architecture for data ingestion and processing must be designed to be portable, allowing for easy integration of new data sources and types as the project evolves.

6.0 User Experience (UX) Design Vision

The UX vision for this tool will draw inspiration from popular, user-friendly financial dashboards available today. The design should prioritize:
*   **Clean and Intuitive Interface:** Easy navigation and clear presentation of information.
*   **Data Visualization Focus:** Graphs and charts should be prominent, easily understandable, and interactive where possible.
*   **Personalization:** Features like watchlists and portfolio tracking should be easily accessible.
*   **Minimalist Design:** Avoid clutter, focusing on essential information to prevent user overwhelm.
*   **Responsiveness:** While primarily for local desktop use, the Streamlit web deployment should offer a reasonable experience across common browser window sizes.

7.0 Technical Specifications

7.1 Technology Stack
*   **Programming Language:** Python
*   **Web Framework/UI:** Streamlit

7.2 Deployment Model
*   **Deployment Environment:** Local machine.
*   **Accessibility:** Accessible via a web browser on the local machine.

7.3 System Capacity
*   **Current User Count:** Designed primarily for a single user (personal demo).
*   **Future User Count:** The system should conceptually allow for up to 20 users in a future, non-demo scenario, though this demo's immediate focus is not on multi-user scalability.

7.4 Historical Data Depth
*   Ability to retrieve and display up to 10 years of historical data for financial assets.

7.5 API Integration
*   Integration with various free financial data APIs.
*   Robust error handling for API rate limits and data retrieval failures.

8.0 Non-Functional Requirements

8.1 Performance
*   **Response Time:** For a demo, data retrieval and dashboard rendering should be reasonably quick, but not necessarily optimized for milliseconds. Performance for a single user is the primary concern.
*   **Data Loading:** Historical data for 10 years should load efficiently enough for personal analysis.

8.2 Scalability
*   **User Scalability:** Not a primary concern for this demo (single-user focus).
*   **Data Scalability:** The design should be amenable to integrating more data sources and types in the future without a complete re-architecture.

8.3 Security
*   **Basic Security:** As this is a local demo for personal use, only basic security considerations are required. This includes secure handling of API keys (e.g., environment variables) and basic input validation to prevent common vulnerabilities, but not enterprise-grade security.

8.4 Maintainability
*   **Code Quality:** Adherence to Python best practices for readability and maintainability.
*   **Modularity:** Modular design for data handling to support portability and future data source additions.

9.0 Constraints & Limitations

9.1 Timeline
*   **Development Period:** Within one week.

9.2 Budget
*   **Financial Resources:** Zero budget (reliance on free APIs and open-source tools).

9.3 Resources
*   Limited to individual developer effort.

10.0 Future Considerations

*   **Expanded Data Sources:** Integration with additional financial data providers, potentially paid APIs for more comprehensive or real-time data.
*   **Advanced Analytics:** Implementation of more sophisticated analytical models, machine learning for predictions.
*   **User Management:** Features for multiple users, personalized dashboards, and access control.
*   **Deployment:** Cloud deployment for broader accessibility and scalability.
*   **Real-time Data:** Upgrade market overview and specific asset data to real-time updates.

## Technology Stack
FINANCIAL RESEARCH TOOL DEMO - TECHNOLOGY STACK

This document outlines the recommended technology stack for the "Financial Research Tool Demo" project. The selection prioritizes rapid development, no-budget constraints, local deployment, and leveraging Python's robust ecosystem to meet the project's core requirements for data retrieval, analysis, visualization, and a market overview.

1. Core Framework & Language

*   **Streamlit (v1.x):**
    *   **Type:** Web Application Framework (Python-native)
    *   **Justification:** Explicitly requested in "technical_environment_constraints". Streamlit is ideal for creating interactive data applications and dashboards with minimal code, perfectly aligning with the "within a week, no budget" timeline. Its Python-centric nature simplifies the development process for data scientists and analysts, making it suitable for a personal "demo".
*   **Python (v3.9+):**
    *   **Type:** Programming Language
    *   **Justification:** Explicitly requested in "technical_environment_constraints". Python is the industry standard for data science, financial analysis, and machine learning, offering an extensive ecosystem of libraries for data manipulation, analysis, visualization, and API integration, which are critical for this project.

2. Data Acquisition & APIs

*   **yfinance (Python Library):**
    *   **Type:** Financial Data API Wrapper
    *   **Justification:** Provides free access to Yahoo Finance's historical market data (stock prices, company fundamentals, market indices) and real-time quotes. This directly addresses the "data_sources_and_types" requirement for free APIs and covers "10 years of historical data" efficiently.
*   **newsapi-python (Python Library) or RSS/Web Scraping (e.g., BeautifulSoup, requests):**
    *   **Type:** News Data API Wrapper / Web Scraping Tools
    *   **Justification:** To gather "news headlines" and "important economic news" for the market overview and potential basic "sentiment analysis". NewsAPI has a generous free tier. For "no budget" and more control, direct RSS feed parsing or targeted web scraping could be explored using libraries like `BeautifulSoup` and `requests` if specific financial news sources are identified.
*   **Other Free Financial APIs (e.g., Alpha Vantage, Financial Modeling Prep - with rate limits):**
    *   **Type:** Supplementary Financial Data APIs
    *   **Justification:** To diversify data sources and potentially cover gaps not met by yfinance, especially for more detailed company fundamentals or specific market indicators, fitting the "data and information may include more in the future, so the coding may need to be portable" requirement. Acknowledges rate limits for free tiers.

3. Data Storage

*   **SQLite (v3.x):**
    *   **Type:** Embedded Relational Database
    *   **Justification:** Ideal for "local deployment" and "no budget". SQLite is a serverless, file-based database that requires no separate setup, making it perfect for a personal "demo". It supports structured data storage, efficient querying of "10 years of historical data", and is natively supported by Python (`sqlite3` module). This ensures data portability and easier management compared to plain CSV files for internal storage, while still allowing for easy "csv_export_specifications".
*   **CSV Files:**
    *   **Type:** Flat-file data storage
    *   **Justification:** Explicitly required for "csv_export_specifications". CSVs will be used for exporting both raw and processed financial data, fulfilling user needs for external analysis.

4. Data Processing & Analysis

*   **Pandas (Python Library):**
    *   **Type:** Data Manipulation and Analysis Library
    *   **Justification:** Essential for handling and cleaning the "stock prices, company fundamentals, market indices, news headlines". Pandas DataFrames are the de-facto standard for tabular data in Python, enabling efficient operations for "historical performance analysis", creating "watchlists", and preparing data for "pre-defined analysis templates".
*   **NumPy (Python Library):**
    *   **Type:** Numerical Computing Library
    *   **Justification:** Provides fundamental numerical operations, especially for array manipulation, which underpins Pandas and other analytical libraries. Used for efficient computations in financial models.
*   **NLTK (Natural Language Toolkit) / TextBlob (Python Libraries):**
    *   **Type:** Natural Language Processing (NLP) Libraries
    *   **Justification:** For basic "sentiment analysis" of news headlines, as requested for the dashboard and market overview. NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) or TextBlob offer quick, rule-based sentiment scoring suitable for a "demo" with "no budget" and "within a week" timeline, without requiring complex machine learning model training.

5. Data Visualization

*   **Plotly / Plotly Express (Python Libraries):**
    *   **Type:** Interactive Visualization Library
    *   **Justification:** Highly recommended for generating interactive and aesthetically pleasing graphs for the "dashboard showing the graph to do the data analysis". Streamlit has excellent native integration with Plotly, enabling "historical performance analysis", "major index performance", and "sector performance" visualizations that meet the "user experience design vision" of popular tools. Plotly Express simplifies common plot types.
*   **Matplotlib / Seaborn (Python Libraries):**
    *   **Type:** Static & Statistical Visualization Libraries
    *   **Justification:** While Plotly will be primary for interactivity, Matplotlib offers foundational plotting capabilities, and Seaborn builds on it to create more complex statistical plots easily. These can serve as alternatives or supplementary tools for specific non-interactive graphs, if needed, maintaining flexibility.

6. Deployment & Environment Management

*   **pip (Python Package Installer):**
    *   **Type:** Package Management System
    *   **Justification:** Standard tool for installing and managing Python libraries.
*   **requirements.txt:**
    *   **Type:** Dependency Specification File
    *   **Justification:** To ensure reproducible environments for the project. Essential for managing all specified libraries and their versions, making the project easily runnable by others and portable.
*   **Web Browser:**
    *   **Type:** Client Interface
    *   **Justification:** As specified in "technical_environment_constraints" and "deployment_accessibility_model", the Streamlit application will be accessed locally via a standard web browser.

7. Security Considerations (Basic)

*   **Python's built-in `secrets` module (or similar):**
    *   **Type:** Cryptographically Strong Random Number Generation
    *   **Justification:** For basic security practices like securely managing API keys locally, addressing the "basic security as it is only a demo for personal use" requirement. API keys will not be hardcoded directly into the application.

This comprehensive stack leverages the strengths of the Python ecosystem to deliver the "Financial Research Tool Demo" efficiently and effectively within the given constraints. The modularity of these components also supports the "data and information may include more in the future, so the coding may need to be portable" requirement.

## Project Structure
PROJECTSTRUCTURE
This document outlines the file and folder organization for the "Financial research tool demo" project. The structure is designed for clarity, modularity, and ease of development, particularly considering the use of Python and Streamlit, and the potential for future expansion.

1.  **Project Root (`./`)**
    *   `main.py`
        *   **Description:** The primary entry point for the Streamlit application. This script initializes the Streamlit app and orchestrates the loading and display of different sections (e.g., Dashboard, Market Overview, Data Export). It will manage navigation between the main pages.
        *   **Purpose:** To launch the Streamlit interface and act as the central hub for the application's user flow.
    *   `requirements.txt`
        *   **Description:** A text file listing all Python packages and their versions required to run the project.
        *   **Purpose:** To ensure consistent development and deployment environments by specifying all necessary dependencies for Streamlit, data handling (pandas, numpy), data visualization (plotly, matplotlib), API interactions, and any other libraries.
    *   `README.md`
        *   **Description:** Provides a high-level overview of the project, including its purpose, key features, setup instructions, and how to run the application locally.
        *   **Purpose:** To serve as the initial guide for anyone interacting with the project, facilitating quick understanding and setup.
    *   `.gitignore`
        *   **Description:** A configuration file for Git that specifies intentionally untracked files and directories to be ignored (e.g., virtual environment folders, API keys, cached data, processed data that can be regenerated).
        *   **Purpose:** To keep the version control clean and prevent sensitive or transient files from being committed to the repository.

2.  **`app/` (Streamlit Application Pages)**
    *   **Description:** This directory contains the specific Streamlit pages or main sections that constitute the user interface of the application. Each file here will typically correspond to a distinct view presented to the user.
    *   `dashboard.py`
        *   **Description:** Implements the Streamlit code for the main financial dashboard. This page will include sections for watchlists, alerts (simplified for demo), portfolio tracking (basic), pre-defined analysis templates, and historical performance analysis graphs.
        *   **Purpose:** To provide a personalized analytical view of financial data for individual investors.
    *   `market_overview.py`
        *   **Description:** Contains the Streamlit code for displaying the overall market glance. This page will feature major index performance, top gainers/losers, sector performance, important economic news headlines, and market sentiment indicators.
        *   **Purpose:** To give users a quick, at-a-glance summary of current market conditions, updated hourly or slower as per requirements.
    *   `data_export.py`
        *   **Description:** Handles the Streamlit UI elements for exporting financial data. Users will be able to select parameters for exporting both raw and processed data into CSV files.
        *   **Purpose:** To allow users to retrieve the underlying data for further external analysis or record-keeping.
    *   `__init__.py`
        *   **Description:** An empty file that signifies `app/` is a Python package, allowing its modules to be imported elsewhere in the project.

3.  **`data/` (Data Storage)**
    *   **Description:** This directory is designated for storing all forms of financial data, fetched from APIs, processed, or cached. Given the "local demo" and "no budget" constraints, flat files (CSV) are primarily used.
    *   `raw/`
        *   **Description:** Subdirectory for storing raw, unprocessed data directly fetched from APIs. This serves as a persistent record of the initial data state.
        *   `stocks/`: Raw historical stock price data for individual tickers (e.g., `AAPL.csv`, `MSFT.csv`).
        *   `fundamentals/`: Raw company fundamental data (e.g., financial statements).
        *   `indices/`: Raw historical data for market indices (e.g., `^GSPC.csv` for S&P 500).
        *   `news/`: Raw news headlines and associated metadata.
    *   `processed/`
        *   **Description:** Subdirectory for storing data after it has undergone cleaning, transformation, and potentially feature engineering. This data is optimized for direct use by the dashboard and analysis functions.
        *   `stocks/`: Processed stock data, potentially including technical indicators (e.g., moving averages) or pre-calculated metrics.
        *   `market_summary.csv`: Aggregated and processed data used for the market overview page.
        *   `sentiment/`: Processed sentiment scores derived from news headlines.
    *   `cache/`
        *   **Description:** Temporary storage for API responses or computationally expensive results to reduce redundant data fetching and speed up the application.
        *   **Purpose:** To improve performance and reduce API call limits during development and demo usage.
    *   `user_data/` (Optional, for future expansion)
        *   **Description:** Placeholder for user-specific configurations or data, such as personalized watchlists or portfolio settings, if they were to be persisted across sessions in a more complex setup. For this demo, watchlists are likely configured in `config/`.

4.  **`src/` (Source Code - Core Modules)**
    *   **Description:** This directory encapsulates the core Python logic of the application, separated into functional modules to promote reusability and maintainability.
    *   **`src/api/` (API Integration)**
        *   **Description:** Contains modules responsible for interacting with external financial data APIs.
        *   `data_fetcher.py`
            *   **Description:** Implements functions to retrieve financial data from various free APIs (e.g., `yfinance` for Yahoo Finance, potentially others for specific data types like news). It handles API requests, error handling, and basic data parsing.
            *   **Purpose:** To abstract the complexities of external API interactions from the rest of the application.
        *   `__init__.py`: Makes `src/api` a Python package.
    *   **`src/processing/` (Data Processing)**
        *   **Description:** Modules focused on cleaning, transforming, and preparing raw data for analysis and display.
        *   `data_cleaner.py`
            *   **Description:** Functions for handling missing values, data type conversions, outlier detection, and ensuring data consistency across different sources.
            *   **Purpose:** To prepare raw data into a clean and usable format for downstream analysis.
        *   `feature_engineer.py`
            *   **Description:** Functions to create new features or derived metrics from existing data (e.g., calculating moving averages, relative strength index, daily returns).
            *   **Purpose:** To enrich the dataset with analytical features required by the dashboard and analysis tools.
        *   `__init__.py`: Makes `src/processing` a Python package.
    *   **`src/analysis/` (Financial Analysis)**
        *   **Description:** Modules dedicated to performing various financial analyses and calculations.
        *   `historical_analysis.py`
            *   **Description:** Contains functions for calculating historical performance metrics such as returns, volatility, drawdowns, and comparisons over different periods, utilizing 10 years of historical data.
            *   **Purpose:** To power the "historical performance analysis" feature of the dashboard.
        *   `sentiment_analyzer.py`
            *   **Description:** Implements logic for processing news headlines to extract market or stock-specific sentiment. This could be based on a simple lexical approach or leveraging readily available (free) pre-trained models.
            *   **Purpose:** To provide sentiment analysis indicators for the dashboard and market overview.
        *   `portfolio_tracker.py`
            *   **Description:** (Simplified for demo) Functions for basic portfolio management, such as calculating portfolio value or performance based on a given set of holdings.
            *   **Purpose:** To support the "portfolio tracking" feature.
        *   `__init__.py`: Makes `src/analysis` a Python package.
    *   **`src/utils/` (Utility Functions)**
        *   **Description:** General-purpose helper functions that are not tied to a specific domain but are useful across the project.
        *   `helpers.py`
            *   **Description:** Contains small, reusable functions for common tasks like date formatting, data validation, file I/O operations, or data manipulation helpers.
            *   **Purpose:** To prevent code duplication and centralize common helper routines.
        *   `logger.py`
            *   **Description:** Sets up a simple logging mechanism for tracking application events, warnings, and errors.
            *   **Purpose:** To aid in debugging and monitoring the application's behavior during development and demo.
        *   `__init__.py`: Makes `src/utils` a Python package.
    *   **`src/components/` (Streamlit UI Components)**
        *   **Description:** Modules containing reusable Streamlit UI widgets, custom components, or plotting functions that can be imported and used across different `app/` pages.
        *   `chart_generator.py`
            *   **Description:** Functions to generate common financial charts and visualizations (e.g., line charts, candlesticks, bar charts) using libraries like Plotly or Matplotlib, tailored for Streamlit.
            *   **Purpose:** To create consistent and effective data visualizations for the dashboard and market overview.
        *   `table_display.py`
            *   **Description:** Functions to format and display tabular financial data effectively within Streamlit, potentially with styling or interactive features.
            *   **Purpose:** To present data clearly in table formats where appropriate.
        *   `alert_manager.py`
            *   **Description:** (Simplified for demo) Functions for displaying hypothetical alerts or notifications within the Streamlit UI based on certain data conditions.
            *   **Purpose:** To demonstrate the "alerts" feature.
        *   `__init__.py`: Makes `src/components` a Python package.

5.  **`config/` (Configuration Files)**
    *   **Description:** Stores application-wide settings, parameters, and sensitive information.
    *   `settings.py`
        *   **Description:** A Python file containing application-wide constants and configurable parameters, such as API endpoints, default stock symbols, refresh frequencies (e.g., hourly for market overview), and data paths. For a local demo, API keys might also be stored here directly (though environment variables are recommended for production).
        *   **Purpose:** To centralize and easily manage application configuration.
    *   `watchlists.json` / `watchlists.py`
        *   **Description:** A file (JSON or Python list) defining default or demo watchlists to be pre-loaded into the dashboard.
        *   **Purpose:** To provide initial data for the watchlist feature without requiring user input immediately.
    *   `api_keys.ini` (or similar)
        *   **Description:** (Optional, if not using environment variables or `settings.py`) A file to store API keys for different services, allowing for basic separation of sensitive information. *Given it's a demo and basic security is fine, environment variables are a strong consideration here.*

6.  **`scripts/` (Helper Scripts)**
    *   **Description:** Contains standalone Python scripts for tasks that are not part of the main Streamlit application flow but support its operation.
    *   `update_data.py`
        *   **Description:** A script designed to be run periodically (e.g., via a cron job or manually) to fetch the latest raw data from APIs and then process it, updating the contents of the `data/raw` and `data/processed` directories. This fulfills the "updated every hour or maybe slower" requirement for market data.
        *   **Purpose:** To ensure the dashboard always has reasonably fresh data without requiring constant manual intervention or real-time API calls within the Streamlit app.
    *   `setup_env.py`
        *   **Description:** A script to automate the initial setup process, such as installing Python dependencies, creating necessary directories, and potentially fetching an initial batch of historical data to populate the `data/` directory.
        *   **Purpose:** To streamline the initial project setup for new users or developers.

7.  **`docs/` (Documentation)**
    *   **Description:** This directory holds various project documentation files.
    *   `PROJECTSTRUCTURE.txt`
        *   **Description:** This document itself, detailing the project's file and folder organization.
        *   **Purpose:** To provide a clear map of the codebase for developers.
    *   `USERGUIDE.md`
        *   **Description:** A simple guide explaining how to use the demo tool, covering its features and basic interactions.
        *   **Purpose:** To assist end-users in navigating and utilizing the application.
    *   `DESIGN_CHOICES.md`
        *   **Description:** Documents key architectural, technical, or design decisions made during the project's development, especially given the constraints (e.g., choice of APIs, data persistence strategy).
        *   **Purpose:** To provide context for design choices and aid in future modifications or understanding.

## Database Schema Design
1. Overview

The database schema design outlines the structure for storing financial data and user-specific information for the \"Financial research tool demo.\" The primary goal is to efficiently store historical stock prices, company fundamentals, market indices, news, and user-defined configurations (watchlists, portfolios, alerts, analysis templates). This schema is designed to support the dashboard features and market overview functionalities, while also being portable for potential future expansion.

2. Database Technology

Given the project constraints of local deployment, no budget, a tight timeline (within a week), and a single-user demo focus, **SQLite** has been selected as the relational database management system (RDBMS). SQLite is an embedded, file-based database that requires no separate server process, making it ideal for a Python/Streamlit application deployed locally. Its lightweight nature and ease of integration with Python (via the `sqlite3` module) align perfectly with the project\'s technical environment and resource limitations.

3. Data Model - Entities and Relationships

The core entities identified for the financial research tool are:

*   **Companies**: Stores fundamental information about individual stocks.
*   **Market Indices**: Stores information about major market indices.
*   **Stock Prices**: Historical price data for individual stocks.
*   **Index Prices**: Historical price data for market indices.
*   **News Articles**: Information from financial news sources.
*   **Users**: (Even for a single demo user) Manages user accounts for personalization.
*   **Watchlists**: User-defined collections of stocks to monitor.
*   **Watchlist Items**: Links stocks to specific watchlists.
*   **Portfolios**: User-defined collections of actual stock holdings.
*   **Holdings**: Details of stocks within a user\'s portfolio.
*   **Alerts**: User-defined notifications based on price or other criteria.
*   **Analysis Templates**: Pre-defined analysis configurations for easy reuse.
*   **Market Sentiment**: Aggregated sentiment indicators (future expansion).

**Relationships Overview:**

*   One `Company` has many `Stock Prices`.
*   One `Market Index` has many `Index Prices`.
*   One `User` can have many `Watchlists`, `Portfolios`, `Alerts`, and `Analysis Templates`.
*   One `Watchlist` can have many `Watchlist Items`. Each `Watchlist Item` links to one `Company` (Many-to-Many through `Watchlist Items`).
*   One `Portfolio` can have many `Holdings`. Each `Holding` links to one `Company` (Many-to-Many through `Holdings`).
*   An `Alert` can be associated with either a `Company` or a `Market Index`.
*   `News Articles` can optionally be linked to `Companies` via their ticker.

4. Database Schema Details

Below are the detailed table definitions, including column names, data types, constraints, and descriptions.

**Table: `Users`**
*   **Description**: Stores basic information for application users. Initially, it will contain a single entry for the demo user.
*   **Columns**:
    *   `user_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the user.
    *   `username` TEXT NOT NULL UNIQUE
        *   Login username (e.g., "demo_user").
    *   `email` TEXT
        *   User\'s email address.
    *   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the user account was created.

**Table: `Companies`**
*   **Description**: Stores fundamental data and identifying information for individual stocks.
*   **Columns**:
    *   `company_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the company.
    *   `ticker` TEXT NOT NULL UNIQUE
        *   Stock ticker symbol (e.g., "AAPL", "MSFT").
    *   `company_name` TEXT NOT NULL
        *   Full company name (e.g., "Apple Inc.").
    *   `exchange` TEXT
        *   Stock exchange where the company is listed (e.g., "NASDAQ", "NYSE").
    *   `sector` TEXT
        *   Industry sector (e.g., "Technology", "Healthcare").
    *   `industry` TEXT
        *   Specific industry within the sector (e.g., "Consumer Electronics", "Pharmaceuticals").
    *   `market_cap` REAL
        *   Current market capitalization.
    *   `currency` TEXT
        *   Currency of the stock (e.g., "USD", "EUR").
    *   `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp of the last fundamental data update.

**Table: `MarketIndices`**
*   **Description**: Stores information about major market indices.
*   **Columns**:
    *   `index_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the market index.
    *   `symbol` TEXT NOT NULL UNIQUE
        *   Index symbol (e.g., "^GSPC" for S&P 500).
    *   `index_name` TEXT NOT NULL
        *   Full name of the index (e.g., "S&P 500").
    *   `description` TEXT
        *   Brief description of the index.
    *   `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp of the last index information update.

**Table: `StockPrices`**
*   **Description**: Stores historical daily or hourly price data for individual stocks. Designed to hold up to 10 years of historical data.
*   **Columns**:
    *   `price_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the price record.
    *   `company_id` INTEGER NOT NULL
        *   Foreign Key to `Companies.company_id`.
    *   `timestamp` TIMESTAMP NOT NULL
        *   Date and time of the price record (e.g., YYYY-MM-DD HH:MM:SS).
    *   `open` REAL
        *   Opening price.
    *   `high` REAL
        *   Highest price during the period.
    *   `low` REAL
        *   Lowest price during the period.
    *   `close` REAL
        *   Closing price.
    *   `volume` INTEGER
        *   Trading volume.
    *   `adjusted_close` REAL
        *   Close price adjusted for splits and dividends.
    *   `UNIQUE(company_id, timestamp)`
        *   Ensures unique price records for a given company at a specific timestamp.
*   **Relationships**:
    *   FOREIGN KEY (`company_id`) REFERENCES `Companies`(`company_id`)

**Table: `IndexPrices`**
*   **Description**: Stores historical daily or hourly price data for market indices.
*   **Columns**:
    *   `price_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the price record.
    *   `index_id` INTEGER NOT NULL
        *   Foreign Key to `MarketIndices.index_id`.
    *   `timestamp` TIMESTAMP NOT NULL
        *   Date and time of the price record.
    *   `open` REAL
        *   Opening price.
    *   `high` REAL
        *   Highest price during the period.
    *   `low` REAL
        *   Lowest price during the period.
    *   `close` REAL
        *   Closing price.
    *   `volume` INTEGER
        *   Trading volume (if available for indices).
    *   `UNIQUE(index_id, timestamp)`
        *   Ensures unique price records for a given index at a specific timestamp.
*   **Relationships**:
    *   FOREIGN KEY (`index_id`) REFERENCES `MarketIndices`(`index_id`)

**Table: `NewsArticles`**
*   **Description**: Stores fetched financial news headlines and related information.
*   **Columns**:
    *   `article_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the news article.
    *   `title` TEXT NOT NULL
        *   Headline of the news article.
    *   `summary` TEXT
        *   Brief summary or excerpt of the article content.
    *   `publish_date` TIMESTAMP NOT NULL
        *   Date and time the article was published.
    *   `source` TEXT
        *   Source of the article (e.g., "Reuters", "Finviz").
    *   `url` TEXT UNIQUE
        *   URL to the full article (ensures no duplicate articles).
    *   `related_ticker` TEXT
        *   Ticker symbol of a company the article is primarily about (nullable).
    *   `sentiment_score` REAL
        *   Numerical sentiment score (e.g., -1.0 to 1.0), to be implemented in the future.
*   **Relationships**:
    *   (Optional, a trigger or Python logic can link `related_ticker` to `Companies.ticker`)

**Table: `Watchlists`**
*   **Description**: Stores user-defined watchlists for tracking selected stocks.
*   **Columns**:
    *   `watchlist_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the watchlist.
    *   `user_id` INTEGER NOT NULL
        *   Foreign Key to `Users.user_id`.
    *   `watchlist_name` TEXT NOT NULL
        *   Name of the watchlist (e.g., "Growth Stocks", "Tech Giants").
    *   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the watchlist was created.
    *   `UNIQUE(user_id, watchlist_name)`
        *   Ensures a user cannot have two watchlists with the same name.
*   **Relationships**:
    *   FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)

**Table: `WatchlistItems`**
*   **Description**: Links companies to specific watchlists, enabling a many-to-many relationship.
*   **Columns**:
    *   `item_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the watchlist item.
    *   `watchlist_id` INTEGER NOT NULL
        *   Foreign Key to `Watchlists.watchlist_id`.
    *   `company_id` INTEGER NOT NULL
        *   Foreign Key to `Companies.company_id`.
    *   `added_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the stock was added to the watchlist.
    *   `UNIQUE(watchlist_id, company_id)`
        *   Ensures a stock is added only once per watchlist.
*   **Relationships**:
    *   FOREIGN KEY (`watchlist_id`) REFERENCES `Watchlists`(`watchlist_id`)
    *   FOREIGN KEY (`company_id`) REFERENCES `Companies`(`company_id`)

**Table: `Portfolios`**
*   **Description**: Stores user-defined portfolios for tracking actual stock holdings.
*   **Columns**:
    *   `portfolio_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the portfolio.
    *   `user_id` INTEGER NOT NULL
        *   Foreign Key to `Users.user_id`.
    *   `portfolio_name` TEXT NOT NULL
        *   Name of the portfolio (e.g., "Retirement Fund", "Play Account").
    *   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the portfolio was created.
    *   `UNIQUE(user_id, portfolio_name)`
        *   Ensures a user cannot have two portfolios with the same name.
*   **Relationships**:
    *   FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)

**Table: `Holdings`**
*   **Description**: Details individual stock holdings within a user\'s portfolio.
*   **Columns**:
    *   `holding_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the holding record.
    *   `portfolio_id` INTEGER NOT NULL
        *   Foreign Key to `Portfolios.portfolio_id`.
    *   `company_id` INTEGER NOT NULL
        *   Foreign Key to `Companies.company_id`.
    *   `quantity` REAL NOT NULL
        *   Number of shares held.
    *   `average_cost_basis` REAL
        *   Average price paid per share.
    *   `purchase_date` DATE
        *   Date of the initial purchase.
    *   `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp of the last update to this holding.
    *   `UNIQUE(portfolio_id, company_id)`
        *   Ensures a stock can only be held once per portfolio (aggregate all purchases).
*   **Relationships**:
    *   FOREIGN KEY (`portfolio_id`) REFERENCES `Portfolios`(`portfolio_id`)
    *   FOREIGN KEY (`company_id`) REFERENCES `Companies`(`company_id`)

**Table: `Alerts`**
*   **Description**: Stores user-defined alerts for stocks or market indices.
*   **Columns**:
    *   `alert_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the alert.
    *   `user_id` INTEGER NOT NULL
        *   Foreign Key to `Users.user_id`.
    *   `company_id` INTEGER
        *   Foreign Key to `Companies.company_id` (NULL if alert is for an index).
    *   `index_id` INTEGER
        *   Foreign Key to `MarketIndices.index_id` (NULL if alert is for a company).
    *   `alert_type` TEXT NOT NULL
        *   Type of alert (e.g., "PRICE_ABOVE", "PRICE_BELOW", "VOLUME_SPIKE").
    *   `threshold_value` REAL NOT NULL
        *   The value that triggers the alert (e.g., target price).
    *   `status` TEXT NOT NULL DEFAULT \'ACTIVE\'
        *   Current status of the alert (e.g., "ACTIVE", "TRIGGERED", "INACTIVE").
    *   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the alert was created.
    *   `triggered_at` TIMESTAMP
        *   Timestamp when the alert was last triggered (NULL if not triggered).
    *   `message` TEXT
        *   Custom message for the alert.
*   **Constraints**:
    *   CHECK ((`company_id` IS NOT NULL AND `index_id` IS NULL) OR (`company_id` IS NULL AND `index_id` IS NOT NULL))
        *   Ensures an alert is tied to exactly one company OR one index, not both or neither.
*   **Relationships**:
    *   FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)
    *   FOREIGN KEY (`company_id`) REFERENCES `Companies`(`company_id`)
    *   FOREIGN KEY (`index_id`) REFERENCES `MarketIndices`(`index_id`)

**Table: `AnalysisTemplates`**
*   **Description**: Stores configurations for user-defined or pre-defined analysis templates.
*   **Columns**:
    *   `template_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the template.
    *   `user_id` INTEGER NOT NULL
        *   Foreign Key to `Users.user_id`.
    *   `template_name` TEXT NOT NULL
        *   Name of the analysis template (e.g., "RSI Overbought Scan").
    *   `configuration_json` TEXT
        *   JSON string storing the analysis parameters (e.g., {\"indicator\": \"RSI\", \"period\": 14, \"overbought\": 70}).
    *   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        *   Timestamp when the template was created.
    *   `UNIQUE(user_id, template_name)`
        *   Ensures a user cannot have two templates with the same name.
*   **Relationships**:
    *   FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)

**Table: `MarketSentiment`** (Placeholder for future sentiment analysis)
*   **Description**: Stores aggregated market sentiment indicators, updated periodically.
*   **Columns**:
    *   `sentiment_id` INTEGER PRIMARY KEY AUTOINCREMENT
        *   Unique identifier for the sentiment record.
    *   `timestamp` TIMESTAMP NOT NULL UNIQUE
        *   Timestamp of the sentiment data.
    *   `overall_market_sentiment` REAL
        *   A numerical score representing overall market sentiment (e.g., -1.0 to 1.0).
    *   `source` TEXT
        *   Source or aggregation method (e.g., "News Aggregate", "Social Media Index").
    *   `category` TEXT
        *   Category of sentiment (e.g., "Economic News", "Tech Sector").

5. Considerations for Future Scalability and Portability

While this schema is designed for a local SQLite demo, several aspects ensure future portability and scalability:

*   **Standard SQL Data Types**: The chosen data types (INTEGER, TEXT, REAL, TIMESTAMP) are standard across most relational databases, facilitating migration to systems like PostgreSQL or MySQL if the project grows to require multi-user support, higher performance, or more robust concurrency.
*   **Relational Model**: The use of explicit foreign keys and a normalized relational model helps maintain data integrity and provides a clear structure that can be scaled horizontally or vertically in more complex database environments.
*   **Timestamp-based Data**: All historical data is timestamped, allowing for flexible aggregation (daily, weekly, hourly) and handling of different update frequencies.
*   **User Separation**: Even with one demo user, the `Users` table and user-specific tables (`Watchlists`, `Portfolios`, `Alerts`, `AnalysisTemplates`) provide a clear separation that would support multiple users in a future deployment without major schema redesigns.
*   **API Agnostic Design**: The schema is designed to store the *types* of financial data needed, regardless of the specific free API used. This makes the data ingestion layer portable and adaptable to different data sources as long as they provide the required data points.
*   **Modular Features**: Features like sentiment analysis (`MarketSentiment` table) are designed as separate, optional tables, allowing for phased implementation and avoiding schema bloat for the initial demo.

6. Initial Data Loading Strategy

For the demo, data will be loaded from free financial APIs. The strategy will involve:

*   **Initial Bulk Load**: Upon first run, fetch historical data (up to 10 years for stocks/indices) for a predefined set of ~20 companies/indices and populate `Companies`, `MarketIndices`, `StockPrices`, and `IndexPrices` tables. This will be the most time-consuming step.
*   **Incremental Updates**: Implement a scheduled task (e.g., hourly, as per requirements) to fetch recent data and update the `StockPrices`, `IndexPrices`, `Companies` (for market cap, etc.), `MarketIndices`, and `NewsArticles` tables. This ensures the data remains reasonably fresh without being real-time.
*   **CSV Export**: The system will support exporting selected data (e.g., historical prices for a specific ticker, portfolio holdings) directly from the populated tables to CSV files, as requested. The schema directly supports querying and extracting this data for various user needs.

## User Flow
USERFLOW

This document outlines the key user journeys and interaction patterns for the "Financial Research Tool Demo". It details how an individual investor will navigate the application to retrieve financial data, analyze it, view market overviews, and manage personalized insights, shortening their analysis time and personalizing data needs. Given the Streamlit environment, interaction patterns will lean towards interactive web components like sidebars, input forms, charts, and data tables.

**Core Application Components & Pages:**

*   **Home / Market Overview**: Displays a high-level summary of the stock market.
*   **Stock Dashboard**: Detailed analysis view for a specific stock or asset.
*   **Data Retrieval / Export**: Interface for selecting and exporting raw financial data.
*   **Watchlist**: Manages a list of user-selected stocks for quick monitoring.
*   **Portfolio**: (Basic) Tracks a user's holdings and provides performance insights.
*   **Alerts**: Allows users to set simple notifications based on stock criteria.

---

**User Flow 1: Market Overview & Initial Exploration**

*   **Goal**: The user wants to quickly grasp the current market situation and identify areas of interest.
*   **Actors**: Individual Investor
*   **Pre-conditions**: User has opened the application in their web browser.
*   **Post-conditions**: User has an understanding of the market and has potentially navigated to a specific stock's analysis or identified an action.

**Steps:**

1.  **Screen/Component**: Home Page - Market Overview
    *   **User Action**: User lands on the application's default home page.
    *   **System Response**: The application immediately loads and displays an "Overview" section.
    *   **Wireframe Description/Interaction Pattern**:
        *   A prominent header at the top, e.g., "Financial Market Insights".
        *   A main content area divided into several high-level panels/cards.
        *   Panel 1: "Major Index Performance" (e.g., S&P 500, NASDAQ, Dow Jones) with their current value, daily change (absolute and percentage), and a small line chart for intraday movement.
        *   Panel 2: "Top Gainers" - A concise list (e.g., top 5) of stocks with the largest percentage gain, including symbol, last price, and % change.
        *   Panel 3: "Top Losers" - A concise list (e.g., top 5) of stocks with the largest percentage loss, including symbol, last price, and % change.
        *   Panel 4: "Sector Performance" - A simple bar chart or pie chart showing the performance of major sectors (e.g., Technology, Finance, Healthcare) over the day.
        *   Panel 5: "Important Economic News" - A brief, scrolling list of 2-3 key economic headlines with a timestamp (not full articles).
        *   Panel 6: "Market Sentiment Indicator" - A simple gauge or text indicating overall market sentiment (e.g., "Neutral," "Bullish").
        *   Each stock symbol displayed (in gainers/losers) will be an interactive link.

2.  **Screen/Component**: Navigation Sidebar / Market Overview
    *   **User Action**: User reviews the overview and decides to explore a specific stock or navigate to another feature.
    *   **System Response**: The application is responsive to user clicks.
    *   **Wireframe Description/Interaction Pattern**:
        *   A persistent left-hand sidebar contains primary navigation links: "Market Overview", "Dashboard", "Watchlist", "Portfolio", "Data Export", "Alerts".
        *   Clicking a stock symbol in "Top Gainers" or "Top Losers" will automatically navigate the user to the "Stock Dashboard" for that specific stock (User Flow 2).
        *   Clicking any of the sidebar navigation links will load the respective component in the main content area.

---

**User Flow 2: Detailed Stock Analysis & Dashboard Customization**

*   **Goal**: The user wants to perform in-depth analysis on a specific stock, view historical data, and apply various analytical tools.
*   **Actors**: Individual Investor
*   **Pre-conditions**: User is on the "Market Overview" page or has explicitly navigated to the "Dashboard" section.
*   **Post-conditions**: User has viewed detailed stock data, potentially saved it to a watchlist/portfolio, and understood its performance characteristics.

**Steps:**

1.  **Screen/Component**: Stock Search Input (integrated into Dashboard page)
    *   **User Action**: User wants to analyze a specific stock.
    *   **System Response**: Provides an input mechanism for stock symbol entry.
    *   **Wireframe Description/Interaction Pattern**:
        *   On the "Dashboard" page, at the top, a prominent text input field labeled "Enter Stock Symbol (e.g., AAPL)".
        *   An "Analyze" button next to the input field or auto-submit on Enter key.
        *   If the user navigated from the Market Overview by clicking a symbol, this field will be pre-filled, and the dashboard will automatically load.

2.  **Screen/Component**: Stock Dashboard - Main View
    *   **User Action**: User enters a valid stock symbol and initiates analysis.
    *   **System Response**: The dashboard populates with data for the selected stock.
    *   **Wireframe Description/Interaction Pattern**:
        *   **Stock Header**: Displays the company name, current price, daily change (absolute and percentage), and a small "Add to Watchlist" button/icon.
        *   **Key Metrics Panel**: Quick glance at important data: Open, High, Low, Volume, Market Cap, P/E Ratio (if available), Dividend Yield (if available).
        *   **Interactive Chart Area**:
            *   A primary candlestick or line chart showing historical price data.
            *   Date range selectors (e.g., 1D, 5D, 1M, 3M, 6M, YTD, 1Y, 5Y, 10Y, Max) above or below the chart.
            *   Ability to select different chart types (e.g., Line, Candlestick).
            *   Basic technical indicators (e.g., SMA, EMA, RSI) can be toggled on/off via dropdowns or checkboxes.
        *   **Analysis Templates Section**:
            *   A dropdown or set of buttons for "Pre-defined Analysis Templates" (e.g., "Growth Stock Analysis", "Value Stock Screener", "Momentum Play").
            *   Selecting a template will auto-configure certain indicators or display specific data points relevant to that template.
        *   **Company Fundamentals Panel**: Displays key fundamental data points (e.g., Revenue, Net Income, EPS, Debt-to-Equity Ratio) in a tabular or summarized format.
        *   **News & Sentiment Panel**: Displays recent news headlines specific to the company and potentially a sentiment score derived from those headlines.
        *   **Interaction**: All elements are designed for responsiveness. Changing date ranges or toggling indicators will update the chart dynamically without a full page reload.

3.  **Screen/Component**: Watchlist/Portfolio Integration
    *   **User Action**: User decides to add the analyzed stock to their watchlist or portfolio.
    *   **System Response**: Updates the respective list and provides confirmation.
    *   **Wireframe Description/Interaction Pattern**:
        *   A "Add to Watchlist" button/icon next to the stock symbol. Clicking it adds the stock to the user's "Watchlist".
        *   (Future) A separate button or option to "Add to Portfolio" which would prompt for quantity and purchase price, then update the "Portfolio" section.
        *   A small confirmation message (e.g., "Stock added to Watchlist!") appears briefly.

---

**User Flow 3: Data Retrieval & Export to CSV**

*   **Goal**: The user wants to download raw financial data for a specific stock or market index into a CSV file for external analysis.
*   **Actors**: Individual Investor
*   **Pre-conditions**: User is on any page of the application.
*   **Post-conditions**: User has successfully downloaded a CSV file containing the requested financial data.

**Steps:**

1.  **Screen/Component**: Navigation Sidebar / Data Export Page
    *   **User Action**: User clicks "Data Export" in the sidebar.
    *   **System Response**: Loads the data export interface.
    *   **Wireframe Description/Interaction Pattern**:
        *   Main content area dedicated to data export options.

2.  **Screen/Component**: Data Export Form
    *   **User Action**: User selects data parameters for export.
    *   **System Response**: Prepares data based on selection.
    *   **Wireframe Description/Interaction Pattern**:
        *   **Input Field**: "Stock Symbol/Ticker" (e.g., AAPL, ^GSPC for S&P 500).
        *   **Dropdown**: "Data Type" (e.g., "Historical Prices", "Company Fundamentals", "News Headlines"). Default to "Historical Prices".
        *   **Date Range Pickers**: "Start Date" and "End Date" calendar widgets. Default to 1 year historical data.
        *   **Checkbox/Radio Button**: "Include Dividends", "Include Stock Splits".
        *   **Button**: "Generate CSV".
        *   **Interaction**: Selecting "Company Fundamentals" might disable date range as it's typically point-in-time data. "News Headlines" might require a date range and potentially a keyword input. For this demo, focus on "Historical Prices".

3.  **Screen/Component**: Data Export Confirmation / Download
    *   **User Action**: User clicks "Generate CSV".
    *   **System Response**: Processes the request, retrieves data from the API, formats it into CSV, and initiates a download.
    *   **Wireframe Description/Interaction Pattern**:
        *   A temporary loading indicator (e.g., "Generating CSV...") appears.
        *   Upon successful generation, the browser's native download prompt will appear, allowing the user to save the `.csv` file (e.g., `AAPL_HistoricalPrices_2014-01-01_2024-01-01.csv`).
        *   If there's an error (e.g., invalid symbol, no data for range), an error message is displayed (e.g., "Error: Could not retrieve data for AAPL. Please check the symbol and date range.").

---

**User Flow 4: Watchlist & Portfolio Management**

*   **Goal**: The user wants to keep track of a personalized set of stocks (Watchlist) and monitor their basic investment holdings (Portfolio).
*   **Actors**: Individual Investor
*   **Pre-conditions**: User has navigated to the "Watchlist" or "Portfolio" page.
*   **Post-conditions**: Watchlist or Portfolio is updated, and the user can see personalized performance.

**Steps:**

1.  **Screen/Component**: Navigation Sidebar / Watchlist Page
    *   **User Action**: User clicks "Watchlist" in the sidebar.
    *   **System Response**: Displays the user's current watchlist.
    *   **Wireframe Description/Interaction Pattern**:
        *   **Header**: "My Watchlist".
        *   **Input Field**: "Add Symbol to Watchlist" with an "Add" button.
        *   **Watchlist Table**: A table displaying:
            *   Stock Symbol
            *   Company Name
            *   Last Price
            *   Daily Change (absolute and percentage)
            *   Market Cap
            *   A "Remove" button/icon for each row.
        *   **Interaction**: Clicking on a stock symbol in the table will navigate to that stock's "Dashboard" (User Flow 2). Adding a new symbol updates the table dynamically. Removing a symbol removes the row.

2.  **Screen/Component**: Navigation Sidebar / Portfolio Page (Basic Demo)
    *   **User Action**: User clicks "Portfolio" in the sidebar.
    *   **System Response**: Displays the user's basic portfolio holdings and performance.
    *   **Wireframe Description/Interaction Pattern**:
        *   **Header**: "My Portfolio".
        *   **Input Form**: (For demo, a simple form) "Add Holding: Symbol, Quantity, Purchase Price".
        *   **Portfolio Summary**: A small panel showing "Total Portfolio Value", "Today's Gain/Loss", "Overall Gain/Loss".
        *   **Holdings Table**: A table displaying:
            *   Stock Symbol
            *   Company Name
            *   Quantity
            *   Average Purchase Price
            *   Current Price
            *   Current Value
            *   Unrealized Gain/Loss (absolute and percentage)
            *   A "Remove" button/icon for each row.
        *   **Interaction**: Adding a new holding updates the table and summary dynamically. Removing a holding removes the row.

---

**User Flow 5: Setting Up Alerts**

*   **Goal**: The user wants to set simple alerts for price movements of specific stocks.
*   **Actors**: Individual Investor
*   **Pre-conditions**: User has navigated to the "Alerts" page.
*   **Post-conditions**: An alert has been successfully created and is active.

**Steps:**

1.  **Screen/Component**: Navigation Sidebar / Alerts Page
    *   **User Action**: User clicks "Alerts" in the sidebar.
    *   **System Response**: Loads the alert management interface.
    *   **Wireframe Description/Interaction Pattern**:
        *   **Header**: "Manage Alerts".
        *   **Alert Creation Form**:
            *   **Input Field**: "Stock Symbol".
            *   **Dropdown**: "Alert Type" (e.g., "Price Above", "Price Below").
            *   **Input Field**: "Target Price".
            *   **Button**: "Set Alert".
        *   **Active Alerts Table**: A table displaying:
            *   Stock Symbol
            *   Alert Condition (e.g., "Price Above $180.00")
            *   Status (e.g., "Active", "Triggered")
            *   A "Delete" button/icon for each row.
        *   **Interaction**: Setting an alert adds it to the table. Deleting removes it. When an alert is triggered (for demo purposes, a simple notification within the app or console output suffices), its status updates.

## Styling Guidelines
STYLING GUIDELINES

This document outlines the visual and interactive design principles for the Financial Research Tool Demo. The goal is to create a clean, professional, and highly usable interface that empowers individual investors to efficiently analyze financial data, shortening the time needed for market analysis. The design is inspired by popular financial tools, prioritizing clarity and data focus within the Streamlit framework.

1.  UI/UX PRINCIPLES

    *   Clarity & Readability: Financial data can be complex. The interface must prioritize clear presentation of information, ensuring all text, numbers, and charts are easily legible.
    *   Efficiency: Minimize cognitive load and interaction steps. Users should be able to quickly access and understand critical data with minimal effort. The design should facilitate rapid analysis.
    *   Consistency: Maintain a consistent look and feel across all components and pages to foster familiarity and predictability, reducing the learning curve.
    *   Data-Focused: The design should recede into the background, allowing the data to be the primary focus. Avoid unnecessary visual clutter that distracts from core information.
    *   Feedback: Provide clear visual feedback for user interactions (e.g., button states, data loading indicators, successful/unsuccessful operations).
    *   Personalization Readiness: Design components with an eye towards future personalization options, even if not fully implemented in this demo, to allow for tailored user experiences.
    *   Basic Responsiveness: While primarily for local use, the layout should adapt reasonably well to different browser window sizes to ensure a consistent experience across varying display conditions.

2.  COLOR PALETTE

    The color palette is chosen to convey trust, professionalism, and clarity, while providing clear indicators for financial performance.

    *   Primary Action/Positive Performance: `#4CAF50` (Green)
        *   Usage: Buttons for primary actions (e.g., "Generate Report", "Export Data"), positive financial indicators (e.g., stock gains, up arrows).
    *   Secondary Action/Negative Performance: `#F44336` (Red)
        *   Usage: Buttons for destructive actions (if any), negative financial indicators (e.g., stock losses, down arrows), error messages.
    *   Neutral Palette (for backgrounds, text, borders):
        *   Dark Text/Heading: `#212121`
        *   Body Text: `#424242`
        *   Subtle Text/Label: `#757575`
        *   Primary Background: `#FFFFFF` (White)
        *   Secondary Background/Card: `#F5F5F5` (Light Gray)
        *   Borders/Dividers: `#E0E0E0` (Lighter Gray)
    *   Information/Utility:
        *   Info/Links: `#2196F3` (Blue)
        *   Warning/Caution: `#FFC107` (Amber)
    *   Chart Specific Colors:
        *   For multi-series charts, use a diverse yet harmonious set of colors that ensure sufficient contrast and distinction. Prioritize green for positive and red for negative where applicable.
        *   Ensure accessibility in color choices, maintaining sufficient contrast.

3.  TYPOGRAPHY

    Readability is paramount for presenting financial data effectively. A clean, sans-serif font family is preferred, leveraging Streamlit's default typography where possible.

    *   Font Family: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif` (or Streamlit's default sans-serif font for performance and consistency).
    *   Headings:
        *   H1 (Page Title): `2.2em` / `28px`, `font-weight: 600` (Semi-bold), `#212121`
        *   H2 (Section Title): `1.8em` / `24px`, `font-weight: 500` (Medium), `#212121`
        *   H3 (Subsection Title): `1.4em` / `18px`, `font-weight: 500` (Medium), `#424242`
    *   Body Text:
        *   Default: `1em` / `16px`, `font-weight: 400` (Regular), `#424242`
        *   Small Text/Labels/Captions: `0.875em` / `14px`, `font-weight: 400` (Regular), `#757575`
    *   Monospace Font: For displaying stock tickers, code snippets, or specific data points where character alignment is important, use `Consolas, monospace` or `Fira Code, monospace`.
    *   Line Height: `1.5` for body text to improve readability and visual comfort.

4.  LAYOUT & SPACING

    Leverage Streamlit's layout capabilities to create a clear and organized structure.

    *   Grid System: Utilize `st.columns` for structured content distribution, `st.container` for grouping, and `st.sidebar` for navigation.
    *   Padding:
        *   Global Page Padding: A comfortable padding around the main content area (e.g., `2rem` or `32px`).
        *   Component Padding: Consistent internal padding within card-like components (`1rem` or `16px`).
    *   Margin:
        *   Between Major Sections: `2rem` (32px) vertical margin.
        *   Between Sub-elements: `1rem` (16px) vertical margin between related elements, `0.5rem` (8px) for smaller gaps.
    *   Alignment: Left-alignment for most text and data elements. Numerical data in tables should be right-aligned for easy comparison.

5.  UI COMPONENTS

    Primarily utilize Streamlit's native components, focusing on clear data presentation and user interaction.

    *   Buttons:
        *   Primary Actions: Use Streamlit's `type="primary"` for buttons with `Primary Accent` color. Text should be concise and actionable.
        *   Secondary Actions: Default Streamlit buttons for less critical actions.
        *   States: Streamlit handles default, hover, active, and disabled states naturally.
    *   Input Fields (Text, Select, Number Inputs):
        *   Clear and concise labels positioned above the input field.
        *   Consistent sizing and alignment.
        *   Validation feedback (e.g., error messages) should be clearly displayed using the `Error` color.
    *   Data Tables (`st.dataframe`, `st.table`):
        *   Ensure column headers are clear and informative.
        *   For improved readability, consider alternating row backgrounds (e.g., `#F5F5F5` and `#FFFFFF`) if easily configurable via custom CSS or Streamlit's theming.
        *   Numerical data should be right-aligned; textual data left-aligned.
        *   Key performance indicators (KPIs) showing positive changes can be highlighted in `Primary Accent` (green), negative in `Secondary Accent` (red).
    *   Charts/Graphs:
        *   Utilize Streamlit's native charting integrations (e.g., Plotly, Altair).
        *   Color Use: Consistently apply `Primary Accent` (green) for positive trends/values and `Secondary Accent` (red) for negative. For other data series, use distinct colors from the defined palette or a well-chosen chart-specific palette that ensures contrast.
        *   Labels & Titles: All charts must have clear, concise titles and appropriately labeled axes.
        *   Legends: Ensure legends are visible, understandable, and non-overlapping.
        *   Tooltips: Provide detailed information on hover for data points.
    *   Navigation:
        *   Use `st.sidebar` for primary navigation (e.g., "Dashboard", "Watchlists", "Portfolio", "Settings").
        *   Navigation items should have clear, descriptive labels.
    *   Cards/Panels (`st.container`, `st.expander`):
        *   Use these to group related information visually. A subtle background (`#F5F5F5`) and a light border (`#E0E0E0`) can define these sections if custom CSS is applied.
        *   Maintain consistent corner radius (e.g., `4px`) for a softer look.

6.  IMAGERY AND ICONS

    *   Icons: Use icons sparingly for quick visual cues (e.g., "Export" icon, "Add to Watchlist" icon, "Refresh" icon).
        *   Style: Prefer simple, clear, and consistent icons (e.g., solid or outline style from a reputable icon library like Font Awesome or Streamlit's built-in icons if available).
        *   Color: Icons should typically inherit text color or use `Info` blue for interactive elements.
    *   Illustrations/Graphics: Not a primary focus for this demo due to budget and time constraints. If introduced in the future, they should be minimalist, clean, and align with the professional aesthetic.

7.  ACCESSIBILITY CONSIDERATIONS

    While a full accessibility audit is out of scope for a personal demo with no budget, basic principles should be followed to improve usability for all.

    *   Color Contrast: Ensure sufficient contrast between text and background colors (aim for WCAG AA standard or better).
    *   Font Sizes: Maintain minimum font sizes for readability (`16px` for body text, `14px` for small text).
    *   Interactive Elements: Ensure interactive elements (buttons, links) are clearly distinguishable, have sufficient click/tap targets, and provide visual feedback on interaction.
    *   Keyboard Navigation: Streamlit's native components generally support keyboard navigation; ensure custom elements (if any) are also navigable.
    *   Alternative Text: (Future consideration) For complex images or charts, provide concise alternative text or summary descriptions where possible to convey information to screen reader users.
