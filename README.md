# TRIP.LOG 광저우

광저우 3박 4일 여행 일정·장소·그림 지도 앱. 배포 주소: https://subak805-netizen.github.io/trip-log/

- 고치는 곳: `index.src.html`, `style.retro.css` → `python3 build.py` → `docs/index.html`(배포) · `index.html`(claude.ai 링크용)
- 저장: 일정=localStorage `triplog_gz_v1`, 내 사진=IndexedDB `triplog_gz` (같은 주소의 다른 앱 저장공간을 쓰지 않음)

## 출처
- 글꼴 Galmuri11 — Lee Minseo, SIL Open Font License 1.1 (https://github.com/quiple/galmuri)
- 명소 사진 — 위키미디어 공용 자유 이용 사진, 작가·라이선스는 `photos/meta.json`과 앱 정보 탭에 표시
