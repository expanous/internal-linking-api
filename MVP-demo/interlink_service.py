import re
import spacy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from typing import List, Dict, Set, Tuple, Optional
import unicodedata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InterlinkService:
    """
    A service that intelligently inserts interlinks into HTML content based on
    a provided list of target pages and their associated terms.
    """
    
    def __init__(self, nlp_model: str = "en_core_web_sm"):
        """
        Initialize the InterlinkService with spaCy NLP model.
        
        Args:
            nlp_model: spaCy model name to use for tokenization and lemmatization
        """
        try:
            self.nlp = spacy.load(nlp_model)
            logger.info(f"Loaded spaCy model: {nlp_model}")
        except OSError:
            logger.warning(f"spaCy model {nlp_model} not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", nlp_model])
            self.nlp = spacy.load(nlp_model)
        
        # Elements where we want to insert links
        self.linkable_elements = {
            'p', 'li', 'td', 'div', 'span', 'article', 'section', 
            'blockquote', 'figcaption', 'caption'
        }
        
        # Elements where we don't want to insert links
        self.excluded_elements = {
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'script', 'style',
            'nav', 'header', 'footer', 'aside'
        }
    
    def extract_terms_from_url(self, url: str) -> List[str]:
        """
        Extract potential terms from a URL path, including multi-word phrases and key single words.
        """
        # Common English stop words to exclude
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
            'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
            'or', 'but', 'not', 'what', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
        }
        
        # Important financial acronyms and short terms to whitelist
        financial_acronyms = {
            'etf', 'ipo', 'cfd', 'mt4', 'mt5', 'api', 'otc', 'dax', 'gtd', 'pip', 'net',
            'gdp', 'g20', 'g10', 'bbb', 'ccc', 'sec', 'roe', 'npl', 'peg', 'imf', 'bep',
            'ism', 'emv', 'xpo', 'amm', 'dma', 'ddu', 'grs', 'irs', 'vix', 'dow', 'vif',
            'xva', 'etp', 'fis', 'tsx', 'cac', 'sse', 'jse', 'lbs', 'omx', 'del', 'cum',
            'mix', 'put', 'buy', 'out', 'low', 'mid', 'tax', 'for', 'all', 'off', 'tri',
            'non', 'per', 'bar', 'kse', 'pse', 'ups', 'a50', '100', '225', '200', '500',
            'web', 'app', 'key', 'top', 'are', 'usd', 'eur', 'aud', 'jpy', 'cad', 'gbp',
            'chf', 'nzd', 'amd', 'tui', 'arm', 'sui', 'neo', 'inu', 'lot', 'oil', 'nio',
            'fee', 'how', 'our', 'why', 'day', 'sar', 'esg', 'ppp', 'web3', 'croci',
            'comex', 'opec', 'node', 'vwap', 'ebitda', 'ebid', 'moneyness', 'paydown',
            'layering', 'delta', 'staking', 'sampling', 'stagflation', 'sell', 'year',
            'cost', 'risk', 'time', 'fund', 'bond', 'swap', 'call', 'put', 'buy', 'sell'
        }
        
        parsed = urlparse(url)
        path = parsed.path.lower()
        terms = set()
        segments = path.split('/')
        for segment in segments:
            if segment and segment not in ['en-int', 'learn', 'glossary', 'market-guides']:
                # Remove common suffixes
                clean_segment = re.sub(r'-(definition|guide|trading|funds?|market|what|is|the|of|a|an)$', '', segment)
                # Add full phrase (hyphens/underscores to spaces)
                if '-' in clean_segment or '_' in clean_segment:
                    phrase = clean_segment.replace('-', ' ').replace('_', ' ')
                    if 2 <= len(phrase.split()) <= 4:
                        terms.add(phrase)
                # Add all 1-4 word n-grams from the segment
                words = re.split(r'[-_]', clean_segment)
                for n in range(1, min(5, len(words)+1)):
                    for i in range(len(words)-n+1):
                        ngram = ' '.join(words[i:i+n])
                        if len(ngram) > 2:
                            # Filter out stop words unless they're financial acronyms
                            if len(ngram) <= 3:
                                # For short terms (3 chars or less), only include if they're financial acronyms
                                if ngram.lower() in financial_acronyms:
                                    terms.add(ngram)
                            else:
                                # For longer terms, exclude if they're stop words
                                if ngram.lower() not in stop_words:
                                    terms.add(ngram)
        return list(terms)
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison (lowercase, remove extra whitespace).
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())
        return text
    
    def lemmatize_text(self, text: str) -> str:
        """
        Lemmatize text using spaCy.
        
        Args:
            text: Input text
            
        Returns:
            Lemmatized text
        """
        doc = self.nlp(text)
        return ' '.join([token.lemma_ for token in doc])
    
    def find_matching_terms(self, text: str, target_terms: List[str]) -> List[Tuple[str, str, int]]:
        """
        Find matching terms in text with their original form and position.
        
        Args:
            text: Text to search in
            target_terms: List of target terms to match
            
        Returns:
            List of tuples (original_text, target_term, position)
        """
        matches = []
        normalized_text = self.normalize_text(text)
        lemmatized_text = self.lemmatize_text(normalized_text)
        
        for target_term in target_terms:
            # Normalize and lemmatize target term
            normalized_target = self.normalize_text(target_term)
            lemmatized_target = self.lemmatize_text(normalized_target)
            
            # Find all occurrences
            pattern = re.escape(lemmatized_target)
            for match in re.finditer(pattern, lemmatized_text):
                start, end = match.span()
                
                # Get the original text at this position
                original_text = text[start:end]
                
                # Skip if already matched or too short
                if len(original_text) < 3:
                    continue
                
                matches.append((original_text, target_term, start))
        
        return matches
    
    def is_valid_link_location(self, element) -> bool:
        """
        Check if an element is a valid location for inserting links.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            True if valid location, False otherwise
        """
        # Check if element is in excluded elements
        if element.name in self.excluded_elements:
            return False
        
        # Check if element is inside an excluded element
        for parent in element.parents:
            if parent.name in self.excluded_elements:
                return False
        
        # Check if element is inside a link
        for parent in element.parents:
            if parent.name == 'a':
                return False
        
        return True
    
    def should_insert_link(self, element, current_page_url: str, target_url: str) -> bool:
        """
        Check if we should insert a link at this location.
        
        Args:
            element: BeautifulSoup element
            current_page_url: URL of the current page
            target_url: URL of the target page
            
        Returns:
            True if link should be inserted, False otherwise
        """
        # Don't link to the current page
        if current_page_url and target_url:
            current_domain = urlparse(current_page_url).netloc
            target_domain = urlparse(target_url).netloc
            if current_domain == target_domain:
                current_path = urlparse(current_page_url).path
                target_path = urlparse(target_url).path
                if current_path == target_path:
                    return False
        
        return True
    
    def _prepare_target_phrases(self, target_terms: List[str]):
        """
        Prepare a list of (lemmas, original, length) for each target term/phrase.
        Returns a list of dicts with keys: 'lemmas', 'original', 'length'.
        """
        prepared = []
        for term in target_terms:
            doc = self.nlp(term)
            lemmas = tuple(token.lemma_.lower() for token in doc)
            prepared.append({
                'lemmas': lemmas,
                'original': term,
                'length': len(lemmas)
            })
        # Sort by length descending so longer phrases are matched first
        prepared.sort(key=lambda x: -x['length'])
        return prepared

    def _find_phrase_matches(self, doc, prepared_phrases, used_terms):
        """
        Find the first match for each phrase in the doc, skipping already used terms.
        Returns a list of dicts: {start, end, text, phrase, length}
        """
        matches = []
        token_lemmas = [token.lemma_.lower() for token in doc]
        
        # Sort phrases by length (longest first) to prioritize longer matches
        sorted_phrases = sorted(prepared_phrases, key=lambda x: -x['length'])
        
        for phrase in sorted_phrases:
            if phrase['original'] in used_terms:
                continue
            n = phrase['length']
            for i in range(len(token_lemmas) - n + 1):
                if tuple(token_lemmas[i:i+n]) == phrase['lemmas']:
                    # Only match if at word boundaries
                    start_char = doc[i].idx
                    end_char = doc[i+n-1].idx + len(doc[i+n-1])
                    
                    # Check if this match overlaps with any existing match
                    overlaps = False
                    for existing_match in matches:
                        if (start_char < existing_match['end'] and end_char > existing_match['start']):
                            overlaps = True
                            break
                    
                    if not overlaps:
                        matches.append({
                            'start': start_char,
                            'end': end_char,
                            'text': doc.text[start_char:end_char],
                            'phrase': phrase['original'],
                            'length': n
                        })
                        break  # Only first occurrence per phrase
        return matches

    def _select_non_overlapping_matches(self, matches):
        """
        Given a list of matches (with start, end, length), select the maximal set of non-overlapping matches,
        preferring longer matches and earlier positions.
        """
        # Sort by -length, start (longest matches first, then earliest position)
        matches = sorted(matches, key=lambda m: (-m['length'], m['start']))
        selected = []
        occupied = set()
        
        for m in matches:
            rng = set(range(m['start'], m['end']))
            if occupied & rng:
                continue
            selected.append(m)
            occupied.update(rng)
        
        # Sort back by start position for replacement
        selected.sort(key=lambda m: m['start'])
        return selected

    def process_html(self, html_content: str, target_entries: List[Dict], current_page_url: str = "") -> str:
        if not html_content or not target_entries:
            return html_content
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract terms from target URLs
        target_terms_map = {}
        for entry in target_entries:
            url = entry.get('url', '')
            if url:
                terms = self.extract_terms_from_url(url)
                for term in terms:
                    if term not in target_terms_map:
                        target_terms_map[term] = url
        if not target_terms_map:
            logger.warning("No valid terms found in target entries")
            return html_content
        
        prepared_phrases = self._prepare_target_phrases(list(target_terms_map.keys()))
        used_terms = set()
        used_urls = set()
        
        # Process each text node in order, updating used_terms as we go
        for element in soup.find_all(text=True):
            if not self.is_valid_link_location(element.parent):
                continue
            text = str(element)
            if not text.strip():
                continue
            # Only consider terms not already used
            filtered_phrases = [p for p in prepared_phrases if p['original'] not in used_terms and target_terms_map[p['original']] not in used_urls]
            if not filtered_phrases:
                continue
            doc = self.nlp(text)
            matches = self._find_phrase_matches(doc, filtered_phrases, set())
            if not matches:
                continue
            # Select non-overlapping, longest matches for this node
            node_matches = self._select_non_overlapping_matches(matches)
            if not node_matches:
                continue
            # Build new nodes
            new_nodes = []
            last_idx = 0
            for match in node_matches:
                # Add text before match
                if match['start'] > last_idx:
                    new_nodes.append(text[last_idx:match['start']])
                target_url = target_terms_map[match['phrase']]
                anchor_tag = soup.new_tag('a', href=target_url)
                anchor_tag.string = text[match['start']:match['end']]
                new_nodes.append(anchor_tag)
                last_idx = match['end']
                # Mark term and URL as used globally
                used_terms.add(match['phrase'])
                used_urls.add(target_url)
            # Add remaining text
            if last_idx < len(text):
                new_nodes.append(text[last_idx:])
            element.replace_with(*new_nodes)
        return str(soup)
    
    def process_html_with_glossary(self, html_content: str, glossary_entries: List[Dict], current_page_url: str = "") -> str:
        """
        Alternative method that accepts glossary entries with explicit terms.
        
        Args:
            html_content: HTML string to process
            glossary_entries: List of glossary entries with 'term' and 'url' keys
            current_page_url: URL of the current page (optional)
            
        Returns:
            Updated HTML string with interlinks
        """
        if not html_content or not glossary_entries:
            return html_content
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Create target terms map
        target_terms_map = {}
        for entry in glossary_entries:
            term = entry.get('term', '')
            url = entry.get('url', '')
            if term and url:
                target_terms_map[term.lower()] = url
        
        if not target_terms_map:
            logger.warning("No valid terms found in glossary entries")
            return html_content
        
        # Track used terms to avoid duplicates
        used_terms = set()
        
        # Process text nodes
        for element in soup.find_all(text=True):
            if not self.is_valid_link_location(element.parent):
                continue
            
            text = str(element)
            if not text.strip():
                continue
            
            # Find matches in this text node
            matches = self.find_matching_terms(text, list(target_terms_map.keys()))
            
            # Sort matches by position (reverse to avoid index shifting)
            matches.sort(key=lambda x: x[2], reverse=True)
            
            for original_text, target_term, position in matches:
                target_url = target_terms_map[target_term]
                
                # Skip if term already used or shouldn't link
                if target_term in used_terms:
                    continue
                
                if not self.should_insert_link(element.parent, current_page_url, target_url):
                    continue
                
                # Create link element
                link_tag = soup.new_tag('a', href=target_url)
                link_tag.string = original_text
                
                # Replace text with link
                before_text = text[:position]
                after_text = text[position + len(original_text):]
                
                # Create new text nodes and link
                new_nodes = []
                if before_text:
                    new_nodes.append(soup.new_string(before_text))
                new_nodes.append(link_tag)
                if after_text:
                    new_nodes.append(soup.new_string(after_text))
                
                # Replace the original text node
                element.replace_with(*new_nodes)
                
                # Mark term as used
                used_terms.add(target_term)
                
                # After replacement, break to avoid further replacements on this node
                break
        
        return str(soup)


# Example usage and testing
def main():
    """Example usage of the InterlinkService."""
    
    # Initialize service
    service = InterlinkService()
    
    # Example HTML content
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
    
    # Example target entries
    target_entries = [
        {"url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
        {"url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
        {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"},
        {"url": "https://capital.com/en-int/learn/market-guides/algo-trading"}
    ]
    
    # Process HTML
    result = service.process_html(html_content, target_entries, "https://capital.com/en-int/learn/financial-markets")
    
    print("Original HTML:")
    print(html_content)
    print("\n" + "="*50 + "\n")
    print("Processed HTML:")
    print(result)


if __name__ == "__main__":
    main() 