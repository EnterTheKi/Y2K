export default {
  async fetch(request, env) {
    // the asset router already serves "/" via index.html and
    // pretty-redirects /blog.html -> /blog; let it speak first
    const res = await env.ASSETS.fetch(request);

    // not on the branch — show the owl's 404 (with the real 404 status)
    if (res.status === 404) {
      const nf = await env.ASSETS.fetch(new URL("/404.html", new URL(request.url).origin));
      return new Response(nf.body, { status: 404, headers: nf.headers });
    }
    return res;
  }
};
