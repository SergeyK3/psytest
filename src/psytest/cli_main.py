from pathlib import Path
import pandas as pd
from psytest.bank import load_items
from psytest.scoring import score_paei
from psytest.report import render_report


def main():
    base = Path(__file__).resolve().parents[2] / 'data' / 'bank'
    items = load_items(base/'paei_items.csv')
    # Заглушка ответов: все по 4
    resp = pd.DataFrame({'item_id': items['item_id'], 'answer': 4})
    scores = score_paei(items, resp)
    scores_dict = dict(zip(scores['scale'], scores['raw']))
    out = Path(__file__).resolve().parents[2]/'out_report.docx'
    tpl = Path(__file__).resolve().parents[2]/'templates'/'report_template.docx'
    render_report(scores_dict, tpl, out)
    print('Report generated:', out)

if __name__ == '__main__':
    main()
