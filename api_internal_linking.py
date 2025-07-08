#!/usr/bin/env python3
"""
FastAPI-based API for Enhanced Internal Linking System
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import tempfile
import os
from enhanced_internal_linking import EnhancedInternalLinker

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Internal Linking API",
    description="API for intelligent internal linking of financial articles using AI-powered glossary",
    version="1.0.0"
)

# Initialize the linker
linker = EnhancedInternalLinker()

# Pydantic models for request/response
class ArticleRequest(BaseModel):
    content: str
    max_links: Optional[int] = 12
    current_url: Optional[str] = None

class ArticleResponse(BaseModel):
    html_content: str
    total_links: int
    existing_links: int
    new_links_added: int
    max_links: int
    current_url: Optional[str] = None

class ProcessingResult(BaseModel):
    article_file: str
    total_matches: int
    unique_terms: List[str]
    matches_by_category: Dict[str, List[Dict]]

class StatisticsResponse(BaseModel):
    total_terms: int
    total_aliases: int
    unique_urls: int
    categories: Dict[str, int]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Enhanced Internal Linking API",
        "version": "1.0.0",
        "endpoints": {
            "/docs": "API documentation",
            "/stats": "Get glossary statistics",
            "/process": "Process article content",
            "/upload": "Upload and process article file",
            "/categories": "Get all categories",
            "/terms/{category}": "Get terms by category"
        }
    }

@app.get("/stats", response_model=StatisticsResponse)
async def get_statistics():
    """Get glossary statistics"""
    try:
        stats = linker.get_statistics()
        return StatisticsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get all available categories"""
    try:
        categories = linker.get_categories()
        return {"categories": categories, "count": len(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")

@app.get("/terms/{category}")
async def get_terms_by_category(category: str):
    """Get all terms in a specific category"""
    try:
        terms = linker.get_terms_by_category(category)
        return {
            "category": category,
            "terms": terms,
            "count": len(terms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting terms: {str(e)}")

@app.post("/process", response_model=ArticleResponse)
async def process_article(request: ArticleRequest):
    """Process article content and return HTML with internal links"""
    try:
        # Create temporary file with content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            # Add current_url if provided
            if request.current_url:
                f.write(f'{{current_url = "{request.current_url}"}}\n')
            f.write(request.content)
            temp_file = f.name
        
        try:
            # Process the article
            html_content = linker.create_html_links(temp_file, max_links=request.max_links)
            
            # Count links in the result
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            total_links = len(soup.find_all('a'))
            
            # Count existing vs new links more accurately
            # Parse the original content without the current_url line
            original_content = request.content
            if request.current_url:
                # Remove the current_url line if it was added
                lines = original_content.split('\n')
                if lines and lines[0].strip().startswith('{current_url'):
                    original_content = '\n'.join(lines[1:])
            
            original_soup = BeautifulSoup(original_content, 'html.parser')
            existing_links = len(original_soup.find_all('a'))
            new_links_added = total_links - existing_links
            
            return ArticleResponse(
                html_content=html_content,
                total_links=total_links,
                existing_links=existing_links,
                new_links_added=new_links_added,
                max_links=request.max_links,
                current_url=request.current_url
            )
        finally:
            # Clean up temporary file
            os.unlink(temp_file)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing article: {str(e)}")

@app.post("/upload", response_model=ArticleResponse)
async def upload_and_process_article(
    file: UploadFile = File(...),
    max_links: int = 12
):
    """Upload and process an article file"""
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(content_str)
            temp_file = f.name
        
        try:
            # Process the article
            html_content = linker.create_html_links(temp_file, max_links=max_links)
            
            # Count links
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            total_links = len(soup.find_all('a'))
            
            original_soup = BeautifulSoup(content_str, 'html.parser')
            existing_links = len(original_soup.find_all('a'))
            new_links_added = total_links - existing_links
            
            return ArticleResponse(
                html_content=html_content,
                total_links=total_links,
                existing_links=existing_links,
                new_links_added=new_links_added,
                max_links=max_links
            )
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing uploaded file: {str(e)}")

@app.post("/analyze")
async def analyze_article(request: ArticleRequest):
    """Analyze article content without creating HTML links"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            if request.current_url:
                f.write(f'{{current_url = "{request.current_url}"}}\n')
            f.write(request.content)
            temp_file = f.name
        
        try:
            # Analyze the article
            result = linker.process_article(temp_file)
            # Convert to the expected format
            return {
                "article_file": result.get('article_file', ''),
                "total_matches": result.get('total_matches', 0),
                "unique_terms": result.get('unique_terms', []),
                "matches_by_category": result.get('matches_by_category', {})
            }
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing article: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test if the linker is working
        stats = linker.get_statistics()
        return {
            "status": "healthy",
            "glossary_loaded": stats['total_terms'] > 0,
            "total_terms": stats['total_terms']
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 