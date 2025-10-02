async function authWithTelegram(authUrl, tg, csrfToken, mainUrl) {
  try {
    let response = await fetch(authUrl, {
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
      window.location.href = mainUrl;
    } else {
      tg.showAlert(`Authorization failed: ${result.error}`);
      tg.close();
    }
  } catch (error) {
    tg.showAlert(`Authorization error: ${error}`);
    tg.close();
  }
}
