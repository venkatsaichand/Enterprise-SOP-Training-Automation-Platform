import json

import streamlit as st

from utils import (
    build_dependency_install_message,
    build_export_text,
    build_slides_pptx,
    extract_text_from_upload,
    generate_sop_training_package,
    get_missing_dependencies,
    normalize_sop_text,
)


st.set_page_config(page_title="AI SOP Training Engine", layout="wide")


def render_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-soft: #f4f7fb;
            --text: #0f172a;
            --muted: #64748b;
            --border: #d9e2ec;
            --border-strong: #cbd5e1;
            --accent: #111827;
            --accent-hover: #0b1220;
            --accent-soft: #eff6ff;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
        }

        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top center, rgba(148, 163, 184, 0.10), transparent 24%),
                var(--bg);
            color: var(--text);
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            max-width: 880px;
            padding-top: 4.5rem;
            padding-bottom: 4rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        .hero {
            text-align: center;
            margin: 0 auto 2.75rem auto;
        }

        .hero-title {
            font-size: 3.4rem;
            line-height: 0.96;
            letter-spacing: -0.06em;
            font-weight: 700;
            color: var(--text);
            margin: 0 0 1rem 0;
        }

        .hero-subtitle {
            max-width: 640px;
            margin: 0 auto;
            font-size: 1.05rem;
            line-height: 1.85;
            color: var(--muted);
        }

        .section-label {
            font-size: 0.78rem;
            line-height: 1;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            color: #94a3b8;
            margin-bottom: 0.75rem;
        }

        .section-title {
            font-size: 1.2rem;
            line-height: 1.2;
            letter-spacing: -0.03em;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 0.45rem;
        }

        .section-copy {
            font-size: 0.96rem;
            line-height: 1.75;
            color: var(--muted);
            margin-bottom: 1.25rem;
        }

        .output-title {
            font-size: 1.08rem;
            line-height: 1.2;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text);
            margin-bottom: 1rem;
        }

        .status-row {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin: 1rem 0 1rem 0;
            color: #166534;
            font-size: 0.98rem;
            font-weight: 600;
            line-height: 1.5;
        }

        .status-dot {
            width: 0.7rem;
            height: 0.7rem;
            border-radius: 999px;
            background: #16a34a;
            flex: 0 0 auto;
        }

        .slide-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 22px;
            box-shadow: var(--shadow);
            padding: 1.3rem 1.4rem;
            margin: 0.9rem 0 1rem 0;
        }

        .slide-title {
            margin: 0 0 0.65rem 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text);
        }

        .stRadio > div {
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .stRadio [role="radiogroup"] {
            display: flex;
            gap: 0.6rem;
        }

        .stRadio [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.55rem 1rem;
            min-height: 46px;
        }

        .stRadio [role="radiogroup"] label:hover {
            border-color: var(--border-strong);
            background: var(--surface-soft);
        }

        .stRadio [role="radiogroup"] label p {
            color: var(--text) !important;
            font-size: 0.95rem;
            font-weight: 500;
        }

        [data-testid="stFileUploader"] {
            margin-top: 0.75rem;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: #ffffff !important;
            border: 1px dashed var(--border-strong) !important;
            border-radius: 20px !important;
            padding: 0.95rem 1.05rem !important;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #94a3b8 !important;
            background: #f8fafc !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: var(--text) !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] div,
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileUploaderDropzoneInstructions"] small {
            color: var(--muted) !important;
            opacity: 1 !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: var(--accent) !important;
            color: #ffffff !important;
            border: 1px solid var(--accent) !important;
            border-radius: 999px !important;
            font-weight: 600 !important;
            opacity: 1 !important;
            box-shadow: none !important;
        }

        [data-testid="stFileUploaderDropzone"] button:hover {
            background: var(--accent-hover) !important;
            border-color: var(--accent-hover) !important;
        }

        [data-testid="stFileUploaderFile"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            color: var(--text) !important;
        }

        [data-testid="stFileUploaderFile"] * {
            color: var(--text) !important;
            opacity: 1 !important;
        }

        [data-testid="stFileUploader"] button[kind="secondary"],
        [data-testid="stFileUploader"] button[kind="tertiary"] {
            background: transparent !important;
            border: none !important;
            color: var(--text) !important;
            box-shadow: none !important;
            padding: 0 !important;
            min-width: auto !important;
            height: auto !important;
        }

        [data-testid="stFileUploader"] svg {
            color: var(--text) !important;
            fill: var(--text) !important;
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 320px;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            background: var(--surface-soft) !important;
            color: var(--text) !important;
            caret-color: var(--text) !important;
            padding: 1rem 1.05rem !important;
            font-size: 0.97rem !important;
            line-height: 1.75 !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: #94a3b8 !important;
            box-shadow: 0 0 0 1px #94a3b8 !important;
        }

        .stButton > button {
            min-width: 220px;
            height: 3.1rem;
            border-radius: 999px;
            border: 1px solid var(--accent);
            background: var(--accent);
            color: #ffffff;
            font-size: 0.97rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            transition: background-color 150ms ease, transform 150ms ease, box-shadow 150ms ease;
            box-shadow: 0 12px 24px rgba(17, 24, 39, 0.12);
        }

        .stButton > button:hover {
            background: var(--accent-hover);
            border-color: var(--accent-hover);
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 16px 28px rgba(17, 24, 39, 0.15);
        }

        .stDownloadButton > button {
            height: 2.85rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #ffffff;
            color: var(--text);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            margin: 0.35rem 0 1rem 0;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab"] {
            min-height: 44px;
            padding: 0 1rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #ffffff !important;
            color: var(--text) !important;
        }

        .stTabs [data-baseweb="tab"] p {
            color: inherit !important;
            opacity: 1 !important;
            font-weight: 500 !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: var(--accent) !important;
            border-color: var(--accent) !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] p {
            color: #ffffff !important;
        }

        @media (max-width: 840px) {
            .block-container {
                padding-top: 3rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero-title {
                font-size: 2.55rem;
            }

            .hero-subtitle {
                font-size: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <h1 class="hero-title">AI SOP Training Engine</h1>
            <p class="hero-subtitle">Convert complex SOPs into structured training modules instantly</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_summary_tab(summary: list[str]) -> None:
    st.markdown('<div class="output-title">Summary</div>', unsafe_allow_html=True)
    for item in summary:
        st.markdown(f"- {item}")


def render_training_tab(training_steps: list[dict[str, str]]) -> None:
    st.markdown('<div class="output-title">Training Guide</div>', unsafe_allow_html=True)
    for index, step in enumerate(training_steps, start=1):
        st.markdown(f"### {index}. {step['title']}")
        st.markdown(f"**Owner:** {step['owner']}")
        st.markdown(f"**Action:** {step['action']}")
        st.markdown(f"**Outcome:** {step['outcome']}")
        st.markdown(f"**Decision Trigger:** {step['decision_trigger']}")


def render_quiz_tab(quiz: list[dict[str, str]]) -> None:
    st.markdown('<div class="output-title">Quiz</div>', unsafe_allow_html=True)
    for index, item in enumerate(quiz, start=1):
        st.markdown(f"**Q{index}. {item['question']}**")
        st.markdown(f"- Answer: {item['answer']}")
        st.markdown(f"- Explanation: {item['explanation']}")


def render_list_tab(title: str, items: list[str]) -> None:
    st.markdown(f'<div class="output-title">{title}</div>', unsafe_allow_html=True)
    for item in items:
        st.markdown(f"- {item}")


def render_improvements_tab(improvements: list[dict[str, str]]) -> None:
    st.markdown('<div class="output-title">Improvements</div>', unsafe_allow_html=True)
    for item in improvements:
        st.markdown(f"- {item['theme']}: {item['improvement']} ({item['impact']})")


def render_slides_tab(package: dict) -> None:
    st.markdown('<div class="output-title">Slides</div>', unsafe_allow_html=True)
    slide_deck = package.get("slides", {})
    deck_title = slide_deck.get("deck_title", package.get("sop_name", "Slide Deck"))
    st.markdown(f"**{deck_title}**")

    for slide in slide_deck.get("slides", []):
        bullets = "".join(f"<li>{bullet}</li>" for bullet in slide.get("bullets", []))
        visuals = "".join(f"<li>{visual}</li>" for visual in slide.get("visual_suggestions", []))
        visuals_html = ""
        if visuals:
            visuals_html = f"<p><strong>Visual Suggestions</strong></p><ul>{visuals}</ul>"

        st.markdown(
            f"""
            <div class="slide-card">
                <div class="slide-title">Slide {slide['slide_number']}: {slide['title']}</div>
                <ul>{bullets}</ul>
                {visuals_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    design_notes = slide_deck.get("design_notes", {})
    if design_notes:
        st.markdown("**Design Notes**")
        if design_notes.get("color_theme"):
            st.markdown(f"- Color theme: {design_notes['color_theme']}")
        if design_notes.get("font_pairing"):
            st.markdown(f"- Font pairing: {design_notes['font_pairing']}")
        for suggestion in design_notes.get("layout_suggestions", []):
            st.markdown(f"- Layout: {suggestion}")


def render_input_panel() -> tuple[str, str]:
    st.markdown('<div class="section-label">Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Provide your SOP content</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Choose one input method and generate a structured training module from your source material.</div>',
        unsafe_allow_html=True,
    )

    input_mode = st.radio(
        "Input mode",
        options=["Upload File", "Paste Text"],
        horizontal=True,
        label_visibility="collapsed",
    )

    sop_text = ""

    if input_mode == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload File",
            type=["txt", "pdf", "docx"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            sop_text = extract_text_from_upload(uploaded_file)
    else:
        sop_text = st.text_area(
            "Paste Text",
            placeholder="Paste a standard operating procedure here...",
            height=360,
            label_visibility="collapsed",
        )
    return input_mode, sop_text


def main() -> None:
    render_styles()

    if "generated" not in st.session_state:
        st.session_state.generated = False
    if "package" not in st.session_state:
        st.session_state.package = None

    missing_dependencies = get_missing_dependencies()
    if missing_dependencies:
        st.error(build_dependency_install_message(missing_dependencies))
        st.code("python -m pip install -r requirements.txt", language="powershell")
        st.stop()

    render_hero()
    _, sop_text = render_input_panel()
    generate_clicked = st.button("Generate Training")

    if generate_clicked:
        normalized_text = normalize_sop_text(sop_text)
        if not normalized_text:
            st.error("Please upload a file or paste SOP text before generating training content.")
            return

        with st.spinner("Generating training module..."):
            try:
                st.session_state.package = generate_sop_training_package(
                    sop_text=normalized_text,
                )
                st.session_state.generated = True
            except Exception as exc:
                st.session_state.generated = False
                st.session_state.package = None
                st.error(f"Generation failed: {exc}")
                return

    if not st.session_state.generated or not st.session_state.package:
        return

    package = st.session_state.package
    st.markdown(
        """
        <div class="status-row">
            <span class="status-dot"></span>
            <span>Training module generated successfully.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary_tab, training_tab, quiz_tab, mistakes_tab, improvements_tab, slides_tab = st.tabs(
        ["Summary", "Training Guide", "Quiz", "Common Mistakes", "Improvements", "Slides"]
    )

    with summary_tab:
        render_summary_tab(package["summary"])

    with training_tab:
        render_training_tab(package["training_guide"])

    with quiz_tab:
        render_quiz_tab(package["quiz"])

    with mistakes_tab:
        render_list_tab("Common Mistakes", package["common_mistakes"])

    with improvements_tab:
        render_improvements_tab(package["improvements"])

    with slides_tab:
        render_slides_tab(package)

    json_output = json.dumps(package, indent=2, ensure_ascii=True)
    txt_output = build_export_text(package)
    pptx_data = build_slides_pptx(package)

    download_col1, download_col2 = st.columns(2)
    with download_col1:
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name="sop_training_output.json",
            mime="application/json",
            use_container_width=True,
        )
    with download_col2:
        st.download_button(
            label="Download TXT",
            data=txt_output,
            file_name="sop_training_output.txt",
            mime="text/plain",
            use_container_width=True,
        )
    st.download_button(
        label="Download PPTX",
        data=pptx_data,
        file_name="sop_training_slides.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
