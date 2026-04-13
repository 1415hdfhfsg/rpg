/* =========================================================================
   review_carousel.js
   리뷰 섹션 — 베스트 리뷰 카드 자동 회전(슬라이드)
   - 데스크톱: 3개씩 노출되는 정적 그리드 + 5초마다 카드 강조 토글
   - 모바일: 1열 그리드에서 가로 스와이프(스냅)
   - 카페24 적용 시: 별점 평균/리뷰 수는 #review_avg, #review_count 같은
     쇼핑몰 변수로 치환 가능
   ========================================================================= */
(function () {
  'use strict';

  const root = document.querySelector('[data-review-root]');
  if (!root) return;

  const cards = Array.from(root.querySelectorAll('.review-card'));
  if (cards.length === 0) return;

  let activeIdx = 0;

  /* 카드 강조: 활성화된 카드만 살짝 부각 (CSS transform 활용) */
  function highlight(idx) {
    cards.forEach((c, i) => {
      const isActive = i === idx;
      c.style.transform = isActive ? 'translateY(-6px)' : 'translateY(0)';
      c.style.boxShadow  = isActive
        ? '0 14px 36px rgba(61, 53, 48, 0.12)'
        : '0 0 0 rgba(0,0,0,0)';
    });
  }

  /* 자동 회전 — 5초 간격
     사용자가 카드 위에 마우스를 올리면 일시정지 */
  let timer = null;
  function start() {
    timer = setInterval(() => {
      activeIdx = (activeIdx + 1) % cards.length;
      highlight(activeIdx);
    }, 5000);
  }
  function stop() { if (timer) clearInterval(timer); timer = null; }

  cards.forEach((c, i) => {
    c.addEventListener('mouseenter', () => { stop(); highlight(i); activeIdx = i; });
    c.addEventListener('mouseleave', () => { start(); });
  });

  highlight(0);
  start();

  /* 평균 별점 카운트업 애니메이션 */
  const avgEl = document.querySelector('[data-review-avg]');
  if (avgEl) {
    const target = parseFloat(avgEl.dataset.target || '4.8');
    let current = 0;
    const step = target / 30;
    const counter = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(counter); }
      avgEl.firstChild.textContent = current.toFixed(1);
    }, 30);
  }
})();
