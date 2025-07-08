# Internal Linking Script

A Python script that performs basic internal linking for articles using lemmatized text matching with spaCy.

## Features

- **Lemmatized Text Matching**: Uses spaCy for NLP and lemmatization to find exact or lemmatized matches
- **Glossary Term Extraction**: Automatically extracts glossary terms from URLs in YAML format
- **Duplicate Prevention**: Ensures the same term isn't linked multiple times
- **Partial Word Protection**: Avoids partial word matches (e.g., "diversify" won't match "diversification")
- **HTML Link Generation**: Creates HTML versions with anchor tags
- **Case-Insensitive Matching**: Handles variations in capitalization

## Requirements

- Python 3.7+
- spaCy with English language model
- PyYAML

## Installation

1. Install required packages:
```bash
pip install spacy pyyaml
python -m spacy download en_core_web_sm
```

2. Ensure you have:
   - `urls.yaml` file with list of URLs
   - `Articles/` directory with article files

## Usage

### Basic Usage

```python
from internal_linking import InternalLinker

# Initialize the linker
linker = InternalLinker()

# Get unique matches for an article
matches = linker.get_unique_matches('Articles/policy-mix')
for term, url in matches:
    print(f"'{term}' -> {url}")

# Create HTML version with links
html_content = linker.create_html_links('Articles/policy-mix', 'output.html')
```

### Process All Articles

```python
# Process all articles in the Articles directory
results = linker.process_all_articles()

for article_name, result in results.items():
    print(f"{article_name}: {result['total_matches']} matches")
```

### Available Methods

- `get_unique_matches(article_file)`: Returns list of unique (term, url) tuples
- `process_article(article_file)`: Returns detailed results including total matches
- `create_html_links(article_file, output_file)`: Creates HTML version with anchor tags
- `process_all_articles(articles_dir)`: Processes all articles in a directory

## Input Format

### URLs File (`urls.yaml`)
```yaml
- https://capital.com/en-int/learn/glossary/term-definition
- https://capital.com/en-int/learn/glossary/another-term-definition
```

### Article Files
Plain text files in the `Articles/` directory.

## Output

The script returns matched phrases and their target URLs:

```
Found 10 unique matches:
  - 'policy mix' -> https://capital.com/en-int/learn/glossary/policy-mix-definition
  - 'economics' -> https://capital.com/en-int/learn/glossary/economics-definition
  - 'monetary policy' -> https://capital.com/en-int/learn/glossary/monetary-policy-definition
```

## Example Output

For the policy-mix article, the script finds matches like:
- "policy mix" → policy-mix-definition
- "economics" → economics-definition  
- "monetary policy" → monetary-policy-definition
- "interest rates" → interest-rates-definition
- "inflation" → inflation-definition

## HTML Output

The script can generate HTML with anchor tags:

```html
A <a href="https://capital.com/en-int/learn/glossary/policy-mix-definition">policy mix</a> refers to a combination of fiscal and monetary policies...
```

## Algorithm Details

1. **Term Extraction**: Extracts glossary terms from URLs ending with "-definition"
2. **Text Preprocessing**: Uses spaCy for lemmatization and normalization
3. **Variation Matching**: Handles singular/plural forms and lemmatized versions
4. **Position Tracking**: Ensures no overlapping matches
5. **First Occurrence Only**: Links only the first occurrence of each term

## Files

- `internal_linking.py`: Main script with InternalLinker class
- `example_usage.py`: Example usage demonstrations
- `extract_urls_to_yaml.py`: Script to convert XML sitemap to YAML
- `urls.yaml`: List of URLs (generated from sitemap)
- `Articles/`: Directory containing article files

## Running Examples

```bash
# Run the main script
python3 internal_linking.py

# Run example usage
python3 example_usage.py
``` 