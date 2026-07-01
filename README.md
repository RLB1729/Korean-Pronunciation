# Korean Pronunciation Engine

A comprehensive Python library that converts Korean text into all valid standard pronunciations according to the official Korean Standard Pronunciation Rules (표준 발음법).

Unlike simple text-to-phoneme converters, this engine utilizes morphological analysis and a rule-based state machine to accurately handle edge cases, morpheme boundaries, and multiple valid pronunciation branches.

---

## Features

* **Generates all valid Korean pronunciations:** Capable of outputting multiple standard pronunciations for words that have acceptable variants (e.g., "선의" -> `[서늬, 서니]`).
* **Rule-based pronunciation engine:** Faithfully implements the official Korean pronunciation rules sequentially.
* **Morphological analysis:** Integrates with `kiwipiepy` to distinguish between grammatical particles and lexical stems, enabling context-aware rule application.
* **State branching strategy:** Employs Breadth-First Search (BFS) to safely branch and explore alternative pronunciations simultaneously.
* **Extensible architecture:** Rules are separated into modular components, making it easy to add or refine phonetic behaviors.
* **No strict dependencies:** Includes a built-in fallback morphological analyzer if external NLP libraries are not available.

---

## Table of Contents

- [Project Overview](#project-overview)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [Python API](#python-api)
- [Examples](#examples)
- [Pronunciation Rules](#pronunciation-rules)
- [Multiple Pronunciation Generation](#multiple-pronunciation-generation)
- [Internal Design](#internal-design)
- [Configuration](#configuration)
- [Testing](#testing)
- [Performance](#performance)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [FAQ](#faq)

---

## Project Overview

Korean pronunciation is heavily influenced by surrounding characters, morpheme boundaries, and grammatical context. Simple dictionary lookups or character-by-character replacements fail to capture phenomena like palatalization, liquidization, or complex double coda neutralization.

This project solves this by constructing an immutable representation of syllables and routing them through a predefined rule pipeline. It serves as a reliable tool for linguistic researchers, Korean language learners, and developers building text-to-speech (TTS) systems.

---

## How It Works

The engine processes input text through a systematic pipeline:

**Input**
↓
**Morphological Analysis:** The text is analyzed (using Kiwi or a fallback) to identify parts of speech (POS) and morpheme boundaries.
↓
**Tokenization & Hangul Decomposition:** Characters are decomposed into phonetic Jamo (Choseong, Jungseong, Jongseong) and wrapped in a rich `Syllable` object containing grammatical metadata.
↓
**Pronunciation Rule Engine (BFS):** The initial state is passed through a pipeline of 10 sequential rule groups.
↓
**State Branching:** If a rule allows multiple valid pronunciations (e.g., vowel alternatives or optional saisiot), the engine branches the state into multiple parallel realities.
↓
**Duplicate Removal:** At the end of each rule application, identical phonetic states are deduplicated using a canonical string key to prevent combinatorial explosion.
↓
**Output:** The final states are composed back into Hangul strings and returned along with the history of applied rules.

---

## Architecture

```text
       User Input
           │
           ▼
  Morphological Analyzer (Kiwi / Simple)
           │
           ▼
       Tokenizer (Decomposes to Jamo + Tags)
           │
           ▼
  Pronunciation Engine (BFS Evaluator)
           │
           ├── Vowel Rule
           ├── Sound Addition Rule
           ├── H-Rule
           ├── Liaison Rule
           ├── Palatalization Rule
           ├── Fortition Rule
           ├── Double Coda Rule
           ├── Neutralization Rule
           ├── Nasalization Rule
           └── Liquidization Rule
           │
           ▼
    Branched States (Deduplicated)
           │
           ▼
   Final Composed Pronunciations
```

---

## Directory Structure

```text
korean_pronunciation/
├── analyzers/              # Morphological analysis wrappers
│   ├── base.py             # Base class for analyzers
│   ├── kiwi_analyzer.py    # kiwipiepy integration (highly recommended)
│   └── simple_analyzer.py  # Dependency-free fallback analyzer
├── rules/                  # Isolated rule implementations
│   ├── base.py             # Abstract BaseRule class
│   ├── vowel_rules.py      # Vowel changes (제4-5항)
│   ├── sound_addition.py   # 'ㄴ' addition at boundaries (제29-30항)
│   └── ...                 # Other specific phonetic rules
├── tests/                  # Pytest integration and unit tests
├── engine.py               # BFS-based pronunciation engine logic
├── pipeline.py             # Defines the standard rule execution order
├── state.py                # Immutable Syllable and PronunciationState classes
├── hangul.py               # Hangul unicode decomposition/composition math
├── jamo_constants.py       # Hex offsets for Jamo calculations
├── tokenizer.py            # Converts raw text and tokens into Syllable states
└── main.py                 # Command-line interface entry point
```

---

## Installation

Currently, the project is designed to be run directly from the source directory.

**Requirements:**
* Python 3.7+

**Dependencies:**
- While the library works out of the box, installing the `kiwipiepy` library is **highly recommended** for accurate morpheme boundary detection.
- To use the Graphical User Interface (GUI), you must install `PySide6`.

```bash
# Clone the repository (or navigate to the directory)
cd 20260628_KoreanPronunciation

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows

# Install the optional (but recommended) morphological analyzer
pip install kiwipiepy

# Install PySide6 (required for the GUI)
pip install PySide6
```

---

## Usage

The project supports three official user interfaces (CLI, Interactive Console, and GUI) as well as a programmatic Python API. All interfaces utilize the same underlying pronunciation engine.

### 1. Command-Line Interface (CLI)

You can convert text directly from the command line.

**Standard Output:**
```bash
python -m korean_pronunciation.main "맛있다"
```
*Output:*
```text
마딛따 (rules: CodaNeutralizationRule, FortitionRule, DoubleCodaRule)
마싣따 (rules: LiaisonRule, FortitionRule, DoubleCodaRule)
```

**JSON Output:**
```bash
python -m korean_pronunciation.main "우리의" --json
```

**Help:**
```bash
python -m korean_pronunciation.main --help
```

### 2. Interactive Console Mode (REPL)

For a continuous interactive console environment, run:

```bash
python -m korean_pronunciation.console
```

*Example Session:*
```text
=====================================
Korean Pronunciation Converter
Type 'exit' to quit.
=====================================

Input:
> 맛있다

Pronunciations

1. 마딛따
2. 마싣따

-------------------------------------

Input:
> exit
Goodbye.
```

### 3. Graphical User Interface (GUI)

To launch the desktop GUI app (which is clean, minimal, and fully accessible):

```bash
python -m korean_pronunciation.gui
```

**Pre-built Standalone Executable:**
If you prefer not to use terminal commands, a pre-built standalone executable is available in the `dist` directory:
- Run [dist/KoreanPronunciationGUI.exe](file:///c:/06_Codes/Python/20260628_KoreanPronunciation/dist/KoreanPronunciationGUI.exe) directly to launch the application.


**GUI Features:**
- **Input Text Field:** Type any Korean words or sentences. Press **Enter** or click **Convert** to view results.
- **Copy Button:** Copies all formatted pronunciations to your clipboard.
- **Clear Button:** Resets all input/output fields and status bar.
- **Status Bar:** Provides contextual messages (e.g. "Ready", "Converting...", "Copied to clipboard").
- **Responsive Processing:** The pronunciation engine runs on a background thread so the UI remains completely fluid.

### 4. Python API

Use the engine programmatically in your scripts:

```python
from korean_pronunciation import get_pronunciation, get_pronunciations

# Get the primary pronunciation
primary = get_pronunciation("국물")
print(primary)  # 궁물

# Get all valid pronunciations with metadata
results = get_pronunciations("선의")
for res in results:
    print(f"{res['pronunciation']} (Rules: {', '.join(res['applied_rules'])})")
# Output:
# 서니 (Rules: VowelRule, LiaisonRule)
# 서늬 (Rules: LiaisonRule)
```

---

## Examples

| Input | Output | Phenomenon |
| :--- | :--- | :--- |
| **읽다** | `익따` | Double Coda Simplification + Fortition |
| **국물** | `궁물` | Nasalization |
| **같이** | `가치` | Palatalization |
| **옷이** | `오시` | Liaison (Resyllabification) |
| **서울역** | `서울력` | 'ㄴ' Addition + Liquidization |
| **우리의** | `[우리의, 우리에]` | Vowel exception (Genitive '의' -> '에') |

---

## Pronunciation Rules

The engine implements the official Korean Standard Pronunciation rules sequentially in the following priority order:

| Stage | Rule Class | Official Section | Description |
| :--- | :--- | :--- | :--- |
| 1 | `VowelRule` | 제4-5항 | Applies vowel changes and branches for alternatives (e.g., 의 -> 이/에). |
| 2 | `SoundAdditionRule` | 제29-30항 | Inserts 'ㄴ' at compound word boundaries. |
| 3 | `HRule` | 제12항 | Handles 'ㅎ' aspiration, deletion, and nasalization. |
| 4 | `LiaisonRule` | 제13-16항 | Links codas to the empty onsets of subsequent syllables. |
| 5 | `PalatalizationRule` | 제17항 | Transforms ㄷ/ㅌ + ㅣ into ㅈ/ㅊ. |
| 6 | `FortitionRule` | 제23-27항 | Tensification (ㄱ, ㄷ, ㅂ, ㅅ, ㅈ -> ㄲ, ㄸ, ㅃ, ㅆ, ㅉ). |
| 7 | `DoubleCodaRule` | 제10-11항 | Simplifies complex double codas (e.g., ㄺ -> ㄱ or ㄹ). |
| 8 | `CodaNeutralizationRule`| 제8-9항 | Reduces syllable-final consonants to representative sounds. |
| 9 | `NasalizationRule` | 제18-19항 | Assimilates consonants near nasals. |
| 10 | `LiquidizationRule` | 제20항 | Handles lateral assimilation (ㄴ <-> ㄹ). |

---

## Multiple Pronunciation Generation

Certain Korean words possess multiple acceptable pronunciations (e.g., "냇가" -> `[내까, 낻까]`). 

To handle this safely, the engine utilizes a **Breadth-First Search (BFS)** strategy. When a state reaches a rule that has optional or alternative outputs, the rule returns an array of multiple newly derived `PronunciationState` objects. The engine maintains all generated states simultaneously.

To prevent exponential explosion, the engine immediately deduplicates equivalent phonetic states at the end of each rule stage using a deterministic phonetic string key (`canonical_key()`).

---

## Internal Design

### Immutable States
Both `Syllable` and `PronunciationState` are implemented as frozen dataclasses. Rules do not mutate states; they yield modified copies. This guarantees stability during BFS branching.

### Jamo Arithmetic
The library avoids bulky string replacements by utilizing raw Unicode code-point arithmetic (`hangul.py`). It decomposes Hangul blocks into numerical indices for Choseong, Jungseong, and Jongseong, manipulates the indices based on phonological rules, and accurately composes them back into complete blocks.

---

## Configuration

Currently, configuration is strictly code-driven.

The primary point of configuration is the morphological analyzer. The engine defaults to using `KiwiAnalyzer` if `kiwipiepy` is installed. If it is unavailable, it gracefully degrades to `SimpleAnalyzer`.

You can explicitly inject an analyzer when creating the engine:

```python
from korean_pronunciation.engine import PronunciationEngine
from korean_pronunciation.pipeline import create_standard_pipeline
from korean_pronunciation.analyzers.simple_analyzer import SimpleAnalyzer

engine = PronunciationEngine(
    pipeline=create_standard_pipeline(),
    analyzer=SimpleAnalyzer()
)
```

---

## Testing

The project maintains a test suite covering unit tests for Hangul manipulation, discrete rule behaviors, and full-pipeline integration scenarios.

**Running Tests:**
Requires `pytest`.
```bash
pip install pytest
pytest korean_pronunciation/tests/
```

Coverage focuses on challenging phonological edge cases and ensures no rule causes negative bleeding (e.g., "물약을 먹은 야옹이" preventing invalid 'ㄴ' additions).

---

## Performance

The engine leverages immediate deduplication during the BFS traversal. Even if a word creates 4 alternative branches, duplicates are pruned at every step, keeping the state array extremely small (typically < 4 states at any time).

**Known Bottlenecks:**
The most computationally expensive phase is the initial morphological analysis. If processing massive datasets, reusing the `KiwiAnalyzer` instance rather than re-instantiating it is highly recommended.

---

## Limitations

* **Fallback Analyzer Accuracy:** If `kiwipiepy` is absent, the engine uses the `SimpleAnalyzer` which relies entirely on spacing and heuristics. This can result in inaccurate rule application for complex bound nouns or compound verbs.
* **Compound Noun Boundaries:** 'ㄴ' addition heavily relies on correct POS tagging to identify compound boundaries. Extremely obscure or unregistered compound nouns might not trigger the addition properly.
* **Missing Package Distribution:** Currently, there is no `setup.py` or `pyproject.toml` to install the package cleanly via `pip install .`.

---

## Future Improvements

1. **Package Management:** Add `pyproject.toml` and publish the library to PyPI for standard distribution.
2. **Custom Dictionaries:** Allow users to inject custom user dictionaries into the morphological analyzer to force specific compound boundaries.
3. **Caching:** Implement LRU caching at the `get_pronunciations` level to speed up repeated queries for common words.

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Ensure you have `pytest` and `kiwipiepy` installed.
3. If adding a new rule or edge case exception, locate the appropriate module inside `korean_pronunciation/rules/`.
4. Add corresponding test cases to `korean_pronunciation/tests/`.
5. Ensure all tests pass (`pytest korean_pronunciation/tests/`) before submitting a pull request.

---

## License

No license is currently specified for this repository. Please contact the maintainer for usage rights.

---

## FAQ

**Why does the engine return multiple pronunciations?**
The Korean Standard Pronunciation rules explicitly allow variants for specific phenomena, such as the pronunciation of the vowel "의" in non-initial syllables, or the optional insertion of saisiot in certain compounds.

**Why doesn't a certain word produce an expected pronunciation?**
First, ensure you have `kiwipiepy` installed. Accurate pronunciation relies heavily on correct morphological tags (e.g., identifying a grammatical particle vs. a noun stem). If the analyzer misidentifies a morpheme, subsequent rules (like liaison or fortition) may be skipped or applied incorrectly.

**Does the project support entire sentences?**
Yes. Sentences can be passed directly to the engine. The morphological analyzer separates the sentence into tokens, and the engine evaluates liaison and neutralization across word boundaries where applicable.
