#!/usr/bin/env python3
"""
Script to process URLs from urls.yaml and generate enriched JSON objects for glossary terms.
Uses the provided prompt to extract terms, aliases, and categories.
"""

import yaml
import json
import re
from urllib.parse import urlparse
from typing import List, Dict, Optional
import time

def extract_term_from_url(url: str) -> Optional[str]:
    """
    Extract the main term from a glossary URL.
    
    Args:
        url: The glossary URL
        
    Returns:
        The extracted term or None if not a glossary URL
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    # Look for glossary entries
    if 'glossary' in path_parts:
        for part in path_parts:
            if part.endswith('-definition'):
                term = part.replace('-definition', '')
                # Convert hyphens to spaces and clean up
                term_clean = term.replace('-', ' ').strip()
                return term_clean
    
    return None

def generate_aliases(term: str) -> List[str]:
    """
    Generate common aliases for a term.
    
    Args:
        term: The main term
        
    Returns:
        List of aliases including the original term
    """
    aliases = [term]
    
    # Add singular/plural variations
    if term.endswith('s'):
        aliases.append(term[:-1])  # Remove 's' for singular
    else:
        aliases.append(term + 's')  # Add 's' for plural
    
    # Add common variations based on term patterns
    if 'trading' in term:
        aliases.append(term.replace('trading', 'trade'))
        aliases.append(term.replace('trading', 'trades'))
    
    if 'fund' in term:
        if term.endswith('funds'):
            aliases.append(term.replace('funds', 'fund'))
        elif term.endswith('fund'):
            aliases.append(term.replace('fund', 'funds'))
    
    if 'investment' in term:
        aliases.append(term.replace('investment', 'investing'))
    
    # Add common abbreviations
    if 'exchange traded fund' in term:
        aliases.append('ETF')
        aliases.append('ETFs')
    
    if 'initial public offering' in term:
        aliases.append('IPO')
        aliases.append('IPOs')
    
    # Remove duplicates and return
    return list(dict.fromkeys(aliases))

def categorize_term(term: str) -> str:
    """
    Categorize a term based on its content.
    
    Args:
        term: The term to categorize
        
    Returns:
        The category
    """
    term_lower = term.lower()
    
    # Trading and investment categories
    if any(word in term_lower for word in ['trading', 'trade', 'trader']):
        return 'trading strategies'
    elif any(word in term_lower for word in ['fund', 'investment', 'portfolio']):
        return 'investment funds'
    elif any(word in term_lower for word in ['stock', 'share', 'equity']):
        return 'equity markets'
    elif any(word in term_lower for word in ['forex', 'currency', 'fx']):
        return 'foreign exchange'
    elif any(word in term_lower for word in ['crypto', 'bitcoin', 'blockchain']):
        return 'cryptocurrency'
    elif any(word in term_lower for word in ['commodity', 'oil', 'gold', 'silver']):
        return 'commodities'
    elif any(word in term_lower for word in ['bond', 'yield', 'fixed income']):
        return 'fixed income'
    elif any(word in term_lower for word in ['index', 'indices']):
        return 'market indices'
    elif any(word in term_lower for word in ['derivative', 'option', 'futures', 'cfd']):
        return 'derivatives'
    elif any(word in term_lower for word in ['risk', 'volatility', 'hedge']):
        return 'risk management'
    elif any(word in term_lower for word in ['technical', 'chart', 'indicator']):
        return 'technical analysis'
    elif any(word in term_lower for word in ['fundamental', 'earnings', 'valuation']):
        return 'fundamental analysis'
    elif any(word in term_lower for word in ['economy', 'gdp', 'inflation', 'monetary']):
        return 'economics'
    else:
        return 'general finance'

def process_glossary_urls(urls_file: str = 'urls.yaml', output_file: str = 'glossary_terms.json'):
    """
    Process URLs from YAML file and generate enriched JSON objects.
    
    Args:
        urls_file: Path to the YAML file containing URLs
        output_file: Path to save the JSON output
    """
    # Load URLs
    with open(urls_file, 'r') as f:
        urls = yaml.safe_load(f)
    
    glossary_terms = []
    
    print(f"Processing {len(urls)} URLs...")
    
    for i, url in enumerate(urls, 1):
        # Extract term from URL
        term = extract_term_from_url(url)
        
        if term:
            # Generate aliases
            aliases = generate_aliases(term)
            
            # Categorize term
            category = categorize_term(term)
            
            # Create JSON object
            term_obj = {
                "term": term,
                "url": url,
                "aliases": aliases,
                "category": category
            }
            
            glossary_terms.append(term_obj)
            
            if i % 50 == 0:
                print(f"Processed {i}/{len(urls)} URLs...")
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(glossary_terms, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Processed {len(glossary_terms)} glossary terms")
    print(f"📁 Saved to: {output_file}")
    
    # Show some statistics
    categories = {}
    for term_obj in glossary_terms:
        cat = term_obj['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Categories breakdown:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} terms")
    
    return glossary_terms

def main():
    """Main function to run the processing."""
    try:
        terms = process_glossary_urls()
        print(f"\n🎉 Successfully processed {len(terms)} glossary terms!")
        
        # Show a few examples
        print(f"\n📝 Example entries:")
        for i, term_obj in enumerate(terms[:3]):
            print(f"\n{i+1}. {term_obj['term']}")
            print(f"   Category: {term_obj['category']}")
            print(f"   Aliases: {', '.join(term_obj['aliases'][:5])}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 