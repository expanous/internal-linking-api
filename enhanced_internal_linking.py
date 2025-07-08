#!/usr/bin/env python3
"""
Enhanced Internal Linking Service that uses enriched glossary terms with aliases and categories.
"""

import json
import spacy
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Set, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedInternalLinker:
    """
    Enhanced internal linker that uses enriched glossary terms with aliases and categories.
    """
    
    def __init__(self, glossary_file: str = 'glossary_terms.json', nlp_model: str = "en_core_web_sm"):
        """
        Initialize the EnhancedInternalLinker.
        
        Args:
            glossary_file: Path to the JSON file containing enriched glossary terms
            nlp_model: spaCy model name to use
        """
        self.glossary_file = glossary_file
        self.nlp = spacy.load(nlp_model)
        self.glossary_terms = self._load_glossary_terms()
        self.term_to_url_map = self._create_term_mapping()
        
    def _load_glossary_terms(self) -> List[Dict]:
        """
        Load glossary terms from JSON file.
        
        Returns:
            List of glossary term dictionaries
        """
        try:
            with open(self.glossary_file, 'r', encoding='utf-8') as f:
                terms = json.load(f)
            logger.info(f"Loaded {len(terms)} glossary terms from {self.glossary_file}")
            return terms
        except FileNotFoundError:
            logger.warning(f"Glossary file {self.glossary_file} not found. Creating empty glossary.")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file: {e}")
            return []
    
    def _create_term_mapping(self) -> Dict[str, str]:
        """
        Create a mapping from all aliases to their URLs.
        
        Returns:
            Dictionary mapping terms/aliases to URLs
        """
        term_map = {}
        for term_obj in self.glossary_terms:
            url = term_obj.get('url', '')
            if url:
                # Map the main term
                term_map[term_obj['term'].lower()] = url
                # Map all aliases
                for alias in term_obj.get('aliases', []):
                    term_map[alias.lower()] = url
        return term_map
    
    def get_terms_by_category(self, category: str) -> List[Dict]:
        """
        Get all terms in a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of term objects in that category
        """
        return [term for term in self.glossary_terms if term.get('category') == category]
    
    def get_categories(self) -> List[str]:
        """
        Get all available categories.
        
        Returns:
            List of unique categories
        """
        return list(set(term.get('category', '') for term in self.glossary_terms))
    
    def find_matches(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Find all matches in the text, but only link each unique URL once.
        
        Args:
            text: The text to search in
            
        Returns:
            List of (term, url, start, end) tuples with only one link per unique URL
        """
        matches = []
        text_lower = text.lower()
        used_urls = set()  # Track which URLs have already been linked
        
        # Parse HTML to find existing links
        soup = BeautifulSoup(text, 'html.parser')
        existing_link_positions = self._get_existing_link_positions(text, soup)
        
        # Sort terms by length (longest first) to avoid partial matches
        sorted_terms = sorted(self.term_to_url_map.keys(), key=len, reverse=True)
        
        for term in sorted_terms:
            url = self.term_to_url_map[term]
            
            # Skip if we've already linked this URL
            if url in used_urls:
                continue
                
            # Find all occurrences of the term
            start = 0
            while True:
                start = text_lower.find(term, start)
                if start == -1:
                    break
                
                end = start + len(term)
                
                # Check if this is a complete word match and not within existing links
                if self._is_complete_word_match(text, start, end) and not self._is_within_existing_links(start, end, existing_link_positions):
                    matches.append((term, url, start, end))
                    used_urls.add(url)  # Mark this URL as used
                    break  # Only take the first occurrence of this term
                
                start = end
        
        return matches
    
    def _find_matches_with_tracking(self, text: str, used_urls: set, max_matches: int = None, current_url: str = None) -> List[Tuple[str, str, int, int]]:
        """
        Find matches in text while tracking used URLs across multiple calls, skipping self-links.
        
        Args:
            text: The text to search in
            used_urls: Set of URLs that have already been used
            max_matches: Maximum number of matches to return (None for unlimited)
            current_url: The current URL to exclude from linking (for self-linking)
            
        Returns:
            List of (term, url, start, end) tuples
        """
        matches = []
        text_lower = text.lower()
        
        # Parse HTML to find existing links
        soup = BeautifulSoup(text, 'html.parser')
        existing_link_positions = self._get_existing_link_positions(text, soup)
        
        # Sort terms by length (longest first) to avoid partial matches
        sorted_terms = sorted(self.term_to_url_map.keys(), key=len, reverse=True)
        
        for term in sorted_terms:
            # Stop if we've reached the maximum matches
            if max_matches is not None and len(matches) >= max_matches:
                break
                
            url = self.term_to_url_map[term]
            
            # Skip if we've already linked this URL
            if url in used_urls:
                continue
                
            # Skip if this is the current_url (self-link)
            if current_url and url.rstrip('/') == current_url.rstrip('/'):
                continue
                
            # Find all occurrences of the term
            start = 0
            while True:
                start = text_lower.find(term, start)
                if start == -1:
                    break
                
                end = start + len(term)
                
                # Check if this is a complete word match and not within existing links
                if self._is_complete_word_match(text, start, end) and not self._is_within_existing_links(start, end, existing_link_positions):
                    matches.append((term, url, start, end))
                    used_urls.add(url)  # Mark this URL as used
                    break  # Only take the first occurrence of this term
                
                start = end
        
        return matches
    
    def _is_complete_word_match(self, text: str, start: int, end: int) -> bool:
        """
        Check if the match is a complete word.
        
        Args:
            text: The original text
            start: Start position of match
            end: End position of match
            
        Returns:
            True if it's a complete word match
        """
        # Check character before
        if start > 0 and text[start-1].isalnum():
            return False
        
        # Check character after
        if end < len(text) and text[end].isalnum():
            return False
        
        return True
    
    def _is_within_anchor_tag(self, text: str, start: int, end: int) -> bool:
        """
        Check if the match is already within an anchor tag.
        
        Args:
            text: The original text
            start: Start position of match
            end: End position of match
            
        Returns:
            True if the match is within an anchor tag
        """
        # Find the last opening <a tag before our match
        last_a_start = text.rfind('<a', 0, start)
        if last_a_start == -1:
            return False
        
        # Find the closing > of the opening tag
        tag_end = text.find('>', last_a_start)
        if tag_end == -1 or tag_end > start:
            return False
        
        # Find the closing </a> tag after our match
        closing_a = text.find('</a>', end)
        if closing_a == -1:
            return False
        
        # Check if there's a closing </a> between our match and the next opening <a
        next_a_start = text.find('<a', end)
        if next_a_start != -1 and next_a_start < closing_a:
            return False
        
        return True
    
    def _get_existing_link_positions(self, text: str, soup: BeautifulSoup) -> List[Tuple[int, int]]:
        """
        Get positions of existing anchor tags in the text.
        
        Args:
            text: The original text
            soup: BeautifulSoup parsed HTML
            
        Returns:
            List of (start, end) positions of existing links
        """
        positions = []
        for link in soup.find_all('a'):
            # Get the text content of the link
            link_text = link.get_text()
            if link_text:
                # Find the position of this link text in the original text
                start = text.find(link_text)
                if start != -1:
                    end = start + len(link_text)
                    positions.append((start, end))
        return positions
    
    def _is_within_existing_links(self, start: int, end: int, existing_positions: List[Tuple[int, int]]) -> bool:
        """
        Check if the match position overlaps with any existing link.
        
        Args:
            start: Start position of match
            end: End position of match
            existing_positions: List of (start, end) positions of existing links
            
        Returns:
            True if the match overlaps with an existing link
        """
        for link_start, link_end in existing_positions:
            # Check if there's any overlap
            if (start < link_end and end > link_start):
                return True
        return False
    
    def _is_within_any_html_tag(self, text: str, start: int, end: int) -> bool:
        """
        Check if the match is within any HTML tag (not just anchor tags).
        
        Args:
            text: The original text
            start: Start position of match
            end: End position of match
            
        Returns:
            True if the match is within any HTML tag
        """
        # Look backwards from start to find the last < character
        last_open = text.rfind('<', 0, start)
        if last_open == -1:
            return False
        
        # Look forwards from start to find the next > character
        next_close = text.find('>', start)
        if next_close == -1:
            return False
        
        # If the last < is before the next >, we're inside a tag
        return last_open < next_close
    
    def process_article(self, article_file: str) -> Dict:
        """
        Process an article and find internal linking opportunities.
        
        Args:
            article_file: Path to the article file
            
        Returns:
            Dictionary with processing results
        """
        try:
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"Article file {article_file} not found")
            return {}
        
        matches = self.find_matches(content)
        
        # Group matches by category
        matches_by_category = {}
        for term, url, start, end in matches:
            # Find the category for this term
            category = self._get_category_for_term(term)
            if category not in matches_by_category:
                matches_by_category[category] = []
            matches_by_category[category].append({
                'term': term,
                'url': url,
                'start': start,
                'end': end,
                'context': content[max(0, start-50):min(len(content), end+50)]
            })
        
        return {
            'article_file': article_file,
            'total_matches': len(matches),
            'matches_by_category': matches_by_category,
            'unique_terms': list(set(term for term, _, _, _ in matches))
        }
    
    def _get_category_for_term(self, term: str) -> str:
        """
        Get the category for a given term.
        
        Args:
            term: The term to look up
            
        Returns:
            The category
        """
        for term_obj in self.glossary_terms:
            if term_obj['term'].lower() == term or term in [alias.lower() for alias in term_obj.get('aliases', [])]:
                return term_obj.get('category', 'unknown')
        return 'unknown'
    
    def _extract_current_url(self, content: str) -> str:
        """
        Extract the current_url from the article if present.
        Returns the URL as a string, or None if not found.
        """
        match = re.search(r'\{current_url\s*=\s*"([^"]+)"\}', content)
        if match:
            return match.group(1).rstrip('/')
        return None

    def create_html_links(self, article_file: str, output_file: str = None, max_links: int = 12) -> str:
        """
        Create HTML version with internal links, avoiding existing links and self-links.
        """
        try:
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"Article file {article_file} not found")
            return ""

        # Extract current_url if present
        current_url = self._extract_current_url(content)
        if current_url:
            logger.info(f"Detected current_url for self-link exclusion: {current_url}")

        # Parse the HTML (skip the current_url line if present)
        html_start = content.find('<')
        html_content = content[html_start:] if html_start != -1 else content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Count existing links
        existing_links = len(soup.find_all('a'))
        logger.info(f"Found {existing_links} existing links in the article")

        # Calculate how many new links we can add
        available_slots = max(0, max_links - existing_links)
        logger.info(f"Can add up to {available_slots} new links (max: {max_links})")

        if available_slots <= 0:
            logger.info("No new links will be added - article already has maximum links")
            return content

        # Track used URLs across all text nodes
        used_urls = set()
        links_added = 0

        # Find all text nodes that are not inside anchor tags
        text_nodes = []
        for element in soup.find_all(string=True):
            if element.parent.name != 'a':
                text_nodes.append(element)

        # Process each text node for matches
        for text_node in text_nodes:
            if text_node.strip() and links_added < available_slots:
                matches = self._find_matches_with_tracking(str(text_node), used_urls, available_slots - links_added, current_url)
                matches.sort(key=lambda x: x[2], reverse=True)
                text_content = str(text_node)
                for term, url, start, end in matches:
                    if links_added >= available_slots:
                        break
                    original_text = text_content[start:end]
                    html_link = f'<a href="{url}">{original_text}</a>'
                    text_content = text_content[:start] + html_link + text_content[end:]
                    links_added += 1
                new_soup = BeautifulSoup(text_content, 'html.parser')
                text_node.replace_with(new_soup)

        result = str(soup)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
        logger.info(f"Added {links_added} new links. Total links: {existing_links + links_added}")
        return result
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the glossary.
        
        Returns:
            Dictionary with statistics
        """
        categories = {}
        total_aliases = 0
        
        for term_obj in self.glossary_terms:
            category = term_obj.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
            total_aliases += len(term_obj.get('aliases', []))
        
        return {
            'total_terms': len(self.glossary_terms),
            'total_aliases': total_aliases,
            'categories': categories,
            'unique_urls': len(set(term_obj.get('url', '') for term_obj in self.glossary_terms))
        }

def main():
    """Main function to demonstrate usage."""
    # Initialize the enhanced linker
    linker = EnhancedInternalLinker()
    
    # Show statistics
    stats = linker.get_statistics()
    print("=== GLOSSARY STATISTICS ===")
    print(f"Total terms: {stats['total_terms']}")
    print(f"Total aliases: {stats['total_aliases']}")
    print(f"Unique URLs: {stats['unique_urls']}")
    print(f"Categories: {len(stats['categories'])}")
    
    print("\n=== CATEGORIES ===")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: {count} terms")
    
    # Process an example article
    print("\n=== PROCESSING EXAMPLE ARTICLE ===")
    result = linker.process_article('Articles/policy-mix')
    
    if result:
        print(f"Article: {result['article_file']}")
        print(f"Total matches: {result['total_matches']}")
        print(f"Unique terms: {len(result['unique_terms'])}")
        
        print("\nMatches by category:")
        for category, matches in result['matches_by_category'].items():
            print(f"\n{category} ({len(matches)} matches):")
            for match in matches[:3]:  # Show first 3 matches
                print(f"  - '{match['term']}' -> {match['url']}")
                print(f"    Context: ...{match['context']}...")
    
    # Demonstrate link limiting
    print("\n=== LINK LIMITING DEMO ===")
    print("Creating HTML with 12-link limit...")
    html = linker.create_html_links('Articles/policy-mix', 'demo-12-links.html', max_links=12)
    print("✅ Demo completed! Check demo-12-links.html")

if __name__ == "__main__":
    main() 