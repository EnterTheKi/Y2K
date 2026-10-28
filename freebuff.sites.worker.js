export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let path = url.pathname;
    if (path.endsWith("/")) path += "index.html";

    const res = await env.ASSETS.fetch(new Request(new URL(path + url.search, url.origin), request));

    // not on the branch — show the owl's 404 (with the real 404 status)
    if (res.status === 404 && path !== "/404.html") {
      const nf = await env.ASSETS.fetch(new URL("/404.html", url.origin));
      return new Response(nf.body, { status: 404, headers: nf.headers });
    }
    return res;
  }
};
