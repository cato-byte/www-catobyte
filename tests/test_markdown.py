import re

from sitegen.markdown import render_data_block, render_markdown, slugify

POST = """## My title

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Cover caption](../../images/cover.webp)

Intro paragraph that is long enough to be used as the summary of this post.

### Section one

![Figure caption](../../images/figure.png)

```python
def f():
    if True:
        return "<tag>"
```

| a | b |
|---|---|
| 1 | 2 |
"""


def test_title_cover_and_date_are_extracted():
    r = render_markdown(POST)
    assert r.title == "My title"
    assert r.cover == "../../images/cover.webp"
    assert r.cover_alt == "Cover caption"
    assert "PUBLISH_DATE" not in r.body_html
    assert "My title" not in r.body_html
    assert "cover.webp" not in r.body_html


def test_headings_start_at_h2_and_get_ids():
    r = render_markdown(POST)
    assert '<h2 id="section-one">Section one</h2>' in r.body_html
    assert "<h3" not in r.body_html


def test_standalone_image_becomes_figure_with_lazy_loading():
    r = render_markdown(POST)
    assert "<figure>" in r.body_html
    assert "<figcaption>Figure caption</figcaption>" in r.body_html
    assert 'loading="lazy"' in r.body_html


def test_code_keeps_indentation_and_is_escaped():
    r = render_markdown(POST)
    assert r.has_code
    assert '<pre class="line-numbers"><code class="language-python">' in r.body_html
    assert "        return &quot;&lt;tag&gt;&quot;" in r.body_html


def test_tables_are_wrapped_for_horizontal_scroll():
    r = render_markdown(POST)
    assert '<div class="table-wrap"><table>' in r.body_html


def test_summary_skips_short_and_image_paragraphs():
    assert render_markdown(POST).summary.startswith("Intro paragraph")


def test_projects_keep_their_first_heading():
    r = render_markdown("## At a glance\n\nText.", extract_title=False)
    assert r.title == ""
    assert '<h2 id="at-a-glance">' in r.body_html


def test_duplicate_headings_get_unique_ids():
    r = render_markdown("## Notes\n\n## Notes\n", extract_title=False)
    assert 'id="notes"' in r.body_html and 'id="notes-2"' in r.body_html


def test_slugify_handles_accents_and_punctuation():
    assert slugify("Déduplication & clés!") == "déduplication-clés"


def test_data_blocks_render_from_csv(tmp_path):
    csv_path = tmp_path / "by_country.csv"
    csv_path.write_text("country,Companies\nFR,200\nIE,<b>50</b>\n", encoding="utf-8")
    table = render_data_block("table", csv_path)
    assert "<td>&lt;b&gt;50&lt;/b&gt;</td>" in table  # CSV content is escaped

    csv_path.write_text("country,Companies\nFR,200\nIE,50\n", encoding="utf-8")
    bars = render_data_block("bars", csv_path)
    assert 'width="100.00"' in bars and 'width="25.00"' in bars


def test_missing_data_file_renders_nothing(tmp_path):
    assert render_data_block("table", tmp_path / "missing.csv") == ""
    r = render_markdown("Text\n\n<!-- table: missing.csv -->\n", extract_title=False, data_dir=tmp_path)
    assert "table" not in r.body_html


def test_summary_skips_link_only_index_paragraphs():
    source = "## T\n\n[Broadcast joins](#a)\n[Key concepts](#b)\n\nA real first paragraph that explains what this guide covers in detail.\n"
    assert render_markdown(source).summary.startswith("A real first paragraph")


GUIDE = """## A guide

Intro paragraph that explains what this guide covers and how to use it well.

<!-- QA -->

### Basics

#### What is a thing?

A thing is *something*.

```python
thing = 1
```

#### Why use a thing?

Because.

### Advanced

#### What is a thing?

The same question in another category.
"""


def test_qa_guide_turns_questions_into_cards_grouped_by_category():
    r = render_markdown(GUIDE)
    assert r.title == "A guide"
    assert r.qa_sections == [("basics", "Basics", 2), ("advanced", "Advanced", 1)]
    assert r.question_count == 3
    assert r.body_html.count('<details class="qa"') == 3
    assert r.body_html.count("</details>") == 3
    assert '<h2 id="basics">Basics</h2>' in r.body_html
    assert '<summary data-n="1">What is a thing?</summary>' in r.body_html
    # The answer, code included, stays inside its card; duplicate questions get unique ids.
    first = r.body_html.split('<details class="qa" id="why-use-a-thing">')[0]
    assert "<em>something</em>" in first and "thing = 1" in first
    assert 'id="what-is-a-thing-2"' in r.body_html
    # Numbers are fixed in the HTML, so filtering the list doesn't renumber the questions.
    assert re.findall(r'data-n="(\d+)"', r.body_html) == ["1", "2", "3"]
    # The template puts the contents list between the intro and the first category.
    intro, questions = r.body_html.split("<!-- qa-nav -->")
    assert "Intro paragraph" in intro and questions.lstrip().startswith('<div class="qa-guide">')
    assert r.summary.startswith("Intro paragraph")


def test_posts_without_qa_marker_have_no_cards():
    r = render_markdown(POST)
    assert r.qa_sections == [] and "<details" not in r.body_html


LEARNING_GUIDE = """## A guide

Intro paragraph that explains what this guide covers and how to use it well.

<!-- QA -->

<!-- stage: Foundations -->

### Basics

<!-- unit: First unit -->

<!-- goals -->

- Explain a thing.

<!-- concept -->

Things connect *like this*.

<!-- example -->

```sql
-- <!-- unit: not a marker inside code -->
SELECT 1;
```

#### What is a thing?

A thing.

<!-- challenge -->

Build a thing.

<!-- solution -->

Like so.

<!-- takeaways -->

- Things matter.

<!-- stage: Practice -->

### Scenarios

Mixed problems.

#### Combine things?

Yes.
"""


def test_learning_guide_parses_stages_units_and_blocks():
    from sitegen.markdown import group_stages
    r = render_markdown(LEARNING_GUIDE)
    basics, scenarios = r.guide_sections
    assert [(stage, [s.id for s in secs]) for stage, secs in group_stages(r.guide_sections)] == [
        ("Foundations", ["basics"]), ("Practice", ["scenarios"])]
    unit = basics.units[0]
    assert (unit.id, unit.title, unit.has_intro) == ("first-unit", "First unit", True)
    assert "<em>like this</em>" in unit.concept and "not a marker inside code" in unit.example
    assert "Build a thing" in unit.challenge and "Like so" in unit.solution and "Things matter" in unit.takeaways
    assert [(q.id, q.number) for q in unit.questions] == [("what-is-a-thing", 1)]
    # Questions without a unit marker form an untitled unit; text under ### is the section lead.
    assert scenarios.units[0].title == "" and scenarios.units[0].questions[0].number == 2
    assert "Mixed problems" in scenarios.lead
    assert r.qa_sections == [("basics", "Basics", 1), ("scenarios", "Scenarios", 1)]
