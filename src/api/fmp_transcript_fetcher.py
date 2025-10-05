"""
FMP Transcript Fetcher - Get earnings call transcripts from Financial Modeling Prep
"""
import requests
import streamlit as st
from datetime import datetime
import time


class FMPTranscriptFetcher:
    """Fetcher for FMP earnings transcripts"""
    
    def __init__(self, api_key: str):
        """
        Initialize FMP Transcript Fetcher
        
        Args:
            api_key: API key for Financial Modeling Prep
        """
        self.api_key = api_key
        self.base_url = 'https://financialmodelingprep.com'
        
    def _rate_limit_wait(self, wait_time: float = 0.5):
        """Wait between API calls to avoid rate limits"""
        time.sleep(wait_time)
    
    def get_available_transcripts(self, limit: int = 100):
        """
        Get list of available earnings transcripts
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of available transcripts or empty list on error
        """
        try:
            url = f'{self.base_url}/stable/earning-call-transcript-latest'
            params = {
                'apikey': self.api_key,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                else:
                    print(f"FMP API returned unexpected format: {data}")
                    return []
            else:
                print(f"FMP API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error fetching available transcripts: {e}")
            return []
    
    @st.cache_data(ttl=3600)
    def get_transcript(_self, symbol: str, year: int = None, quarter: int = None):
        """
        Get earnings call transcript for a specific company
        
        Strategy:
        1. First get the list of available transcripts
        2. Find the most recent one for this symbol
        3. Then fetch the specific transcript with year/quarter
        
        Args:
            symbol: Stock ticker symbol
            year: Fiscal year (optional)
            quarter: Quarter number (optional)
            
        Returns:
            Dict with transcript data or None on error
        """
        try:
            # Step 1: Get list of available transcripts to find the right one
            print(f"Fetching available transcripts for {symbol}...")
            available = _self.get_available_transcripts(limit=100)
            
            if not available:
                print(f"No transcripts available from API")
                return None
            
            # Step 2: Find transcripts for this symbol
            symbol_transcripts = [t for t in available if t.get('symbol', '').upper() == symbol.upper()]
            
            if not symbol_transcripts:
                print(f"No transcript found for {symbol} in available list")
                return None
            
            # Get the most recent one
            latest = symbol_transcripts[0]
            transcript_year = latest.get('fiscalYear') or latest.get('year')
            transcript_quarter = latest.get('period', 'Q1').replace('Q', '')
            
            print(f"Found transcript: {symbol} Q{transcript_quarter} {transcript_year}")
            
            # Step 3: Try to fetch the actual transcript content
            # Method 1: Try with year and quarter
            endpoints_to_try = [
                f'/api/v3/earning_call_transcript/{symbol}?year={transcript_year}&quarter={transcript_quarter}',
                f'/api/v4/batch_earning_call_transcript/{symbol}?year={transcript_year}&quarter={transcript_quarter}',
            ]
            
            for endpoint_url in endpoints_to_try:
                try:
                    url = f'{_self.base_url}{endpoint_url}&apikey={_self.api_key}'
                    print(f"Trying: {endpoint_url}")
                    
                    response = requests.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if we got actual content
                        if isinstance(data, list) and len(data) > 0:
                            transcript = data[0]
                            if transcript.get('content'):
                                print(f"✅ Successfully fetched transcript content!")
                                return transcript
                        elif isinstance(data, dict) and data.get('content'):
                            print(f"✅ Successfully fetched transcript content!")
                            return data
                    
                    _self._rate_limit_wait()
                    
                except Exception as e:
                    print(f"Endpoint failed: {e}")
                    continue
            
            # If we couldn't get the content, return the metadata at least
            print(f"⚠️ Could only get transcript metadata, not full content")
            return {
                'symbol': latest.get('symbol'),
                'quarter': transcript_quarter,
                'year': transcript_year,
                'date': latest.get('date', 'Unknown'),
                'content': None  # Will trigger fallback to sample data
            }
                
        except Exception as e:
            print(f"Error fetching transcript for {symbol}: {e}")
            return None
    
    def get_sample_transcript(self, symbol: str = "AAPL"):
        """
        Get sample transcript for testing (fallback when API fails)
        
        Args:
            symbol: Stock ticker
            
        Returns:
            Dict with sample transcript data
        """
        return {
            'symbol': symbol,
            'quarter': 3,
            'year': 2024,
            'date': '2024-08-01',
            'content': f"""
SAMPLE EARNINGS CALL TRANSCRIPT FOR {symbol}

Operator: Good afternoon, and welcome to the {symbol} Q3 2024 Earnings Conference Call.

CEO: Thank you for joining us today. I'm pleased to report strong financial results for the quarter. Our revenue grew 15% year-over-year, driven by robust demand across all product lines.

Key highlights include:
- Revenue of $95 billion, up 15% YoY
- Operating margin improved to 28%
- Strong cash flow generation of $25 billion
- Continued investment in R&D and innovation

We're seeing particular strength in our services segment, which grew 20% year-over-year. Our product ecosystem continues to drive customer loyalty and engagement.

CFO: From a financial perspective, we delivered excellent results. Gross margin expanded by 100 basis points to 45%, reflecting favorable product mix and operational efficiency improvements.

Operating expenses were well controlled at $13 billion, representing 14% of revenue. We generated $28 billion in operating cash flow during the quarter.

We returned $25 billion to shareholders through dividends and share repurchases, demonstrating our commitment to capital allocation.

Looking ahead, we expect continued momentum. We're investing heavily in artificial intelligence and machine learning capabilities, which we believe will drive future growth.

Our balance sheet remains strong with $50 billion in net cash. This positions us well to continue investing in innovation while returning capital to shareholders.

Analyst Q&A:

Analyst 1: Can you provide more color on the services growth?

CEO: Absolutely. Services revenue reached $25 billion, up 20% year-over-year. We're seeing strong adoption across our subscription offerings. Customer engagement metrics are at all-time highs, with average revenue per user increasing steadily.

The installed base continues to expand, now exceeding 2 billion active devices. This creates a strong foundation for recurring revenue growth. We're particularly excited about new service offerings launching next quarter.

Analyst 2: What are your thoughts on the competitive landscape?

CEO: Competition remains intense, but we believe our integrated ecosystem provides significant differentiation. Our focus on privacy, security, and user experience resonates strongly with customers.

We're seeing market share gains in key segments. Our premium positioning allows us to maintain healthy margins while investing in innovation. The combination of hardware, software, and services creates switching costs that protect our market position.

Analyst 3: How should we think about margin trajectory going forward?

CFO: We expect margins to remain healthy. Product mix will be a key driver, with services contributing an increasing share of revenue. Services carry higher margins and help offset pressure in hardware.

We're also driving operational efficiencies through automation and scale. Supply chain improvements have reduced costs. However, we continue to invest heavily in R&D, which we view as essential for long-term competitiveness.

Overall, we feel confident about maintaining operating margins in the 27-29% range while continuing to invest for growth.

Closing Remarks:

CEO: In summary, we delivered strong results this quarter. Revenue and earnings exceeded expectations. Cash flow remains robust, enabling significant capital returns.

Looking ahead, we're excited about our product pipeline. Several major launches are planned for the coming quarters. We're investing in next-generation technologies that will drive future growth.

Our business model remains resilient, with diversified revenue streams and a loyal customer base. We're confident in our ability to continue delivering value for shareholders.

Thank you for your continued support. We look forward to updating you on our progress next quarter.

Operator: This concludes today's conference call. Thank you for participating.

[END OF TRANSCRIPT]

Note: This is a sample transcript for demonstration purposes.
            """.strip()
        }

