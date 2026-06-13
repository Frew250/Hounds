(function () {
  const FAQ = [
    {
      keywords: ["hello", "hi", "hey", "hiya", "howdy", "greetings", "sup"],
      reply:
        "Hey there! I'm Hounds_Bot — your guide to all things Hounds of Cuchulain. Ask me about shows, booking, music, or anything else!",
    },
    {
      keywords: ["show", "gig", "concert", "perform", "tour", "upcoming", "next", "date"],
      reply:
        "Check the Shows section on this page for our next six dates, or hit 'View all shows' for the full list. We play venues across Vancouver Island and beyond!",
    },
    {
      keywords: ["book", "booking", "hire", "event", "festival", "wedding", "private", "venue"],
      reply:
        "We'd love to play your event! Email Wolf at hounds.of.cuchulain@gmail.com. We're available for festivals, theatres, pubs, and private events.",
    },
    {
      keywords: ["album", "music", "song", "track", "listen", "cd", "vinyl", "bandcamp", "spotify", "stream", "download"],
      reply:
        "Stream us on Spotify or support us directly on Bandcamp. Physical CDs are available at shows and by mail order — see the Shop section for details!",
    },
    {
      keywords: ["merch", "shirt", "hoodie", "clothing", "gear", "hat", "tote"],
      reply:
        "Shirts, hoodies, and more branded with Hounds artwork — head to the Shop section to see what's in stock.",
    },
    {
      keywords: ["contact", "email", "reach", "message", "get in touch", "inquiry"],
      reply:
        "Email Wolf at hounds.of.cuchulain@gmail.com. We aim to reply within 2–3 business days.",
    },
    {
      keywords: ["about", "band", "members", "who", "story", "history", "origin"],
      reply:
        "The Hounds of Cuchulain are a Celtic folk band based in Victoria, BC. We blend traditional Irish and Scottish reels, jigs, and ballads with gritty modern songwriting — big choruses, rowdy singalongs, and moments of quiet storytelling. Check the About section for the full story!",
    },
    {
      keywords: ["instagram", "facebook", "social", "follow", "twitter", "tiktok"],
      reply:
        "Find us on Instagram @hounds_of_cuchulain and Facebook at facebook.com/hounds.of.cuchulain. We post show updates, new music, and band life regularly.",
    },
    {
      keywords: ["victoria", "bc", "island", "vancouver", "location", "where", "based"],
      reply:
        "We're based in Victoria, BC on Vancouver Island and tour across the island and beyond. Want us somewhere specific? Drop us a line!",
    },
    {
      keywords: ["epk", "press", "media", "photo", "bio", "promo"],
      reply:
        "Our EPK has our bio, photos, and everything press needs. Hit the EPK link in the navigation at the top of the page.",
    },
    {
      keywords: ["ticket", "tickets", "buy", "purchase", "admission", "price", "cost"],
      reply:
        "Ticket info varies by show — click a date in the Shows section to see the Get Tickets link for that gig.",
    },
    {
      keywords: ["celtic", "folk", "irish", "scottish", "gaelic", "style", "genre", "sound", "music"],
      reply:
        "We play Celtic folk rooted in Irish and Scottish tradition — fiddles, whistles, and big singalong choruses — with original songs woven in. It's a session and a show all at once.",
    },
  ];

  const FALLBACK =
    "Good question! For anything specific, email Wolf at hounds.of.cuchulain@gmail.com. Sláinte! 🍺";

  function getReply(text) {
    const lower = text.toLowerCase();
    for (const entry of FAQ) {
      if (entry.keywords.some((kw) => lower.includes(kw))) return entry.reply;
    }
    return FALLBACK;
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // ── Build DOM ──────────────────────────────────────────────────────────────
  const widget = document.createElement("div");
  widget.id = "hc-widget";
  widget.innerHTML = `
    <button class="hc-fab" id="hcToggle" aria-label="Chat with Hounds Bot" aria-expanded="false">
      <svg class="hc-fab-icon hc-icon-chat" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 2H4C2.9 2 2 2.9 2 4v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
      <svg class="hc-fab-icon hc-icon-close" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
      <span class="hc-fab-label">Chat</span>
    </button>
    <div class="hc-window" id="hcWindow" aria-hidden="true" role="dialog" aria-label="Chat with Hounds Bot">
      <div class="hc-header">
        <div class="hc-header-left">
          <div class="hc-avatar" aria-hidden="true">🐺</div>
          <div class="hc-header-text">
            <span class="hc-bot-name">Hounds_Bot</span>
            <span class="hc-bot-status">Online</span>
          </div>
        </div>
        <button class="hc-close" id="hcClose" aria-label="Close chat">&times;</button>
      </div>
      <div class="hc-messages" id="hcMessages" role="log" aria-live="polite" aria-label="Chat messages"></div>
      <div class="hc-suggestions" id="hcSuggestions">
        <button class="hc-chip">Upcoming shows</button>
        <button class="hc-chip">Book the band</button>
        <button class="hc-chip">Our music</button>
      </div>
      <div class="hc-input-row">
        <input class="hc-input" id="hcInput" type="text" placeholder="Ask me anything…" autocomplete="off" aria-label="Message" maxlength="300" />
        <button class="hc-send" id="hcSend" aria-label="Send message">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

  const toggle = document.getElementById("hcToggle");
  const win = document.getElementById("hcWindow");
  const closeBtn = document.getElementById("hcClose");
  const input = document.getElementById("hcInput");
  const sendBtn = document.getElementById("hcSend");
  const msgContainer = document.getElementById("hcMessages");
  const chips = document.getElementById("hcSuggestions");

  let isOpen = false;
  let greeted = false;

  // ── Message helpers ────────────────────────────────────────────────────────
  function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `hc-msg hc-msg--${sender}`;
    if (sender === "bot") {
      msg.innerHTML = `<span class="hc-prefix">Hounds_Bot:</span> ${escapeHtml(text)}`;
    } else {
      msg.textContent = text;
    }
    msgContainer.appendChild(msg);
    msgContainer.scrollTop = msgContainer.scrollHeight;
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "hc-msg hc-msg--bot hc-typing";
    el.id = "hcTyping";
    el.innerHTML = `<span class="hc-prefix">Hounds_Bot:</span> <span class="hc-dots"><span></span><span></span><span></span></span>`;
    msgContainer.appendChild(el);
    msgContainer.scrollTop = msgContainer.scrollHeight;
  }

  function removeTyping() {
    const el = document.getElementById("hcTyping");
    if (el) el.remove();
  }

  // ── Open / Close ───────────────────────────────────────────────────────────
  function openChat() {
    isOpen = true;
    win.classList.add("open");
    win.setAttribute("aria-hidden", "false");
    toggle.setAttribute("aria-expanded", "true");
    toggle.classList.add("is-open");
    if (!greeted) {
      greeted = true;
      setTimeout(() => {
        addMessage(
          "Dia dhuit! I'm Hounds_Bot — ask me about shows, booking, our music, or anything else about the band.",
          "bot"
        );
      }, 250);
    }
    setTimeout(() => input.focus(), 50);
  }

  function closeChat() {
    isOpen = false;
    win.classList.remove("open");
    win.setAttribute("aria-hidden", "true");
    toggle.setAttribute("aria-expanded", "false");
    toggle.classList.remove("is-open");
  }

  // ── Send ───────────────────────────────────────────────────────────────────
  function handleSend(text) {
    const msg = (text || input.value).trim();
    if (!msg) return;
    addMessage(msg, "user");
    input.value = "";
    chips.style.display = "none";
    showTyping();
    setTimeout(() => {
      removeTyping();
      addMessage(getReply(msg), "bot");
    }, 600);
  }

  // ── Events ─────────────────────────────────────────────────────────────────
  toggle.addEventListener("click", () => (isOpen ? closeChat() : openChat()));
  closeBtn.addEventListener("click", closeChat);
  sendBtn.addEventListener("click", () => handleSend());
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") handleSend(); });
  chips.addEventListener("click", (e) => {
    if (e.target.classList.contains("hc-chip")) handleSend(e.target.textContent);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && isOpen) closeChat(); });
})();
