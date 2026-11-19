# Changhai Zhou — Academic Homepage

**[Visit the academic homepage](https://changhaizhou98.github.io/).**

GitHub Pages publishes this Jekyll site from the root of `main`.
The homepage front matter forwards the former `/zhouchanghai/` URLs to `/`.

## Editing the site

- Edit the homepage, news, and publication list in `_pages/about.md`.
- Edit the profile and site metadata in `_config.yml` and navigation in `_data/navigation.yml`.
- Keep publication figures in `images/papers/` and research notes with their figures and data in `notes/`.
- Edit site styles in `assets/css/main.scss`.

## Local preview

With Ruby and Bundler installed, run the following commands from the repository root.

```bash
bundle install
bundle exec jekyll serve
```

Run the content checks with Python.

```bash
python3 -m unittest discover -v
```
