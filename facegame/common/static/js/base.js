function url(name, c) {
  try {
    return URLS_BASE.slice(0,-1) + dutils.urls.resolve(name, c);
  } catch(e) {
    // API out-of-sync
    console.log("INVALID URLPATTERN", name, c);
    return '#?invalid='+name;
  }
}
