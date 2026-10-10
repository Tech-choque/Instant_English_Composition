"""data/questions.tsv から Anki のデッキ（.apkg）を作る。

表: 日本語（端末の読み上げで日本語を再生）／裏: 英文（端末の読み上げで英語を再生）。
音声ファイルは入れず、Anki の {{tts}} タグで端末の読み上げ機能を使う。

使い方: pip install genanki && python tools/make_anki.py 出力先.apkg
"""
import csv
import sys
from pathlib import Path

import genanki

ROOT = Path(__file__).resolve().parent.parent

# ID を固定しておくと、作り直したデッキを取り込んだときに重複せず上書きされる
MODEL_ID = 1728544001
DECK_ID = 1728544002

CSS = """
.card { font-family: sans-serif; font-size: 24px; text-align: center; line-height: 1.6; }
.ja { font-size: 22px; }
.en { font-size: 26px; font-weight: bold; margin-top: 12px; }
"""

model = genanki.Model(
    MODEL_ID,
    "瞬間英作文（音声）",
    fields=[{"name": "Japanese"}, {"name": "English"}],
    templates=[{
        "name": "日本語→英語",
        "qfmt": '<div class="ja">{{Japanese}}</div>{{tts ja_JP:Japanese}}',
        "afmt": '<div class="ja">{{Japanese}}</div><hr id="answer"><div class="en">{{English}}</div>{{tts en_US:English}}',
    }],
    css=CSS,
)


class Note(genanki.Note):
    @property
    def guid(self):
        # 英文を直しても同じカードとして扱う（学習履歴を残す）ため、日本語だけから作る
        return genanki.guid_for(self.fields[0])


def main(out):
    deck = genanki.Deck(DECK_ID, "瞬間英作文")
    with open(ROOT / "data" / "questions.tsv", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            deck.add_note(Note(model=model, fields=[row["ja"], row["en"]]))
    genanki.Package(deck).write_to_file(out)
    print(f"{len(deck.notes)}枚 → {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eisakubun.apkg")
