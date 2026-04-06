# gPocket Renewal — 디자인 가이드

> 신규 화면 추가 시 이 문서의 패턴을 반드시 따를 것.
> 기준 파일: `gpocket_renewal_v1.html` + `colors.css`

---

## 0. 색상 시스템 (colors.css)

**`colors.css` 파일 하나만 수정하면 전체 목업의 색상이 한 번에 바뀝니다.**

### 구조

| 섹션 | 변수 접두사 | 역할 |
|------|-------------|------|
| 앱 UI — Primary | `--c-primary-*` | 버튼, 지도 마커, 토글, 활성 탭 등 주요 인터랙션 색 |
| 앱 UI — Success | `--c-success-*` | 확인/저장 버튼, 완료 상태 |
| 앱 UI — Slate | `--c-slate-*` | 텍스트, 배경, 테두리 등 중립 색 |
| 캔버스 / 목업 | `--color-*` | 목업 레이아웃(phone 프레임, 라벨 등) 색 |

### 색상 변경 방법

```css
/* colors.css 에서 이 값만 바꾸면 됩니다 */

--c-primary: #1A91DA;   /* 버튼·마커·토글 메인 색 */
--c-success: #27AB83;   /* 확인·저장 버튼 색 */
```

- `--c-primary` 변경 → 앱 내 모든 파란 버튼, 지도 마커, 토글 자동 반영
- `--c-success` 변경 → 확인·저장 버튼, 완료 상태 배지 자동 반영
- 세부 shade(`--c-primary-dark`, `--c-primary-subtle` 등)는 hover, 배경 등 파생 색상

> HTML 파일이나 Tailwind 클래스는 건드리지 않아도 됩니다.

---

## 1. 화면 기본 구조

모든 화면은 `390×844px` iPhone 프레임 기준.

```html
<div class="relative" style="position:absolute;left:{x}px;top:{y}px;">
  <div class="screen-label">{번호}. {Screen Name}</div>
  <div class="phone">
    <div class="notch"></div>
    <div class="w-full h-full bg-{white|slate-50} relative overflow-hidden">

      <!-- 1) Status Bar -->
      <!-- 2) Header -->
      <!-- 3) Content -->
      <!-- 4) FAB (있는 경우) -->
      <div class="home-indicator" style="background:rgba(0,0,0,0.15)"></div>
    </div>
  </div>
  <div class="screen-label-bottom">{English Name}<span>{한글 설명}</span></div>
</div>
```

---

## 2. 배경색

| 화면 유형 | 배경색 | 예시 |
|-----------|--------|------|
| 목록/대시보드 (독립 페이지) | `bg-slate-50` | Project List, Member Manage, My Page |
| 폼/모달 (modalStack으로 열리는 화면) | `bg-white` | Server Manage, Add Server, Dataset Manage |
| 지도 화면 | `map-placeholder` 클래스 | Map View, Edit Session |

---

## 3. Status Bar

모든 화면 동일하게 사용.

```html
<div class="status-bar text-slate-800">
  <span>9:41</span>
  <div class="flex gap-1.5 items-center opacity-60">
    <svg width="16" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M5 12.55a11 11 0 0 1 14.08 0"/>
    </svg>
    <svg width="16" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="1" y="6" width="18" height="12" rx="2"/>
    </svg>
  </div>
</div>
```

---

## 4. 헤더 패턴

### 4-A. 뒤로가기 헤더 (독립 페이지)

배경 `bg-white`, 하단 border 없음. 우측에 액션 버튼 올 수 있음.

```html
<div class="bg-white px-5 pt-2 pb-4">
  <div class="flex items-center justify-between">
    <!-- 뒤로가기 -->
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-main)" stroke-width="2">
      <polyline points="15 18 9 12 15 6"/>
    </svg>
    <h1 class="text-lg font-bold text-slate-900">{제목}</h1>
    <div class="w-6"></div> <!-- 또는 액션 버튼 -->
  </div>
</div>
```

### 4-B. 닫기(X) 헤더 (모달 화면)

`border-b` 없이 사용 (Server Manage 기준). 단, 탭이 없는 폼 화면은 `border-b border-slate-100` 추가.

```html
<div class="px-5 pt-2 pb-4 flex items-center justify-between">
  <!-- 닫기 -->
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-main)" stroke-width="2">
    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
  <h1 class="text-lg font-bold text-slate-900">{제목}</h1>
  <div class="w-6"></div>
</div>
```

