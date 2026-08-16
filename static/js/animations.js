document.addEventListener("DOMContentLoaded", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
