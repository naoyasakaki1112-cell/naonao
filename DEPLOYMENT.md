# GitHub + Vercel Deployment

YOHAKU LPをGitHubとVercelで運用するための手順です。

## 1. GitHubリポジトリを作る

GitHubで新規リポジトリを作成します。

推奨:

- Repository name: `yohaku-lp`
- Visibility: 最初は `Private`
- READMEや.gitignoreは追加しない

作成後、GitHubが表示するHTTPS URLを控えます。

例:

```text
https://github.com/<your-account>/yohaku-lp.git
```

## 2. ローカルからGitHubへpush

このフォルダで以下を実行します。

```powershell
.\scripts\connect-github.ps1 -RepositoryUrl "https://github.com/<your-account>/yohaku-lp.git"
```

認証を求められた場合は、GitHubのブラウザ認証またはPersonal Access Tokenを使います。

## 3. VercelでGitHubリポジトリをImport

Vercelで以下を選びます。

1. Add New Project
2. Import Git Repository
3. `yohaku-lp` を選択
4. Framework Presetは `Other`
5. Build Commandは空でOK
6. Output Directoryも空でOK
7. Deploy

`vercel.json` で `/` は `lp.html` に向くように設定済みです。

## 4. 予約フォームの通知メール設定

本番でメール通知を使う場合、VercelのProject Settingsで以下の環境変数を設定します。

```text
RESEND_API_KEY=...
ORDER_NOTIFICATION_EMAIL=予約相談を受け取るメールアドレス
ORDER_FROM_EMAIL=YOHAKU <your-verified-domain@example.com>
```

未設定でもフォームはデモ受付として動きます。

## 5. 自動デプロイ

VercelのGitHub連携だけで自動デプロイします。

`main` ブランチにpushすると、Vercelが自動で再デプロイします。
GitHub ActionsやGitHub Secretsの設定は不要です。

## 6. 更新運用

LPの文言や画像を変更したら、以下の流れです。

```powershell
git add .
git commit -m "Update YOHAKU LP"
git push
```

VercelのGitHub連携、またはGitHub Actionsが自動で再デプロイします。