---

## 5. 탭

```html
<div class="flex gap-1 bg-slate-100 rounded-xl p-1">
  <div class="flex-1 text-center py-2 rounded-lg bg-white text-sm font-semibold text-brand-600 shadow-sm">활성 탭</div>
  <div class="flex-1 text-center py-2 rounded-lg text-sm text-slate-500">비활성 탭</div>
</div>
```

---

## 6. 카드 패턴

### 6-A. 일반 카드 (비활성/목록)

```html
<div class="rounded-2xl border border-slate-200 bg-white p-4">
  <div class="flex items-center gap-3">
    <!-- 아이콘 -->
    <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
      <svg .../>  <!-- stroke="var(--color-text-muted)" -->
    </div>
    <!-- 텍스트 -->
    <div class="flex-1">
      <div class="font-semibold text-slate-600 text-sm">{제목}</div>
      <div class="text-xs text-slate-400 mt-0.5">{부제}</div>
    </div>
    <!-- 우측 요소 (badge / chevron / button) -->
  </div>
</div>
```

### 6-B. 선택/활성 카드 (expanded accordion)

```html
<div class="rounded-2xl border-2 border-brand-400 bg-brand-50 overflow-hidden">
  <div class="p-4 flex items-center gap-3">
    <div class="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center">
      <svg ... stroke="white" stroke-width="1.8"/>
    </div>
    <div class="flex-1">
      <div class="font-semibold text-slate-800 text-sm">{제목}</div>
      <div class="text-xs text-slate-400 mt-0.5">{부제}</div>
    </div>
    <!-- 위쪽 chevron -->
    <svg width="16" height="16" ... stroke="var(--color-brand)" stroke-width="2">
      <polyline points="18 15 12 9 6 15"/>
    </svg>
  </div>
  <!-- 액션 버튼 행 -->
  <div class="px-4 pb-3 flex gap-2">
    ...
  </div>
</div>
```

### 6-C. Project 카드 (shadow 있는 대형 카드)

```html
<div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 card-hover">
  ...
</div>
```

---

## 7. 아코디언 액션 버튼

카드 펼침 상태에서 하단에 수평 배치. 주요 액션은 `brand`, 파괴적 액션은 `slate`.

```html
<div class="px-4 pb-3 flex gap-2">
  <button class="flex-1 py-2 text-xs font-medium text-brand-600 bg-white rounded-lg border border-brand-200 flex items-center justify-center gap-1">
    <svg width="13" height="13" .../>정보
  </button>
  <button class="flex-1 py-2 text-xs font-medium text-brand-600 bg-white rounded-lg border border-brand-200 flex items-center justify-center gap-1">
    <svg width="13" height="13" .../>편집
  </button>
  <button class="flex-1 py-2 text-xs font-medium text-slate-500 bg-white rounded-lg border border-slate-200 flex items-center justify-center gap-1">
    <svg width="13" height="13" .../>삭제
  </button>
</div>
```

---

## 8. 뱃지 / 태그

```html
<!-- 브랜드 (활성, 역할) -->
<span class="px-2.5 py-1 bg-brand-50 text-brand-600 text-xs rounded-lg font-medium">Owner</span>

<!-- 중립 (비활성 역할) -->
<span class="px-2.5 py-1 bg-slate-100 text-slate-500 text-xs rounded-lg font-medium">Editor</span>

<!-- 상태 pill (활성 표시) -->
<span class="px-2 py-0.5 bg-accent-100 text-accent-700 text-xs rounded-full font-medium">활성</span>

<!-- 지오메트리 타입 태그 -->
<span class="px-2.5 py-1 bg-brand-50 text-brand-600 text-xs rounded-lg font-medium">Point</span>
<span class="px-2.5 py-1 bg-accent-50 text-accent-600 text-xs rounded-lg font-medium">LineString</span>
<span class="px-2.5 py-1 bg-amber-50 text-amber-600 text-xs rounded-lg font-medium">Polygon</span>
```

---

## 9. 폼 필드 (입력 화면)

