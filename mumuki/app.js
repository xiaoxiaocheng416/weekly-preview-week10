const data = window.referenceData;
const visualHookGroupsData = window.visualHookGroupsData || [];
const app = document.querySelector("#app");

const lanceSkitSkeleton = {
  title: "Old solution fails → product gives visible proof",
  creator: "@lanceshopfinds1",
  sourceTitle: "Product Solves the Annoying Part",
  localVideo: "assets/videos/skit-lanceshopfinds1-7618446657650314509.mp4",
  thesis: "The video is not selling mouthwash first. It sells the belief that the viewer's current solution looks normal but is not actually doing the job.",
  coreMechanic: "Accuse the problem → let the person defend their current habit → prove that habit fails → hand them the product → show a visible result.",
  skeleton: [
    ["Problem accusation", "No wonder your breath stinks so bad."],
    ["Defensive response", "My breath stinks?"],
    ["Existing habit defense", "Am I not supposed to rinse my mouth out with mouthwash?"],
    ["Old solution rejection", "But you're using American mouthwash. That does nothing for you, by the way."],
    ["Skeptic response", "Really?"],
    ["Failed proof of old solution", "Yeah. And look, as you spit, nothing comes out."],
    ["Curiosity gap", "Wait, there's something that's supposed to come out?"],
    ["Product handoff", "Yes. Try this."],
    ["Product identity question", "What is this?"],
    ["Product category / authority", "This is Japanese mouthwash."],
    ["Simple mechanism", "It actually pulls that gunk and dirt out of your mouth."],
    ["Demo action", "He uses the product on camera."],
    ["Visible proof / reaction", "Ew. Oh, my gosh. You see that? What the heck?"],
    ["Proof explanation", "All that plaque, gunk and build up comes right out with that brand."],
    ["Belief shift", "I've never seen a mouthwash actually pull that."],
    ["Immediate benefit", "My breath smells so much better."],
    ["Authority line", "In Japan, they actually take their oral care seriously."],
    ["Price objection", "Is this expensive? Like 40, $50?"],
    ["Price reassurance", "No, it's actually very affordable."],
    ["TikTok Shop CTA", "I'll leave a link down below in the orange shopping cart."]
  ],
  slotMap: [
    ["(problem)", "breath stinks → dull skin / flat skin / tired-looking skin"],
    ["(current solution)", "American mouthwash → raw banana / raw honey directly on face"],
    ["(old solution failure)", "nothing comes out → raw banana or honey is not formulated skincare, so the effect is not concentrated enough"],
    ["(product identity)", "Japanese mouthwash → Korean Honey Banana BDRN Ampoule"],
    ["(visible proof)", "gunk comes out → ampoule texture, glow finish, plumper-looking skin"],
    ["(authority)", "Japan takes oral care seriously → K-beauty knows how to make glow wearable"]
  ],
  mumukiDirection: [
    "Keep the two-person interruption.",
    "Open on someone putting raw banana or honey directly on their face.",
    "Do not pitch MUMUKI first.",
    "Attack the raw ingredient version as not strong or formulated enough, not just messy.",
    "Use “Try this” as the reveal.",
    "Position MUMUKI as the formulated BDRN + collagen version of that ingredient idea.",
    "Show ampoule texture immediately after reveal.",
    "Proof is visual: finish, glow, spread, skin look.",
    "CTA stays short."
  ]
};

const scriptIdeaSections = [
  {
    title: "Skit",
    count: "1 skeleton",
    href: "#/script-idea/skit",
    note: "Two-person setup. Old solution fails. Product reveal gives proof."
  },
  {
    title: "Talking Head 01",
    count: "coming next",
    href: "#/script-idea/talking-head-01",
    note: "Creator explains the angle directly."
  },
  {
    title: "Talking Head 02",
    count: "coming next",
    href: "#/script-idea/talking-head-02",
    note: "Creator uses proof and product logic."
  }
];

