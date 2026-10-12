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
