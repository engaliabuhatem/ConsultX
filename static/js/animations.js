document.addEventListener("DOMContentLoaded", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------------------------------------------------------------------
  // Pressure gauge — the design comp's transition motif. Drawn as inline
  // SVG rather than shipped as a file so it inherits the surrounding color,
  // and its needle sweeps -60deg to +60deg with total scroll progress.
  // ---------------------------------------------------------------------
  const gauges = document.querySelectorAll("[data-gauge]");
  gauges.forEach((el) => {
    const size = Number(el.dataset.gaugeSize) || 64;
    const tick = el.dataset.gaugeTick || "#FAD02C";
    const dial = el.dataset.gaugeDial || "rgba(254,252,246,.45)";
    el.innerHTML = `
      <svg width="${size}" height="${size * 0.62}" viewBox="0 0 100 62" aria-hidden="true" focusable="false">
        <g stroke="${dial}" stroke-width="2.4" stroke-linecap="round">
          <line x1="20" y1="42" x2="24" y2="36"/>
          <line x1="30" y1="24" x2="33" y2="29"/>
          <line x1="50" y1="16" x2="50" y2="22"/>
          <line x1="70" y1="24" x2="67" y2="29"/>
          <line x1="80" y1="42" x2="76" y2="36"/>
        </g>
        <line class="needle" x1="50" y1="46" x2="26" y2="38" stroke="${tick}" stroke-width="2.6" stroke-linecap="round"/>
        <circle cx="50" cy="46" r="3.4" fill="${tick}"/>
      </svg>`;
  });

  if (gauges.length && !prefersReducedMotion) {
    const needles = document.querySelectorAll(".needle");
    let queued = false;
    const updateGauges = () => {
      queued = false;
      const doc = document.documentElement;
      const scrollable = doc.scrollHeight - doc.clientHeight;
      const progress = scrollable > 0 ? doc.scrollTop / scrollable : 0;
      const angle = -60 + progress * 120;
      needles.forEach((n) => {
        n.style.transform = `rotate(${angle}deg)`;
      });
    };
    // rAF-coalesced: scroll fires far more often than the screen repaints.
    document.addEventListener(
      "scroll",
      () => {
        if (!queued) {
          queued = true;
          requestAnimationFrame(updateGauges);
        }
      },
      { passive: true },
    );
    updateGauges();
  }

  // ---------------------------------------------------------------------
  // Reveal-on-scroll for the hero and chapter copy. The .reveal rule only
  // hides anything under (prefers-reduced-motion: no-preference), so with
  // reduced motion this observer is simply never wired up and the content
  // is visible from first paint.
  // ---------------------------------------------------------------------
  const revealables = document.querySelectorAll(".reveal");
  if (revealables.length && !prefersReducedMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 },
    );
    revealables.forEach((el) => io.observe(el));
  }

  // --- AOS: simple declarative scroll-reveals (grids, cards, sections) ---
  if (window.AOS) {
    AOS.init({
      duration: 600,
      easing: "ease-out-cubic",
      once: true,
      offset: 60,
      disable: prefersReducedMotion,
    });
  }

  if (prefersReducedMotion || !window.gsap) return;

  // --- GSAP: things AOS can't do declaratively ---
  gsap.registerPlugin(ScrollTrigger);

  // Stat counters count up from 0 once scrolled into view. Values are stored
  // as free-text ("150+", "25+") in the CMS, so parse the leading number and
  // preserve whatever suffix follows it.
  document.querySelectorAll("[data-counter]").forEach((el) => {
    const raw = el.textContent.trim();
    const match = raw.match(/^(\d+)(.*)$/);
    if (!match) return;

    const target = parseInt(match[1], 10);
    const suffix = match[2];
    const counter = { val: 0 };
    el.textContent = "0" + suffix;

    ScrollTrigger.create({
      trigger: el,
      start: "top 85%",
      once: true,
      onEnter: () => {
        gsap.to(counter, {
          val: target,
          duration: 1.6,
          ease: "power2.out",
          onUpdate: () => {
            el.textContent = Math.floor(counter.val) + suffix;
          },
        });
      },
    });
  });

  // Subtle hero background parallax — image drifts slower than scroll.
  const heroImg = document.querySelector("[data-hero-parallax]");
  if (heroImg) {
    gsap.to(heroImg, {
      yPercent: 12,
      ease: "none",
      scrollTrigger: {
        trigger: heroImg,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });
  }
});
