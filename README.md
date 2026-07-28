# YOHAKU LP

受注生産の和ルームディフューザー `YOHAKU` のLPです。

## 公開構成

- `lp.html`: 公開用LP
- `lp.css`: LPスタイル
- `lp.js`: 予約フォーム送信
- `api/order.js`: Vercel Functionsの予約受付API
- `assets/`: 商品画像
- `.github/workflows/vercel.yml`: GitHub ActionsからVercelへ本番デプロイ
- `vercel.json`: Vercel設定

## GitHub + Vercelでデプロイする流れ

1. GitHubで新規リポジトリを作成
2. このフォルダをGitHubへpush
3. VercelでそのGitHubリポジトリをImport
4. VercelのProject Settingsで環境変数を設定
5. `main` ブランチへpushすると自動デプロイ

## Vercel環境変数

予約フォームの通知メールを本番運用する場合は、Vercelに以下を設定してください。

- `RESEND_API_KEY`: ResendのAPIキー
- `ORDER_NOTIFICATION_EMAIL`: 予約相談を受け取るメールアドレス
- `ORDER_FROM_EMAIL`: 送信元メールアドレス。未設定時はResendのテスト送信元を使います

GitHub Actionsからデプロイする場合は、GitHub Secretsに以下も設定してください。

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

VercelのGitHub連携だけで運用する場合、GitHub Actionsは使わなくても構いません。
