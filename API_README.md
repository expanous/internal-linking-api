# Enhanced Internal Linking API

A FastAPI-based REST API for intelligent internal linking of financial articles using AI-powered glossary terms.

## Features

- 🧠 **AI-Powered Glossary**: 411 financial terms with 1,720 aliases across 123 categories
- 🔗 **Smart Internal Linking**: Automatically adds relevant internal links to articles
- 🚫 **Self-Link Prevention**: Avoids linking to the article's own URL
- 📊 **Link Limiting**: Configurable maximum links per article (default: 12)
- 📁 **File Upload Support**: Process articles via file upload or direct content
- 🔍 **Analysis Mode**: Analyze articles without creating links
- 📈 **Statistics**: Get detailed glossary and processing statistics

## Quick Start

### 1. Install Dependencies

```bash
pip install -r api_requirements.txt
```

### 2. Start the API Server

```bash
python3 api_internal_linking.py
```

The API will be available at `http://localhost:8000`

### 3. Access API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/health` | GET | Health check |
| `/stats` | GET | Get glossary statistics |
| `/categories` | GET | Get all available categories |
| `/terms/{category}` | GET | Get terms by category |

### Processing Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process` | POST | Process article content and return HTML with links |
| `/upload` | POST | Upload and process article file |
| `/analyze` | POST | Analyze article content without creating links |

## Usage Examples

### Process Article Content

```python
import requests

url = "http://localhost:8000/process"
payload = {
    "content": "<p>Revenue and ETFs are important financial concepts.</p>",
    "max_links": 5,
    "current_url": "https://capital.com//en-int/learn/glossary/revenue-definition"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Total links: {result['total_links']}")
print(f"New links added: {result['new_links_added']}")
print(f"HTML content: {result['html_content']}")
```

### Upload Article File

```python
import requests

url = "http://localhost:8000/upload"
files = {"file": open("article.html", "rb")}
params = {"max_links": 10}

response = requests.post(url, files=files, params=params)
result = response.json()
```

### Get Statistics

```python
import requests

response = requests.get("http://localhost:8000/stats")
stats = response.json()

print(f"Total terms: {stats['total_terms']}")
print(f"Total aliases: {stats['total_aliases']}")
print(f"Categories: {len(stats['categories'])}")
```

## Request/Response Models

### ArticleRequest
```json
{
    "content": "string",
    "max_links": 12,
    "current_url": "string (optional)"
}
```

### ArticleResponse
```json
{
    "html_content": "string",
    "total_links": 10,
    "existing_links": 3,
    "new_links_added": 7,
    "max_links": 12,
    "current_url": "string (optional)"
}
```

### StatisticsResponse
```json
{
    "total_terms": 411,
    "total_aliases": 1720,
    "unique_urls": 411,
    "categories": {
        "Finance": 55,
        "Investment": 33,
        "Trading": 23
    }
}
```

## Testing

Run the test client to verify API functionality:

```bash
python3 test_api_client.py
```

## Configuration

### Environment Variables

- `PORT`: API server port (default: 8000)
- `HOST`: API server host (default: 0.0.0.0)

### Glossary File

The API uses `glossary_terms.json` for the financial terms database. This file contains:
- 411 financial terms
- 1,720 aliases
- 123 categories
- URLs for each term

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request
- `500`: Internal server error

Error responses include detailed error messages:

```json
{
    "detail": "Error processing article: File not found"
}
```

## Performance

- **Processing Speed**: ~100ms per article
- **Memory Usage**: ~50MB (including glossary)
- **Concurrent Requests**: Supports multiple simultaneous requests

## Security Considerations

- Input validation on all endpoints
- Temporary file cleanup
- No persistent storage of uploaded content
- Rate limiting recommended for production use

## Production Deployment

For production deployment, consider:

1. **WSGI Server**: Use Gunicorn with Uvicorn workers
2. **Reverse Proxy**: Nginx for load balancing
3. **Rate Limiting**: Implement request rate limiting
4. **Monitoring**: Add health checks and metrics
5. **SSL/TLS**: Enable HTTPS

Example Gunicorn command:
```bash
gunicorn api_internal_linking:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the test client for usage examples
3. Check server logs for error details 