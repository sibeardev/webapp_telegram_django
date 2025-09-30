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

async function authWithTelegram(url, tg, csrfToken) {
  try {
    let response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        initData: tg.initData,
        initDataUnsafe: tg.initDataUnsafe,
      }),
    });

    let result = await response.json();
    if (result.ok) {
      window.location.href = "/";
    } else {
      tg.showAlert(`Authorization failed: ${result.error}`);
      tg.close();
    }
  } catch (error) {
    tg.showAlert(`Authorization error: ${error}`);
    tg.close();
  }
}
