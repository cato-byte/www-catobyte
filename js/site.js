// Loaded in <head> without defer: the class below must be set before first paint
// so the collapsed mobile menu doesn't flash open.
document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  const setOpen = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  };

  toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && nav.classList.contains("is-open")) {
      setOpen(false);
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header")) setOpen(false);
  });
});

// Study guides: expand/collapse all answers, filter questions, open a question linked by #id.
document.addEventListener("DOMContentLoaded", () => {
  const tools = document.querySelector(".qa-tools");
  const cards = [...document.querySelectorAll("details.qa")];
  if (!tools || !cards.length) return;
  tools.hidden = false;

  tools.querySelector('[data-qa="open"]').addEventListener("click", () => cards.forEach((c) => { if (!c.hidden) c.open = true; }));
  tools.querySelector('[data-qa="close"]').addEventListener("click", () => cards.forEach((c) => { c.open = false; }));

  const input = tools.querySelector("[data-qa-filter]");
  const status = tools.querySelector("[data-qa-status]");
  const headings = [...document.querySelectorAll(".qa-guide h2")];
  const fold = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const texts = cards.map((c) => fold(c.textContent));
  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const words = fold(input.value).split(/\s+/).filter(Boolean);
      let shown = 0;
      cards.forEach((card, i) => {
        const match = words.every((w) => texts[i].includes(w));
        card.hidden = !match;
        if (match) shown += 1;
      });
      // Hide a category heading when none of its questions match.
      headings.forEach((h) => {
        let el = h.nextElementSibling;
        let any = false;
        while (el && el.tagName !== "H2") {
          if (el.matches("details.qa") && !el.hidden) any = true;
          el = el.nextElementSibling;
        }
        h.hidden = !any;
      });
      status.textContent = words.length ? input.dataset.status.replace("{n}", shown) : "";
    }, 120);
  });

  const openFromHash = () => {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target && target.matches("details.qa")) target.open = true;
  };
  window.addEventListener("hashchange", openFromHash);
  openFromHash();
});
