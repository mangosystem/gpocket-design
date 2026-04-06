#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
canvas_tool.py — gPocket Design Canvas 관리 도구

사용법:
  python canvas_tool.py apply                        # JSON → HTML 전체 적용
  python canvas_tool.py move <id> <x> <y>            # 위치 변경 후 apply
  python canvas_tool.py renumber <id> <num>          # 번호 변경 후 apply
  python canvas_tool.py add <id> <num> <name> <x> <y> # 화면 추가
  python canvas_tool.py remove <id>                  # 화면 제거 (JSON에서만)
  python canvas_tool.py status                       # 현재 화면 목록 표시
"""

import json
import re
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANVAS_JSON = os.path.join(BASE_DIR, "canvas.json")
HTML_FILE   = os.path.join(BASE_DIR, "gpocket_renewal_v1.html")

BOUNDARY_START = "<!-- BOUNDARY_START -->"
BOUNDARY_END   = "<!-- BOUNDARY_END -->"

# ──────────────────────────────────────────────
# 색상 매핑
# ──────────────────────────────────────────────
COLOR_MAP = {
    "muted":   {
        "stroke":  "var(--color-text-muted)",
        "fill_row": "rgba(15,23,42,0.02)",
        "fill_sub": "rgba(15,23,42,0.03)",
        "text":    "var(--color-text-sub)",
    },
    "brand":   {
        "stroke":  "var(--color-brand)",
        "fill_row": "rgba(23,101,167,0.02)",
        "fill_sub": "rgba(23,101,167,0.03)",
        "text":    "var(--color-brand)",
    },
    "success": {
        "stroke":  "var(--color-success)",
        "fill_row": "rgba(39,171,131,0.02)",
        "fill_sub": "rgba(39,171,131,0.03)",
        "text":    "var(--color-success-text)",
    },
    "warning": {
        "stroke":  "var(--color-warning)",
        "fill_row": "rgba(245,158,11,0.03)",
        "fill_sub": "rgba(245,158,11,0.04)",
        "text":    "var(--color-amber-dark)",
    },
}


# ──────────────────────────────────────────────
# JSON 로드 / 저장
# ──────────────────────────────────────────────
def load_canvas():
    with open(CANVAS_JSON, encoding="utf-8") as f:
        return json.load(f)


def save_canvas(data):
    with open(CANVAS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# HTML 로드 / 저장
# ──────────────────────────────────────────────
def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()


def save_html(content):
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)


# ──────────────────────────────────────────────
# 바운더리 SVG 생성
# ──────────────────────────────────────────────
def compute_rect(screen_ids, screens_by_id, sw, sh, pad):
    """그룹에 속한 화면들의 바운딩 박스 계산."""
    xs = [screens_by_id[sid]["x"] for sid in screen_ids if sid in screens_by_id]
    ys = [screens_by_id[sid]["y"] for sid in screen_ids if sid in screens_by_id]
    if not xs:
        return None
    min_x, min_y = min(xs), min(ys)
    max_x, max_y = max(xs) + sw, max(ys) + sh
    rx = min_x - pad
    ry = min_y - pad
    rw = (max_x - min_x) + pad * 2
    rh = sh + pad * 2
    return rx, ry, rw, rh


def build_boundary_svg(data):
    cfg       = data["canvas"]
    sw, sh    = cfg["screenWidth"], cfg["screenHeight"]
    pad_sub   = cfg["padding"]        # 14
    pad_row   = 30

    screens_by_id = {s["id"]: s for s in data["screens"]}

    lines = []
    lines.append("")
    lines.append("  <!-- ================================================================")
    lines.append("       BOUNDARY BOXES — 행별 섹션 구분")
    lines.append("       ================================================================ -->")
    lines.append("")

    for rg in data["rowGroups"]:
        c   = COLOR_MAP[rg["color"]]
        r   = compute_rect(rg["screens"], screens_by_id, sw, sh, pad_row)
        if r is None:
            continue
        rx, ry, rw, rh = r
        label = rg["label"].replace("&", "&amp;")
        lines.append(f'  <!-- {rg["id"]}: {rg["label"]} -->')
        lines.append(
            f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}"'
        )
        lines.append(
            f'        rx="16" fill="{c["fill_row"]}" stroke="{c["stroke"]}"'
        )
        lines.append(
            f'        stroke-width="1.5" stroke-dasharray="10,6"/>'
        )
        lines.append(
            f'  <text x="{rx + 16}" y="{ry - 4}" font-size="13" font-weight="700"'
        )
        lines.append(
            f'        fill="{c["text"]}" font-family="Pretendard, sans-serif">{label}</text>'
        )
        lines.append("")

    lines.append("  <!-- ================================================================")
    lines.append("       SUB-BOUNDARY BOXES — 기능별 세부 그룹")
    lines.append("       ================================================================ -->")
    lines.append("")

    for sg in data["subGroups"]:
        c   = COLOR_MAP[sg["color"]]
        r   = compute_rect(sg["screens"], screens_by_id, sw, sh, pad_sub)
        if r is None:
            continue
        rx, ry, rw, rh = r
        label = sg["label"].replace("&", "&amp;")
        lines.append(f'  <!-- {sg["id"]}: {sg["label"]} -->')
        lines.append(
            f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}"'
        )
        lines.append(
            f'        rx="12" fill="{c["fill_sub"]}" stroke="{c["stroke"]}"'
        )
        lines.append(
            f'        stroke-width="1.2" opacity="0.7"/>'
        )
        lines.append(
            f'  <text x="{rx + 12}" y="{ry - 4}" font-size="11" font-weight="600"'
        )
        lines.append(
            f'        fill="{c["text"]}" font-family="Pretendard, sans-serif">{label}</text>'
        )
        lines.append("")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# apply: JSON → HTML 반영
# ──────────────────────────────────────────────
def cmd_apply(data=None):
    if data is None:
        data = load_canvas()

    screens_by_id = {s["id"]: s for s in data["screens"]}
    html = load_html()
    changed_positions = []
    changed_labels    = []

    # 1) data-screen 속성을 가진 div의 position 업데이트
    def replace_position(m):
        sid    = m.group(1)
        before = m.group(0)
        if sid not in screens_by_id:
            return before
        s   = screens_by_id[sid]
        new = (
            f'<div class="relative" data-screen="{sid}" '
            f'style="position:absolute;left:{s["x"]}px;top:{s["y"]}px;">'
        )
        if new != before:
            changed_positions.append(sid)
        return new

    html = re.sub(
        r'<div class="relative" data-screen="([^"]+)" '
        r'style="position:absolute;left:\d+px;top:\d+px;">',
        replace_position,
        html,
    )

    # 2) screen-label 텍스트를 "N. Name"으로 업데이트
    #    각 data-screen div 직후에 오는 .screen-label div 찾기
    def replace_label(m):
        sid         = m.group(1)
        full_match  = m.group(0)
        if sid not in screens_by_id:
            return full_match
        s       = screens_by_id[sid]
        new_txt = f'{s["num"]}. {s["name"]}'
        updated = re.sub(
            r'(<div class="screen-label">)[^<]*(</div>)',
            lambda lm: lm.group(1) + new_txt + lm.group(2),
            full_match,
            count=1,
        )
        if updated != full_match:
            changed_labels.append(sid)
        return updated

    html = re.sub(
        r'<div class="relative" data-screen="([^"]+)"[^>]*>[\s\n]*'
        r'<div class="screen-label">[^<]*</div>',
        replace_label,
        html,
        flags=re.DOTALL,
    )

    # 3) BOUNDARY 마커 사이 내용 재생성
    if BOUNDARY_START in html and BOUNDARY_END in html:
        new_svg = build_boundary_svg(data)
        html = re.sub(
            re.escape(BOUNDARY_START) + r".*?" + re.escape(BOUNDARY_END),
            BOUNDARY_START + new_svg + "\n  " + BOUNDARY_END,
            html,
            flags=re.DOTALL,
        )
        print("  [OK] SVG boundary 섹션 재생성 완료")
    else:
        print("  [WARN] BOUNDARY 마커를 찾을 수 없습니다. HTML에 마커가 있는지 확인하세요.")

    save_html(html)

    print(f"  [OK] 위치 업데이트: {len(changed_positions)}개 {changed_positions or ''}")
    print(f"  [OK] 레이블 업데이트: {len(changed_labels)}개 {changed_labels or ''}")
    print("  [OK] apply 완료 →", HTML_FILE)


# ──────────────────────────────────────────────
# move
# ──────────────────────────────────────────────
def cmd_move(sid, x, y):
    data = load_canvas()
    for s in data["screens"]:
        if s["id"] == sid:
            old_x, old_y = s["x"], s["y"]
            s["x"], s["y"] = int(x), int(y)
            save_canvas(data)
            print(f"  [OK] '{sid}' 위치 변경: ({old_x},{old_y}) → ({x},{y})")
            cmd_apply(data)
            return
    print(f"  [ERROR] 화면 ID '{sid}'를 찾을 수 없습니다.")
    sys.exit(1)


# ──────────────────────────────────────────────
# renumber
# ──────────────────────────────────────────────
def cmd_renumber(sid, num):
    data = load_canvas()
    for s in data["screens"]:
        if s["id"] == sid:
            old_num = s["num"]
            s["num"] = int(num)
            save_canvas(data)
            print(f"  [OK] '{sid}' 번호 변경: {old_num} → {num}")
            cmd_apply(data)
            return
    print(f"  [ERROR] 화면 ID '{sid}'를 찾을 수 없습니다.")
    sys.exit(1)


# ──────────────────────────────────────────────
# add
# ──────────────────────────────────────────────
def cmd_add(sid, num, name, x, y):
    data = load_canvas()
    for s in data["screens"]:
        if s["id"] == sid:
            print(f"  [ERROR] ID '{sid}'가 이미 존재합니다.")
            sys.exit(1)
    new_screen = {"id": sid, "num": int(num), "name": name, "x": int(x), "y": int(y)}
    data["screens"].append(new_screen)
    # 번호 순 정렬
    data["screens"].sort(key=lambda s: s["num"])
    save_canvas(data)
    print(f"  [OK] 화면 추가: {sid} ({num}. {name}) @ ({x},{y})")
    print("  [INFO] HTML에 해당 div를 직접 추가한 후 apply를 실행하세요.")


# ──────────────────────────────────────────────
# remove
# ──────────────────────────────────────────────
def cmd_remove(sid):
    data = load_canvas()
    before = len(data["screens"])
    data["screens"] = [s for s in data["screens"] if s["id"] != sid]
    # subGroups, rowGroups에서도 제거
    for g in data.get("rowGroups", []):
        if sid in g["screens"]:
            g["screens"].remove(sid)
    for g in data.get("subGroups", []):
        if sid in g["screens"]:
            g["screens"].remove(sid)
    if len(data["screens"]) == before:
        print(f"  [ERROR] 화면 ID '{sid}'를 찾을 수 없습니다.")
        sys.exit(1)
    save_canvas(data)
    print(f"  [OK] '{sid}' JSON에서 제거 완료")
    print("  [INFO] HTML의 해당 div는 수동으로 제거하세요.")


# ──────────────────────────────────────────────
# status
# ──────────────────────────────────────────────
def cmd_status():
    data = load_canvas()
    screens = data["screens"]
    print(f"\n  gPocket Canvas - total {len(screens)} screens\n")
    print(f"  {'NUM':>4}  {'ID':<22} {'NAME':<26} {'X':>6} {'Y':>6}")
    print("  " + "-" * 70)
    for s in sorted(screens, key=lambda x: x["num"]):
        print(f"  {s['num']:>4}  {s['id']:<22} {s['name']:<26} {s['x']:>6} {s['y']:>6}")
    print()

    # HTML 에서 data-screen 개수 확인
    html = load_html()
    found_ids = re.findall(r'data-screen="([^"]+)"', html)
    print(f"  HTML data-screen 속성: {len(found_ids)}개")

    json_ids  = {s["id"] for s in screens}
    html_id_set = set(found_ids)
    missing_in_html = json_ids - html_id_set
    missing_in_json = html_id_set - json_ids

    if missing_in_html:
        print(f"  [WARN] JSON에 있지만 HTML에 없음: {sorted(missing_in_html)}")
    if missing_in_json:
        print(f"  [WARN] HTML에 있지만 JSON에 없음: {sorted(missing_in_json)}")
    if not missing_in_html and not missing_in_json:
        print("  [OK] JSON ↔ HTML 완전 일치")

    has_start = BOUNDARY_START in html
    has_end   = BOUNDARY_END   in html
    print(f"  BOUNDARY 마커: START={'있음' if has_start else '없음'}, END={'있음' if has_end else '없음'}")
    print()


# ──────────────────────────────────────────────
# 마커 삽입 헬퍼 (초기 1회)
# ──────────────────────────────────────────────
def insert_markers_if_missing():
    """HTML에 BOUNDARY 마커가 없으면 기존 바운더리 섹션을 감싸서 삽입."""
    html = load_html()
    if BOUNDARY_START in html:
        return  # 이미 있음

    # SVG defs 닫는 태그 바로 뒤 ~ ARROWS 섹션 직전을 마커로 감싸기
    # 패턴: </defs> 이후 첫 번째 <!-- BOUNDARY ... --> 블록 전체를 찾아서 마커로 감쌈
    pattern = (
        r'(</defs>\s*\n)'
        r'((?:.*?<!-- ={3,}.*?BOUNDARY.*?={3,}.*?-->.*?\n'
        r'(?:.*?\n)*?)'
        r'(?=\s*<!-- ={3,}.*?ARROWS))'
    )
    m = re.search(pattern, html, re.DOTALL)
    if m:
        old_block = m.group(2)
        new_block = BOUNDARY_START + "\n" + old_block + "  " + BOUNDARY_END + "\n"
        html = html[:m.start(2)] + new_block + html[m.end(2):]
        save_html(html)
        print("  [OK] BOUNDARY 마커 삽입 완료")
    else:
        print("  [WARN] BOUNDARY 섹션 자동 감지 실패. HTML을 직접 확인하세요.")


# ──────────────────────────────────────────────
# data-screen 속성 일괄 삽입 헬퍼 (초기 1회)
# ──────────────────────────────────────────────
def insert_data_screen_attrs():
    """HTML에 data-screen 속성이 없는 div에 추가."""
    data = load_canvas()
    screens_by_pos = {(s["x"], s["y"]): s for s in data["screens"]}

    html = load_html()

    def add_attr(m):
        x   = int(m.group(1))
        y   = int(m.group(2))
        key = (x, y)
        if key not in screens_by_pos:
            return m.group(0)  # 알 수 없는 위치 — 그대로
        sid = screens_by_pos[key]["id"]
        return f'<div class="relative" data-screen="{sid}" style="position:absolute;left:{x}px;top:{y}px;">'

    # data-screen 없는 것만 대상
    new_html = re.sub(
        r'<div class="relative" style="position:absolute;left:(\d+)px;top:(\d+)px;">',
        add_attr,
        html,
    )

    added = len(re.findall(r'data-screen=', new_html)) - len(re.findall(r'data-screen=', html))
    save_html(new_html)
    print(f"  [OK] data-screen 속성 추가: {added}개")


# ──────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "apply":
        print("\n[apply] canvas.json → HTML 반영 중...")
        insert_data_screen_attrs()
        insert_markers_if_missing()
        cmd_apply()

    elif cmd == "move":
        if len(args) < 4:
            print("사용법: python canvas_tool.py move <id> <x> <y>")
            sys.exit(1)
        cmd_move(args[1], args[2], args[3])

    elif cmd == "renumber":
        if len(args) < 3:
            print("사용법: python canvas_tool.py renumber <id> <num>")
            sys.exit(1)
        cmd_renumber(args[1], args[2])

    elif cmd == "add":
        if len(args) < 6:
            print("사용법: python canvas_tool.py add <id> <num> <name> <x> <y>")
            sys.exit(1)
        cmd_add(args[1], args[2], args[3], args[4], args[5])

    elif cmd == "remove":
        if len(args) < 2:
            print("사용법: python canvas_tool.py remove <id>")
            sys.exit(1)
        cmd_remove(args[1])

    elif cmd == "status":
        cmd_status()

    else:
        print(f"알 수 없는 명령: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
