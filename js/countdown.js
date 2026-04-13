/* =========================================================================
   countdown.js
   100원샵 배너 카운트다운 타이머
   - 한정 오픈 종료 시각까지의 D / H / M / S 갱신
   - 종료 시 배너 카피를 자동으로 안내 메시지로 교체
   - 카페24 적용 시: data-deadline 값을 매월 운영 캘린더에 맞춰 변경
   ========================================================================= */
(function () {
  'use strict';

  const root = document.querySelector('[data-countdown]');
  if (!root) return;

  /* deadline: ISO 형식 (예: 2026-04-30T23:59:59+09:00) */
  const deadlineStr = root.dataset.deadline;
  if (!deadlineStr) return;

  const deadline = new Date(deadlineStr).getTime();
  const dEl = root.querySelector('[data-d]');
  const hEl = root.querySelector('[data-h]');
  const mEl = root.querySelector('[data-m]');
  const sEl = root.querySelector('[data-s]');
  const copyEl = document.querySelector('[data-countdown-copy]');

  function pad(n) { return String(n).padStart(2, '0'); }

  function tick() {
    const diff = deadline - Date.now();
    if (diff <= 0) {
      dEl.textContent = '00';
      hEl.textContent = '00';
      mEl.textContent = '00';
      sEl.textContent = '00';
      if (copyEl) copyEl.textContent = '이번 달 100원샵은 종료되었습니다. 다음 달을 기다려주세요!';
      clearInterval(timer);
      return;
    }
    const sec  = Math.floor(diff / 1000) % 60;
    const min  = Math.floor(diff / (1000 * 60)) % 60;
    const hour = Math.floor(diff / (1000 * 60 * 60)) % 24;
    const day  = Math.floor(diff / (1000 * 60 * 60 * 24));

    dEl.textContent = pad(day);
    hEl.textContent = pad(hour);
    mEl.textContent = pad(min);
    sEl.textContent = pad(sec);
  }

  tick();
  const timer = setInterval(tick, 1000);
})();
