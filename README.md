# LinkedIn Content Studio

A **Human-Oriented Programming (HOP)** crew powered by [crewAI](https://crewai.com) that transforms raw content ideas into high-engagement LinkedIn posts with document-carousel outlines.

## What It Does

This crew creates production-ready LinkedIn content in two formats:

1. **LinkedIn Post**: Hook → Body → CTA → Hashtags → Comment Prompt
2. **Carousel Outline**: 6-8 slide document outline (PDF-ready for LinkedIn)

## The HOP Approach

This project demonstrates **Human-Oriented Programming** principles:

- **Roles**: 4 specialized content agents with clear responsibilities
- **Goals**: Each agent has a specific success metric
- **Backstories**: Agents have personalities that influence their outputs
- **Process**: Sequential hand-offs for deterministic, observable workflow
- **Tools**: Custom tools that enhance agent capabilities

## Architecture

### 4 Specialized Agents

1. **Hook Crafter** - Creates compelling 1-2 line hooks
   - **Tool**: LinkedInResearchTool (analyzes successful hooks)
   - **Output**: 3 alternative hooks optimized for audience

2. **Value Builder** - Transforms ideas into actionable content
   - **Output**: 3-5 bullet points + concrete example

3. **Engagement Architect** - Adds CTAs and engagement elements
   - **Tool**: HashtagGeneratorTool (strategic hashtag recommendations)
   - **Output**: CTA + comment prompt + 5-7 hashtags

4. **Format Alchemist** - Creates carousel slide outlines
   - **Output**: 6-8 slide outline (max 25 words per slide)

### Custom Tools

#### 1. LinkedInResearchTool
**Purpose**: Research trending LinkedIn content and successful hook patterns

**Why It's Important**:
- Grounds content in real-world LinkedIn performance data
- Identifies successful hook patterns and engagement strategies
- Helps avoid generic content by learning from high-performing posts
- Increases relevance by understanding current trends

**How It Works**:
- Provides curated insights based on LinkedIn best practices
- Can integrate with SerperDev API for real-time LinkedIn post analysis (optional)
- Analyzes engagement patterns (likes, comments, shares)
- Returns strategic recommendations for hooks and content structure

**Used By**: Hook Crafter agent

#### 2. HashtagGeneratorTool
**Purpose**: Generate strategic hashtag recommendations for LinkedIn posts

**Why It's Important**:
- Hashtags increase post impressions by 30-50% on LinkedIn
- Balances trending vs niche hashtags for optimal reach + relevance
- Saves manual hashtag research time
- Ensures consistent hashtag strategy

**How It Works**:
- Analyzes topic keywords + audience profile
- Generates mix of broad (high reach) and niche (high relevance) tags
- Follows LinkedIn best practices (5-7 tags optimal)
- Provides strategy breakdown and usage tips

**Used By**: Engagement Architect agent

## Installation

### Prerequisites
- Python >=3.10 <3.14
- OpenAI API key (or other LLM provider)
- (Optional) SerperDev API key for enhanced LinkedIn research

### Setup

1. **Install dependencies**:
```bash
pip install uv
crewai install
```

Or using pip directly:
```bash
pip install -e .
```

2. **Configure environment**:
Add your API keys to `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For enhanced LinkedIn research
SERPER_API_KEY=your_serper_api_key_here
```

3. **Verify installation**:
```bash
hop_ref --help
```

## Usage

### Interactive Mode (Recommended)
```bash
hop_ref
```
You'll be prompted to enter:
- Topic: "How to turn code reviews into a team growth engine"
- Audience: "Senior engineers and EMs"

### Direct Input Mode
```bash
hop_ref --topic "AI agents in production" --audience "Tech leads and architects"
```

### With Verbose Output
```bash
hop_ref --verbose
```
Shows detailed agent reasoning, tool usage, and decision-making process.

### Custom Output Directory
```bash
hop_ref --output-dir ~/Desktop/linkedin_posts/
```

### All Options Combined
```bash
hop_ref \
  --topic "Building agentic workflows with crewAI" \
  --audience "Python developers and AI engineers" \
  --verbose \
  --output-dir ./my_posts/
```

## CLI Options

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--topic` | | Content topic | Interactive prompt |
| `--audience` | | Target audience | Interactive prompt |
| `--verbose` | `-v` | Show agent reasoning | `false` |
| `--output-dir` | `-o` | Output directory | `output/` |
| `--help` | `-h` | Show help | |

## Output Files

### Console Output
The complete LinkedIn post with:
- 3 hook options
- Selected hook + body content
- Concrete example
- CTA + comment prompt
- Strategic hashtags

### `output/carousel_outline.md`
Slide-by-slide carousel breakdown:
- Slide 1: Title/Promise
- Slides 2-7: Core content beats (1 idea per slide)
- Final slide: CTA

## Workflow

```
User Input (topic + audience)
        ↓
[Hook Crafter + LinkedInResearchTool]
    → Research successful hooks
    → Generate 3 options
        ↓
[Value Builder]
    → Choose best hook
    → Create 3-5 actionable points
    → Add concrete example
        ↓
[Engagement Architect + HashtagGeneratorTool]
    → Craft CTA
    → Create comment prompt
    → Generate strategic hashtags
        ↓
[Format Alchemist]
    → Transform into carousel outline
    → 6-8 slides (max 25 words each)
        ↓
Output: Post + Carousel Outline
```

## Project Structure

```
hop_ref/
├── src/hop_ref/
│   ├── crew.py                    # LinkedInContentStudio crew definition
│   ├── main.py                    # CLI entry point with Typer
│   ├── config/
│   │   ├── agents.yaml            # 4 agent definitions
│   │   └── tasks.yaml             # 4 task definitions
│   └── tools/
│       ├── linkedin_research_tool.py    # Custom LinkedIn research tool
│       ├── hashtag_generator_tool.py    # Custom hashtag generator
│       └── custom_tool.py               # Template for additional tools
├── output/                        # Generated content (carousel outlines)
├── .env                          # API keys and configuration
├── pyproject.toml                # Project dependencies
└── README.md                     # This file
```

## Customization

### Add More Tools

Create a new tool in `src/hop_ref/tools/`:

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    query: str = Field(..., description="Input description")

class MyCustomTool(BaseTool):
    name: str = "My Custom Tool"
    description: str = "What this tool does"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, query: str) -> str:
        # Tool logic here
        return result
```

Then assign it to an agent in `crew.py`:

```python
@agent
def my_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['my_agent'],
        tools=[MyCustomTool()]
    )
```

### Modify Agent Behavior

Edit `src/hop_ref/config/agents.yaml` to change:
- Role: Agent's responsibility
- Goal: Success criteria
- Backstory: Personality and approach

### Adjust Task Requirements

Edit `src/hop_ref/config/tasks.yaml` to modify:
- Description: Task instructions
- Expected output: Output format and requirements
- Agent: Which agent performs the task

## Why This Works on LinkedIn

Based on LinkedIn performance data:

1. **Hooks dominate**: First 2 lines visible before "see more" - 80% of users don't expand
2. **Document carousels perform**: Top content format for dwell time and saves
3. **Hashtags increase reach**: 30-50% more impressions with strategic tagging
4. **Engagement compounds**: Comments and interaction boost algorithmic visibility
5. **Consistency wins**: Regular cadence builds authority and reach

## Examples

### Example 1: Tech Leadership
```bash
hop_ref --topic "Async communication for distributed teams" \
        --audience "Engineering managers"
```

### Example 2: Career Growth
```bash
hop_ref --topic "From IC to Staff Engineer in 3 years" \
        --audience "Mid-level engineers"
```

### Example 3: Product Strategy
```bash
hop_ref --topic "User research that actually changes roadmaps" \
        --audience "Product managers and designers"
```

## Demo-Ready Features

- **Sequential process**: Easy to observe and explain
- **Verbose mode**: Shows agent reasoning for educational demos
- **Tool visibility**: Demonstrates how tools enhance agents
- **Multiple outputs**: Post + carousel for different content formats
- **CLI flexibility**: Interactive or flag-based for different audiences

## Extending the Crew

Future enhancement ideas:

1. **QA Agent**: Add a 5th agent to fact-check and enforce style
2. **Analytics Agent**: Ingest post performance data to suggest improvements
3. **Newsletter Variant**: Transform content into LinkedIn newsletter format
4. **PDF Export Tool**: Auto-generate PDF carousel from outline
5. **A/B Testing**: Generate multiple versions for testing
6. **Hierarchical Process**: Parallelize ideation and formatting at scale

## Troubleshooting

### Import Errors
Ensure you've installed the package:
```bash
pip install -e .
```

### API Key Issues
Check `.env` file has valid keys:
```bash
cat .env
```

### Output Not Generated
Run with `--verbose` to see where the process fails:
```bash
hop_ref --verbose
```

### Tool Not Working
LinkedInResearchTool works without SERPER_API_KEY (uses best practices).
Add the key for real-time LinkedIn data.

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

## License

This project is based on the crewAI framework and follows its licensing terms.

---

**Built with Human-Oriented Programming principles using crewAI**
