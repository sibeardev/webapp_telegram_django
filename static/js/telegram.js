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

function setTheme(tg) {
  const htmlTag = document.documentElement;
  if (!tg || !tg.colorScheme) return;

  if (tg.colorScheme === "light") {
    htmlTag.classList.remove("dark");
    htmlTag.classList.add("light");
  } else {
    htmlTag.classList.remove("light");
    htmlTag.classList.add("dark");
  }
}
