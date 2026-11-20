# Changhai Zhou (周昌海) — Academic Homepage

**[Visit the academic homepage of Changhai Zhou (周昌海 | zhouchanghai | changhaizhou)](https://changhaizhou98.github.io/).**

Changhai Zhou (周昌海) is a direct-track PhD candidate at Fudan University working across the full stack of trillion-parameter (T-scale) foundation models—from pre-training and mid-training to post-training—as well as efficient LLMs, model compression, PEFT, long-context RL, adaptive inference, and multi-tenant LLM serving systems.

GitHub Pages publishes this Jekyll site from the root of `main`.
The homepage front matter forwards `/zhouchanghai/` and `/changhaizhou/` URLs to `/`.

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
