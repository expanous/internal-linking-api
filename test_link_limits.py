#!/usr/bin/env python3
"""
Test script to demonstrate the 12-link limit functionality.
"""

from enhanced_internal_linking import EnhancedInternalLinker

def test_link_limits():
    """Test different link limit scenarios."""
    linker = EnhancedInternalLinker()
    
    print("🔗 LINK LIMIT TESTING")
    print("=" * 50)
    
    # Test 1: Article with no existing links
    print("\n📄 TEST 1: Policy-mix article (0 existing links)")
    print("-" * 40)
    html = linker.create_html_links('Articles/policy-mix', 'test-policy-12.html', max_links=12)
    
    # Test 2: Article with many existing links
    print("\n📄 TEST 2: ETF article (21 existing links)")
    print("-" * 40)
    html = linker.create_html_links('Articles/etf', 'test-etf-12.html', max_links=12)
    
    # Test 3: Custom limit of 5
    print("\n📄 TEST 3: Policy-mix with 5-link limit")
    print("-" * 40)
    html = linker.create_html_links('Articles/policy-mix', 'test-policy-5.html', max_links=5)
    
    # Test 4: Very low limit
    print("\n📄 TEST 4: Policy-mix with 2-link limit")
    print("-" * 40)
    html = linker.create_html_links('Articles/policy-mix', 'test-policy-2.html', max_links=2)
    
    print("\n✅ All tests completed! Check the generated HTML files.")

if __name__ == "__main__":
    test_link_limits() 