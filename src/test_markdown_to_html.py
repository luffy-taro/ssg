import unittest

from parser import extract_title, markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote</blockquote></div>",
        )

    def test__multiline_blockquote(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><blockquote>"I am in fact a Hobbit in all but size."-- J.R.R. Tolkien</blockquote></div>""",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_combined_image_and_link(self):
        md = """
![Alt text](https://example.com/image.png) is an image, and [this is a link](https://example.com).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><img src="https://example.com/image.png" alt="Alt text" /> is an image, and <a href="https://example.com">this is a link</a>.</p></div>',
        )

    def test_inline_formatting_with_links_and_images(self):
        md = """
This is **bold** text with a [link](https://example.com) and an ![image](https://example.com/image.png).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bold</b> text with a <a href="https://example.com">link</a> and an <img src="https://example.com/image.png" alt="image" />.</p></div>',
        )


    def test_header_is_present(self):
        md = """
# HEADING
"""
        title = extract_title(md)
        self.assertEqual("HEADING", title)


    def test_header_is_not_present(self):
        md = """
## HEADING
"""
        with self.assertRaises(Exception):
            extract_title(md)

    

if __name__ == "__main__":
    unittest.main()
