// Basic interactivity and dynamic content for The Hounds of Cuchulain site

// NAV TOGGLE
const nav = document.querySelector(".nav");
const navToggle = document.querySelector(".nav-toggle");
const mobileNav = document.getElementById("mobileNav");
const mobileNavLinks = mobileNav ? mobileNav.querySelectorAll("a") : [];
const navBackdrop = document.querySelector(".nav-backdrop");
const navLinks = document.querySelectorAll(".nav-list a");

function closeNav() {
  nav.classList.remove("open");
  navToggle.setAttribute("aria-expanded", "false");
  if (mobileNav) { mobileNav.classList.remove("open"); mobileNav.setAttribute("aria-hidden", "true"); }
  if (navBackdrop) navBackdrop.classList.remove("visible");
  document.body.style.overflow = "";
}

if (nav && navToggle) {
  navToggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    if (mobileNav) { mobileNav.classList.toggle("open", isOpen); mobileNav.setAttribute("aria-hidden", String(!isOpen)); }
    if (navBackdrop) navBackdrop.classList.toggle("visible", isOpen);
    document.body.style.overflow = isOpen ? "hidden" : "";
  });

  mobileNavLinks.forEach((link) => link.addEventListener("click", closeNav));

  const mobileNavClose = mobileNav ? mobileNav.querySelector(".mobile-nav-close") : null;
  if (mobileNavClose) mobileNavClose.addEventListener("click", closeNav);

  if (navBackdrop) navBackdrop.addEventListener("click", closeNav);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) closeNav();
  });
}

// SMOOTH SCROLL FOR BUTTONS WITH data-scroll-target
document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;

  const scrollTarget = target.dataset.scrollTarget;
  if (!scrollTarget) return;

  const destination = document.querySelector(scrollTarget);
  if (destination) {
    event.preventDefault();
    destination.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

// DYNAMIC SHOWS LIST (home and Shows page)
// Data comes from global window.showsData defined in shows-data.js
const showsListEl = document.querySelector(".shows-list");
const showsDetailBodyEl = document.querySelector(".shows-detail-body");
const showsScope = showsListEl ? showsListEl.getAttribute("data-shows-scope") || "upcoming" : "upcoming";
let renderedShows = [];

function parseShowDate(show) {
  // Expect formats like "Jan 15, 2026"
  const parsed = Date.parse(show.date);
  return Number.isNaN(parsed) ? new Date() : new Date(parsed);
}

function isUpcomingShow(show) {
  const showDate = parseShowDate(show);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return showDate.getTime() >= today.getTime();
}

function getSortedShows() {
  if (!Array.isArray(window.showsData)) return [];

  return [...window.showsData].sort(
    (a, b) => parseShowDate(a).getTime() - parseShowDate(b).getTime()
  );
}

function getShowsForCurrentView() {
  const sortedShows = getSortedShows();
  return showsScope === "all" ? sortedShows : sortedShows.filter(isUpcomingShow);
}

function getDefaultShowIndex(shows) {
  if (!shows.length) return -1;

  const nextUpcomingIndex = shows.findIndex(isUpcomingShow);
  if (nextUpcomingIndex !== -1) return nextUpcomingIndex;

  return shows.length - 1;
}

function getShowStatus(show) {
  const isPast = !isUpcomingShow(show);

  if (isPast) {
    return {
      isPast: true,
      className: "show-status show-status--past",
      label: show.pastLabel || "Played",
      href: null,
      external: false,
    };
  }

  if (show.status === "soldout") {
    return {
      isPast: false,
      className: "show-status show-status--soldout",
      label: "Sold Out",
      href: null,
      external: false,
    };
  }

  if (show.status === "call") {
    return {
      isPast: false,
      className: "show-status show-status--call",
      label: "Call to reserve",
      href: show.phone ? `tel:${show.phone}` : null,
      external: false,
    };
  }

  if (show.status === "info") {
    return {
      isPast: false,
      className: "show-status",
      label: show.statusLabel || "Details coming soon",
      href: show.infoUrl && show.infoUrl !== "#" ? show.infoUrl : null,
      external: Boolean(show.infoUrl && show.infoUrl !== "#"),
    };
  }

  return {
    isPast: false,
    className: "show-status show-status--tickets",
    label: "Get Tickets",
    href: show.ticketUrl && show.ticketUrl !== "#" ? show.ticketUrl : null,
    external: true,
  };
}

function renderShows() {
  if (!showsListEl || !showsDetailBodyEl || !Array.isArray(window.showsData)) return;

  showsListEl.innerHTML = "";

  const allShows = getShowsForCurrentView();

  const limitAttr = showsListEl.getAttribute("data-shows-limit");
  const limit = limitAttr ? Number(limitAttr) : NaN;
  renderedShows =
    Number.isFinite(limit) && limit > 0 ? allShows.slice(0, limit) : allShows;

  renderedShows.forEach((show, index) => {
    const showStatus = getShowStatus(show);
    const card = document.createElement("button");
    card.type = "button";
    card.className = showStatus.isPast ? "show-card show-card--past" : "show-card";
    card.setAttribute("data-index", String(index));

    const badgeHtml = showStatus.href
      ? `<a href="${showStatus.href}" class="${showStatus.className}" ${showStatus.external ? 'target="_blank" rel="noopener noreferrer"' : ""} onclick="event.stopPropagation()">${showStatus.label}</a>`
      : `<span class="${showStatus.className}">${showStatus.label}</span>`;

    card.innerHTML = `
      <div>
        <div class="show-date">${show.date}</div>
      </div>
      <div>
        <div class="show-city">${show.city}</div>
        <div class="show-venue">${show.venue}</div>
      </div>
      ${badgeHtml}
    `;

    card.addEventListener("click", () => {
      selectShow(index);
    });

    showsListEl.appendChild(card);
  });

  const defaultIndex = getDefaultShowIndex(renderedShows);

  if (defaultIndex !== -1) {
    selectShow(defaultIndex, { scrollList: showsScope === "all" });
  }
}

function formatPhone(digits) {
  const d = digits.replace(/\D/g, "");
  return d.length === 10
    ? `(${d.slice(0, 3)}) ${d.slice(3, 6)}-${d.slice(6)}`
    : digits;
}

function selectShow(index, options = {}) {
  if (!showsDetailBodyEl || !showsListEl) return;

  const show = renderedShows[index];
  if (!show) return;

  const showStatus = getShowStatus(show);

  showsListEl.querySelectorAll(".show-card").forEach((card) => {
    card.classList.toggle(
      "is-selected",
      card.getAttribute("data-index") === String(index)
    );
  });

  if (options.scrollList) {
    const selectedCard = showsListEl.querySelector(`.show-card[data-index="${index}"]`);
    if (selectedCard) {
      selectedCard.scrollIntoView({ block: "center", behavior: "auto" });
    }
  }

  const timeFragment = show.time ? `<p><strong>Time:</strong> ${show.time}</p>` : "";

  const callFragment = show.phone
    ? `<a href="tel:${show.phone}" class="show-status show-status--call">Call to reserve: ${formatPhone(show.phone)}</a>`
    : `<span class="show-status show-status--call">Call to reserve</span>`;

  const infoFragment = showStatus.href
    ? `<a href="${showStatus.href}" class="btn btn-outline" ${showStatus.external ? 'target="_blank" rel="noopener noreferrer"' : ""}>${showStatus.label}</a>`
    : `<span class="${showStatus.className}">${showStatus.label}</span>`;

  showsDetailBodyEl.innerHTML = `
    <p><strong>Date:</strong> ${show.date}</p>
    <p><strong>City:</strong> ${show.city}</p>
    <p><strong>Venue:</strong> ${show.venue}</p>
    ${timeFragment}
    <p>${show.description}</p>
    ${
      showStatus.isPast
        ? `<span class="${showStatus.className}">${showStatus.label}</span>`
        : show.status === "tickets"
        ? `<a href="${show.ticketUrl}" class="btn btn-outline" target="_blank" rel="noopener noreferrer">Get Tickets</a>`
        : show.status === "call"
          ? callFragment
          : show.status === "info"
            ? infoFragment
          : `<span class="show-status show-status--soldout">Sold Out</span>`
    }
  `;

  showsDetailBodyEl.hidden = false;

  const detailIntro = showsDetailBodyEl.previousElementSibling;
  if (detailIntro && detailIntro.classList.contains("muted")) {
    detailIntro.remove();
  }
}

renderShows();

// ACTIVE NAV LINK ON SCROLL
const sections = document.querySelectorAll("main section[id]");

function updateActiveNav() {
  const scrollY = window.scrollY;
  const offset = 120;

  let currentSectionId = null;
  sections.forEach((section) => {
    const rect = section.getBoundingClientRect();
    const top = rect.top + scrollY - offset;
    const bottom = top + section.offsetHeight;

    if (scrollY >= top && scrollY < bottom) {
      currentSectionId = section.id;
    }
  });

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || !href.startsWith("#")) return;
    const id = href.slice(1);
    link.classList.toggle("active", id === currentSectionId);
  });
}

