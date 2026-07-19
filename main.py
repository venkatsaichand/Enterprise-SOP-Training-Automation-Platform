import json
import os

import streamlit as st

from prompts import PROMPT_LIBRARY
from utils import (
    build_dependency_install_message,
    build_export_text,
    build_slides_markdown,
    build_slides_pptx,
    extract_text_from_upload,
    generate_sop_training_package,
    get_missing_dependencies,
    normalize_sop_text,
)


st.set_page_config(page_title="AI SOP Training Engine", layout="wide")

def extract_text(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        import PyPDF2
        pdf = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text

    elif file_type == "docx":
        return read_docx(uploaded_file)

    else:
        return None

def render_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-soft: #f8fafc;
            --text: #0f172a;
            --muted: #64748b;
            --border: #e5e7eb;
            --border-strong: #dbe3ec;
            --accent: #111827;
            --accent-hover: #0b1220;
            --success-bg: #ecfdf5;
            --success-border: #bbf7d0;
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
            max-width: 800px;
            padding-top: 4.5rem;
            padding-bottom: 4rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        [data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.75rem;
            padding-left: 1.15rem;
            padding-right: 1.15rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--muted);
        }

        .hero {
            text-align: center;
            margin: 0 auto 3rem auto;
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

        .input-card,
        .output-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 22px;
            box-shadow: var(--shadow);
        }

        .input-card {
            padding: 1.6rem;
            margin-bottom: 2rem;
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

        .stRadio > div {
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .stRadio [role="radiogroup"] {
            display: flex;
            gap: 0.5rem;
        }

        .stRadio [role="radiogroup"] label {
            background: var(--surface-soft);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.6rem 1rem;
        }

        .stRadio [role="radiogroup"] label p {
            color: var(--text);
            font-size: 0.94rem;
            font-weight: 500;
        }

        div[data-testid="stFileUploader"] {
            border: 1px dashed var(--border-strong);
            border-radius: 18px;
            background: var(--surface-soft);
            padding: 0.75rem;
        }

        div[data-testid="stFileUploader"] section {
            padding: 1.1rem 0.85rem;
        }

        div[data-testid="stFileUploader"] small {
            color: var(--muted);
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 360px;
            border: 1px solid var(--border);
            border-radius: 18px;
            background: var(--surface-soft);
            color: var(--text);
            padding: 1rem 1.05rem;
            font-size: 0.97rem;
            line-height: 1.75;
            box-shadow: none;
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: #cbd5e1;
            box-shadow: none;
        }

        .helper-text {
            margin-top: 0.9rem;
            font-size: 0.88rem;
            line-height: 1.7;
            color: #94a3b8;
        }

        .cta-row {
            display: flex;
            justify-content: center;
            margin: 0 0 2.2rem 0;
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

        .stButton > button:focus:not(:active) {
            color: #ffffff;
            border-color: var(--accent);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.45rem;
            margin-bottom: 1rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 40px;
            padding: 0 1rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.72);
            color: var(--muted);
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent) !important;
            color: #ffffff !important;
            border-color: var(--accent) !important;
        }

        .output-card {
            padding: 1.5rem;
            margin-top: 0.65rem;
        }

        .output-title {
            font-size: 1.08rem;
            line-height: 1.2;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text);
            margin-bottom: 1rem;
        }

        .content-row {
            padding: 0.95rem 0;
            border-bottom: 1px solid var(--border);
        }

        .content-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .content-row:first-child {
            padding-top: 0.2rem;
        }

        .content-copy {
            font-size: 0.97rem;
            line-height: 1.8;
            color: #1f2937;
        }

        .step-index {
            display: inline-block;
            min-width: 2rem;
            color: #94a3b8;
            font-weight: 700;
        }

        .quiz-kicker {
            font-size: 0.76rem;
            line-height: 1;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            color: #94a3b8;
            margin-bottom: 0.45rem;
        }

        .downloads {
            margin-top: 1.3rem;
        }

        .stDownloadButton > button {
            height: 2.85rem;
            border-radius: 999px;
            border: 1px solid var(--border);
            background: #ffffff;
            color: var(--text);
        }

        [data-testid="stAlertContainer"] > div {
            border-radius: 16px;
            border: 1px solid var(--border);
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

            .input-card,
            .output-card {
                border-radius: 18px;
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
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown('<div class="output-title">Summary</div>', unsafe_allow_html=True)
    for item in summary:
        st.markdown(f"- {item}")
    st.markdown("</section>", unsafe_allow_html=True)


def render_training_tab(training_steps: list[dict[str, str]]) -> None:
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown('<div class="output-title">Training Guide</div>', unsafe_allow_html=True)
    for index, step in enumerate(training_steps, start=1):
        st.markdown(f"### {index}. {step['title']}")
        st.markdown(f"**Owner:** {step['owner']}")
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        st.markdown(f"**Action:** {step['action']}")
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        st.markdown(f"**Outcome:** {step['outcome']}")
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        st.markdown(f"**Decision Trigger:** {step['decision_trigger']}")
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)


def render_quiz_tab(quiz: list[dict[str, str]]) -> None:
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown('<div class="output-title">Quiz</div>', unsafe_allow_html=True)
    for index, item in enumerate(quiz, start=1):
        st.markdown(f"**Q{index}. {item['question']}**")
        st.markdown(f"- Answer: {item['answer']}")
        st.markdown(f"- Explanation: {item['explanation']}")
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)


def render_list_tab(title: str, items: list[str]) -> None:
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="output-title">{title}</div>', unsafe_allow_html=True)
    for item in items:
        st.markdown(f"- {item}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)


def render_improvements_tab(improvements: list[dict[str, str]]) -> None:
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown('<div class="output-title">Improvements</div>', unsafe_allow_html=True)
    for item in improvements:
        st.markdown(f"- {item['theme']}: {item['improvement']} ({item['impact']})")
    st.markdown("</section>", unsafe_allow_html=True)


def render_slides_tab(package: dict) -> None:
    st.markdown('<section class="output-card">', unsafe_allow_html=True)
    st.markdown('<div class="output-title">Slides</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="content-row">
            <div class="content-copy"><pre>{build_slides_markdown(package)}</pre></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</section>", unsafe_allow_html=True)


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

    st.markdown('<section class="input-card">', unsafe_allow_html=True)
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
        uploaded_file = st.file_uploader("Upload File", type=["txt", "pdf", "docx"], label_visibility="collapsed")
        st.markdown(
            '<div class="helper-text">Upload a `.txt` or `.pdf` SOP file. Extracted content will appear below automatically.</div>',
            unsafe_allow_html=True,
        )
        if uploaded_file is not None:
            extracted_text = extract_text_from_upload(uploaded_file)
            if extracted_text:
                sop_text = extracted_text
    else:
        sop_text = st.text_area(
            "Paste Text",
            placeholder="Paste a standard operating procedure here...",
            height=360,
            label_visibility="collapsed",
        )
        st.markdown(
            '<div class="helper-text">Paste the full SOP text to generate a summary, training guide, and quiz.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    generate_clicked = st.button("Generate Training")
    st.markdown("</div>", unsafe_allow_html=True)

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
    st.success("Training module generated successfully.")
    st.markdown(
        """
<style>
p, li {
    line-height: 1.7;
    margin-bottom: 6px;
}
</style>
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

    json_output = json.dumps(st.session_state.package, indent=2, ensure_ascii=True)
    txt_output = build_export_text(st.session_state.package)
    pptx_data = build_slides_pptx(st.session_state.package)
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
