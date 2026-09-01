from pathlib import Path

from enhanced_pdf_report import DesignConfig, EnhancedPDFReportV2


def test_full_pdf_uses_bundled_regular_and_bold_dejavu_for_cyrillic(safe_tmp_path):
    charts_dir = safe_tmp_path / "charts"
    output = safe_tmp_path / "full_cyrillic_report.pdf"
    generator = EnhancedPDFReportV2(
        template_dir=charts_dir,
        include_questions_section=True,
    )
    interpretations = {
        "paei": "Кириллическая интерпретация управленческих ролей.",
        "disc": "Описание поведения и взаимодействия.",
        "hexaco": "Описание личностных качеств.",
        "soft_skills": "Коммуникация, лидерство и работа в команде.",
        "general": "Общее заключение и рекомендации.",
    }

    result, drive_link = generator.generate_enhanced_report(
        participant_name="Тестовый Участник",
        test_date="2026-09-01 12:00",
        paei_scores={"P": 7.0, "A": 6.0, "E": 8.0, "I": 5.0},
        disc_scores={"D": 7.0, "I": 6.0, "S": 5.0, "C": 4.0},
        hexaco_scores={"H": 4.0, "E": 3.0, "X": 5.0, "A": 4.0, "C": 5.0, "O": 3.0},
        soft_skills_scores={
            "Коммуникация": 8.0,
            "Работа в команде": 7.0,
            "Лидерство": 6.0,
            "Критическое мышление": 7.0,
            "Управление временем": 6.0,
            "Стрессоустойчивость": 8.0,
            "Восприимчивость к критике": 5.0,
            "Адаптивность": 8.0,
            "Решение проблем": 7.0,
            "Креативность": 6.0,
        },
        ai_interpretations=interpretations,
        out_path=output,
        user_answers={"paei": {}, "disc": {}, "hexaco": {}, "soft_skills": {}},
    )

    pdf_bytes = output.read_bytes()
    assert result == output
    assert drive_link is None
    assert output.stat().st_size > 10_000
    assert DesignConfig.BODY_FONT == "PsyTest-DejaVuSans"
    assert DesignConfig.TITLE_FONT == "PsyTest-DejaVuSans-Bold"
    assert b"DejaVuSans" in pdf_bytes
    assert Path("fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf").is_file()
    assert Path("fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Bold.ttf").is_file()
