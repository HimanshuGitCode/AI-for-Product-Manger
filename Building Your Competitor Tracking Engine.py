import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import datetime
import hashlib
import json

class CompetitorTracker:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)
        self.history = {}
        
    def track_website(self, url, selectors):
        """
        Track specific sections of competitor websites
        selectors: dict with keys like 'pricing', 'features', etc.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            changes = {}
            for section, selector in selectors.items():
                content = soup.select_one(selector)
                if content:
                    current_hash = self._get_hash(content.text)
                    
                    # Check if we have a previous version
                    if url in self.history and section in self.history[url]:
                        if current_hash != self.history[url][section]['hash']:
                            # Content changed - analyze with AI
                            changes[section] = self._analyze_change(
                                self.history[url][section]['content'],
                                content.text
                            )
                    
                    # Update history
                    self.history.setdefault(url, {})
                    self.history[url][section] = {
                        'hash': current_hash,
                        'content': content.text,
                        'last_checked': datetime.now().isoformat()
                    }
            
            return changes
        
        except Exception as e:
            return {'error': str(e)}
    
    def _get_hash(self, content):
        return hashlib.md5(content.encode()).hexdigest()
    
    def _analyze_change(self, old_content, new_content):
        """Analyze changes using GPT-4"""
        prompt = f"""
        Compare these two versions of content and explain key changes:
        
        Old version:
        {old_content}
        
        New version:
        {new_content}
        
        Focus on:
        1. Major feature changes
        2. Pricing changes
        3. Positioning changes
        4. Potential strategic implications
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a competitive intelligence analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
