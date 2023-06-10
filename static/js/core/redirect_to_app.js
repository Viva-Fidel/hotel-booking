function redirectToApp() {
    // Set default app URL
    var appUrl = "/";

    // Get user agent and convert to lower case
    var userAgent = navigator.userAgent.toLowerCase();

    // If user agent contains "iphone" or "ipad", redirect to App Store for iOS
    if (
      userAgent.indexOf("iphone") !== -1 ||
      userAgent.indexOf("ipad") !== -1
    ) {
      window.location.href = "https://apps.apple.com/ru/app/";
    }

    // If user agent contains "android", redirect to Google Play Store for Android
    else if (userAgent.indexOf("android") !== -1) {
      window.location.href = "https://play.google.com/store/apps/";
    }

    // If user agent contains "windows", redirect to the default app URL
    else if (userAgent.indexOf("windows") !== -1) {
      window.location.href = appUrl;
    }

    // For all other user agents, redirect to the default app URL
    else {
      window.location.href = appUrl;
    }
  }