#!/usr/bin/env python3
"""
Example usage of the InterlinkService demonstrating the exact use case from requirements.
"""

from interlink_service import InterlinkService

def main():
    """Demonstrate the interlink service with the example from requirements."""
    
    print("Interlink Service - Example Usage")
    print("=" * 50)
    
    # Initialize the service
    service = InterlinkService()
    
    # Example HTML content (as specified in requirements)
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
    
    # Target entries as specified in requirements
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/algo-trading"}
    ]
    
    print("INPUT:")
    print("HTML Content:")
    print(html_content)
    print("\nTarget Entries:")
    for entry in target_entries:
        print(f"  - {entry['url']}")
    
    print("\n" + "=" * 50)
    print("PROCESSING...")
    
    # Process the HTML
    result = service.process_html(html_content, target_entries, "https://capital.com/en-int/learn/financial-markets")
    
    print("\nOUTPUT:")
    print("Updated HTML with interlinks:")
    print(result)
    
    print("\n" + "=" * 50)
    print("ANALYSIS:")
    
    # Extract and display the processed paragraph
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(result, 'html.parser')
    paragraphs = soup.find_all('p')
    
    print("Processed paragraphs:")
    for i, p in enumerate(paragraphs, 1):
        print(f"\nParagraph {i}:")
        print(p.prettify())
    
    # Count links
    links = soup.find_all('a')
    print(f"\nTotal links inserted: {len(links)}")
    
    print("\n" + "=" * 50)
    print("EXPECTED BEHAVIOR VERIFICATION:")
    
    # Verify expected behavior
    expected_terms = ['stocks', 'ETFs', 'commodities', 'portfolio', 'index funds', 'algorithmic trading']
    found_terms = [link.get_text() for link in links]
    
    print("Expected terms to be linked:")
    for term in expected_terms:
        found = any(term.lower() in found_term.lower() for found_term in found_terms)
        status = "✓" if found else "✗"
        print(f"  {status} {term}")
    
    # Check that no links are in headings
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_links = [h.find('a') for h in headings if h.find('a')]
    
    if not heading_links:
        print("  ✓ No links inserted in headings")
    else:
        print(f"  ✗ Found {len(heading_links)} links in headings (should be 0)")
    
    # Check for duplicate links
    link_urls = [link.get('href') for link in links]
    unique_urls = set(link_urls)
    
    if len(link_urls) == len(unique_urls):
        print("  ✓ No duplicate links (each target URL used only once)")
    else:
        print(f"  ✗ Found duplicate links: {len(link_urls)} total, {len(unique_urls)} unique")

if __name__ == "__main__":
    main() 