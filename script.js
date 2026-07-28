const quantityInput = document.querySelector("#quantity");
const [decreaseButton, increaseButton] = document.querySelectorAll(".quantity-control button");
const checkoutButton = document.querySelector(".checkout-button");

function setQuantity(nextValue) {
  const min = Number(quantityInput.min);
  const max = Number(quantityInput.max);
  const value = Math.min(max, Math.max(min, nextValue));
  quantityInput.value = String(value);
}

decreaseButton.addEventListener("click", () => {
  setQuantity(Number(quantityInput.value) - 1);
});

increaseButton.addEventListener("click", () => {
  setQuantity(Number(quantityInput.value) + 1);
});

checkoutButton.addEventListener("click", () => {
  checkoutButton.textContent = "予約カートに追加しました";
  checkoutButton.dataset.added = "true";

  window.setTimeout(() => {
    checkoutButton.textContent = "予約カートに入れる";
    checkoutButton.dataset.added = "false";
  }, 2200);
});
