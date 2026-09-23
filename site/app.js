(function () {
  "use strict";
  var DATA = window.APP_DATA;
  var CATS = DATA.categories;
  var CAT_LABEL = {};
  CATS.forEach(function (c) { CAT_LABEL[c.id] = c.label; });
  var CAT_COLOR = {
    pulpar: "var(--accent)",
    periapical_aguda: "var(--danger)",
    periapical_cronica: "var(--gold)",
    disseminacao: "var(--plum)",
    osteomielite: "var(--blue)",
    geral: "var(--ink-soft)"
  };
  var CAT_SOFT = {
    pulpar: "var(--accent-soft)",
    periapical_aguda: "var(--danger-soft)",
    periapical_cronica: "var(--gold-soft)",
    disseminacao: "var(--plum-soft)",
    osteomielite: "var(--blue-soft)",
    geral: "var(--surface-2)"
  };

  function storage(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { /* privado/bloqueado: ignora */ }
  }

  /* ---------------- theme ---------------- */
  function applyTheme(t) {
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    else document.documentElement.removeAttribute("data-theme");
  }
  (function initTheme() {
    var saved = storage("pp_theme");
    if (saved) applyTheme(saved);
    document.getElementById("themeToggle").addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme");
      var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      var effectiveDark = current ? current === "dark" : prefersDark;
      var next = effectiveDark ? "light" : "dark";
      applyTheme(next);
      storage("pp_theme", next);
    });
  })();

  var state = {
    mode: storage("pp_mode") || "flashcards",
    category: storage("pp_cat") || "all",
    flashOrder: [],
    flashIndex: 0,
    quizOrder: [],
    quizIndex: 0,
    quizScore: 0,
    quizAnswered: false
  };

  function filteredDiseases() {
    if (state.category === "all") return DATA.diseases;
    return DATA.diseases.filter(function (d) { return d.categoria === state.category; });
  }
  function filteredQuiz() {
    if (state.category === "all") return DATA.quiz;
    return DATA.quiz.filter(function (q) { return q.categoria === state.category; });
  }
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function mediaHTML(d, photoClass) {
    if (d.foto) {
      return '<div class="dg-frame photo ' + (photoClass || "") + '">' +
        '<img src="' + d.foto.file + '" alt="' + d.foto.caption.replace(/"/g, "&quot;") + '" loading="lazy">' +
        "</div>";
    }
    return '<div class="dg-frame">' + d.svg + "</div>";
  }
  function creditHTML(d) {
    if (!d.foto) return "";
    var isUrl = /^https?:\/\//.test(d.foto.source || "");
    var srcHTML = isUrl
      ? '<a href="' + d.foto.source + '" target="_blank" rel="noopener">fonte</a>'
      : d.foto.source;
    return '<p style="font-size:11px;color:var(--ink-faint);text-align:center;margin:6px 0 0;line-height:1.4;">' +
      'Foto: ' + d.foto.author + " &middot; " + d.foto.license +
      " &middot; " + srcHTML + "</p>";
  }

  /* ---------------- chips ---------------- */
  function renderChips() {
    var bar = document.getElementById("filterbar");
    bar.innerHTML = "";
    bar.appendChild(mkChip("all", "Todas", DATA.diseases.length));
    CATS.forEach(function (c) {
      var n = DATA.diseases.filter(function (d) { return d.categoria === c.id; }).length;
      bar.appendChild(mkChip(c.id, c.label, n));
    });
  }
  function mkChip(id, label, n) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "chip"; b.textContent = label;
    var span = document.createElement("span");
    span.className = "n"; span.textContent = n;
    b.appendChild(span);
    b.dataset.active = state.category === id ? "true" : "false";
    b.addEventListener("click", function () {
      state.category = id; storage("pp_cat", id);
      resetFlash(); resetQuiz();
      renderChips(); renderAll();
    });
    return b;
  }

  /* ---------------- flashcards ---------------- */
  function resetFlash() {
    state.flashOrder = filteredDiseases().map(function (d) { return d.id; });
    state.flashIndex = 0;
  }
  function currentCard() {
    var list = filteredDiseases();
    if (!list.length) return null;
    var id = state.flashOrder[state.flashIndex];
    return list.find(function (d) { return d.id === id; }) || list[0];
  }
  function renderFlash() {
    var list = filteredDiseases();
    var card = document.getElementById("flashcard");
    if (!list.length) {
      document.getElementById("deckCount").textContent = "0 / 0";
      card.hidden = true;
      return;
    }
    card.hidden = false;
    card.dataset.flipped = "false";
    var d = currentCard();
    document.getElementById("deckCount").textContent = (state.flashIndex + 1) + " / " + list.length;
    var cat = document.getElementById("frontCat");
    cat.textContent = CAT_LABEL[d.categoria];
    cat.style.background = CAT_SOFT[d.categoria]; cat.style.color = CAT_COLOR[d.categoria];
    document.getElementById("frontImg").outerHTML = mediaHTML(d).replace('class="dg-frame', 'id="frontImg" class="dg-frame');
    document.getElementById("frontResumo").textContent = d.resumo;
    document.getElementById("backName").textContent = d.nome;
    document.getElementById("backBody").innerHTML = [
      ["Características clínicas", d.clinico],
      ["Localização típica", d.localizacao],
      ["Causa / etiologia", d.etiologia],
      ["Sintomas", d.sintomas],
      ["Testes / vitalidade", d.testes],
      ["Radiografia", d.radiografico],
      ["Tratamento", d.tratamento],
      ["Como diferenciar", d.diferenciar]
    ].map(function (sec) {
      return '<div class="bk"><span class="lbl">' + sec[0] + "</span><p>" + sec[1] + "</p></div>";
    }).join("") + creditHTML(d);
  }
  function stepFlash(delta) {
    var list = filteredDiseases();
    if (!list.length) return;
    state.flashIndex = (state.flashIndex + delta + list.length) % list.length;
    renderFlash();
  }

  /* ---------------- quiz ---------------- */
  function resetQuiz() {
    state.quizOrder = shuffle(filteredQuiz());
    state.quizIndex = 0; state.quizScore = 0; state.quizAnswered = false;
    document.getElementById("quizEnd").hidden = true;
    document.getElementById("quizActive").hidden = false;
  }
  function renderQuiz() {
    var list = state.quizOrder;
    var activeBox = document.getElementById("quizActive");
    if (!list.length) {
      activeBox.hidden = true;
      document.getElementById("quizEnd").hidden = true;
      return;
    }
    if (state.quizIndex >= list.length) { finishQuiz(); return; }
    activeBox.hidden = false;
    document.getElementById("quizEnd").hidden = true;
    var q = list[state.quizIndex];
    document.getElementById("quizCounter").textContent = (state.quizIndex + 1) + " / " + list.length;
    document.getElementById("quizBar").style.width = Math.round(state.quizIndex / list.length * 100) + "%";
    document.getElementById("quizScore").textContent = "Acertos: " + state.quizScore;
    var media = document.getElementById("quizMedia");
    if (q.foto) {
      media.hidden = false;
      media.innerHTML = '<div class="dg-frame photo"><img src="' + q.foto.file + '" alt="" loading="lazy"></div>';
    } else if (q.kind === "image") {
      media.hidden = false;
      media.innerHTML = '<div class="dg-frame">' + q.svg + "</div>";
    } else {
      media.hidden = true; media.innerHTML = "";
    }
    document.getElementById("quizPrompt").textContent = q.prompt;
    var wrap = document.getElementById("quizOptions");
    wrap.innerHTML = "";
    var letters = ["A", "B", "C", "D"];
    q.options.forEach(function (opt, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "qopt";
      b.innerHTML = '<span class="k">' + letters[i] + "</span><span>" + opt + "</span>";
      b.addEventListener("click", function () { answerQuiz(opt, b); });
      wrap.appendChild(b);
    });
    document.getElementById("quizFeedback").hidden = true;
    document.getElementById("quizNext").hidden = true;
    state.quizAnswered = false;
  }
  function answerQuiz(chosen, btnEl) {
    if (state.quizAnswered) return;
    state.quizAnswered = true;
    var q = state.quizOrder[state.quizIndex];
    var correct = chosen === q.correct;
    if (correct) state.quizScore++;
    Array.prototype.forEach.call(document.querySelectorAll(".qopt"), function (b) {
      b.disabled = true;
      var label = b.querySelector("span:last-child").textContent;
      if (label === q.correct) b.dataset.state = "correct";
      else if (b === btnEl) b.dataset.state = "wrong";
    });
    var fb = document.getElementById("quizFeedback");
    fb.hidden = false;
    fb.className = "quiz-feedback " + (correct ? "ok" : "bad");
    fb.innerHTML = "<b>" + (correct ? "Correto." : "Não é isso.") + "</b> " + q.explain;
    document.getElementById("quizScore").textContent = "Acertos: " + state.quizScore;
    document.getElementById("quizNext").hidden = false;
  }
  function finishQuiz() {
    document.getElementById("quizActive").hidden = true;
    var end = document.getElementById("quizEnd");
    end.hidden = false;
    var total = state.quizOrder.length;
    document.getElementById("quizFinalScore").textContent = state.quizScore + "/" + total;
    var pct = total ? Math.round(state.quizScore / total * 100) : 0;
    var msg = pct >= 80 ? "Muito bem — você está pronto(a) para a prova."
      : pct >= 50 ? "Bom começo. Revise os cartões das questões erradas."
        : "Vale revisar os flashcards antes de tentar de novo.";
    document.getElementById("quizFinalMsg").textContent = pct + "% de acertos. " + msg;
  }

  /* ---------------- table ---------------- */
  function renderTable() {
    var q = (document.getElementById("tableSearch").value || "").toLowerCase();
    var list = filteredDiseases().filter(function (d) {
      if (!q) return true;
      var hay = [d.nome, d.aparenciaCurta, d.localizacao, d.causaCurta, d.tratamentoCurto, d.clinico].join(" ").toLowerCase();
      return hay.indexOf(q) !== -1;
    });
    var tbody = document.getElementById("tableBody");
    if (!list.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-msg">Nenhuma doença encontrada.</td></tr>';
      return;
    }
    tbody.innerHTML = list.map(function (d) {
      return "<tr>"
        + '<td class="cat-dot"><span class="dot" style="background:' + CAT_COLOR[d.categoria] + '" title="' + CAT_LABEL[d.categoria] + '"></span></td>'
        + '<td class="name">' + d.nome + "</td>"
        + "<td>" + d.aparenciaCurta + "</td>"
        + "<td>" + d.localizacao + "</td>"
        + "<td>" + d.causaCurta + "</td>"
        + "<td>" + d.tratamentoCurto + "</td>"
        + "</tr>";
    }).join("");
  }

  /* ---------------- mode switching ---------------- */
  function renderAll() {
    if (state.mode === "flashcards") { if (!state.flashOrder.length) resetFlash(); renderFlash(); }
    if (state.mode === "quiz") { if (!state.quizOrder.length) resetQuiz(); renderQuiz(); }
    if (state.mode === "table") { renderTable(); }
  }
  function setMode(mode) {
    state.mode = mode; storage("pp_mode", mode);
    Array.prototype.forEach.call(document.querySelectorAll(".modebar button"), function (b) {
      var on = b.dataset.mode === mode;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    ["flashcards", "quiz", "table"].forEach(function (m) {
      document.getElementById("view-" + m).classList.toggle("active", m === mode);
    });
    renderAll();
  }

  /* ---------------- wire up ---------------- */
  Array.prototype.forEach.call(document.querySelectorAll(".modebar button"), function (b) {
    b.addEventListener("click", function () { setMode(b.dataset.mode); });
  });
  document.getElementById("flashcard").addEventListener("click", function () {
    var flipped = this.dataset.flipped === "true";
    this.dataset.flipped = flipped ? "false" : "true";
  });
  document.getElementById("flipBtn").addEventListener("click", function () {
    document.getElementById("flashcard").click();
  });
  document.getElementById("prevBtn").addEventListener("click", function () { stepFlash(-1); });
  document.getElementById("nextBtn").addEventListener("click", function () { stepFlash(1); });
  document.getElementById("shuffleBtn").addEventListener("click", function () {
    state.flashOrder = shuffle(state.flashOrder); state.flashIndex = 0; renderFlash();
  });
  document.getElementById("quizNext").addEventListener("click", function () {
    state.quizIndex++; renderQuiz();
  });
  document.getElementById("quizRestart").addEventListener("click", function () {
    resetQuiz(); renderQuiz();
  });
  document.getElementById("tableSearch").addEventListener("input", renderTable);
  document.addEventListener("keydown", function (e) {
    if (state.mode !== "flashcards") return;
    if (e.key === "ArrowLeft") stepFlash(-1);
    if (e.key === "ArrowRight") stepFlash(1);
    if (e.key === " ") { e.preventDefault(); document.getElementById("flashcard").click(); }
  });

  renderChips();
  setMode(state.mode);
})();