window.addEventListener("scroll", () => {
  window.requestAnimationFrame(updateActiveNav);
});

updateActiveNav();

// GALLERY LIGHTBOX
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const lightboxClose = document.getElementById("lightboxClose");
const lbPrevBtn = document.getElementById("lightboxPrev");
const lbNextBtn = document.getElementById("lightboxNext");
let lbImages = [];
let lbIndex = 0;

if (lightbox && lightboxImg) {
  document.addEventListener("click", (e) => {
    if (e.target.closest(".gallery-grid") && e.target.tagName === "IMG") {
      lbImages = Array.from(document.querySelectorAll(".gallery-grid img"));
      lbIndex = lbImages.indexOf(e.target);
      openLightbox();
    }
  });

  function openLightbox() {
    const img = lbImages[lbIndex];
    if (!img) return;
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    if (lbPrevBtn) lbPrevBtn.disabled = lbIndex === 0;
    if (lbNextBtn) lbNextBtn.disabled = lbIndex === lbImages.length - 1;
  }

  function closeLightbox() {
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    lightboxImg.src = "";
    document.body.style.overflow = "";
  }

  if (lbPrevBtn) lbPrevBtn.addEventListener("click", (e) => { e.stopPropagation(); if (lbIndex > 0) { lbIndex--; openLightbox(); } });
  if (lbNextBtn) lbNextBtn.addEventListener("click", (e) => { e.stopPropagation(); if (lbIndex < lbImages.length - 1) { lbIndex++; openLightbox(); } });
  if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) closeLightbox(); });
  document.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("open")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft" && lbIndex > 0) { lbIndex--; openLightbox(); }
    if (e.key === "ArrowRight" && lbIndex < lbImages.length - 1) { lbIndex++; openLightbox(); }
  });
}

// FOOTER YEAR
const yearEl = document.getElementById("year");
if (yearEl) {
  yearEl.textContent = String(new Date().getFullYear());
}