const skitSkeletonBeats = [
  {
    title: "Callout",
    original: "No wonder your breath stinks so bad.",
    meaning: "Start with a direct problem callout."
  },
  {
    title: "Defensive reaction",
    original: "My breath stinks?",
    meaning: "Let the other person push back."
  },
  {
    title: "Existing habit defense",
    original: "Am I not supposed to rinse my mouth out with mouthwash?",
    meaning: "They explain the thing they already do."
  },
  {
    title: "Old solution attack",
    original: "You're using American mouthwash. That does nothing for you.",
    meaning: "Attack the current solution, not the person."
  },
  {
    title: "Proof old solution fails",
    original: "Look, as you spit, nothing comes out.",
    meaning: "Show why the old solution is weak."
  },
  {
    title: "Curiosity gap",
    original: "Wait, there's something that's supposed to come out?",
    meaning: "Create the gap before showing the product."
  },
  {
    title: "Product reveal",
    original: "Yes. Try this.",
    meaning: "Only reveal the product after the viewer understands the gap."
  },
  {
    title: "Simple mechanism",
    original: "It actually pulls that gunk and dirt out of your mouth.",
    meaning: "Explain the mechanism in one plain sentence."
  },
  {
    title: "Visible proof",
    original: "Ew. Oh my gosh. You see that?",
    meaning: "The result has to be visible on camera."
  },
  {
    title: "Benefit + CTA",
    original: "My breath smells so much better. Link in the orange cart.",
    meaning: "Close with the benefit and buying path."
  }
];