```html
<div class="px-6 pt-5 space-y-5">
  <div>
    <label class="text-xs font-semibold text-slate-500 uppercase tracking-wider">{필드명}</label>
    <input type="text" placeholder="{placeholder}"
      class="mt-2 w-full border border-slate-200 rounded-xl px-4 py-3.5 text-sm outline-none" />
  </div>
</div>
```

---

## 10. FAB (Floating Action Button)

항상 `absolute bottom-10 right-5`.

```html
<div class="absolute bottom-10 right-5 z-30">
  <div class="fab bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-500/30">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
      <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
  </div>
</div>
```

---

## 11. 아이콘 컨테이너 크기 기준

| 용도 | 크기 | 클래스 |
|------|------|--------|
| 카드 내 아이콘 (표준) | 40×40 | `w-10 h-10 rounded-xl` |
| 멤버 아바타 | 44×44 | `w-11 h-11 rounded-full` |
| 소형 아바타 (스택) | 24×24 | `w-6 h-6 rounded-full` |
| SVG 아이콘 (카드 내) | 20×20 | `width="20" height="20"` |
| SVG 아이콘 (버튼 내) | 13–14×13–14 | `width="13" height="13"` |

아이콘 색상:
- 활성/선택: `bg-brand-500`, 아이콘 `stroke="white" stroke-width="1.8"`
- 비활성: `bg-slate-100`, 아이콘 `stroke="var(--color-text-muted)" stroke-width="1.8"`

---

## 12. 텍스트 계층

| 역할 | 클래스 |
|------|--------|
| 화면 제목 | `text-lg font-bold text-slate-900` |
| 카드 제목 (활성) | `font-semibold text-slate-800 text-sm` |
| 카드 제목 (비활성) | `font-semibold text-slate-600 text-sm` |
| 부제 / 메타 | `text-xs text-slate-400 mt-0.5` |
| 레이블 (폼) | `text-xs font-semibold text-slate-500 uppercase tracking-wider` |
| 버튼 텍스트 | `text-xs font-medium` |

---

## 13. 캔버스 배치 (행/열 좌표)

| Row | top (px) | 주요 화면 |
|-----|----------|-----------|
| 0 | 0 | Home → Login → ProjList → ProjDetail → MapView → EditSession → Drawer |
| 1 | 1050 | OffGPKG / Register / SearchJoin / ProjCreate / AddGeo / FeatureSel / AttrForm / VertexEdit / DelConfirm |
| 2 | 2100 | GPKGCreate / SyncOffline / DatasetCols / MemberMgmt / FeatureInfo / EditHistory / LayerMgmt / GPS / CQLFilter / Bookmark |
| 3 | 3150 | MyPage / FS-A / FS-B / FS-C / DatasetManage / ServerMgmt / AddServer |
| 4 | 4200 | Empty/Error / DialogToast |

열 간격: **600px**. 신규 화면은 빈 슬롯 먼저 채우고, 없으면 새 Row 추가.

---

## 14. SVG 화살표 색상 규칙

| 색상 | 의미 |
|------|------|
| 회색 `#94A3B8` | 주 네비게이션 흐름 |
| 파랑 `#3EAAE0` | 피처 편집 흐름 |
| 초록 `#27AB83` | 피처 추가 흐름 |
| 빨강 `#EF4444` | 삭제 흐름 |
| 노랑 `#F59E0B` | 오프라인 흐름 |

---

## 15. CTA Semantic Rule

CTA uses role classes only: `btn-cta btn-cta--primary|positive|danger`.
Do not hardcode CTA color with `from-*`, `to-*`, `text-*`, `shadow-*` utility classes.

```html
<button class="... btn-cta btn-cta--primary">저장</button>
<button class="... btn-cta btn-cta--positive">전송</button>
<button class="... btn-cta btn-cta--danger">삭제</button>
```

---

## 16. Token Layer Rule

Use semantic/role tokens first. Do not hardcode color values directly in new styles.

| Layer | Prefix | Rule |
|------|--------|------|
| Canonical source | `--sem-*` | Single source for actual color values |
| Role / component intent | `--role-*` | Map intent (CTA, mode, etc.) to canonical tokens |
| Legacy alias (compat) | `--color-*` | Existing screen compatibility only (`@deprecated`) |

Color change point for maintenance:
- Brand: `--sem-brand*`
- Success: `--sem-success*`
- Mode: `--sem-mode-pinogio*`, `--sem-mode-everyone*`, `--sem-mode-offline*`
