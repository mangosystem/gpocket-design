# gPocket 3.0 — Renewal Design Mockup

gPocket 모바일 GIS 앱의 리뉴얼 디자인 목업입니다. (36개 화면)

---

## 파일 구성

| 파일 | 설명 |
|------|------|
| `gpocket_renewal_v1.html` | 전체 화면 목업 (브라우저에서 열기) |
| `colors.css` | **색상 변수 파일 — 디자이너가 수정하는 파일** |

---

## 색상 수정 방법

> **`colors.css` 파일만 수정하면 됩니다.**  
> 이 파일의 값을 바꾸면 전체 화면에 즉시 반영됩니다.

### 색상 변수 목록

```css
/* 브랜드 색상 */
--color-brand: #1A91DA;        /* 메인 브랜드 파란색 */
--color-brand-dark: #0B69A3;   /* 브랜드 진한 파란색 */

/* 상태 색상 */
--color-danger: #EF4444;       /* 오류/삭제 빨간색 */
--color-success: #27AB83;      /* 성공/확인 초록색 */
--color-warning: #F59E0B;      /* 경고 노란색 */

/* 텍스트 */
--color-text-main: #334155;    /* 주요 텍스트 */
--color-text-sub: #64748B;     /* 보조 텍스트 */
--color-text-muted: #94A3B8;   /* 흐린 텍스트/아이콘 */

/* 테두리/배경 */
--color-border: #E2E8F0;       /* 구분선 */
--color-bg-subtle: #F1F5F9;    /* 카드/섹션 배경 */
```

### 수정 예시

`--color-brand: #1A91DA;` 를 원하는 색상 코드로 변경

```css
/* 변경 전 */
--color-brand: #1A91DA;

/* 변경 후 */
--color-brand: #FF6B35;
```

---

## 화면 보는 방법

1. `gpocket_renewal_v1.html` 을 크롬/엣지 브라우저로 열기
2. **드래그**: 캔버스 이동
3. **Shift + 스크롤**: 확대/축소

---

## 주의사항

- `gpocket_renewal_v1.html` 내부 코드는 직접 수정하지 않는 것을 권장합니다
- 색상 수정은 반드시 `colors.css` 에서만 진행해 주세요
- 두 파일(`html` + `css`)은 항상 같은 폴더에 있어야 합니다
