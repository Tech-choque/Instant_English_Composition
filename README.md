# Instant English Composition

スマホで使う、瞬間英作文と発音チェックの試作。

## 2つのページ

| ページ | 置き場所 | やること |
| --- | --- | --- |
| 瞬間英作文 | claude.ai の Artifact（ソースは `artifact/eisakubun.html`） | お題を出す／答えの例／Claudeの添削（本人のプランで動く） |
| 発音チェック | GitHub Pages（`index.html`） | Azureのお手本音声／録音して音素ごとに採点 |

分けている理由: Artifactの中ではマイクが使えず、Azureへの通信もページの制限（CSP）で止められる（2026-10-10、Android の Claude アプリで確認）。
逆に GitHub Pages のページからは Claude を呼べない。そこで、瞬間英作文のページから発音チェックのページへ、英文をリンクで渡している（`?text=英文&ja=お題`）。

## Azureのキー

- コードにもリポジトリにも入れない。発音チェックのページで本人が入力し、その端末のブラウザ（localStorage）にだけ保存する
- リージョンは `japaneast`

## 使っているもの

- `vendor/speech-sdk/`: Microsoft の Speech SDK（ブラウザ版）1.51.0。npm パッケージから、再配布が許されているファイルだけを置いている（`REDIST.txt`）

## Anki（通勤中に音声だけで回す）

- `data/questions.tsv`: お題と英文（Artifact の12問と同じ）
- `tools/make_anki.py`: ここから `.apkg` を作る。表は日本語、裏は英文で、どちらも端末の読み上げ（Anki の `{{tts}}`）で再生する
- 作った `.apkg` はリポジトリに入れない（`.gitignore`）
