#!/usr/bin/env python3
"""
Test script for the InterlinkService demonstrating various use cases.
"""

import sys
import os
from interlink_service import InterlinkService

def test_basic_functionality():
    """Test basic interlink functionality."""
    print("=" * 60)
    print("TEST 1: Basic Functionality")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <head><title>Financial Markets Guide</title></head>
    <body>
        <h1>Understanding Financial Markets</h1>
        <p>The global electronic marketplace is a major platform for investors to trade company stocks, bonds, exchange-traded funds (ETFs), commodities and other financial instruments.</p>
        <p>Portfolio management involves diversifying investments across different asset classes including index funds and mutual funds.</p>
        <div>
            <p>Algorithmic trading has become increasingly popular in modern markets.</p>
        </div>
    </body>
    </html>
    """
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/algo-trading"}
    ]
    
    result = service.process_html(html_content, target_entries, "https://capital.com/en-int/learn/financial-markets")
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def test_glossary_entries():
    """Test with explicit glossary entries."""
    print("=" * 60)
    print("TEST 2: Glossary Entries with Explicit Terms")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <body>
        <p>Investors often use ETFs to build diversified portfolios. Many choose index funds for their low costs and broad market exposure.</p>
        <p>When trading commodities, it's important to understand market dynamics and risk management strategies.</p>
    </body>
    </html>
    """
    
    glossary_entries = [
        {"term": "ETFs", "url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"term": "portfolios", "url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"term": "index funds", "url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"term": "commodities", "url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"}
    ]
    
    result = service.process_html_with_glossary(html_content, glossary_entries)
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def test_excluded_elements():
    """Test that links are not inserted in excluded elements."""
    print("=" * 60)
    print("TEST 3: Excluded Elements (Headings, Links)")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <body>
        <h1>Portfolio Management Guide</h1>
        <nav>
            <a href="/about">About ETFs</a>
        </nav>
        <p>This guide covers portfolio management strategies using ETFs and index funds.</p>
        <h2>Understanding Commodities</h2>
        <p>Commodities trading involves various financial instruments.</p>
    </body>
    </html>
    """
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"}
    ]
    
    result = service.process_html(html_content, target_entries)
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def test_duplicate_prevention():
    """Test that only the first occurrence of each term is linked."""
    print("=" * 60)
    print("TEST 4: Duplicate Prevention")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <body>
        <p>ETFs are popular investment vehicles. Many investors choose ETFs for their diversification benefits.</p>
        <p>When discussing ETFs, it's important to understand their structure and costs.</p>
        <p>ETFs have revolutionized the investment landscape.</p>
    </body>
    </html>
    """
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"}
    ]
    
    result = service.process_html(html_content, target_entries)
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def test_case_insensitive_matching():
    """Test case-insensitive matching."""
    print("=" * 60)
    print("TEST 5: Case-Insensitive Matching")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <body>
        <p>ETFs, etfs, and Etfs are all the same thing.</p>
        <p>Portfolio, PORTFOLIO, and portfolio management.</p>
    </body>
    </html>
    """
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"}
    ]
    
    result = service.process_html(html_content, target_entries)
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def test_multi_word_terms():
    """Test multi-word term matching."""
    print("=" * 60)
    print("TEST 6: Multi-Word Terms")
    print("=" * 60)
    
    service = InterlinkService()
    
    html_content = """
    <html>
    <body>
        <p>Index funds provide broad market exposure at low costs.</p>
        <p>Exchange-traded funds are popular investment vehicles.</p>
        <p>Share trading involves buying and selling company stocks.</p>
    </body>
    </html>
    """
    
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"}
    ]
    
    result = service.process_html(html_content, target_entries)
    
    print("Original HTML:")
    print(html_content)
    print("\nProcessed HTML:")
    print(result)
    print("\n" + "-" * 60)

def main():
    """Run all tests."""
    print("InterlinkService Test Suite")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_glossary_entries()
        test_excluded_elements()
        test_duplicate_prevention()
        test_case_insensitive_matching()
        test_multi_word_terms()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 