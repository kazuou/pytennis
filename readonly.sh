#!/bin/bash

# 既存のJSONファイルのパス
json_file=".vscode/settings.json"
# ReadOnlyのファイルを探すディレクトリのパス
# directory="/path/to/your/directory"
directory="."
# 一時ファイル
temp_file=$(mktemp)

# 現在の JSON ファイル内容を一時ファイルにコピー
cp "$json_file" "$temp_file"

# ディレクトリ内のすべてのファイルをループ
for file in "$directory"/*; do
  # ファイルのみを対象にする
  if [[ -f "$file" ]]; then
    # ファイルに書き込み権限があるかどうかを確認
    if [[ ! -w "$file" ]]; then
      base_file=$(basename "$file")

      # JSONファイルを更新 (f2 にファイル名をキーとし、true を値として追加。ただし、重複を避ける)
      jq --arg key "$base_file" '
        ."files.readonlyInclude" |= if has($key) then . else . + {($key): true} end
      ' "$temp_file" > "${temp_file}.new"

      # 新しく生成されたファイルを元の一時ファイルに置き換え
      mv "${temp_file}.new" "$temp_file"
    fi
  fi
done

# 更新された内容を確認
cat "$temp_file"

# 一時ファイルの内容で元のJSONファイルを更新
mv "$temp_file" "$json_file"
