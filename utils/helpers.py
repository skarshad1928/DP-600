from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai.models import PromptBundle


DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]

# Every blueprint below maps 1:1 onto a numbered skill area of the official
# Microsoft Exam DP-600: Implementing Analytics Solutions Using Microsoft
# Fabric skills-measured outline (as of July 21, 2026). No skill area is
# treated as "extra" or optional -- all three carry their own weighting on
# the exam, matching the exam's own structure.
PRACTICE_BLUEPRINTS = {
    "maintain_solution": {
        "title": "Maintain a Data Analytics Solution",
        "summary": "Skill area 1 of DP-600 (25-30%): security, governance, and the analytics development lifecycle.",
        "section_name": "Maintain a Data Analytics Solution",
        "exam_weight": "25-30%",
        "prompt_attrs": ("maintain_solution_system_prompt", "maintain_solution_generate_prompt"),
        "topic_groups": {
            "Implement Security & Governance": [
                "Workspace-Level Access Controls",
                "Item-Level Access Controls",
                "Row-Level Security",
                "Column-Level Security",
                "Object-Level Security",
                "File-Level Access Control",
                "Sensitivity Labels on Items",
                "Endorsing Items (Promoted/Certified)",
            ],
            "Maintain the Analytics Development Lifecycle": [
                "Version Control for a Workspace",
                "Power BI Desktop Projects (.pbip)",
                "Deployment Pipelines",
                "Impact Analysis of Downstream Dependencies",
                "Deploying Semantic Models via the XMLA Endpoint",
                "Power BI Template Files (.pbit)",
                "Power BI Data Source Files (.pbids)",
                "Shared Semantic Models",
            ],
        },
        "default_patterns": [
            "DP-600 Core",
            "Scenario-Based Style",
            "Best-Practice Judgment Questions",
            "Conceptual Trap Questions",
        ],
    },
    "prepare_data": {
        "title": "Prepare Data",
        "summary": "Skill area 2 of DP-600 (45-50%): getting data, transforming it, and querying/analyzing it in Fabric.",
        "section_name": "Prepare Data",
        "exam_weight": "45-50%",
        "prompt_attrs": ("prepare_data_system_prompt", "prepare_data_generate_prompt"),
        "topic_groups": {
            "Get Data": [
                "Creating a Data Connection",
                "OneLake Catalog Discovery",
                "Real-Time Hub Discovery",
                "Ingesting or Accessing Data",
                "Choosing Between Data Stores",
                "OneLake Integration for Eventhouse",
                "OneLake Integration for Semantic Models",
            ],
            "Transform Data": [
                "Views, Functions & Stored Procedures",
                "Enriching Data with New Columns or Tables",
                "Star Schema for a Lakehouse or Warehouse",
                "Denormalizing Data",
                "Aggregating Data",
                "Merging or Joining Data",
                "Resolving Duplicate, Missing, or Null Data",
                "Converting Column Data Types",
                "Filtering Data",
            ],
            "Query & Analyze Data": [
                "Visual Query Editor",
                "SQL for Filtering & Aggregation",
                "KQL for Filtering & Aggregation",
                "DAX for Filtering & Aggregation",
            ],
        },
        "default_patterns": [
            "DP-600 Core",
            "Scenario-Based Style",
            "Query/Code Output Prediction",
            "Conceptual Trap Questions",
        ],
    },
    "semantic_models": {
        "title": "Implement & Manage Semantic Models",
        "summary": "Skill area 3 of DP-600 (25-30%): designing, building, and optimizing enterprise-scale semantic models.",
        "section_name": "Implement and Manage Semantic Models",
        "exam_weight": "25-30%",
        "prompt_attrs": ("semantic_models_system_prompt", "semantic_models_generate_prompt"),
        "topic_groups": {
            "Design & Build Semantic Models": [
                "Choosing a Storage Mode",
                "Star Schema for a Semantic Model",
                "Relationships & Bridge Tables",
                "Many-to-Many Relationships",
                "DAX Variables & Iterators",
                "Table Filtering Functions",
                "Windowing Functions",
                "Information Functions",
                "Calculation Groups",
                "Dynamic Format Strings",
                "Field Parameters",
                "Large Semantic Model Storage Format",
                "Composite Models",
            ],
            "Optimize Enterprise-Scale Semantic Models": [
                "Query & Report Visual Performance",
                "Improving DAX Performance",
                "Direct Lake Default Fallback Behavior",
                "Direct Lake Refresh Behavior",
                "Direct Lake on OneLake vs. SQL Analytics Endpoint",
                "Incremental Refresh for Semantic Models",
            ],
        },
        "default_patterns": [
            "DP-600 Core",
            "Scenario-Based Style",
            "DAX Deep-Dive Questions",
            "Conceptual Trap Questions",
        ],
    },
}

