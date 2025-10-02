function checkTelegramWebApp(tg) {
  if (typeof tg === "undefined") {
    console.error("Not running inside Telegram WebApp");
    return false;
  }

  if (!tg.initData || tg.initData.length === 0) {
    console.error("Telegram WebApp initData is missing");
    return false;
  }

  return true;
}
