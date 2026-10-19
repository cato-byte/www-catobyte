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
// Learning guides (.qa-learning) add learn/review mode, review marks, mixed review and section navigation.
document.addEventListener("DOMContentLoaded", () => {
  const tools = document.querySelector(".qa-tools");
  const cards = [...document.querySelectorAll("details.qa")];
  if (!tools || !cards.length) return;
  tools.hidden = false;
  const guide = document.querySelector(".qa-guide");
  const learning = guide.classList.contains("qa-learning");

  // localStorage can be missing or throw (private mode, blocked storage): marks then last for the visit only.
  const store = {
    get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* not persisted */ } },
  };

  tools.querySelector('[data-qa="open"]').addEventListener("click", () => cards.forEach((c) => { if (!c.hidden) c.open = true; }));
  tools.querySelector('[data-qa="close"]').addEventListener("click", () => cards.forEach((c) => { c.open = false; }));

  const input = tools.querySelector("[data-qa-filter]"); // flat guides only
  const status = tools.querySelector("[data-qa-status]");
  const fold = (text) => text.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const texts = cards.map((c) => fold(c.querySelector("summary").textContent + " " + c.querySelector(".qa-answer").textContent));

  // Review marks: "review" or "ok" per question id. Opening an answer is never recorded as progress.
  const marksKey = tools.dataset.storage;
  const marks = learning ? store.get(marksKey, {}) : {};
  const showSelect = tools.querySelector("[data-qa-show]");
  let mixed = null; // Set of cards in the current mixed review, or null

  const paintMark = (card) => {
    const mark = marks[card.id] || "";
    card.dataset.mark = mark;
    card.querySelectorAll("[data-mark]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mark === mark)));
  };

  if (learning) {
    document.querySelector(".qa-marks-note").hidden = false;
    cards.forEach((card) => {
      const bar = document.createElement("p");
      bar.className = "qa-marks";
      for (const [mark, label] of [["review", tools.dataset.markReview], ["ok", tools.dataset.markOk]]) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.mark = mark;
        button.textContent = label;
        button.addEventListener("click", () => {
          if (marks[card.id] === mark) delete marks[card.id]; else marks[card.id] = mark;
          store.set(marksKey, marks);
          paintMark(card);
          if (showSelect && showSelect.value !== "all") apply();
        });
        bar.append(button);
      }
      card.querySelector(".qa-answer").append(bar);
      paintMark(card);
    });
  }

  // Hide headings (flat guides) or units and sections (learning guides) left without visible questions.
  const hideEmptyGroups = () => {
    if (learning) {
      document.querySelectorAll(".qa-learning .unit").forEach((u) => { u.hidden = !u.querySelector("details.qa:not([hidden])"); });
      document.querySelectorAll(".qa-learning .guide-section").forEach((s) => { s.hidden = !s.querySelector(".unit:not([hidden])"); });
      return;
    }
    document.querySelectorAll(".qa-guide h2").forEach((h) => {
      let el = h.nextElementSibling;
      let any = false;
      while (el && el.tagName !== "H2") {
        if (el.matches("details.qa") && !el.hidden) any = true;
        el = el.nextElementSibling;
      }
      h.hidden = !any;
    });
  };

  const apply = () => {
    const words = input ? fold(input.value).split(/\s+/).filter(Boolean) : [];
    const show = showSelect ? showSelect.value : "all";
    let shown = 0;
    cards.forEach((card, i) => {
      const mark = marks[card.id] || "";
      const match = words.every((w) => texts[i].includes(w))
        && (show === "all" || (show === "unmarked" ? !mark : mark === show))
        && (!mixed || mixed.has(card));
      card.hidden = !match;
      if (match) shown += 1;
    });
    const filtering = words.length > 0 || show !== "all" || mixed !== null;
    guide.classList.toggle("is-filtering", filtering);
    hideEmptyGroups();
    if (mixed) {
      const sections = new Set([...mixed].map((c) => c.closest(".guide-section").dataset.section));
      status.textContent = tools.dataset.mixedStatus.replace("{n}", mixed.size).replace("{s}", sections.size);
    } else {
      status.textContent = filtering ? input.dataset.status.replace("{n}", shown) : "";
    }
  };

  let timer;
  input?.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(apply, 120); });

  if (learning) {
    showSelect?.addEventListener("change", apply);

    // Mixed review: ten questions spread over several sections, the ones marked "review again" first.
    const mixedStart = tools.querySelector('[data-qa="mixed"]');
    const mixedEnd = tools.querySelector('[data-qa="mixed-end"]');
    const setMixed = (set) => {
      mixed = set;
      mixedStart.hidden = Boolean(set);
      mixedEnd.hidden = !set;
      cards.forEach((c) => { c.open = false; });
      apply();
      if (set) guide.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    mixedStart.addEventListener("click", () => {
      const shuffled = cards.map((c) => [Math.random() - (marks[c.id] === "review" ? 1 : marks[c.id] === "ok" ? -1 : 0), c])
        .sort((a, b) => a[0] - b[0]).map(([, c]) => c);
      const picked = new Set();
      const perSection = {};
      for (const pass of [2, Infinity]) {
        for (const card of shuffled) {
          const section = card.closest(".guide-section").dataset.section;
          if (picked.size >= 10) break;
          if (picked.has(card) || (perSection[section] || 0) >= pass) continue;
          picked.add(card);
          perSection[section] = (perSection[section] || 0) + 1;
        }
      }
      setMixed(picked);
    });
    mixedEnd.addEventListener("click", () => setMixed(null));

    // Learn mode shows each unit's concept; review mode hides it so the questions come first.
    const modeButtons = [...tools.querySelectorAll("[data-mode]")];
    const setMode = (mode) => {
      guide.dataset.mode = mode;
      modeButtons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mode === mode)));
      store.set("guide-mode", mode);
    };
    modeButtons.forEach((b) => b.addEventListener("click", () => setMode(b.dataset.mode)));
    setMode(store.get("guide-mode", "learn"));

    // Section selector (phones) and sidebar (desktop) follow the section being read.
    const jump = tools.querySelector("[data-qa-jump]");
    jump?.addEventListener("change", () => { location.hash = jump.value; });
    const navLinks = new Map([...document.querySelectorAll("[data-nav-section]")].map((a) => [a.dataset.navSection, a]));
    const setCurrent = (id) => {
      if (jump) jump.value = id;
      navLinks.forEach((a, key) => {
        if (key === id) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
        a.parentElement.classList.toggle("is-current", key === id);
      });
    };
    if ("IntersectionObserver" in window) {
      const visible = new Set();
      const sections = [...document.querySelectorAll(".guide-section")];
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
        const first = sections.find((s) => visible.has(s));
        if (first) setCurrent(first.dataset.section);
      }, { rootMargin: "-40% 0px -55% 0px" });
      sections.forEach((s) => observer.observe(s));
    }
  }

  const openFromHash = () => {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target) return;
    if (target.matches("details.qa")) target.open = true;
    // A "review the concept" link shows the concepts again.
    if (target.matches(".unit-title") && guide.dataset.mode === "review") tools.querySelector('[data-mode="learn"]')?.click();
  };
  window.addEventListener("hashchange", openFromHash);
  openFromHash();
});
