#!/bin/bash

# スクリプトを厳密に実行するモード（エラー発生時にスクリプトを停止）
set -e

# 作業ディレクトリの変更
# cd /path/to/your/repo (必要に応じてコメントを外して使用)

# 1. 現在のステータスの確認
echo "現在のGitステータスを表示します:"
git status

# 2. 変更の追加
echo "全ての変更をステージングします..."
git add .

# 3. コミットメッセージの取得
read -p "コミットメッセージを入力してください: " commit_message

# 4. コミットを作成
echo "コミットを作成中: '$commit_message'"
git commit -m "$commit_message"

# 5. リモートリポジトリへのプッシュ
current_branch=$(git branch --show-current)
echo "リモートリポジトリにプッシュしています（ブランチ: $current_branch）..."
git push origin $current_branch
#git push origin master    masterは最初のブランチ。手元のデータ。 originはリモートリポジトリのデフオルト
#orgin/master は　リモートにあるmaster

# 6. ブランチのリセットとクリーンアップ
# echo "ローカルリポジトリのリセットとクリーンアップを行います..."
# git reset --hard
# git clean -fd

echo "Git操作が完了しました。"

#source deactivate