function route() {
  const hash = window.location.hash || "#/";
  const path = hash.replace(/^#/, "");

  if (path.startsWith("/skit/")) {
    renderSkitDetail(path.split("/").pop());
  } else if (path.startsWith("/reference-video/")) {
    renderReferenceCategory(path.split("/").pop());
  } else if (path === "/reference-video") {
    renderReferenceVideo();
  } else if (path === "/visual-hook-bank" || path === "/visual-hook-grouping") {
    renderVisualHookGrouping();
  } else if (path === "/script-idea/skit") {
    renderSkitScriptIdea();
  } else if (path.startsWith("/script-idea/talking-head")) {
    renderComingSoonScriptIdea(path);
  } else if (path === "/script-idea") {
    renderScriptIdea();
  } else {
    renderHome();
  }

  setActiveNav(path === "/visual-hook-grouping" ? "/visual-hook-bank" : path);
}

function setActiveNav(path) {
  document.querySelectorAll(".nav a").forEach((link) => {
    const target = link.dataset.route;
    const isActive = target === "/" ? path === "/" : path.startsWith(target);
    link.classList.toggle("is-active", isActive);
  });
}

function renderHome() {
  app.innerHTML = `
    <section class="page home-page">
      <div class="product-hero">
        <figure class="product-image-card">
          <img src="assets/thumbnail-ampoule.webp" alt="MUMUKI Honey Banana BDRN Ampoule">
        </figure>

        <div class="product-copy">
          <p class="eyebrow">Hero product</p>
          <h1>MUMUKI Honey Banana BDRN Ampoule</h1>
          <p class="hero-note">
            Banana natural t0x is already super viral on TikTok.
            MUMUKI turns banana + honey skincare into a Korean glass-skin ampoule.
          </p>

          <div class="hot-points">
            <article>
              <span>01</span>
              <strong>What is BDRN?</strong>
              <p>Honey Banana PDRN + collagen.</p>
            </article>
            <article>
              <span>02</span>
              <strong>Plumper looking skin</strong>
            </article>
            <article>
              <span>03</span>
              <strong>Firmer looking skin</strong>
            </article>
            <article>
              <span>04</span>
              <strong>Glass glow</strong>
            </article>
          </div>
        </div>
      </div>
    </section>
  `;
}

function renderReferenceVideo() {
  app.innerHTML = `
    <section class="page">
      <div class="page-header">
        <div>
          <p class="eyebrow">Reference library</p>
          <h1>Reference Video</h1>
        </div>
      </div>

      <div class="category-grid">
        ${categoryCard("Viral Non TikTokShop Video", "viral", data.viralNonTikTokShop.length)}
        ${categoryCard("Talking Head", "talking-head", data.talkingHead.length)}
        ${categoryCard("Skit", "skit", data.skit.length)}
      </div>
    </section>
  `;
}

function categoryCard(title, slug, count) {
  return `
    <a class="category-card" href="#/reference-video/${slug}">
      <p class="eyebrow">${count} references</p>
      <h2>${title}</h2>
    </a>
  `;
}

function renderReferenceCategory(slug) {
  const config = getReferenceConfig(slug);

  app.innerHTML = `
    <section class="page">
      <a class="back-link" href="#/reference-video">← Back to Reference Video</a>
      <div class="page-header">
        <div>
          <p class="eyebrow">Reference Video</p>
          <h1>${config.title}</h1>
        </div>
        <p class="small-note">${config.items.length} references</p>
      </div>

      <div class="gallery-grid">
        ${config.items.map((item, index) => universalGalleryCard(item, index, config.type)).join("")}
      </div>
    </section>
  `;

  refreshTikTokEmbed();
}

function renderVisualHookGrouping() {
  const totalClips = visualHookGroupsData.reduce((sum, group) => sum + group.items.length, 0);

  app.innerHTML = `
    <section class="page visual-hook-page">
      <div class="page-header">
        <div>
          <p class="eyebrow">Banana & Honey Clips</p>
          <h1>Visual Hook Bank</h1>
        </div>
        <p class="small-note">${visualHookGroupsData.length} groups. ${totalClips} selected clips.</p>
      </div>

      <div class="group-stack">
        ${visualHookGroupsData.map((group) => hookGroupSection(group)).join("")}
      </div>
    </section>
  `;
}

function hookGroupSection(group) {
  return `
    <section class="hook-group-section" id="${group.id}">
      <div class="hook-group-head">
        <div>
          <span class="group-chip">${group.label}</span>
          <h2>${group.title}</h2>
          <p>${group.why}</p>
        </div>
        <strong>${group.items.length} clips</strong>
      </div>

      <div class="hook-gallery-grid">
        ${group.items.map((item) => hookClipCard(item)).join("")}
      </div>
    </section>
  `;
}

function hookClipCard(item) {
  const start = item.startSeconds ?? "";
  const end = item.endSeconds ?? "";
  const time = start !== "" && end !== "" ? `${Number(start).toFixed(1)}-${Number(end).toFixed(1)}s` : "";
  const priority = item.clipPriority ? `P${item.clipPriority}` : "Clip";

  return `
    <article class="hook-card">
      <div class="hook-video">
        <video class="local-video" controls preload="metadata" playsinline>
          <source src="${item.clipPath}" type="video/mp4">
        </video>
      </div>
      <div class="hook-body">
        <div class="hook-meta-row">
          <span class="meta">${item.creator}</span>
          <span class="pill">${priority}</span>
        </div>
        <h3>${item.title}</h3>
        <p>${time}</p>
      </div>
    </article>
  `;
}

function getReferenceConfig(slug) {
  const map = {
    "viral": {
      title: "Viral Non TikTokShop Video",
      items: data.viralNonTikTokShop,
      type: "viral"
    },
    "talking-head": {
      title: "Talking Head",
      items: data.talkingHead,
      type: "talking"
    },
    "skit": {
      title: "Skit",
      items: data.skit,
      type: "skit"
    }
  };

  return map[slug] || map.viral;
}

function universalGalleryCard(item, index, type) {
  const video = item.localVideo
    ? localVideo(item)
    : item.url && item.videoId
      ? tiktokEmbed(item)
      : `<div class="empty-video">Add reference video</div>`;
  const bodyContent = `
    <p class="meta">${item.creator || item.source || type}</p>
    <h3>${item.title}</h3>
    <span class="pill">${item.status}</span>
  `;
  const body = type === "skit"
    ? `<a class="gallery-body gallery-link-body" href="#/skit/${item.id}">${bodyContent}</a>`
    : `<div class="gallery-body">${bodyContent}</div>`;

  return `
    <article class="gallery-card ${type === "skit" ? "is-clickable" : ""}">
      <div class="gallery-video">
        ${video}
      </div>
      ${body}
    </article>
  `;
}

function renderSkitDetail(id) {
  const item = data.skit.find((entry) => entry.id === id);
  if (!item) {
    renderReferenceVideo();
    return;
  }

  app.innerHTML = `
    <section class="page">
      <a class="back-link" href="#/reference-video">← Back to Reference Video</a>
      <div class="page-header">
        <div>
          <p class="eyebrow">${item.creator}</p>
          <h1>${item.title}</h1>
        </div>
        <p class="small-note">${item.status}. This page is built for teardown, not decoration.</p>
      </div>

      <div class="detail-layout">
        <aside class="video-panel">
          <div class="video-frame">
            ${item.localVideo ? localVideo(item) : tiktokEmbed(item)}
          </div>
        </aside>

        <div>
          <article class="detail-card">
            <p class="eyebrow">Reference teardown</p>
            ${detailRow("Why it worked", item.whyItWorks)}
            ${detailRow("Core pattern", item.pattern)}
            ${detailRow("MUMUKI translation", item.mumukiTranslation)}
          </article>

          <article class="detail-card">
            <p class="eyebrow">Shoot this version</p>
            ${detailRow("Opening shot", item.openingShot)}
            ${detailRow("Text overlay", item.overlay)}
            ${detailRow("Shot list", `<ol>${item.shotList.map((shot) => `<li>${shot}</li>`).join("")}</ol>`)}
            ${detailRow("Raw demo", item.rawDemo)}
          </article>
        </div>
      </div>
    </section>
  `;

  refreshTikTokEmbed();
}

function renderScriptIdea() {
  app.innerHTML = `
    <section class="page script-page">
      <div class="page-header">
        <div>
          <p class="eyebrow">Execution layer</p>
          <h1>Script Idea</h1>
        </div>
        <p class="small-note">
          Pick a format first. Then write the script.
        </p>
      </div>

      <div class="script-nav-grid">
        ${scriptIdeaSections.map((section) => scriptIdeaCard(section)).join("")}
      </div>
    </section>
  `;
}

function scriptIdeaCard(section) {
  return `
    <a class="script-idea-card" href="${section.href}">
      <p class="eyebrow">${section.count}</p>
      <h2>${section.title}</h2>
      <p>${section.note}</p>
    </a>
  `;
}

function renderSkitScriptIdea() {
  app.innerHTML = `
    <section class="page script-page script-detail-page">
      <a class="back-link" href="#/script-idea">← Back to Script Idea</a>
      <div class="page-header">
        <div>
          <p class="eyebrow">Skit</p>
          <h1>Skit Skeleton</h1>
        </div>
      </div>

      ${scriptSkitSkeletonCard(lanceSkitSkeleton)}
    </section>
  `;
}

function renderComingSoonScriptIdea(path) {
  const title = path.includes("02") ? "Talking Head 02" : "Talking Head 01";
  app.innerHTML = `
    <section class="page script-page">
      <a class="back-link" href="#/script-idea">← Back to Script Idea</a>
      <div class="page-header">
        <div>
          <p class="eyebrow">Script Idea</p>
          <h1>${title}</h1>
        </div>
        <p class="small-note">We will build this after the skit skeleton is locked.</p>
      </div>
    </section>
  `;
}

function scriptSkitSkeletonCard(item) {
  return `
    <article class="script-skeleton-card">
      <div class="script-reference-panel">
        <p class="eyebrow">Skit reference</p>
        <div class="script-video-frame">
          ${localVideo(item)}
        </div>
        <div class="script-reference-copy">
          <p class="meta">${item.creator}</p>
          <h2>${item.sourceTitle}</h2>
        </div>
      </div>

      <div class="script-breakdown">
        <section class="script-section">
          <div class="section-head">
            <p class="eyebrow">Original skeleton</p>
          </div>
          <div class="beat-list">
            ${skitSkeletonBeats.map((beat, index) => skitSkeletonBeat(beat, index)).join("")}
          </div>
        </section>
      </div>
    </article>
  `;
}

function skitSkeletonBeat(beat, index) {
  return `
    <div class="beat-row skit-beat-row">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <div>
        <strong>${beat.title}</strong>
        <p>${beat.original}</p>
        <small>${beat.meaning}</small>
      </div>
    </div>
  `;
}

function skeletonBeat(beat, index) {
  return `
    <div class="beat-row">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <div>
        <strong>${beat[0]}</strong>
        <p>${beat[1]}</p>
      </div>
    </div>
  `;
}

function slotMapRow(slot) {
  return `
    <div class="slot-map-row">
      <strong>${slot[0]}</strong>
      <p>${slot[1]}</p>
    </div>
  `;
}

function tiktokEmbed(item) {
  return `
    <blockquote
      class="tiktok-embed"
      cite="${item.url}"
      data-video-id="${item.videoId}"
      style="max-width: 420px; min-width: 280px;"
    >
      <section>
        <a target="_blank" rel="noreferrer" href="${item.url}">Watch ${item.creator} on TikTok</a>
      </section>
    </blockquote>
  `;
}

function localVideo(item) {
  return `
    <video class="local-video" controls preload="metadata" playsinline>
      <source src="${item.localVideo}" type="video/mp4">
    </video>
  `;
}

function detailRow(label, value) {
  const content = String(value || "").trim().startsWith("<")
    ? value
    : `<p>${value}</p>`;

  return `
    <div class="detail-row">
      <strong>${label}</strong>
      ${content}
    </div>
  `;
}

function refreshTikTokEmbed() {
  const oldScript = document.querySelector("#tiktok-embed-script");
  if (oldScript) oldScript.remove();

  const script = document.createElement("script");
  script.id = "tiktok-embed-script";
  script.async = true;
  script.src = "https://www.tiktok.com/embed.js";
  document.body.appendChild(script);
}

window.addEventListener("hashchange", route);
route();
