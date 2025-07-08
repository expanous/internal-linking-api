#!/usr/bin/env python3
"""
Test script to verify link counting logic
"""

from enhanced_internal_linking import EnhancedInternalLinker
from bs4 import BeautifulSoup
import tempfile
import os

def test_link_counting():
    """Test link counting logic"""
    print("🔍 Testing Link Counting Logic")
    print("=" * 40)
    
    # Initialize linker
    linker = EnhancedInternalLinker()
    
    # Read the revenue article
    with open('Articles/revenue', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count existing links in original content
    soup = BeautifulSoup(content, 'html.parser')
    existing_links = soup.find_all('a')
    print(f"Original article has {len(existing_links)} existing links:")
    for i, link in enumerate(existing_links, 1):
        print(f"  {i}. {link.get_text()} -> {link.get('href')}")
    
    # Create HTML with links
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(content)
        temp_file = f.name
    
    try:
        html_output = linker.create_html_links(temp_file, max_links=12)
        
        # Count total links in output
        output_soup = BeautifulSoup(html_output, 'html.parser')
        total_links = output_soup.find_all('a')
        
        print(f"\nOutput has {len(total_links)} total links:")
        for i, link in enumerate(total_links, 1):
            print(f"  {i}. {link.get_text()} -> {link.get('href')}")
        
        print(f"\n📊 Summary:")
        print(f"  Original links: {len(existing_links)}")
        print(f"  Total links: {len(total_links)}")
        print(f"  New links added: {len(total_links) - len(existing_links)}")
        
        # Check if any original links were modified
        original_hrefs = [link.get('href') for link in existing_links]
        output_hrefs = [link.get('href') for link in total_links]
        
        print(f"\n🔍 Link Analysis:")
        print(f"  Original hrefs: {original_hrefs}")
        print(f"  Output hrefs: {output_hrefs}")
        
        # Find new links (not in original)
        new_links = []
        for link in total_links:
            if link.get('href') not in original_hrefs:
                new_links.append(link)
        
        print(f"\n✨ New links added:")
        for i, link in enumerate(new_links, 1):
            print(f"  {i}. {link.get_text()} -> {link.get('href')}")
            
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    test_link_counting() 