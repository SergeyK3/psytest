import streamlit as st
import pandas as pd
from pathlib import Path
from tempfile import TemporaryDirectory

from psytest.bank import load_items
from psytest.scoring import score_paei, score_disc, score_hexaco
from psytest.report import render_report
from psytest.report_pdf import render_pdf
from psytest.charts import make_radar

st.set_page_config(page_title="Психологическое тестирование (PAEI → DISC → HEXACO)", layout="wide")

BASE = Path(__file__).resolve().parents[2]
BANK = BASE / "data" / "bank"
INTERP = BASE / "data" / "interpretations"
TPL = BASE / "templates" / "report_template.docx"

# --- INIT STATE
if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}   # {test_id: {item_id: answer}}
if "scores" not in st.session_state:
    st.session_state.scores = {}    # {test_id: {scale: raw}}

def norm_0_60(items_df: pd.DataFrame, scores_raw: dict) -> dict:
    items_per_scale = items_df.groupby("scale")["item_id"].count().to_dict()
    max_per_scale = {k: v * 5 for k, v in items_per_scale.items()}
    return {s: round(v * 60.0 / max(max_per_scale.get(s, 1), 1), 2) for s, v in scores_raw.items()}

def run_test(test_id: str, items_path: Path, title: str, key_prefix: str):
    st.header(title)
    items = load_items(items_path).copy()
    items["item_id"] = items["item_id"].astype(int)

    with st.form(f"{key_prefix}_form", clear_on_submit=False):
        for _, row in items.iterrows():
            st.slider(
                label=str(row["text"]),
                min_value=1, max_value=5, value=3, step=1,
                key=f"{key_prefix}_q_{int(row['item_id'])}"
            )
        submitted = st.form_submit_button("Рассчитать")

    if not submitted:
        return False  # not finished

    # собрать ответы
    ans = {int(i): int(st.session_state[f"{key_prefix}_q_{int(i)}"]) for i in items["item_id"]}
    st.session_state.answers[test_id] = ans

    # посчитать баллы
    df_resp = pd.DataFrame({"item_id": list(ans.keys()), "answer": list(ans.values())})
    if test_id == "PAEI":
        df_scores = score_paei(items, df_resp)
        interp_csv = INTERP / "interpretations_paei.csv"
    elif test_id == "DISC":
        df_scores = score_disc(items, df_resp)
        interp_csv = INTERP / "interpretations_disc.csv"
    else:
        df_scores = score_hexaco(items, df_resp)
        interp_csv = INTERP / "interpretations_hexaco.csv"

    st.subheader("Результаты (сырые баллы)")
    st.dataframe(df_scores, use_container_width=True)

    # словари баллов
    scores_raw = dict(zip(df_scores["scale"], df_scores["raw"]))
    st.session_state.scores[test_id] = scores_raw
    scaled = norm_0_60(items, scores_raw)

    # радар
    labels = sorted(scores_raw.keys())
    values = [scaled[s] for s in labels]
    with TemporaryDirectory() as tmpd:
        tmp = Path(tmpd)
        chart_path = tmp / f"{test_id}_radar.png"
        make_radar(labels, values, chart_path)
        st.image(str(chart_path), caption=f"Профиль {test_id} (нормирован 0..60)")

        # DOCX
        docx_path = tmp / f"Отчёт_{test_id}.docx"
        render_report(
            scores_raw=scores_raw,
            items_df=items,
            interpretations_path=interp_csv,
            template_path=TPL,
            out_path=docx_path,
            title=f"Отчёт по психологическому тестированию ({test_id})",
            participant="Код участника: ______",
        )
        with open(docx_path, "rb") as f:
            st.download_button(f"⬇️ Скачать DOCX ({test_id})", data=f.read(),
                               file_name=f"Отчёт_{test_id}.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # PDF
        pdf_path = tmp / f"Отчёт_{test_id}.pdf"
        render_pdf(scores_raw, chart_path, pdf_path, title=f"Отчёт ({test_id})")
        with open(pdf_path, "rb") as f:
            st.download_button(f"⬇️ Скачать PDF ({test_id})", data=f.read(),
                               file_name=f"Отчёт_{test_id}.pdf", mime="application/pdf")

    st.info("Нажмите «Далее», чтобы перейти к следующему тесту.")
    return True

# --- PROGRESS HEADER
steps_names = {1: "PAEI", 2: "DISC", 3: "HEXACO", 4: "Готово"}
st.progress((st.session_state.step - 1) / 3)
st.caption(f"Шаг {st.session_state.step}/4: {steps_names[st.session_state.step]}")

# --- SEQUENTIAL FLOW
done = False
if st.session_state.step == 1:
    done = run_test("PAEI", BANK/"paei_items.csv", "Тест 1/3 — PAEI", "paei")
elif st.session_state.step == 2:
    done = run_test("DISC", BANK/"disc_items.csv", "Тест 2/3 — DISC", "disc")
elif st.session_state.step == 3:
    done = run_test("HEXACO", BANK/"hexaco_items.csv", "Тест 3/3 — HEXACO", "hexaco")
else:
    st.header("Готово 🎉")
    st.write("Вы прошли все тесты. Ниже — краткая сводка по результатам.")
    for test_id, scores in st.session_state.scores.items():
        st.write(f"**{test_id}**:", scores)
    st.button("Начать заново", on_click=lambda: (st.session_state.clear(), None))

if done and st.session_state.step < 3:
    st.button("Далее →", on_click=lambda: setattr(st.session_state, "step", st.session_state.step + 1))
elif done and st.session_state.step == 3:
    st.button("Завершить →", on_click=lambda: setattr(st.session_state, "step", 4))
