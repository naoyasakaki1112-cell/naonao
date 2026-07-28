module.exports = async function handler(request, response) {
  if (request.method !== "POST") {
    response.setHeader("Allow", "POST");
    return response.status(405).json({ message: "POST only" });
  }

  const body = request.body || {};
  const required = ["scent", "quantity", "useCase", "name", "email"];
  const missing = required.filter((key) => !body[key]);

  if (missing.length > 0) {
    return response.status(400).json({ message: "必須項目が不足しています。" });
  }

  const resendKey = process.env.RESEND_API_KEY;
  const to = process.env.ORDER_NOTIFICATION_EMAIL;
  const from = process.env.ORDER_FROM_EMAIL || "YOHAKU <onboarding@resend.dev>";

  if (!resendKey || !to) {
    console.log("YOHAKU demo order", body);
    return response.status(202).json({
      message: "デモ受付しました。本番ではVercelの環境変数にRESEND_API_KEYとORDER_NOTIFICATION_EMAILを設定してください。",
    });
  }

  const lines = [
    "YOHAKU 予約相談が届きました。",
    "",
    `香り: ${body.scent}`,
    `本数: ${body.quantity}`,
    `用途: ${body.useCase}`,
    `お名前: ${body.name}`,
    `メール: ${body.email}`,
    "",
    "相談内容:",
    body.message || "なし",
  ];

  const sendResponse = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${resendKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to,
      subject: `YOHAKU予約相談: ${body.name}様`,
      text: lines.join("\n"),
    }),
  });

  if (!sendResponse.ok) {
    const detail = await sendResponse.text();
    console.error("Resend error", detail);
    return response.status(502).json({ message: "通知メールの送信に失敗しました。" });
  }

  return response.status(200).json({ message: "予約相談を受け付けました。担当者からご連絡します。" });
};
