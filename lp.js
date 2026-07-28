const form = document.querySelector("#order-form");
const note = document.querySelector("#form-note");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  const original = button.textContent;
  button.disabled = true;
  button.textContent = "送信中...";

  const payload = Object.fromEntries(new FormData(form).entries());

  try {
    const response = await fetch("/api/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    note.textContent = result.message || "受付しました。";
    form.reset();
  } catch (error) {
    note.textContent = "送信に失敗しました。時間をおいて再度お試しください。";
  } finally {
    button.disabled = false;
    button.textContent = original;
  }
});
