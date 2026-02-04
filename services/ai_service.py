import json
import numpy as np
from config import Config
from openai import OpenAI

class AIService:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if self.api_key and self.api_key != "your_openai_api_key":
            self.client = OpenAI(api_key=self.api_key, base_url=Config.OPENAI_BASE_URL)
        else:
            self.client = None

    def generate_embedding(self, text: str):
        if self.client:
            try:
                response = self.client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"Error generating embedding: {e}")
                # Fallback to random if error
                return np.random.rand(1536).tolist()
        else:
            # Mock embedding (random vector for demo)
            return np.random.rand(1536).tolist()

    def classify_and_tag(self, text: str):
        if self.client:
            try:
                prompt = f"""
                Analyze the following text and provide a category and a list of tags.
                Output JSON format only: {{"category": "CategoryName", "tags": ["tag1", "tag2"]}}
                Text: {text[:1000]}
                """
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
                return json.loads(content)
            except Exception as e:
                print(f"Error classifying text: {e}")
                return {"category": "Uncategorized", "tags": []}
        else:
            return {"category": "General", "tags": ["mock_tag"]}

    def cosine_similarity(self, v1, v2):
        if not v1 or not v2:
            return 0
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search_similar(self, query_text: str, notes: list, top_k=10):
        """
        notes: list of KnowledgeNote objects
        """
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
        
        # Sort by score desc
        scored_notes.sort(key=lambda x: x[0], reverse=True)
        
        # Return only the note objects, limited by top_k
        return [note for score, note in scored_notes[:top_k]]
