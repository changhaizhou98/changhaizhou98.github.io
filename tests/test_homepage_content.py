import unittest
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


class HomepageTest(unittest.TestCase):
    def test_about_page_serves_root(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertIn('\npermalink: /\n', about)
        self.assertIn('author_profile: true', about)
        for alias in [
            '/zhouchanghai/',
            '/zhouchanghai/about/',
            '/zhouchanghai/about.html',
            '/zhouchanghai/homepage/',
            '/changhaizhou/',
            '/changhaizhou/about/',
            '/changhaizhou/about.html',
            '/changhaizhou/homepage/',
        ]:
            self.assertIn(f'\n  - {alias}\n', about)

    def test_config_has_empty_baseurl(self):
        config = (ROOT / '_config.yml').read_text()
        self.assertIn('baseurl                  : ""', config)

    def test_github_pages_identity_uses_current_username(self):
        config = (ROOT / '_config.yml').read_text()
        about = (ROOT / '_pages' / 'about.md').read_text()
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('repository               : "changhaizhou98/changhaizhou98.github.io"', config)
        self.assertIn('url                      : "https://changhaizhou98.github.io"', config)
        self.assertIn('github           : "changhaizhou98"', config)
        self.assertIn('https://github.com/changhaizhou98', about)
        self.assertIn('https://changhaizhou98.github.io/', readme)
        self.assertNotIn('manlenzzz', config + about + readme)

    def test_site_identity_is_searchable_by_name(self):
        config = (ROOT / '_config.yml').read_text()
        seo = (ROOT / '_includes' / 'seo.html').read_text()
        about = (ROOT / '_pages' / 'about.md').read_text()
        author_profile = (ROOT / '_includes' / 'author-profile.html').read_text()
        robots = (ROOT / 'robots.txt').read_text()
        self.assertIn('title                    : "Changhai Zhou"', config)
        self.assertIn('seo_title                : "Changhai Zhou (周昌海) | Academic Homepage (zhouchanghai / changhaizhou)"', config)
        self.assertIn('PhD candidate at Fudan University', config)
        for query_term in ['周昌海', 'zhouchanghai', 'changhaizhou', 'Changhai Zhou']:
            self.assertIn(query_term, config)
        self.assertIn('周昌海', about)
        self.assertIn('<meta name="description" content="{{ seo_description }}">', seo)
        self.assertIn('<meta name="keywords" content="{{ site.keywords | escape_once }}">', seo)
        self.assertIn('"@type": "Person"', seo)
        self.assertIn('"name": {{ site.author.name | jsonify }}', seo)
        self.assertIn('"alternateName": {{ site.author.aliases | jsonify }}', seo)
        self.assertIn('author.chinese_name', author_profile)
        self.assertIn('Sitemap: https://changhaizhou98.github.io/sitemap.xml', robots)

    def test_about_highlights_full_stack_trillion_parameter_experience(self):
        config = (ROOT / '_config.yml').read_text()
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertIn('Full-Stack T-Scale LLMs (Pre-/Mid-/Post-Training)', config)
        self.assertNotIn('direct-track', about)
        self.assertNotIn('直博', about)
        for phrase in [
            "combined Master's–PhD program",
            '硕博连读',
            'full stack of trillion-parameter (T-scale) foundation models',
            'pre-training, mid-training, and post-training',
            'model architecture',
            'training efficiency',
            'data-driven',
            '万亿参数（T 级）基础大模型',
            '预训练（Pre-training）、中训练（Mid-training）到后训练（Post-training）',
            '模型全栈',
            '模型结构',
            '训练效率',
            '数据驱动',
        ]:
            self.assertIn(phrase, about)

    def test_site_links_do_not_force_new_tabs(self):
        head = (ROOT / '_includes' / 'head.html').read_text()
        self.assertNotIn('<base', head)
        self.assertNotIn('target="_blank"', head)

    def test_assets_resolve_from_nested_pages(self):
        head = (ROOT / '_includes' / 'head.html').read_text()
        scripts = (ROOT / '_includes' / 'scripts.html').read_text()
        self.assertIn("{{ '/assets/css/main.css' | relative_url }}", head)
        self.assertIn("{{ '/assets/js/main.min.js' | relative_url }}", scripts)
        self.assertNotIn('href="assets/', head)
        self.assertNotIn('src="assets/', scripts)

    def test_scripts_have_no_unused_tracking_includes(self):
        scripts = (ROOT / '_includes' / 'scripts.html').read_text()
        self.assertNotIn('fetch_google_scholar_stats.html', scripts)
        self.assertNotIn('analytics.html', scripts)

    def test_reference_style_sections_present(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertIn('id="about"', about)
        self.assertIn('id="news"', about)
        self.assertIn('id="research-notes"', about)
        self.assertIn('id="publications"', about)
        self.assertIn('id="contact"', about)
        self.assertIn('About Me', about)
        self.assertIn('News', about)
        self.assertIn('When a Better Clock Is Not a Better Sampler', about)

    def test_navigation_points_to_homepage_sections(self):
        nav = (ROOT / '_data' / 'navigation.yml').read_text()
        for anchor in ['#about', '#news', '#research-notes', '#publications', '#contact']:
            self.assertIn(anchor, nav)
        self.assertNotIn('Homepage', nav)
        self.assertNotRegex(nav, r'url:\s+"#research"\s*$')

    def test_news_dates_are_ordered_and_not_synthetic(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        news_dates = re.findall(r'<span class="news-date">([^<]+)</span>', about)
        self.assertGreaterEqual(len(news_dates), 3)
        self.assertEqual(news_dates, sorted(news_dates, reverse=True))
        self.assertNotIn('2025-12', news_dates)

    def test_news_uses_acceptance_timeline(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        news_items = re.findall(
            r'<span class="news-date">([^<]+)</span>\s*'
            r'<span class="news-text">([^<]+)</span>',
            about,
        )
        self.assertEqual(
            news_items,
            [
                ('2026-04-30', 'AutoQRA was accepted to ICML 2026.'),
                ('2026-04-04', 'Deputy, QR-Adaptor, and CoRE were accepted to ACL 2026.'),
                ('2026-01-25', 'Large Language Model Compression with Global Rank and Sparsity Optimization was accepted to ICLR 2026.'),
                ('2025-05-01', 'BSLoRA was accepted to ICML 2025.'),
                ('2025-03-14', 'Enhancing Object Coherence in Layout-to-Image Synthesis was accepted to ICME 2025.'),
                ('2025-01-22', 'RankAdaptor and QPruner were accepted to NAACL 2025.'),
                ('2024-12-09', 'Dynamic Operator Optimization for Efficient Multi-Tenant LoRA Model Serving was accepted to AAAI 2025.'),
            ],
        )
        news_text = ' '.join(text for _, text in news_items)
        self.assertNotIn('available on arXiv', news_text)
        self.assertNotIn('studies million-scale', news_text)

    def test_previous_landing_page_patterns_removed(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertNotIn('profile-hero', about)
        self.assertNotIn('language-switch', about)
        self.assertNotIn('data-lang=', about)

    def test_research_note_has_visual_hero(self):
        note = (ROOT / 'notes' / 'damage-clock-negative-result' / 'index.md').read_text()
        self.assertIn('class="note-hero-visual"', note)
        self.assertIn('class="note-breadcrumb"', note)

    def test_damage_clock_note_exists(self):
        note = ROOT / 'notes' / 'damage-clock-negative-result' / 'index.md'
        self.assertTrue(note.is_file())
        note_text = note.read_text()
        self.assertIn('permalink: /notes/damage-clock-negative-result/', note_text)
        self.assertIn('When a Better Clock Is Not a Better Sampler', note_text)
        self.assertIn('figures/fig_result_delta_revised.svg', note_text)
        self.assertTrue((note.parent / 'figures' / 'fig_result_delta_revised.svg').is_file())
        self.assertTrue((note.parent / 'data' / 'r287_mean_fid.csv').is_file())

    def test_sidebar_does_not_duplicate_research_summary(self):
        author_profile = (ROOT / '_includes' / 'author-profile.html').read_text()
        self.assertNotIn('site.description', author_profile)

    def test_avatar_path_resolves_to_existing_image(self):
        config = (ROOT / '_config.yml').read_text()
        include = (ROOT / '_includes' / 'author-profile.html').read_text()
        avatar_match = re.search(r'avatar\s+:\s+"?([^"\n]+)"?', config)
        self.assertIsNotNone(avatar_match)
        avatar_path = avatar_match.group(1).lstrip('/')
        self.assertTrue((ROOT / avatar_path).exists(), avatar_path)
        self.assertIn('author.avatar | relative_url', include)

    def test_arxiv_publications_use_real_images(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        for image_name in [
            'llm-compression-global-rank-sparsity-main.png',
            'qr-adaptor-mixed-precision-main.png',
            'autoqra-main.png',
            'qpruner-main.png',
        ]:
            self.assertIn(image_name, about)
            self.assertTrue((ROOT / 'images' / 'papers' / image_name).exists())

    def test_complete_publication_groups_and_titles_present(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        for group in [
            'Post-training、模型发布与训练服务',
            'LLM Serving 与推理加速',
            '模型压缩与参数高效适配',
            '多模态生成模型',
            '评测与代码推理',
        ]:
            self.assertIn(group, about)

        for title in [
            'On the Scaling of PEFT: Towards Million Personal Models of Trillion Parameters',
            'LongStraw: Long-Context RL Beyond 2M Tokens under a Fixed GPU Budget',
            'Introducing Macaron-V1',
            'Macaron-V1-Preview: A 749B Personal Agent Model with Mixture of LoRA',
            'MinT: Managed Infrastructure for Training and Serving Millions of LLMs',
            'miniTE: Diagnosing and Bridging the Execution Gap in Native NVFP4 Reinforcement Learning',
            'Hierarchical Skill Evolution for Coding Agents',
            'Positions Are Not Facts: The Mismatch Between KV Caches and Memory',
            'Dynamic Operator Optimization for Efficient Multi-Tenant LoRA Model Serving',
            'Making Activation Sparsity Executable in Grouped Low-Bit LLMs',
            'Deputy: Accelerating Large Language Model Inference with Dynamic Low-Rank Substitution',
            'Large Language Model Compression with Global Rank and Sparsity Optimization',
            'Balancing Fidelity and Plasticity: Aligning Mixed-Precision Fine-Tuning with Linguistic Hierarchies',
            'AutoQRA: Joint Optimization of Mixed-Precision Quantization and Low-rank Adapters for Efficient LLM Fine-Tuning',
            'RankAdaptor: Hierarchical Dynamic Low-Rank Adaptation for Structural Pruned LLMs',
            'QPruner: Probabilistic Decision Quantization for Structured Pruning in Large Language Models',
            'BSLoRA: Enhancing the Parameter Efficiency of LoRA with Intra-Layer and Inter-Layer Sharing',
            'LaRA: Layer-wise Rank Allocation for Efficient Fine-Tuning of Pruned Large Language Models',
            'MJev-Spatial: System One Spatial Intelligence via Native Attention Matching',
            'OneStreamer: Unifying Perception, Memory, and Proactive Response in Streaming Video Interaction',
            'TimeLens2: Generalist Video Temporal Grounding with Multimodal LLMs',
            'GlyphAtlas: Disentangling Stroke Detail from Layout for Scene Text Synthesis',
            'SoulX-FlashHead: Oracle-guided Generation of Infinite Real-time Streaming Talking Heads',
            'Enhancing Object Coherence in Layout-to-Image Synthesis',
            'CoRE: A Fine-Grained Code Reasoning Benchmark Beyond Output Prediction',
        ]:
            self.assertIn(title, about)

    def test_publications_include_authors_and_highlight_me(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertEqual(about.count('class="publication-authors"'), 25)
        self.assertGreaterEqual(about.count('<strong>Changhai Zhou</strong>'), 21)

    def test_mindlab_publications_use_lab_author(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertEqual(about.count('<p class="publication-authors">MindLab</p>'), 4)
        post_training = about.split('LLM Serving 与推理加速', 1)[0]
        self.assertNotIn('<strong>Changhai Zhou</strong> et al.', post_training)

    def test_macaron_v1_and_preview_are_separate_release_entries(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertEqual(about.count('<h3>Introducing Macaron-V1</h3>'), 1)
        self.assertEqual(
            about.count('<h3>Macaron-V1-Preview: A 749B Personal Agent Model with Mixture of LoRA</h3>'),
            1,
        )
        for url in [
            'https://macaron.im/mindlab/research/introducing-macaron-v1',
            'https://huggingface.co/mindlab-research/Macaron-V1-Venti',
            'https://huggingface.co/mindlab-research/Macaron-V1-Tall',
        ]:
            self.assertIn(url, about)

    def test_bslora_marks_first_two_authors_as_equal_contributors(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        self.assertIn(
            'Yuhua Zhou*, Ruifeng Li*, <strong>Changhai Zhou</strong>, Fei Yang, Aimin Pan',
            about,
        )

    def test_hugging_face_daily_paper_rankings_are_prominent_and_linked(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        expected_rankings = [
            ('2606.02437', 'Ranked #2 on Hugging Face Daily Papers'),
            ('2605.13779', 'Ranked #1 on Hugging Face Daily Papers'),
            ('2607.14952', 'Ranked #1 on Hugging Face Daily Papers'),
            ('2610.22276', 'Ranked #2 on Hugging Face Daily Papers'),
            ('2610.01762', 'Ranked #2 on Hugging Face Daily Papers'),
            ('2607.17423', 'Ranked #3 on Hugging Face Daily Papers'),
        ]
        self.assertEqual(about.count('class="pub-rank"'), 6)
        for paper_id, label in expected_rankings:
            self.assertIn(
                f'<a href="https://huggingface.co/papers/{paper_id}" target="_blank" rel="noopener">{label}</a>',
                about,
            )

    def test_longstraw_entry_has_complete_authors_and_direct_pdf(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        expected_authors = (
            '<strong>Changhai Zhou</strong>, Kieran Liu, Yuhua Zhou, Qian Qiao, Jun Gao, '
            'Harry Zhang, Irvine Lu, Nolan Ho, Lucian Li, Andrew Lei, Cleon Cheng, Steven Chiang, '
            'Yihang Zeng, Di Zhang, Rio Yang, Kaijie Chen, Andrew Chen, Pony Ma, Weizhong Zhang, Cheng Jin'
        )
        self.assertIn(expected_authors, about)
        self.assertIn('<p class="pub-meta">Technical Report / 一作</p>', about)
        self.assertIn('https://arxiv.org/pdf/2607.14952', about)

    def test_deputy_is_not_listed_as_first_author(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        match = re.search(
            r'Deputy: Accelerating Large Language Model Inference with Dynamic Low-Rank Substitution.*?'
            r'<p class="pub-meta">([^<]+)</p>',
            about,
            re.S,
        )
        self.assertIsNotNone(match)
        self.assertNotIn('一作', match.group(1))
        self.assertNotIn('共一', match.group(1))

    def test_deputy_authors_are_complete(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        match = re.search(
            r'Deputy: Accelerating Large Language Model Inference with Dynamic Low-Rank Substitution.*?'
            r'<p class="publication-authors">([^<]*(?:<strong>[^<]+</strong>[^<]*)*)</p>',
            about,
            re.S,
        )
        self.assertIsNotNone(match)
        authors = re.sub(r'<[^>]+>', '', match.group(1))
        self.assertEqual(
            authors,
            'Yuhua Zhou*, Shichao Weng*, Changhai Zhou*, Yuhan Wu, Qian Qiao, Jun Gao, Fei Yang†, Aimin Pan†',
        )

    def test_publication_images_are_main_figures_not_cover_pages(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        for image_name in [
            'llm-compression-global-rank-sparsity-main.png',
            'qr-adaptor-mixed-precision-main.png',
            'autoqra-main.png',
            'qpruner-main.png',
            'dynamic-operator-optimization-main.png',
            'scaling-peft-main.png',
            'longstraw-main.png',
            'macaron-v1-main.png',
            'mint-main.png',
            'macaron-v1-preview-main.png',
            'rankadaptor-main.png',
            'bslora-main.png',
            'mjev-spatial-main.png',
            'onestreamer-main.png',
            'timelens2-main.png',
            'glyphatlas-main.png',
            'minite-main.png',
            'hse-main.png',
            'positions-not-facts-main.png',
            'soulx-flashhead-main.png',
            'object-coherence-main.png',
            'core-benchmark-main.png',
        ]:
            self.assertIn(image_name, about)
            self.assertTrue((ROOT / 'images' / 'papers' / image_name).exists())

    def test_placeholder_publication_thumbnails_removed(self):
        about = (ROOT / '_pages' / 'about.md').read_text()
        styles = (ROOT / 'assets' / 'css' / 'main.scss').read_text()
        self.assertNotIn('publication-thumb--', about)
        self.assertNotIn('publication-thumb--', styles)


if __name__ == '__main__':
    unittest.main()
