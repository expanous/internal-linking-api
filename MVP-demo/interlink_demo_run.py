#!/usr/bin/env python3
import yaml
from interlink_service import InterlinkService
from bs4 import BeautifulSoup

# Load all URLs from urls.yaml
def load_urls(yaml_path):
    with open(yaml_path, 'r') as f:
        urls = [line.strip('- ').strip() for line in f if line.strip() and line.strip().startswith('-')]
    return [{"url": url} for url in urls if url.startswith('http')]

# Load HTML content from the article
def load_html(article_path):
    with open(article_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_links(original_html, linked_html):
    """Analyze and summarize the links that were added."""
    original_soup = BeautifulSoup(original_html, 'html.parser')
    linked_soup = BeautifulSoup(linked_html, 'html.parser')
    
    # Find all links in the processed HTML
    links = linked_soup.find_all('a')
    
    print("=" * 60)
    print("INTERLINKING SUMMARY")
    print("=" * 60)
    print(f"Total links inserted: {len(links)}")
    print()
    
    print("DETAILED LINK BREAKDOWN:")
    print("-" * 40)
    
    link_summary = {}
    for i, link in enumerate(links, 1):
        text = link.get_text().strip()
        url = link.get('href', '')
        
        print(f"{i:2d}. '{text}' → {url}")
        
        # Group by URL for summary
        if url not in link_summary:
            link_summary[url] = []
        link_summary[url].append(text)
    
    print()
    print("LINKS BY TARGET URL:")
    print("-" * 40)
    
    for url, terms in link_summary.items():
        print(f"\n{url}")
        for term in terms:
            print(f"  • '{term}'")
    
    print()
    print("STATISTICS:")
    print("-" * 40)
    print(f"• Total unique URLs linked: {len(link_summary)}")
    print(f"• Total terms linked: {len(links)}")
    print(f"• Average terms per URL: {len(links)/len(link_summary):.1f}")
    
    # Show some examples of what wasn't linked
    print()
    print("SAMPLE TERMS THAT COULD BE LINKED (if in glossary):")
    print("-" * 40)
    potential_terms = [
        "trading", "orders", "volume", "price", "timing", "algorithm", 
        "chart analysis", "computer codes", "market conditions", 
        "buy", "sell", "seconds", "financial markets", "1970s", 
        "New York Stock Exchange", "computers", "data processing",
        "institutional", "retail", "pension funds", "investment banks",
        "high-speed software", "mathematical formulae", "automated trading systems",
        "high-frequency trading", "tens of thousands", "trades per second",
        "order execution", "trend trading", "arbitrage strategies",
        "machine learning", "deep-learning", "trading performance",
        "brokerage firms", "institutional investors", "market makers",
        "liquidity", "scalping strategy", "price fluctuations",
        "reduced costs", "flash crashes"
    ]
    
    linked_terms = [link.get_text().strip().lower() for link in links]
    unlinked = [term for term in potential_terms if term.lower() not in linked_terms]
    
    for term in unlinked[:10]:  # Show first 10
        print(f"• {term}")

def main():
    urls = load_urls('../urls.yaml')
    html_content = load_html('../Articles/algo-trading')
    service = InterlinkService()
    result = service.process_html(html_content, urls)
    
    print("\n===== INTERLINKING ANALYSIS =====")
    analyze_links(html_content, result)
    
    print("\n" + "=" * 60)
    print("SAMPLE OF INTERLINKED HTML:")
    print("=" * 60)
    print(result[:1000] + "..." if len(result) > 1000 else result)

if __name__ == "__main__":
    main() 