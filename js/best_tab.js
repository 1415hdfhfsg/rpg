/* =========================================================================
   best_tab.js
   BEST 섹션 탭 전환 모듈
   - [전체 BEST / 식기 / 컵·도시락 / 키친툴] 4개 카테고리
   - 탭 클릭 시 .product-card 의 data-cat 속성으로 필터링
   - 카페24 적용 시: 각 카테고리의 베스트 상품을 #{} 변수로 렌더한 후
     data-cat 속성만 부여하면 동일하게 동작함
   ========================================================================= */
(function () {
  'use strict';

  const ROOT = document.querySelector('[data-best-root]');
  if (!ROOT) return;

  const tabs  = ROOT.querySelectorAll('[data-tab]');
  const cards = ROOT.querySelectorAll('.product-card');
  const subtitleEl = document.querySelector('[data-best-sub]');

  /* 카테고리별 소셜프루프 카피 (서브타이틀 갱신용)
     - "이번 주 N명이 담은 상품" 형태로 행동을 자극 */
  const SOCIAL_COPY = {
    all:    '이번 주 1,284명이 장바구니에 담은 상품',
    plate:  '이번 주 642명이 식기 카테고리에서 담은 상품',
    cup:    '이번 주 318명이 컵·도시락 카테고리에서 담은 상품',
    tool:   '이번 주 197명이 키친툴 카테고리에서 담은 상품'
  };

  function setActive(tab) {
    tabs.forEach(t => t.classList.toggle('is-active', t === tab));
  }

  function filter(cat) {
    cards.forEach(card => {
      const matched = (cat === 'all') || (card.dataset.cat === cat);
      card.style.display = matched ? '' : 'none';
    });
    if (subtitleEl && SOCIAL_COPY[cat]) {
      subtitleEl.textContent = SOCIAL_COPY[cat];
    }
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const cat = tab.dataset.tab;
      setActive(tab);
      filter(cat);
    });
  });

  /* 초기 상태: 전체 BEST */
  filter('all');
})();
