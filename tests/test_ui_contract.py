from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
REPORT = (ROOT / "report.py").read_text(encoding="utf-8")


def test_app_ast_and_ultra_theme_contract():
    ast.parse(APP, filename="app.py")
    for token in ["#070B16", "#111827", "backdrop-filter:blur", "@keyframes uhdWave", "@keyframes uhdPulse", "uhd-stepper", "uhd-filler"]:
        assert token in APP


def test_live_ui_value_additions_are_visual_only_contracts():
    assert "render_ultra_waveform()" in APP
    assert "render_speech_analytics(st.session_state.turns)" in APP
    assert "highlight_filler_words(latest_answer)" in APP
    assert "render_ultra_topbar" in APP


def test_report_accepts_all_app_report_kwargs():
    tree = ast.parse(REPORT, filename="report.py")
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in ("build_markdown_report", "build_pdf_report"):
        args = {a.arg for a in funcs[name].args.args}
        for required in ["research", "cv_filename", "jd_filename"]:
            assert required in args


def test_report_contains_complete_output_sections():
    for token in [
        "ATS-readiness estimate",
        "Performance scores",
        "Suggested better answer",
        "Next improvement",
        "Speech analytics",
        "Presentation cues",
        "Complete UI input / output coverage",
    ]:
        assert token in REPORT


def test_session_snapshot_and_report_export_contracts():
    assert "build_session_snapshot" in APP
    assert "Executive session snapshot" in APP
    assert "session_snapshot=snapshot" in APP
    assert "Executive session snapshot" in REPORT
    assert "ATS risk flags" in REPORT


def test_ats_value_additions_contract():
    evidence = (ROOT / "agent_modules" / "evidence_agent.py").read_text(encoding="utf-8")
    for token in ["risk_flags", "source_format", "parseability_signal"]:
        assert token in evidence
