import json
import numpy as np
from config import Config
from openai import OpenAI
import google.generativeai as genai
import anthropic

class AIService:
    def __init__(self):
        self.provider = Config.AI_PROVIDER.lower()
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize clients based on provider
        if self.provider == "openai":
            if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your_openai_api_key":
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY, base_url=Config.OPENAI_BASE_URL)
                
        elif self.provider == "gemini":
            if Config.GOOGLE_API_KEY and Config.GOOGLE_API_KEY != "your_google_api_key":
                genai.configure(api_key=Config.GOOGLE_API_KEY)
                
        elif self.provider == "claude":
            if Config.ANTHROPIC_API_KEY and Config.ANTHROPIC_API_KEY != "your_anthropic_api_key":
                self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def generate_embedding(self, text: str):
        try:
            if self.provider == "openai" and self.openai_client:
                response = self.openai_client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            
            elif self.provider == "gemini" and Config.GOOGLE_API_KEY:
                # Gemini text-embedding-004
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
                
            elif self.provider == "claude":
                # Claude doesn't have a direct embedding API yet (typically), 
                # often uses Voyage AI or similar. 
                # For simplicity, we might fallback to OpenAI or mock if pure Claude is requested.
                # However, for this demo, let's assume we fallback to mock or warn.
                # NOTE: Anthropic generally recommends external embedding providers.
                # We will return random for now to avoid crashing, or user needs to use OpenAI for embeddings.
                print("Warning: Claude provider selected but Anthropic has no native embedding API. Returning mock.")
                return np.random.rand(1536).tolist()
                
            else:
                return np.random.rand(1536).tolist()
                
        except Exception as e:
            print(f"Error generating embedding ({self.provider}): {e}")
            return np.random.rand(1536).tolist()

    def classify_and_tag(self, text: str):
        prompt = f"""
        Analyze the following text and provide a category and a list of tags.
        Output JSON format only: {{"category": "CategoryName", "tags": ["tag1", "tag2"]}}
        Text: {text[:1000]}
        """
        
        try:
            if self.provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
                return json.loads(content)
                
            elif self.provider == "gemini" and Config.GOOGLE_API_KEY:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                # Gemini often returns text with markdown code blocks
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)
                
            elif self.provider == "claude" and self.anthropic_client:
                message = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                # Extract text content
                content = message.content[0].text
                # Cleanup potential non-json
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
                return {"category": "Uncategorized", "tags": []}
                
            else:
                return {"category": "General", "tags": ["mock_tag"]}
                
        except Exception as e:
            print(f"Error classifying text ({self.provider}): {e}")
            return {"category": "Uncategorized", "tags": []}

    def cosine_similarity(self, v1, v2):
        if not v1 or not v2:
            return 0
        # Ensure vectors are same length (handle provider switch edge case)
        if len(v1) != len(v2):
            return 0
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search_similar(self, query_text: str, notes: list, top_k=10):
        if not query_text:
            return notes
        
        query_embedding = self.generate_embedding(query_text)
        
        scored_notes = []
        for note in notes:
            if note.embedding:
                score = self.cosine_similarity(query_embedding, note.embedding)
                scored_notes.append((score, note))
            else:
                scored_notes.append((0, note))
        
        scored_notes.sort(key=lambda x: x[0], reverse=True)
        return [note for score, note in scored_notes[:top_k]]
