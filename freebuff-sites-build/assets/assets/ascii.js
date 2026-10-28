/* KIAZAKI — quiet machinery: theme, glitch, readout */

(function () {
  "use strict";

  /* theme toggle */
  var btn = document.getElementById("themeToggle");
  if (btn) {
    btn.addEventListener("click", function () {
      var root = document.documentElement;
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("kiazaki-theme", next); } catch (e) {}
    });
  }

  /* subtle char corruption on big ascii blocks (hero only) */
  var owl = document.getElementById("heroOwl");
  if (owl) {
    var glitches = "·.:*~+|-_=/\\:;".split("");

    function textNodes(el, acc) {
      for (var i = 0; i < el.childNodes.length; i++) {
        var n = el.childNodes[i];
        if (n.nodeType === 3 && n.data.trim()) acc.push(n);
        else if (n.nodeType === 1) textNodes(n, acc);
      }
      return acc;
    }

    function glitchOnce() {
      var nodes = textNodes(owl, []);
      if (!nodes.length) { schedule(); return; }
      var node = nodes[Math.floor(Math.random() * nodes.length)];
      var s = node.data;
      var idx = Math.floor(Math.random() * s.length);
      if (/\s/.test(s[idx])) { schedule(); return; }
      var original = s[idx];
      node.data = s.slice(0, idx) + glitches[Math.floor(Math.random() * glitches.length)] + s.slice(idx + 1);
      setTimeout(function () {
        var cur = node.data;
        node.data = cur.slice(0, idx) + original + cur.slice(idx + 1);
        schedule();
      }, 140 + Math.random() * 160);
    }

    function schedule() {
      setTimeout(glitchOnce, 3500 + Math.random() * 4500);
    }
    schedule();
  }

  /* neon sign — spells KIAZAKI letter by letter, drifts, blacks out, repeats */
  var neon = document.querySelector(".hero .neon");
  if (neon) {
    var letters = Array.prototype.slice.call(neon.querySelectorAll("span"));
    var still = false;
    try { still = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

    if (!still && letters.length) {
      var tend = function (fn, ms) { return setTimeout(fn, ms); };

      /* all tubes dead until the sign ignites */
      letters.forEach(function (s) { s.classList.add("off"); });

      function lightOne(k, order, done) {
        var s = letters[order[k]];
        s.classList.remove("off"); /* tube strikes */
        tend(function () {
          if (Math.random() < 0.45) { /* fights, dips, then holds */
            s.classList.add("off");
            tend(function () { s.classList.remove("off"); done(); }, 70 + Math.random() * 160);
          } else { done(); }
        }, 40 + Math.random() * 130);
      }

      function igniteOrder() {
        var order = [0, 1, 2, 3, 4, 5, 6];
        if (Math.random() < 0.18) { /* sometimes the tubes misfire the spelling */
          for (var i = order.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var t = order[i]; order[i] = order[j]; order[j] = t;
          }
        }
        return order;
      }

      function ignite(k, order) {
        if (k >= order.length) { tend(wayward, 4200 + Math.random() * 2800); return; }
        lightOne(k, order, function () {
          tend(function () { ignite(k + 1, order); }, 330 + Math.random() * 240);
        });
      }

      function wayward() {
        var n = 1 + Math.floor(Math.random() * 3);
        (function next(d) {
          if (d >= n) { tend(blackout, 1200 + Math.random() * 1800); return; }
          var s = letters[Math.floor(Math.random() * letters.length)];
          s.classList.add("off");
          tend(function () { s.classList.remove("off"); next(d + 1); }, 90 + Math.random() * 280);
        })(0);
      }

      function blackout() {
        letters.forEach(function (s) { s.classList.add("off"); });
        tend(function () { ignite(0, igniteOrder()); }, 900 + Math.random() * 1000);
      }

      blackout();
    }
  }

  /* 33:27 readout ticker */
  var readout = document.getElementById("readout");
  if (readout) {
    var spin = "/\\|";
    var i = 0;
    setInterval(function () {
      i = (i + 1) % spin.length;
      readout.textContent = "[ 33:27 ]  " + spin[i] + "  気 on-air  " + spin[i] + "  [ 33:27 ]";
    }, 240);
  }
})();
