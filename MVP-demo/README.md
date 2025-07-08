# Interlink Service

A Python backend service that intelligently inserts interlinks into HTML content based on a provided list of glossary or target pages.

## Features

- **Intelligent Term Matching**: Case-insensitive and lemmatized matching using spaCy
- **Multi-word Expression Support**: Handles phrases up to 4 words
- **Smart Link Placement**: Only inserts links in appropriate content areas (p, li, div, etc.)
- **Duplicate Prevention**: Links only the first occurrence of each term per page
- **Exclusion Logic**: Avoids linking in headings, existing links, and navigation elements
- **URL-based Term Extraction**: Automatically extracts terms from target URLs
- **Semantic HTML Preservation**: Maintains original HTML structure and formatting

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy model** (if not already installed):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Quick Start

```python
from interlink_service import InterlinkService

# Initialize the service
service = InterlinkService()

# Your HTML content
html_content = """
<p>The global electronic marketplace is a major platform for investors to trade company stocks, bonds, exchange-traded funds (ETFs), commodities and other financial instruments.</p>
"""

# Target entries (URLs only)
target_entries = [
    {"url": "https://capital.com/en-int/learn/market-guides/what-is-share-trading"},
    {"url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
    {"url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"}
]

# Process the HTML
result = service.process_html(html_content, target_entries)

print(result)
```

## API Reference

### InterlinkService Class

#### Constructor
```python
InterlinkService(nlp_model: str = "en_core_web_sm")
```
- `nlp_model`: spaCy model name (default: "en_core_web_sm")

#### Methods

##### `process_html(html_content, target_entries, current_page_url="")`
Process HTML content and insert interlinks based on URL-extracted terms.

**Parameters:**
- `html_content` (str): HTML string to process
- `target_entries` (List[Dict]): List of dictionaries with "url" keys
- `current_page_url` (str, optional): Current page URL to avoid self-linking

**Returns:**
- `str`: Updated HTML string with interlinks

##### `process_html_with_glossary(html_content, glossary_entries, current_page_url="")`
Process HTML content using explicit glossary terms.

**Parameters:**
- `html_content` (str): HTML string to process
- `glossary_entries` (List[Dict]): List of dictionaries with "term" and "url" keys
- `current_page_url` (str, optional): Current page URL to avoid self-linking

**Returns:**
- `str`: Updated HTML string with interlinks

## Usage Examples

### Example 1: URL-based Term Extraction

```python
from interlink_service import InterlinkService

service = InterlinkService()

html_content = """
<html>
<body>
    <h1>Financial Markets Guide</h1>
    <p>Investors use ETFs to build diversified portfolios. Index funds provide broad market exposure.</p>
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
```

### Example 2: Explicit Glossary Terms

```python
glossary_entries = [
    {"term": "ETFs", "url": "https://capital.com/en-int/learn/market-guides/trade-etfs"},
    {"term": "portfolios", "url": "https://capital.com/en-int/learn/glossary/portfolio-definition"},
    {"term": "index funds", "url": "https://capital.com/en-int/learn/glossary/index-funds-definition"},
    {"term": "commodities", "url": "https://capital.com/en-int/learn/market-guides/what-is-commodity-trading"}
]

result = service.process_html_with_glossary(html_content, glossary_entries)
```

## Matching Logic

### Term Extraction from URLs
The service automatically extracts meaningful terms from target URLs:
- Removes common path segments (en-int, learn, glossary, etc.)
- Splits by hyphens and underscores
- Removes common suffixes (-definition, -guide, -trading, etc.)
- Supports both single words and multi-word phrases

### Matching Rules
- **Case-insensitive**: "ETFs", "etfs", "Etfs" all match
- **Lemmatized**: "portfolios" matches "portfolio"
- **Multi-word**: "index funds" matches "index funds"
- **First occurrence only**: Only the first instance of each term is linked
- **Excluded areas**: No links in headings, existing links, or navigation

### Valid Link Locations
Links are inserted in:
- `<p>`, `<li>`, `<td>`, `<div>`, `<span>`
- `<article>`, `<section>`, `<blockquote>`
- `<figcaption>`, `<caption>`

### Excluded Areas
Links are NOT inserted in:
- `<h1>` through `<h6>` (headings)
- `<a>` (existing links)
- `<script>`, `<style>` (code)
- `<nav>`, `<header>`, `<footer>`, `<aside>` (navigation/layout)

## Testing

Run the comprehensive test suite:

```bash
python test_interlink.py
```

The test suite covers:
- Basic functionality
- Glossary entries with explicit terms
- Excluded elements (headings, links)
- Duplicate prevention
- Case-insensitive matching
- Multi-word terms

## Output Example

**Input HTML:**
```html
<p>The global electronic marketplace is a major platform for investors to trade company stocks, bonds, exchange-traded funds (ETFs), commodities and other financial instruments.</p>
```

**Output HTML:**
```html
<p>The global electronic marketplace is a major platform for investors to trade company <a href="/en-int/learn/market-guides/what-is-share-trading">stocks</a>, bonds, exchange-traded funds (<a href="/en-int/learn/market-guides/trade-etfs">ETFs</a>), <a href="/en-int/learn/market-guides/what-is-commodity-trading">commodities</a> and other financial instruments.</p>
```

## Dependencies

- **beautifulsoup4**: HTML parsing and manipulation
- **spacy**: Natural language processing and lemmatization
- **lxml**: Fast XML/HTML parser backend for BeautifulSoup

## Performance Considerations

- The service uses spaCy for efficient NLP processing
- BeautifulSoup provides robust HTML parsing
- Term extraction is cached during processing
- Large HTML documents are processed efficiently

## Error Handling

- Graceful handling of malformed HTML
- Logging for debugging and monitoring
- Fallback behavior for missing spaCy models
- Validation of input parameters

## License

This project is provided as-is for educational and commercial use. 