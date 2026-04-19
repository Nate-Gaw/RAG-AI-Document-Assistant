from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "documents"

DOCS_DIR.mkdir(parents=True, exist_ok=True)


def write(name: str, content: str) -> None:
    (DOCS_DIR / name).write_text(content, encoding="utf-8")

write(
    "doc_small_1.txt",
    "The capital of France is Paris. It is known for the Eiffel Tower.",
)

write(
    "doc_small_2.txt",
    "Python is a programming language. It is used for data science, web development, and automation.",
)

write(
    "doc_medium_1.txt",
    "Air traffic control systems manage aircraft movement to ensure safety and efficiency. "
    "Controllers monitor aircraft positions and provide instructions. These systems reduce collision risk "
    "and improve traffic flow.",
)

write(
    "doc_medium_2.txt",
    "Basketball is a sport played between two teams of five players. The objective is to score points "
    "by shooting a ball through a hoop.",
)

write(
    "doc_medium_3.txt",
    "Apple is a fruit. Apple Inc. is a technology company.",
)

write(
    "doc_multi_1.txt",
    "New York is a city in the United States.",
)

write(
    "doc_multi_2.txt",
    "Tokyo is the capital of Japan.",
)

# Large document 1: climate change
climate_intro = (
    "Climate change is a long-term shift in global weather patterns. "
    "It is driven by a complex mix of natural variability and human activity. "
    "This report summarizes current observations, projections, and response options. "
)

climate_effects = (
    "Observed effects include rising sea levels, increasing temperatures, more frequent heat waves, "
    "and shifts in seasonal rainfall patterns. Coastal communities face erosion and flooding risks. "
    "Ecosystems respond to warmer oceans and changing habitats. "
)

climate_causes = (
    "Major causes include greenhouse gases from fossil fuel combustion, deforestation, and industrial processes. "
    "Carbon dioxide and methane trap heat and alter the energy balance of the planet. "
)

climate_mitigation = (
    "Mitigation strategies include renewable energy adoption, energy efficiency, electrified transport, "
    "and carbon capture. Policy and market incentives can accelerate these changes. "
)

climate_blocks = []
for i in range(1, 13):
    block = (
        f"Section {i}: "
        + climate_intro
        + climate_causes
        + climate_effects
        + climate_mitigation
        + "This section reviews data sources and regional impacts for planning and risk management. "
    )
    climate_blocks.append(block)

write("doc_large_1.txt", "\n\n".join(climate_blocks))

# Large document 2: technical doc with one latency mention
tech_intro = (
    "This technical report documents system design, throughput targets, and operational constraints. "
    "It includes architecture decisions, reliability expectations, and monitoring guidelines. "
)

tech_sections = []
for i in range(1, 15):
    section = (
        f"Module {i}: "
        + tech_intro
        + "The service uses redundant nodes and a queue-based workflow. "
        + "Metrics include throughput, error rate, and utilization across clusters. "
        + "Operators perform routine checks and capacity planning. "
    )
    tech_sections.append(section)

tech_sections.insert(
    8,
    "Performance Note: The system latency is 120 milliseconds under normal load. "
    "Latency spikes may occur during maintenance windows. ",
)

write("doc_large_2.txt", "\n\n".join(tech_sections))

# Large document 3: very large doc with buried answer
large_intro = (
    "This archival dossier covers multiple initiatives, timelines, and operational notes. "
    "It includes background context, stakeholder summaries, and execution details. "
)

large_blocks = []
for i in range(1, 40):
    large_blocks.append(
        f"Archive Section {i}: "
        + large_intro
        + "Each section records milestones, risks, and post-implementation reviews. "
        + "Data quality checks and governance notes are documented for auditing. "
    )

large_blocks.append(
    "Deep Section: The Orion program began in 2017 after approval by the steering committee. "
    "Subsequent phases focused on stabilization and long-term support."
)

for i in range(40, 80):
    large_blocks.append(
        f"Archive Section {i}: "
        + large_intro
        + "The narrative continues with operational retrospectives and cross-team collaboration details. "
        + "Recommendations and lessons learned are logged for future reference. "
    )

write("doc_large_3.txt", "\n\n".join(large_blocks))