# Ordered list of section keys, matching the skills-measured outline's own
# numbering. Used anywhere the app needs to render all sections "in order".
SECTION_ORDER = [
    "maintain_solution",
    "prepare_data",
    "semantic_models",
]


def load_text_file(path: str | Path) -> str:
    with Path(path).open("r", encoding="utf-8") as handle:
        return handle.read().strip()


def load_json_file(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_parent_directory(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def get_prompt_bundle(settings, blueprint_key: str) -> "PromptBundle":
    from ai.models import PromptBundle

    blueprint = PRACTICE_BLUEPRINTS[blueprint_key]
    system_attr, generation_attr = blueprint["prompt_attrs"]
    return PromptBundle(
        system_prompt_path=str(getattr(settings, system_attr)),
        generation_prompt_path=str(getattr(settings, generation_attr)),
    )


def flatten_topics(topic_groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for topics in topic_groups.values():
        flattened.extend(topics)
    return flattened


def recommend_difficulty(
    accuracy: float,
    attempts: int,
    current_difficulty: str = "Medium",
) -> str:
    current = current_difficulty if current_difficulty in DIFFICULTY_ORDER else "Medium"
    index = DIFFICULTY_ORDER.index(current)
    if attempts < 3:
        return current
    if accuracy >= 80 and index < len(DIFFICULTY_ORDER) - 1:
        return DIFFICULTY_ORDER[index + 1]
    if accuracy < 50 and index > 0:
        return DIFFICULTY_ORDER[index - 1]
    return current


def build_recent_question_summaries(
    questions: list[dict[str, Any]],
    limit: int = 5,
) -> list[str]:
    summaries: list[str] = []
    for item in questions[:limit]:
        topic = item.get("topic", "Unknown Topic")
        subtopic = item.get("subtopic", "Unknown Subtopic")
        question = str(item.get("question", "")).strip().replace("\n", " ")
        short_question = question[:110] + ("..." if len(question) > 110 else "")
        summaries.append(f"{topic} / {subtopic}: {short_question}")
    return summaries


def summarize_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    total_attempts = len(attempts)
    correct_attempts = sum(1 for item in attempts if item.get("is_correct") is True)
    accuracy = round((correct_attempts / total_attempts) * 100, 2) if total_attempts else 0.0

    avg_time = 0.0
    if total_attempts:
        time_values = [int(item.get("time_taken_seconds") or 0) for item in attempts]
        avg_time = round(sum(time_values) / total_attempts, 2)

    topic_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"attempts": 0, "correct": 0, "time_taken_seconds": 0}
    )
    difficulty_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"attempts": 0, "correct": 0}
    )

    for item in attempts:
        topic = str(item.get("topic") or "Unknown")
        topic_stats[topic]["attempts"] += 1
        topic_stats[topic]["correct"] += 1 if item.get("is_correct") is True else 0
        topic_stats[topic]["time_taken_seconds"] += int(item.get("time_taken_seconds") or 0)

        difficulty = str(item.get("difficulty") or "Unknown")
        difficulty_stats[difficulty]["attempts"] += 1
        difficulty_stats[difficulty]["correct"] += 1 if item.get("is_correct") is True else 0

    topic_rows: list[dict[str, Any]] = []
    for topic, values in topic_stats.items():
        topic_attempts = values["attempts"]
        topic_accuracy = round((values["correct"] / topic_attempts) * 100, 2)
        topic_rows.append(
            {
                "topic": topic,
                "attempts": topic_attempts,
                "correct": values["correct"],
                "accuracy": topic_accuracy,
                "avg_time_seconds": round(values["time_taken_seconds"] / topic_attempts, 2),
            }
        )
    topic_rows.sort(key=lambda row: (-row["accuracy"], -row["attempts"], row["topic"]))

    difficulty_rows: list[dict[str, Any]] = []
    for difficulty, values in difficulty_stats.items():
        attempt_count = values["attempts"]
        difficulty_rows.append(
            {
                "difficulty": difficulty,
                "attempts": attempt_count,
                "accuracy": round((values["correct"] / attempt_count) * 100, 2),
            }
        )

    strong_topics = [
        row["topic"] for row in topic_rows if row["attempts"] >= 2 and row["accuracy"] >= 80
    ]
    weak_topics = [
        row["topic"] for row in topic_rows if row["attempts"] >= 2 and row["accuracy"] < 50
    ]

    return {
        "attempts": total_attempts,
        "correct": correct_attempts,
        "accuracy": accuracy,
        "average_time_seconds": avg_time,
        "topic_rows": topic_rows,
        "difficulty_rows": difficulty_rows,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
    }
