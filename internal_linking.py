import yaml
import spacy
import re
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Set
import os

class InternalLinker:
    def __init__(self, urls_file: str = 'urls.yaml'):
        """
        Initialize the InternalLinker with URLs from YAML file.
        
        Args:
            urls_file: Path to the YAML file containing URLs
        """
        self.urls_file = urls_file
        self.nlp = spacy.load("en_core_web_sm")
        self.glossary_terms = self._extract_glossary_terms()
        
    def _extract_glossary_terms(self) -> Dict[str, str]:
        """
        Extract glossary terms from URLs and create a mapping of term -> URL.
        
        Returns:
            Dictionary mapping glossary terms to their URLs
        """
        with open(self.urls_file, 'r') as f:
            urls = yaml.safe_load(f)
        
        glossary_terms = {}
        
        for url in urls:
            # Parse URL to extract the term
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Look for glossary terms (usually in /learn/glossary/term-definition format)
            if 'glossary' in path_parts:
                # Find the term part (before '-definition')
                for part in path_parts:
                    if part.endswith('-definition'):
                        term = part.replace('-definition', '')
                        # Convert hyphens to spaces for better matching
                        term_clean = term.replace('-', ' ')
                        glossary_terms[term_clean] = url
                        break
        
        return glossary_terms
    
    def _preprocess_text(self, text: str) -> spacy.tokens.Doc:
        """
        Preprocess text using spaCy for lemmatization.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            spaCy Doc object
        """
        return self.nlp(text.lower())
    
    def _get_term_variations(self, term: str) -> Set[str]:
        """
        Get various forms of a term for matching (original, lemmatized, etc.).
        
        Args:
            term: Original term
            
        Returns:
            Set of term variations
        """
        variations = {term.lower()}
        
        # Add lemmatized version
        doc = self.nlp(term.lower())
        lemmatized = ' '.join([token.lemma_ for token in doc])
        variations.add(lemmatized)
        
        # Add singular/plural variations
        if term.endswith('s'):
            variations.add(term[:-1].lower())  # Remove 's'
        else:
            variations.add(term + 's')  # Add 's'
        
        return variations
    
    def _is_partial_match(self, term: str, text: str, start: int, end: int) -> bool:
        """
        Check if a match is a partial word match that should be avoided.
        
        Args:
            term: The matched term
            text: Full text
            start: Start position of match
            end: End position of match
            
        Returns:
            True if it's a partial match to avoid
        """
        # Check if the match is surrounded by word boundaries
        if start > 0 and text[start-1].isalnum():
            return True
        if end < len(text) and text[end].isalnum():
            return True
        return False
    
    def _extract_context(self, text: str, start: int, end: int, context_chars: int = 150) -> str:
        """
        Extract context around a match, trying to get full sentences when possible.
        
        Args:
            text: Full text
            start: Start position of match
            end: End position of match
            context_chars: Number of characters to include before and after the match
            
        Returns:
            Context string with the matched term in context
        """
        # Calculate context boundaries
        context_start = max(0, start - context_chars)
        context_end = min(len(text), end + context_chars)
        
        # Extract context
        context = text[context_start:context_end]
        
        # Try to start at a sentence boundary
        if context_start > 0:
            # Look for sentence endings before our context start
            sentence_endings = ['. ', '! ', '? ', '\n\n']
            best_start = context_start
            
            for ending in sentence_endings:
                pos = text.rfind(ending, max(0, context_start - 200), context_start)
                if pos > 0 and pos > best_start - 200:  # Within reasonable range
                    best_start = pos + len(ending)
                    break
            
            if best_start < context_start:
                context = text[best_start:context_end]
        
        # Try to end at a sentence boundary
        if context_end < len(text):
            # Look for sentence endings after our context end
            sentence_endings = ['. ', '! ', '? ', '\n\n']
            best_end = context_end
            
            for ending in sentence_endings:
                pos = text.find(ending, context_end, min(len(text), context_end + 200))
                if pos > 0 and pos < best_end + 200:  # Within reasonable range
                    best_end = pos + len(ending)
                    break
            
            if best_end > context_end:
                context = text[context_start:best_end]
        
        # Clean up the context
        context = context.strip()
        
        # Add ellipsis if we're not at the beginning/end of the text
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context = context + "..."
            
        return context
    
    def _find_matches(self, article_text: str, glossary_terms: Dict[str, str]) -> List[Tuple[str, str, int, int]]:
        """
        Find matches between glossary terms and article text.
        
        Args:
            article_text: The article text to search in
            glossary_terms: Dictionary of terms to their URLs
            
        Returns:
            List of tuples (term, url, start_pos, end_pos)
        """
        matches = []
        used_positions = set()
        used_terms = set()  # Track which terms have been used
        
        # Sort terms by length (longest first) to avoid partial matches
        sorted_terms = sorted(glossary_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for term, url in sorted_terms:
            # Skip if this term has already been used
            if term in used_terms:
                continue
                
            term_variations = self._get_term_variations(term)
            
            for variation in term_variations:
                # Find all occurrences of this variation
                pattern = re.compile(r'\b' + re.escape(variation) + r'\b', re.IGNORECASE)
                
                for match in pattern.finditer(article_text):
                    start, end = match.span()
                    
                    # Check if this position overlaps with already used positions
                    if any(start < used_end and end > used_start 
                           for used_start, used_end in used_positions):
                        continue
                    
                    # Check if it's a partial match
                    if self._is_partial_match(variation, article_text, start, end):
                        continue
                    
                    # Add to matches and mark position as used
                    matches.append((term, url, start, end))
                    used_positions.add((start, end))
                    used_terms.add(term)  # Mark this term as used
                    break  # Only use the first occurrence of each term
        
        # Sort matches by position in text
        matches.sort(key=lambda x: x[2])
        return matches
    
    def process_article(self, article_file: str) -> Dict[str, any]:
        """
        Process an article file and find internal linking opportunities.
        
        Args:
            article_file: Path to the article file
            
        Returns:
            Dictionary with 'matches' key containing list of (term, url) tuples
        """
        # Read article content
        with open(article_file, 'r', encoding='utf-8') as f:
            article_text = f.read()
        
        # Find matches
        matches = self._find_matches(article_text, self.glossary_terms)
        
        # Create detailed matches with context
        detailed_matches = []
        for term, url, start, end in matches:
            context = self._extract_context(article_text, start, end)
            detailed_matches.append({
                'matched_phrase': term,
                'context': context,
                'target_page': url
            })
        
        # Return results
        result = {
            'article_file': article_file,
            'total_matches': len(matches),
            'matches': [(term, url) for term, url, _, _ in matches],
            'detailed_matches': detailed_matches
        }
        
        return result
    
    def get_unique_matches(self, article_file: str) -> List[Tuple[str, str]]:
        """
        Get unique matches for an article (no duplicates).
        
        Args:
            article_file: Path to the article file
            
        Returns:
            List of unique (term, url) tuples
        """
        result = self.process_article(article_file)
        return result['matches']
    
    def get_detailed_matches(self, article_file: str) -> List[Dict[str, str]]:
        """
        Get detailed matches with context for an article.
        
        Args:
            article_file: Path to the article file
            
        Returns:
            List of dictionaries with 'matched_phrase', 'context', and 'target_page' keys
        """
        result = self.process_article(article_file)
        return result['detailed_matches']
    
    def create_html_links(self, article_file: str, output_file: str = None) -> str:
        """
        Create HTML version of article with internal links.
        
        Args:
            article_file: Path to the article file
            output_file: Optional output file path
            
        Returns:
            HTML content with links
        """
        # Read article content
        with open(article_file, 'r', encoding='utf-8') as f:
            article_text = f.read()
        
        # Find matches
        matches = self._find_matches(article_text, self.glossary_terms)
        
        # Sort matches by position in reverse order to avoid index shifting
        matches.sort(key=lambda x: x[2], reverse=True)
        
        # Replace matches with HTML links
        for term, url, start, end in matches:
            original_text = article_text[start:end]
            html_link = f'<a href="{url}">{original_text}</a>'
            article_text = article_text[:start] + html_link + article_text[end:]
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(article_text)
        
        return article_text
    
    def process_all_articles(self, articles_dir: str = 'Articles') -> Dict[str, Dict]:
        """
        Process all articles in a directory.
        
        Args:
            articles_dir: Directory containing article files
            
        Returns:
            Dictionary mapping article files to their results
        """
        results = {}
        
        for filename in os.listdir(articles_dir):
            if os.path.isfile(os.path.join(articles_dir, filename)):
                article_path = os.path.join(articles_dir, filename)
                results[filename] = self.process_article(article_path)
        
        return results

def main():
    """Main function to demonstrate usage."""
    # Initialize the linker
    linker = InternalLinker()
    
    # Process all articles
    results = linker.process_all_articles()
    
    # Print results
    for article_name, result in results.items():
        print(f"\n=== {article_name} ===")
        print(f"Total matches found: {result['total_matches']}")
        
        if result['matches']:
            print("Matches:")
            for term, url in result['matches']:
                print(f"  - '{term}' -> {url}")
        else:
            print("No matches found.")
    
    # Example: Process a specific article with context
    print(f"\n=== Processing specific article with context ===")
    specific_result = linker.process_article('Articles/policy-mix')
    print(f"Article: {specific_result['article_file']}")
    print(f"Matches found: {specific_result['total_matches']}")
    
    for term, url in specific_result['matches']:
        print(f"  - '{term}' -> {url}")
    
    # Example: Get detailed matches with context
    print(f"\n=== Detailed matches with context for policy-mix ===")
    detailed_matches = linker.get_detailed_matches('Articles/policy-mix')
    print(f"Detailed matches found: {len(detailed_matches)}")
    
    for match in detailed_matches:
        print(f"- matched_phrase: {match['matched_phrase']}")
        print(f"- context: {match['context']}")
        print(f"- target_page: {match['target_page']}")
        print()
    
    # Example: Get unique matches only
    print(f"\n=== Unique matches for policy-mix ===")
    unique_matches = linker.get_unique_matches('Articles/policy-mix')
    print(f"Unique matches found: {len(unique_matches)}")
    
    for term, url in unique_matches:
        print(f"  - '{term}' -> {url}")

if __name__ == "__main__":
    main() 