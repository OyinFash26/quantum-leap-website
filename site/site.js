// Quantum Leap Management Services: shared page behaviour.
(function () {
  var WHATSAPP = [["2348023032178", "0802 303 2178"], ["2348163117579", "0816 311 7579"]];

  // Mobile menu
  var btn = document.querySelector(".menu-btn"), nav = document.querySelector("nav.main");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
  }

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Copy buttons
  function selectNear(el) {
    var t = el.parentNode.querySelector(".val, pre");
    if (!t) return;
    var r = document.createRange(); r.selectNodeContents(t);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }
  function copyText(text, el) {
    var done = function () { var t = el.textContent; el.textContent = "Copied"; setTimeout(function () { el.textContent = t; }, 1500); };
    try { navigator.clipboard.writeText(text).then(done, function () { selectNear(el); }); }
    catch (e) { selectNear(el); }
  }
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () { copyText(b.dataset.copy, b); });
  });

  // Pre-tick a service when arriving from a service link, e.g. contact.html#janitorial
  var form = document.getElementById("requestForm");
  if (!form) return;
  var pre = { audit: "s-audit", facility: "s-fm", janitorial: "s-jan", "post-construction": "s-pcc", "real-estate": "s-re" }[location.hash.slice(1)];
  if (pre) { var c = document.getElementById(pre); if (c) c.checked = true; }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var err = document.getElementById("q-err");
    var name = form.elements.name.value.trim(), phone = form.elements.phone.value.trim();
    var svcs = Array.prototype.filter.call(form.querySelectorAll("[name=svc]"), function (c) { return c.checked; }).map(function (c) { return c.value; });
    var missing = [];
    if (!name) missing.push("your name");
    if (!phone) missing.push("a phone or WhatsApp number");
    if (!svcs.length) missing.push("at least one service");
    if (missing.length) { err.textContent = "Add " + missing.join(", ") + " so we can get back to you."; err.hidden = false; return; }
    err.hidden = true;

    var area = form.elements.area.value.trim(), notes = form.elements.notes.value.trim();
    var lines = [
      "Hello Quantum Leap, I'd like to make a request.",
      "Name: " + name,
      "Phone: " + phone,
      "Property: " + form.elements.type.value + (area ? ", " + area : ""),
      "Services: " + svcs.join(", ")
    ];
    if (notes) lines.push("Details: " + notes);
    var msg = lines.join("\n");

    var box = document.createElement("div");
    box.className = "ready";
    box.innerHTML = '<b>Your request is ready to send</b><span>Send it to either of our WhatsApp numbers, or copy it into an email to Quantumleapm@yahoo.com.</span><pre></pre><div class="row"></div>';
    box.querySelector("pre").textContent = msg;
    var row = box.querySelector(".row");
    WHATSAPP.forEach(function (w) {
      var a = document.createElement("a");
      a.className = "btn btn-primary"; a.target = "_blank"; a.rel = "noopener";
      a.href = "https://wa.me/" + w[0] + "?text=" + encodeURIComponent(msg);
      a.textContent = "Send to " + w[1];
      row.appendChild(a);
    });
    var cb = document.createElement("button");
    cb.className = "btn btn-ghost"; cb.type = "button"; cb.textContent = "Copy message";
    row.appendChild(cb);
    cb.addEventListener("click", function () { copyText(msg, cb); });
    var old = form.querySelector(".ready"); if (old) old.remove();
    form.appendChild(box);
    box.scrollIntoView({ block: "nearest" });
  });
})();

// Careers: hide jobs whose closing date has passed (the build also skips them; this covers days between builds)
(function () {
  var jobs = document.querySelectorAll(".job[data-closes]");
  if (!jobs.length) return;
  var d = new Date(), today = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  var open = 0;
  jobs.forEach(function (j) {
    var c = j.getAttribute("data-closes");
    if (c && c < today) j.hidden = true; else open++;
  });
  var empty = document.querySelector(".no-jobs");
  if (empty && !open) empty.hidden = false;
})();
