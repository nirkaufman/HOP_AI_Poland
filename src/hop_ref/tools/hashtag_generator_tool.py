"""
Hashtag Generator Tool - Creates strategic hashtag recommendations for LinkedIn.
Balances broad trending tags with niche audience-specific tags.
"""

from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import re


class HashtagGeneratorInput(BaseModel):
    topic: str = Field(..., description="The main topic of the content")
    audience: str = Field(..., description="The target audience")
    max_tags: int = Field(default=7, description="Maximum number of hashtags (5-10 recommended)")


class HashtagGeneratorTool(BaseTool):
    name: str = "Hashtag Generator Tool"
    description: str = (
        "Generates strategic hashtag recommendations for LinkedIn posts. "
        "Balances broad trending tags with niche audience-specific tags."
    )
    args_schema: Type[BaseModel] = HashtagGeneratorInput

    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'they', 'have', 'will'}
        return list(set(w for w in words if w not in stop_words))[:10]

    def _generate_hashtags(self, topic: str, audience: str, max_tags: int) -> List[str]:
        topic_keywords = self._extract_keywords(topic)
        audience_keywords = self._extract_keywords(audience)

        broad_tags = [
            "#Leadership", "#TechLeadership", "#SoftwareEngineering",
            "#CareerGrowth", "#ProfessionalDevelopment", "#Technology"
        ]

        topic_tags = [f"#{kw.capitalize()}" for kw in topic_keywords[:3]]
        audience_tags = [f"#{kw.capitalize()}" for kw in audience_keywords[:2]]
        engagement_tags = ["#ThoughtLeadership", "#BestPractices"]

        # Combine: 2 broad + 3 topic + 1 audience + 1 engagement
        hashtags = broad_tags[:2] + topic_tags[:3] + audience_tags[:1] + engagement_tags[:1]

        # Remove duplicates
        seen = set()
        unique = []
        for tag in hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique.append(tag)

        return unique[:max_tags]

    def _run(self, topic: str, audience: str, max_tags: int = 7) -> str:
        hashtags = self._generate_hashtags(topic, audience, max_tags)

        return f"""
# Hashtag Recommendations ({len(hashtags)} tags)

{' '.join(hashtags)}

## Strategy:
- **Broad** (2): High reach, larger conversations
- **Topic** (2-3): Medium reach, high relevance
- **Audience** (1): Targeted reach
- **Engagement** (1): Drives interaction

## Usage:
- Add at END of post (after CTA)
- 5-7 tags optimal, 10 max
- First 3 hashtags most important
- Mix broad (100K+ followers) + niche (10K-50K)

**Expected reach increase: +30-50%**
""".strip()
