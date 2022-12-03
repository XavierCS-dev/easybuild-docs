"""
Generate the code reference pages.
Based off https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
"""

from pathlib import Path

import mkdocs_gen_files


# remove the problematic py2.py and symlink the py3.py in its place
Path(f"src/easybuild/tools/py2vs3/py2.py").unlink(missing_ok=True)
Path(f"src/easybuild/tools/py2vs3/py2.py").symlink_to(Path("py3.py"))

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("src/easybuild/").rglob("*.py")):
    module_path = path.relative_to("src").with_suffix("")
    doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path("api", doc_path)

    parts = list(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("api/summary.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
