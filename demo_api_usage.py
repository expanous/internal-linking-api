#!/usr/bin/env python3
"""
Demo script showing how to use the Enhanced Internal Linking API
"""

import requests
import json
from typing import Dict, Any

class InternalLinkingAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get glossary statistics"""
        response = requests.get(f"{self.base_url}/stats")
        return response.json()
    
    def get_categories(self) -> Dict[str, Any]:
        """Get all categories"""
        response = requests.get(f"{self.base_url}/categories")
        return response.json()
    
    def process_article(self, content: str, max_links: int = 12, current_url: str = None) -> Dict[str, Any]:
        """Process article content and add internal links"""
        payload = {
            "content": content,
            "max_links": max_links
        }
        if current_url:
            payload["current_url"] = current_url
        
        response = requests.post(f"{self.base_url}/process", json=payload)
        return response.json()
    
    def analyze_article(self, content: str, current_url: str = None) -> Dict[str, Any]:
        """Analyze article content without creating links"""
        payload = {
            "content": content,
            "current_url": current_url
        }
        
        response = requests.post(f"{self.base_url}/analyze", json=payload)
        return response.json()
    
    def upload_and_process(self, file_path: str, max_links: int = 12) -> Dict[str, Any]:
        """Upload and process an article file"""
        with open(file_path, 'rb') as f:
            files = {"file": f}
            params = {"max_links": max_links}
            response = requests.post(f"{self.base_url}/upload", files=files, params=params)
            return response.json()

def main():
    """Demo the API functionality"""
    print("🚀 Enhanced Internal Linking API Demo")
    print("=" * 50)
    
    # Initialize API client
    api = InternalLinkingAPI()
    
    try:
        # 1. Health check
        print("1. Health Check")
        health = api.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Glossary loaded: {health['glossary_loaded']}")
        print(f"   Total terms: {health['total_terms']}")
        print()
        
        # 2. Get statistics
        print("2. Glossary Statistics")
        stats = api.get_statistics()
        print(f"   Total terms: {stats['total_terms']}")
        print(f"   Total aliases: {stats['total_aliases']}")
        print(f"   Categories: {len(stats['categories'])}")
        print()
        
        # 3. Get top categories
        print("3. Top Categories")
        categories = api.get_categories()
        top_categories = sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (category, count) in enumerate(top_categories, 1):
            print(f"   {i}. {category}: {count} terms")
        print()
        
        # 4. Process sample article
        print("4. Process Sample Article")
        sample_content = """
        <h1>Financial Markets Overview</h1>
        <p>Revenue is a crucial metric for investors analyzing company performance. 
        ETFs provide diversification benefits for retail investors. 
        Capital markets facilitate the flow of funds between investors and companies.</p>
        
        <h2>Key Investment Concepts</h2>
        <ul>
            <li>Revenue growth indicates business expansion</li>
            <li>ETFs offer low-cost diversification</li>
            <li>Investors should consider multiple factors</li>
        </ul>
        """
        
        result = api.process_article(
            content=sample_content,
            max_links=8,
            current_url="https://capital.com//en-int/learn/glossary/revenue-definition"
        )
        
        print(f"   Total links: {result['total_links']}")
        print(f"   Existing links: {result['existing_links']}")
        print(f"   New links added: {result['new_links_added']}")
        print(f"   Max links: {result['max_links']}")
        print()
        
        # 5. Analyze article without creating links
        print("5. Analyze Article (No Links)")
        analysis = api.analyze_article(
            content=sample_content,
            current_url="https://capital.com//en-int/learn/glossary/revenue-definition"
        )
        
        print(f"   Total matches: {analysis['total_matches']}")
        print(f"   Unique terms: {len(analysis['unique_terms'])}")
        print(f"   Terms found: {', '.join(analysis['unique_terms'])}")
        print()
        
        print("   Matches by category:")
        for category, matches in analysis['matches_by_category'].items():
            print(f"     {category}: {len(matches)} matches")
            for match in matches[:2]:  # Show first 2 matches per category
                print(f"       - '{match['term']}' -> {match['url']}")
        print()
        
        # 6. Show HTML preview
        print("6. HTML Output Preview")
        html_preview = result['html_content'][:300] + "..." if len(result['html_content']) > 300 else result['html_content']
        print(f"   {html_preview}")
        print()
        
        print("✅ Demo completed successfully!")
        print(f"\n📖 Full API documentation: {api.base_url}/docs")
        print(f"🔗 Health check: {api.base_url}/health")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   python3 api_internal_linking.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    main() 