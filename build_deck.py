# -*- coding: utf-8 -*-
"""
하네스톤 #1 우승 회고 → 토스 스타일 단일 HTML 발표덱 빌더.
3계층 분리:
  - DATA      : SLIDES (저작 데이터)
  - LOGIC     : render_* (슬라이드 타입별 렌더 함수)
  - PRESENT.  : CSS / JS / HTML 템플릿
이미지는 ./img 상대경로. 결과: ./index.html
엔진 출처: ppt_build/build_deck.py (눈오지 강의덱) — 폰 스크린샷용 렌더러 추가.
"""
import html, os

OUT = os.path.join(os.path.dirname(__file__), "index.html")

def esc(t): return html.escape(t, quote=False)
def img(name): return f"img/{name}"

# ───────────────────────── LOGIC: renderers ─────────────────────────
def s_cover(d):
    return f"""
<section class="slide cover" data-tag="">
  <div class="cover-label">{esc(d['kicker'])}</div>
  <h1 class="cover-title">{d['title']}</h1>
  <p class="cover-sub">{esc(d['sub'])}</p>
  <div class="cover-foot">{esc(d['foot'])}</div>
</section>"""

def s_section(d):
    return f"""
<section class="slide section" data-tag="">
  <div class="sec-no">{esc(d['no'])}</div>
  <div class="sec-kicker">{esc(d['kicker'])}</div>
  <h2 class="sec-title">{d['title']}</h2>
  <p class="sec-goal">{esc(d['goal'])}</p>
</section>"""

def s_big(d):
    sub = f"<p class='big-sub'>{d['sub']}</p>" if d.get('sub') else ""
    return f"""
<section class="slide big {d.get('mood','')}" data-tag="{esc(d.get('tag',''))}">
  <div class="big-mark">{esc(d.get('mark','"'))}</div>
  <h2 class="big-text">{d['title']}</h2>{sub}
  {f"<div class='big-by'>{esc(d['by'])}</div>" if d.get('by') else ""}
</section>"""

def s_bullets(d):
    items="".join(f"<li>{l}</li>" for l in d['items'])
    note=f"<div class='note'>{d['note']}</div>" if d.get('note') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <ul class="bullets">{items}</ul>{note}
</section>"""

def s_cards(d):
    cs=""
    for c in d['cards']:
        no=f"<div class='card-no'>{esc(c['n'])}</div>" if c.get('n') else ""
        cs+=f"<div class='card'>{no}<div class='card-title'>{esc(c['title'])}</div><div class='card-desc'>{c['desc']}</div></div>"
    note=f"<div class='note'>{d['note']}</div>" if d.get('note') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <div class="cards cols{len(d['cards'])}">{cs}</div>{note}
</section>"""

def s_compare(d):
    bad="".join(f"<li>{esc(x)}</li>" for x in d['bad'])
    good="".join(f"<li>{esc(x)}</li>" for x in d['good'])
    note=f"<div class='note'>{d['note']}</div>" if d.get('note') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <div class="cmp">
    <div class="cmp-col bad"><div class="cmp-h">{esc(d.get('badh','이렇게 말하면'))}</div><ul>{bad}</ul></div>
    <div class="cmp-col good"><div class="cmp-h">{esc(d.get('goodh','이렇게 바꾼다'))}</div><ul>{good}</ul></div>
  </div>{note}
</section>"""

def _shots(items, arrow=False):
    cells=""
    for i,it in enumerate(items):
        cap=f"<div class='ph-cap'>{esc(it['cap'])}</div>" if it.get('cap') else ""
        cells+=f"<figure class='ph'><div class='ph-frame'><img src=\"{img(it['img'])}\" alt=\"\"></div>{cap}</figure>"
        if arrow and i < len(items)-1:
            cells+="<div class='ph-arrow'>→</div>"
    return cells

def s_gallery(d):
    note=f"<div class='note'>{d['note']}</div>" if d.get('note') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head tight"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title sm">{d['title']}</h2></div>
  <div class="gallery n{len(d['items'])}">{_shots(d['items'], d.get('arrow',False))}</div>{note}
</section>"""

def s_shot(d):
    pts="".join(f"<li>{l}</li>" for l in d.get('points',[]))
    cap=f"<div class='ph-cap'>{esc(d['cap'])}</div>" if d.get('cap') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <div class="shotsplit">
    <div class="shot-media"><figure class="ph big"><div class="ph-frame"><img src="{img(d['img'])}" alt=""></div>{cap}</figure></div>
    <ul class="bullets">{pts}</ul>
  </div>
</section>"""

def s_wide(d):
    pts="".join(f"<li>{l}</li>" for l in d.get('points',[]))
    body=f"<ul class='bullets sm'>{pts}</ul>" if pts else ""
    cap=f"<div class='cap'>{esc(d['cap'])}</div>" if d.get('cap') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head tight"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title sm">{d['title']}</h2></div>
  <div class="widewrap"><div class="wframe"><img src="{img(d['img'])}" alt=""></div>{cap}</div>{body}
</section>"""

def s_spec(d):
    stats="".join(
      f"<div class='stat'><div class='stat-v'>{s['v']}</div><div class='stat-k'>{esc(s['k'])}</div></div>"
      for s in d['stats'])
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <div class="specsplit">
    <div class="stats">{stats}</div>
    <figure class="proof"><img src="{img(d['img'])}" alt=""><figcaption>{esc(d['cap'])}</figcaption></figure>
  </div>
  {f"<div class='note'>{d['note']}</div>" if d.get('note') else ""}
</section>"""

def s_steps(d):
    cells=""
    for i,st in enumerate(d['steps']):
        arrow="<div class='step-arrow'>→</div>" if i<len(d['steps'])-1 else ""
        cells+=f"<div class='step'><div class='step-no'>{esc(st['n'])}</div><div class='step-title'>{esc(st['title'])}</div><div class='step-desc'>{esc(st['desc'])}</div></div>{arrow}"
    note=f"<div class='note'>{d['note']}</div>" if d.get('note') else ""
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title">{d['title']}</h2></div>
  <div class="steps">{cells}</div>{note}
</section>"""

def s_checklist(d):
    items="".join(f"<li><i>{i+1:02d}</i>{esc(x)}</li>" for i,x in enumerate(d['items']))
    return f"""
<section class="slide" data-tag="{esc(d.get('tag',''))}">
  <div class="s-head tight"><span class="s-tag">{esc(d.get('kicker',''))}</span><h2 class="s-title sm">{d['title']}</h2></div>
  <ol class="chk">{items}</ol>
  {f"<div class='note'>{d['note']}</div>" if d.get('note') else ""}
</section>"""

def s_takeaway(d):
    pts="".join(f"<li>{l}</li>" for l in d['points'])
    return f"""
<section class="slide takeaway" data-tag="{esc(d.get('tag',''))}">
  <div class="tk-badge">{esc(d.get('badge','핵심 정리'))}</div>
  <h2 class="tk-title">{d['title']}</h2>
  <ul class="tk-list">{pts}</ul>
</section>"""

def s_closing(d):
    pts="".join(f"<li>{l}</li>" for l in d.get('points',[]))
    return f"""
<section class="slide closing" data-tag="">
  <div class="cl-kicker">{esc(d['kicker'])}</div>
  <h2 class="cl-title">{d['title']}</h2>
  <ul class="cl-list">{pts}</ul>
  <div class="cl-brand">{esc(d['brand'])}</div>
</section>"""

RENDER={"cover":s_cover,"section":s_section,"big":s_big,"bullets":s_bullets,"cards":s_cards,
 "compare":s_compare,"gallery":s_gallery,"shot":s_shot,"wide":s_wide,"steps":s_steps,
 "spec":s_spec,"checklist":s_checklist,"takeaway":s_takeaway,"closing":s_closing}

# ───────────────────────── DATA ─────────────────────────
T = "하네스톤 #1"

SLIDES = [

# ══════ 오프닝 ══════
{"type":"cover","kicker":"하네스톤 #1 우승 회고",
 "title":'AI는 디자인을<br>더럽게 못합니다',
 "sub":"그래서 디자인 하네스를 만들었습니다",
 "foot":"2026.08.01 바이브마피아클럽 하네스톤 #1 · 최병찬"},

{"type":"big","tag":T,"mark":"?",
 "title":'무언가를 만들 때 가장 큰 적이 뭐냐고 물으면,<br>저는 <span class="hl">디자인</span>이라고 답합니다'},

{"type":"bullets","tag":T,"kicker":"증상","title":"코드는 나오는데, 화면이 이상합니다",
 "items":["시키면 코드는 곧잘 나옵니다. 돌아가고, 에러도 없습니다",
          "그런데 화면을 열면 버튼 크기가 제각각이고 간격이 들쭉날쭉합니다",
          "딱 집어 말하긴 어려운데, <b>“AI가 만들었네”</b> 소리가 나옵니다"]},

{"type":"cards","tag":T,"kicker":"원인","title":"“돌아가는지”는 알아도 “예쁜지”는 모릅니다",
 "cards":[
   {"n":"1","title":"작동은 판정된다","desc":"테스트가 통과했나, 에러가 났나.<br>답이 정해져 있어 기계가 확인합니다"},
   {"n":"2","title":"예쁨은 판정이 안 된다","desc":"“이게 예쁜가?”에는 PASS/FAIL이<br>없습니다. 그래서 그냥 넘어갑니다"},
   {"n":"3","title":"화면이 마지막 관문","desc":"사람 없이 코드 짜는 것보다<br>화면을 끝내는 게 훨씬 어렵습니다"}]},

# ══════ 01. 하네스 ══════
{"type":"section","no":"01","kicker":"WHY HARNESS","title":"디자인 하네스가<br>필요하다",
 "goal":"모델을 바꾸는 게 아니라, 모델이 일하는 틀을 바꾼다"},

{"type":"bullets","tag":T,"kicker":"하네스란","title":"AI를 바꾸는 게 아니라, 일하는 틀을 바꿉니다",
 "items":["같은 사람도 혼자 일할 때와 리뷰·체크리스트가 있는 팀에서 결과가 다릅니다",
          "하네스는 AI한테 그 <b>팀 환경</b>을 만들어주는 겁니다",
          "순서를 정하고 · 단계마다 산출물을 남기고 · 검사할 에이전트를 붙인다"],
 "note":"“그냥 좋은 모델 쓰면 되지 않나요?” — 그 얘기는 뒤에서 다시 하겠습니다. 답은 아니오에 가깝습니다."},

{"type":"cards","tag":T,"kicker":"대회","title":"하네스만으로 겨루는 대회에 나갔습니다",
 "cards":[
   {"title":"주최","desc":"바이브마피아클럽<br>2026.08.01 · AI Native 디자인 해커톤"},
   {"title":"주제","desc":"“토스가 만약<br>여행앱을 만든다면?”"},
   {"title":"PRD 비공개","desc":"심사 직전까지 미공개 +<br>당일 교체. 미리 못 만듭니다"},
   {"title":"조건","desc":"명령어 한 줄 → 무인 실행<br>중간 개입 금지"}],
 "note":"사람이 못 끼어든다는 건, <b>하네스가 견고한 만큼만 결과가 나온다</b>는 뜻입니다."},

{"type":"gallery","tag":T,"kicker":"결과","title":"1조 우승 — 명령어 한 줄로 나온 화면들",
 "items":[{"img":"r-01-home.png","cap":"홈"},{"img":"r-03-search.png","cap":"검색"},
          {"img":"r-05-results.png","cap":"검색 결과"},{"img":"r-06-filter.png","cap":"필터"},
          {"img":"r-07-compare.png","cap":"비교"},{"img":"r-08-fare.png","cap":"운임 선택"}],
 "note":"전부 12개 화면 중 6개입니다. <b>손으로 그린 화면은 하나도 없습니다.</b>"},

{"type":"bullets","tag":T,"kicker":"고백","title":"저는 화면을 만든 사람이 아닙니다",
 "items":["조장은 이동욱 님, 팀에 UX/UI 전문가가 있었습니다",
          "제 몫은 둘. <b>전문가 노하우를 에이전트 지침으로 번역</b>하는 일, 그리고 <b>전날 밤 리허설</b>",
          "오늘 공유하는 건 “제가 만든 것”이 아니라 <b>번역하면서 배운 것</b>입니다"]},

# ══════ 02. 규칙 ══════
{"type":"section","no":"02","kicker":"RULES","title":"예쁜 디자인에도<br>규칙이 있지 않을까",
 "goal":"감각이라면 못 시킨다. 규칙이라면 시킬 수 있다"},

{"type":"compare","tag":T,"kicker":"번역","title":"“예쁘게 만들어줘”는 지시가 아니라 소원입니다",
 "bad":["예쁘게 만들어줘","감각 있게","요즘 느낌으로","토스처럼"],
 "good":["좌우 여백은 전 화면에서 하나의 값","글자 크기는 정해둔 5단 밖으로 안 나간다","색은 7개 예산 안에서만","목록은 최소 4행"],
 "note":"신입 디자이너한테 “예쁘게 해와”라고 하면 못 알아듣습니다. 에이전트도 똑같습니다."},

{"type":"big","tag":T,"mark":"!",
 "title":'예쁨은 창의성이 아니었습니다<br><span class="hl">일관성 + 위계 + 실물감</span>이었습니다',
 "sub":"그리고 셋 다 규칙으로 강제할 수 있습니다"},

{"type":"gallery","tag":T,"kicker":"일관성","title":"헤더·여백·탭바가 같으면, 다른 화면도 한 앱으로 보입니다",
 "items":[{"img":"r-01-home.png","cap":"홈"},{"img":"r-05-results.png","cap":"결과"},{"img":"r-07-compare.png","cap":"비교"}],
 "note":"세 화면의 상단 높이·좌우 여백·모서리 둥글기가 전부 같은 값입니다. 통일감의 8할이 여기서 나옵니다."},

{"type":"big","tag":T,"mark":"✓",
 "title":'규칙은 <span class="hl">판정 가능한 문장</span>이어야 합니다',
 "sub":'“간격을 일관되게” → 취향입니다<br>“8의 배수가 아닌 간격이 있는가” → PASS / FAIL이 나옵니다'},

# ══════ 03. 3대 기둥 ══════
{"type":"section","no":"03","kicker":"THE BIG THREE","title":"제일 컸던 셋",
 "goal":"컴포넌트 · 고객 여정 · 경쟁사 분석"},

{"type":"big","tag":T,"mark":"3",
 "title":'<span class="hl">컴포넌트</span> · <span class="hl">고객 여정</span> · <span class="hl">경쟁사 분석</span>',
 "sub":"나머지 규칙을 다 지켜도, 이 셋이 없으면 “잘 정돈된 남의 화면”이 나옵니다"},

# ① 컴포넌트
{"type":"bullets","tag":T,"kicker":"① 컴포넌트","title":"목수는 매번 나무를 새로 재단하지 않습니다",
 "items":["가구를 만들 때 <b>규격 자재를 조립</b>합니다. 매번 톱질부터 하지 않습니다",
          "화면도 같습니다. 부품을 먼저 만들고, 화면은 <b>조립만</b> 합니다",
          "순서가 뒤집히면 버튼이 필요할 때마다 새로 그립니다 — 그래서 화면마다 다르게 생깁니다"]},

{"type":"wide","tag":T,"kicker":"① 컴포넌트","title":"번호를 못 남긴 부품은, 만든 게 아니다",
 "img":"comp-card.png",
 "cap":"항공권 카드 컴포넌트 — 검색 결과 · 비교 · 운임 화면에 같은 부품이 그대로 들어갑니다",
 "points":["부품마다 일련번호를 붙이고 목록에 남긴다",
           "화면 단계에서 <b>새 부품 생성 금지</b> — 없으면 부품 단계로 되돌아간다"]},

{"type":"cards","tag":T,"kicker":"① 컴포넌트","title":"부품을 먼저 만들면 셋이 따라옵니다",
 "cards":[
   {"n":"1","title":"일관성이 공짜","desc":"같은 부품을 쓰니<br>같게 생길 수밖에 없습니다"},
   {"n":"2","title":"검사가 싸진다","desc":"화면 20개가 아니라<br>부품 8개만 보면 됩니다"},
   {"n":"3","title":"한 번만 고친다","desc":"부품 하나 고치면 끝.<br>화면을 돌아다니지 않습니다"}]},

# ② 고객 여정
{"type":"gallery","tag":T,"kicker":"② 고객 여정","title":"화면 목록이 아니라, 사용자가 걷는 길",
 "arrow":True,
 "items":[{"img":"r-01-home.png","cap":"진입"},{"img":"r-03-search.png","cap":"탐색"},
          {"img":"r-05-results.png","cap":"목록"},{"img":"r-06-filter.png","cap":"좁히기"},
          {"img":"r-07-compare.png","cap":"결정"}],
 "note":"화면 하나하나가 멀쩡해도 순서가 없으면 앱이 안 됩니다."},

{"type":"shot","tag":T,"kicker":"② 고객 여정","title":"그 길을 걷는 사람을 딱 한 명으로 정합니다",
 "img":"r-05-results.png","cap":"“이 사람이 이 화면을 열면, 위쪽 세 칸에 뭐가 있어야 하나”",
 "points":["“여행 앱 사용자”는 사람이 아닙니다. 아무 결정도 못 내리게 하는 말입니다",
           "타깃 한 명을 정하고 <b>화면 상단 3섹션의 우선순위</b>만 결정합니다",
           "여기선 날짜 스크러버가 1순위였습니다 — “이틀 앞당기면 2만원 더 싸요”",
           "페르소나 문서는 안 만듭니다. <b>결정 결과만 뼈대에 반영</b>하고 근거 한 줄"]},

# ③ 경쟁사
{"type":"big","tag":T,"mark":"“","by":"팀 UX/UI 전문가",
 "title":'“당근이 증권 앱을 만든다면,<br>화면에 <span class="hl">내 주변 사람들이 산 종목</span>이 나와야 당근답습니다”',
 "sub":"참고할 건 UI가 아니라, 그 서비스가 세상에서 차지한 자리입니다"},

{"type":"gallery","tag":T,"kicker":"③ 경쟁사","title":"그래서 경쟁사를 세 갈래로 동시에 팠습니다",
 "items":[{"img":"s-toss.png","cap":"토스 (톤 기준)"},{"img":"s-hantu.png","cap":"한국투자"},
          {"img":"s-kiwoom.png","cap":"키움"},{"img":"s-mirae.jpg","cap":"미래에셋"},
          {"img":"s-samsung.png","cap":"삼성증권"}],
 "note":"시간이 제일 많이 드는 단계라 병렬로 돌립니다. 겉(치수·색)과 속(무엇을 파는가)을 따로 기록합니다."},

{"type":"gallery","tag":T,"kicker":"③ 경쟁사","title":"베끼는 게 아니라, 문법을 가져와 우리 도메인에 다시 씁니다",
 "items":[{"img":"c-skyscanner-cal.png","cap":"Skyscanner — 날짜별 최저가 캘린더"},
          {"img":"r-05-results.png","cap":"우리 결과 — 날짜 가격 스크러버"}],
 "note":"“언제 가면 얼마나 싼가”라는 소구는 가져오되, 캘린더 그리드가 아니라 스크러버 한 줄로 압축했습니다."},

{"type":"spec","tag":T,"kicker":"③ 경쟁사","title":"감도는 실측에서 나옵니다",
 "stats":[{"v":"390<i>px</i>","k":"화면 폭"},{"v":"110<i>px</i>","k":"목록 한 줄 높이"},
          {"v":"7<i>개</i>","k":"실제 쓰인 색"},{"v":"×8","k":"모든 간격이 8의 배수"}],
 "img":"p-assets-crop.png","cap":"Penpot ASSETS 실측 — COLORS 5 · Inter 12/14/16/18 · W 390",
 "note":"눈으로 보고 짐작한 값이 아닙니다. <b>재는 순간 그게 그대로 지침이 됩니다.</b>"},

{"type":"bullets","tag":T,"kicker":"③ 경쟁사","title":"없는 건 발명하지 말고 파생시킵니다",
 "items":["당근에는 <b>주가 등락을 표시할 빨강/파랑이 없습니다</b>. 증권 앱엔 필요한데요",
          "여기서 AI를 풀어두면 새 색·새 모양을 발명하고 브랜드가 깨집니다",
          "그래서 <b>추가 허용은 딱 2색</b>. 주조색은 버튼·활성탭 자리를 지킵니다"],
 "note":"원칙 한 줄 — <b>새 값을 만들지 말고 기존 값에서 파생시킨다.</b>"},

# ══════ 04. 하네스 ══════
{"type":"section","no":"04","kicker":"HOW","title":"하네스는<br>이렇게 만들었습니다",
 "goal":"각 단계는 다음 단계를 구속하는 산출물을 낸다"},

{"type":"steps","tag":T,"kicker":"파이프라인","title":"11단계를, 성격이 다른 5덩어리로",
 "steps":[
   {"n":"1","title":"읽기","desc":"PRD에서 화면 목록과 고객 여정을 뽑는다"},
   {"n":"2","title":"조사","desc":"기존 자산 실측 + 경쟁사 3갈래 병렬"},
   {"n":"3","title":"가조립","desc":"HTML로 싸게 한 번 만들어본다"},
   {"n":"4","title":"부품","desc":"번호 붙은 컴포넌트를 만든다"},
   {"n":"5","title":"조립·검사","desc":"화면은 조립만. 다른 에이전트가 채점"}],
 "note":"구속하지 않는 산출물은 장식입니다. “왜 이 단계가 있냐”에 답을 못 합니다."},

{"type":"bullets","tag":T,"kicker":"가조립","title":"비싼 실패 전에, 싼 실패를 먼저 합니다",
 "items":["부품을 제대로 만들기 전에 HTML로 화면을 대충 조립합니다",
          "목적은 예쁜 화면이 아니라 <b>빨리 틀리는 것</b>",
          "종이에 스케치하고 나서 목재를 자르는 것과 같습니다"]},

{"type":"bullets","tag":T,"kicker":"장치","title":"만든 놈이 채점하면, 같은 실수가 반복됩니다",
 "items":["화면을 만드는 에이전트와 평가하는 에이전트를 <b>아예 분리</b>했습니다",
          "평가 쪽은 제작 쪽의 <b>자기 보고서를 일부러 읽지 않습니다.</b> 결과물만 봅니다",
          "보고서를 읽는 순간 “이건 이래서 이렇게 했다”는 변명에 설득당하니까요"],
 "note":"사람도 똑같습니다. 자기 글 오타는 안 보입니다."},

{"type":"gallery","tag":T,"kicker":"중간 검토","title":"검토를 중간중간 넣어라 — 이게 없으면 나머지가 무의미합니다",
 "items":[{"img":"r-09-loading.png","cap":"로딩"},{"img":"r-10-empty.png","cap":"빈 상태"},
          {"img":"r-04-search-error.png","cap":"검색 실패"},{"img":"r-11-pricechange.png","cap":"가격 변동"},
          {"img":"r-12-closed.png","cap":"마감"}],
 "note":"이 다섯 장이 검토 게이트의 증거입니다. 끝에 한 번만 봤으면 절대 안 만들었을 화면들입니다."},

{"type":"bullets","tag":T,"kicker":"중간 검토","title":"관문은 통과/실패만 냅니다",
 "items":["화면 목록이 맞나 → 부품이 다 번호가 있나 → 화면이 규칙을 지켰나",
          "실패하면 <b>그 단계로 되돌아갑니다.</b> 다음으로 못 넘어갑니다",
          "관문이 없으면 에이전트는 <b>틀린 걸 들고 끝까지 갑니다</b> — 무인 실행의 기본 성질입니다"]},

{"type":"bullets","tag":T,"kicker":"루프","title":"지적을 하나씩 고치지 않습니다",
 "items":["지적 20개를 그 자리에서 하나씩 고치면, 다음에 또 20개 나옵니다",
          "<b>비슷한 원인끼리 묶습니다.</b> “간격 틀린 곳 7개”는 사실 문제 하나입니다",
          "묶은 원인을 <b>상위 단계 지침에 반영</b>하고 다시 돌립니다. 최대 3회"],
 "note":"긁힌 자국을 메우는 게 아니라 사포질 방식을 바꾸는 겁니다. 사람이 없을 때 품질이 오르는 유일한 경로."},

# ══════ 05. 실패담 ══════
{"type":"section","no":"05","kicker":"FAILURES","title":"무인 실행이<br>무너지는 지점",
 "goal":"셋 다 코드는 멀쩡했습니다"},

{"type":"bullets","tag":T,"kicker":"무음 실패","title":"제일 무서운 건, 실패처럼 안 생긴 실패입니다",
 "items":["에러가 나면 오히려 낫습니다. 알아채고 고칠 수 있으니까요",
          "<b>무음 실패</b>는 에러 없이, 성공한 척하고, 실제로는 아무 일도 안 일어난 겁니다",
          "영수증은 나왔는데 결제가 안 된 상태입니다. 계산대에선 아무도 모릅니다"]},

{"type":"bullets","tag":T,"kicker":"실물","title":"토큰 바인딩이 조용히 실패했습니다",
 "items":["색에 이름을 붙이고 도형을 그 이름에 묶는 작업. 에러 없이 통과했고 <b>색도 눈으로는 맞았습니다</b>",
          "그런데 다시 읽어보니 <b>묶인 게 하나도 없었습니다.</b> 값만 우연히 맞았던 겁니다",
          "협업자가 변수값을 바꿔도 화면은 반응하지 않습니다. 실사용에서 발견 불가"],
 "note":"전날 밤 리허설에서 발견했습니다. 안 해봤으면 그대로 제출했습니다."},

{"type":"big","tag":T,"mark":"✓",
 "title":'그래서 넣은 것 — <span class="hl">자기점검</span>',
 "sub":"“했다”는 보고를 믿지 않고, 결과를 되읽어서 진짜 들어갔는지 확인한다"},

{"type":"bullets","tag":T,"kicker":"당일","title":"와이파이가 우리 서버를 막고 있었습니다",
 "items":["행사장 네트워크가 저희 디자인 서버로 가는 통신을 차단하고 있었습니다",
          "비밀번호를 잘못 넣은 줄 알고 한참 헤맸고, 결국 <b>집에 있는 맥미니를 경유</b>해 우회했습니다",
          "무인 실행을 준비할 때 정작 챙길 건 코드가 아니라 <b>네트워크 경로</b>였습니다"]},

{"type":"wide","tag":T,"kicker":"당일","title":"남의 작업 위에 그릴 뻔했습니다",
 "img":"p-pages.png",
 "cap":"한 파일 안에 팀원별 페이지가 나란히 — 잘못 고르면 그 즉시 남의 화면 위에 그립니다",
 "points":["페이지 전환이 반영되기 전에 그리기가 시작돼 <b>이전 페이지에 도형이 생겼습니다</b>",
           "혼자 쓰는 파일이면 사고로 끝나지만, 공용 파일이면 <b>남의 작업이 오염</b>됩니다"]},

{"type":"takeaway","tag":T,"badge":"세 실패의 공통점","title":"셋 다 코드는 멀쩡했습니다",
 "points":["셋 다 <b>성공한 것처럼 보였습니다</b> — 에러도, 경고도 없었습니다",
           "셋 다 <b>직접 다시 확인해서</b> 발견했습니다. 안 봤으면 그대로 제출했습니다",
           "무인 실행에서 사람 대신 이 확인을 해줄 건, 하네스밖에 없습니다"]},

{"type":"big","tag":T,"mark":"!",
 "title":'무인 실행이 통하려면,<br>사람이 없어도 <span class="hl">실패를 스스로 알아채는 장치</span>가 먼저 있어야 합니다'},

# ══════ 클로징 ══════
{"type":"cards","tag":T,"kicker":"다음","title":"다음에 한다면 두 가지를 바꾸겠습니다",
 "cards":[
   {"n":"1","title":"중간에 한 번은 사람이 본다","desc":"명령어 한 줄로 끝까지 가는 건 멋있지만<br>리스크가 큽니다. 중간 산출물을 한 번 보고<br>교정하는 편이 결과가 낫습니다"},
   {"n":"2","title":"유인/무인 모드를 스위치로","desc":"사람 승인을 전제로 만든 안전장치는<br>무인 실행에서 <b>오히려 데드락</b>이 됩니다.<br>승인을 영원히 기다리니까요"}]},

{"type":"takeaway","tag":T,"badge":"오늘 가져갈 것","title":"세 가지만 가져가신다면",
 "points":["<b>부품부터 만드세요.</b> 화면은 조립만. “번호 없는 부품은 만든 게 아니다”를 규칙으로 박으면 일관성이 공짜로 따라옵니다",
           "<b>겉이 아니라 여정과 포지션을 베끼세요.</b> 화면 목록이 아니라 사용자가 걷는 길, UI가 아니라 그 서비스가 차지한 자리",
           "<b>검토를 중간중간 넣으세요.</b> 끝에 한 번은 늦습니다. 그리고 만든 놈이 채점하게 두지 마세요"]},

{"type":"checklist","tag":T,"kicker":"부록","title":"critic 루브릭 — 그대로 복사해 쓰세요",
 "items":["모든 화면 폭이 390인가",
          "좌우 여백이 16이 아닌 요소가 있는가 (풀블리드 제외)",
          "8의 배수가 아닌 간격이 있는가",
          "글자 크기가 {10,12,14,16,18} 밖인 텍스트가 있는가",
          "정해둔 7색 밖의 fill/stroke가 있는가",
          "radius가 {4,100} 밖인 도형이 있는가",
          "“Lorem”·“텍스트”·“제목” 더미가 남아 있는가",
          "글자가 컨테이너를 벗어나거나 겹치는 곳이 있는가",
          "목록 화면의 행이 4개 미만인가",
          "요구된 화면·요소 중 누락이 있는가",
          "헤더·탭바가 없는 화면이 있는가 (모달 제외)",
          "같은 역할 요소인데 화면마다 수치가 다른 곳이 있는가"],
 "note":"각 항목 PASS / FAIL. FAIL이면 <b>원인 요소 이름과 수정안을 명시</b>하게 합니다 — 그래야 되돌릴 단계가 정해집니다."},

{"type":"closing","kicker":"마무리",
 "title":"감각은 못 가르칩니다<br>대신 검사표는 줄 수 있습니다",
 "points":["규칙은 취향을 대신하는 게 아니라, 취향이 흔들릴 자리를 없애는 것입니다",
           "좋은 지침은 잘 만든 걸 <b>실제로 재본 데서</b> 나옵니다",
           "팀 UX/UI 전문가 덕분에 지평이 넓어졌습니다"],
 "brand":"하네스톤 #1 · 최병찬"},
]

# ───────────────────────── PRESENTATION ─────────────────────────
def render_slides():
    return "\n".join(RENDER[d["type"]](d) for d in SLIDES)

CSS = r"""
:root{
  --blue:#3182F6; --blue-d:#1B64DA; --blue-soft:#E8F3FF;
  --ink:#191F28; --g700:#333D4B; --g600:#4E5968; --g500:#6B7684; --g400:#8B95A1;
  --bg:#FFFFFF; --bg2:#F7F8FA; --bg3:#F2F4F6; --line:#E5E8EB; --red:#F04452;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#0a0c10;overflow:hidden;
  font-family:"Pretendard","Pretendard Variable","Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;color:var(--ink);letter-spacing:-.2px}
#scaler{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#stage{width:1280px;height:720px;position:relative;transform-origin:center center;
  background:var(--bg);box-shadow:0 30px 90px rgba(0,0,0,.4);overflow:hidden}

.slide{position:absolute;inset:0;padding:56px 72px;opacity:0;visibility:hidden;
  transition:opacity .35s ease;display:flex;flex-direction:column;background:var(--bg)}
.slide.active{opacity:1;visibility:visible;z-index:2}
.slide::after{content:attr(data-tag);position:absolute;right:34px;top:26px;font-size:12px;color:#C2C8D0;font-weight:600}
.hl{color:var(--blue)}
b{font-weight:800;color:var(--ink)}

.s-head{flex:none;margin-bottom:28px}
.s-head.tight{margin-bottom:18px}
.s-tag{display:inline-block;font-size:15px;font-weight:800;color:var(--blue);
  background:var(--blue-soft);padding:6px 15px;border-radius:999px}
.s-title{font-size:42px;line-height:1.24;font-weight:800;margin-top:14px;letter-spacing:-1px}
.s-title.sm{font-size:34px;margin-top:12px}

/* cover */
.cover{justify-content:center;padding:90px 84px;background:
  radial-gradient(1200px 700px at 88% -8%,#EAF2FF 0%,#F7FAFF 42%,#FFFFFF 70%)}
.cover-label{font-size:20px;font-weight:800;color:var(--blue);margin-bottom:24px}
.cover-title{font-size:82px;line-height:1.1;font-weight:900;letter-spacing:-3px}
.cover-sub{font-size:24px;line-height:1.5;color:var(--g600);margin-top:28px;font-weight:600}
.cover-foot{position:absolute;left:84px;bottom:58px;font-size:16px;font-weight:700;color:var(--g400)}
.cover-foot::before{content:"●";color:var(--blue);margin-right:9px;font-size:11px;vertical-align:middle}

/* section divider */
.section{justify-content:center;background:var(--bg3)}
.sec-no{font-size:140px;font-weight:900;line-height:1;letter-spacing:-4px;color:var(--blue)}
.sec-kicker{font-size:17px;font-weight:800;color:var(--g400);letter-spacing:3px;margin-top:16px}
.sec-title{font-size:56px;font-weight:900;line-height:1.14;margin-top:10px;letter-spacing:-1.5px}
.sec-goal{font-size:20px;color:var(--g600);margin-top:24px;line-height:1.55;max-width:820px;font-weight:600;
  border-left:4px solid var(--blue);padding-left:18px}

/* big statement */
.big{justify-content:center;background:var(--bg3);padding:70px 90px}
.big.dark{background:var(--ink)}
.big-mark{font-size:64px;font-weight:900;color:var(--blue);line-height:1;opacity:.9;margin-bottom:18px}
.big-text{font-size:50px;line-height:1.34;font-weight:900;letter-spacing:-1.4px;max-width:1080px}
.big-sub{font-size:22px;line-height:1.6;color:var(--g600);margin-top:28px;font-weight:600;max-width:960px}
.big-by{margin-top:26px;font-size:18px;font-weight:800;color:var(--blue)}

/* bullets */
.bullets{list-style:none;display:flex;flex-direction:column;gap:18px}
.slide > .bullets{flex:1;justify-content:center}
.bullets li{position:relative;font-size:25px;line-height:1.44;color:var(--g700);padding-left:36px;font-weight:600}
.bullets li::before{content:"";position:absolute;left:2px;top:11px;width:13px;height:13px;border-radius:50%;background:var(--blue)}
.bullets.sm li{font-size:20px;padding-left:30px}
.bullets.sm li::before{width:10px;height:10px;top:9px}
.note{margin-top:auto;font-size:18px;color:var(--g600);background:var(--bg3);
  padding:15px 22px;border-radius:14px;line-height:1.5;font-weight:600;flex:none}

/* cards */
.cards{display:grid;gap:18px;margin-top:2px;flex:1;align-content:center}
.cards.cols2{grid-template-columns:repeat(2,1fr)}
.cards.cols3{grid-template-columns:repeat(3,1fr)}
.cards.cols4{grid-template-columns:repeat(4,1fr)}
.card{background:var(--bg2);border:1px solid var(--line);border-radius:20px;padding:26px 22px;
  display:flex;flex-direction:column;gap:11px}
.card-no{width:40px;height:40px;border-radius:12px;background:var(--blue);color:#fff;font-weight:900;
  font-size:19px;display:flex;align-items:center;justify-content:center}
.card-title{font-size:21px;font-weight:800}
.card-desc{font-size:16px;color:var(--g600);line-height:1.5;font-weight:500}

/* compare */
.cmp{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:22px;min-height:0}
.cmp-col{border-radius:20px;padding:26px 28px;display:flex;flex-direction:column;gap:16px}
.cmp-col.bad{background:#FFF3F3;border:1px solid #FFD9DC}
.cmp-col.good{background:#EFF6FF;border:1px solid #D6E7FF}
.cmp-h{font-size:17px;font-weight:800;letter-spacing:-.3px}
.cmp-col.bad .cmp-h{color:var(--red)}
.cmp-col.good .cmp-h{color:var(--blue-d)}
.cmp-col ul{list-style:none;display:flex;flex-direction:column;gap:13px}
.cmp-col li{font-size:21px;font-weight:700;line-height:1.4;padding-left:30px;position:relative;color:var(--g700)}
.cmp-col.bad li::before{content:"✕";position:absolute;left:0;color:var(--red);font-weight:900}
.cmp-col.good li::before{content:"✓";position:absolute;left:0;color:var(--blue);font-weight:900}

/* phone shots — 이미지가 칸에 맞춰 줄어들도록 flex:1 1 0 + contain */
.gallery{flex:1;display:flex;align-items:stretch;justify-content:center;gap:18px;min-height:0}
.gallery.n5,.gallery.n6{gap:10px}
.ph{display:flex;flex-direction:column;gap:9px;min-height:0;min-width:0}
.gallery > .ph{flex:1 1 0}
.ph-frame{flex:1;min-height:0;min-width:0;display:flex;align-items:center;justify-content:center}
.ph-frame img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;
  border-radius:12px;border:1px solid var(--line);box-shadow:0 8px 24px rgba(20,30,70,.12)}
.ph-cap{flex:none;font-size:15px;color:var(--g500);font-weight:700;text-align:center}
.ph-arrow{flex:none;color:var(--blue);font-size:24px;font-weight:900;align-self:center}

/* shot + text */
.shotsplit{flex:1;display:grid;grid-template-columns:330px 1fr;gap:44px;align-items:stretch;min-height:0}
.shot-media{min-height:0;min-width:0;display:flex}
.shot-media .ph{flex:1;min-height:0}

/* wide screenshot */
.widewrap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;min-height:0}
.wframe{min-height:0;min-width:0;display:flex;align-items:center;justify-content:center}
.wframe img{display:block;max-width:100%;max-height:100%;object-fit:contain;border-radius:14px;
  border:1px solid var(--line);box-shadow:0 10px 28px rgba(20,30,70,.12)}
.cap{font-size:16px;color:var(--g500);font-weight:600;text-align:center;flex:none}
.widewrap + .bullets{flex:none;margin-top:16px}

/* spec — 실측 숫자 + 증거 캡처 */
.specsplit{flex:1;display:grid;grid-template-columns:1fr 250px;gap:40px;align-items:center;min-height:0}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.stat{background:var(--bg2);border:1px solid var(--line);border-radius:20px;padding:22px 26px}
.stat-v{font-size:52px;font-weight:900;color:var(--blue);letter-spacing:-2px;line-height:1}
.stat-v i{font-style:normal;font-size:24px;font-weight:800;margin-left:3px;color:var(--blue-d)}
.stat-k{font-size:17px;font-weight:700;color:var(--g600);margin-top:10px}
.proof{height:100%;display:flex;flex-direction:column;gap:9px;min-height:0}
.proof img{flex:1;min-height:0;width:100%;object-fit:contain;object-position:top;border-radius:12px;
  border:1px solid var(--line);background:#1e1e22}
.proof figcaption{flex:none;font-size:13px;color:var(--g500);font-weight:600;line-height:1.4}

/* steps */
.steps{flex:1;display:flex;align-items:stretch;justify-content:center;gap:8px}
.step{flex:1;background:var(--bg2);border:1px solid var(--line);border-radius:20px;padding:24px 18px;
  display:flex;flex-direction:column;gap:12px}
.step-no{width:42px;height:42px;border-radius:50%;background:var(--blue);color:#fff;font-weight:900;font-size:20px;
  display:flex;align-items:center;justify-content:center}
.step-title{font-size:21px;font-weight:800}
.step-desc{font-size:15.5px;color:var(--g600);line-height:1.45;font-weight:500}
.step-arrow{flex:none;color:var(--blue);font-size:26px;font-weight:900;align-self:center}

/* checklist */
.chk{flex:1;list-style:none;display:grid;grid-template-columns:1fr 1fr;grid-auto-flow:column;
  grid-template-rows:repeat(6,1fr);gap:8px 26px;align-content:center;min-height:0}
.chk li{display:flex;align-items:center;gap:13px;font-size:18px;font-weight:600;color:var(--g700);line-height:1.35}
.chk i{flex:none;width:30px;height:30px;border-radius:9px;background:var(--blue-soft);color:var(--blue-d);
  font-style:normal;font-size:14px;font-weight:900;display:flex;align-items:center;justify-content:center}

/* takeaway */
.takeaway{justify-content:center;background:var(--bg3)}
.tk-badge{display:inline-block;align-self:flex-start;font-size:15px;font-weight:800;color:#fff;
  background:var(--blue);padding:8px 18px;border-radius:999px}
.tk-title{font-size:44px;font-weight:900;line-height:1.22;margin:22px 0 30px;letter-spacing:-1px}
.tk-list{list-style:none;display:flex;flex-direction:column;gap:20px}
.tk-list li{position:relative;font-size:22px;line-height:1.48;color:var(--g700);padding-left:46px;font-weight:600}
.tk-list li::before{content:"✓";position:absolute;left:0;top:-1px;width:31px;height:31px;border-radius:10px;
  background:var(--blue);color:#fff;font-size:18px;font-weight:900;display:flex;align-items:center;justify-content:center}

/* closing */
.closing{justify-content:center;align-items:flex-start;
  background:radial-gradient(1000px 620px at 85% 110%,#2C6FF0 0%,#1B64DA 55%,#0F4FB8 100%);color:#fff}
.closing::after{color:rgba(255,255,255,.4)}
.closing b{color:#fff}
.cl-kicker{font-size:19px;font-weight:800;color:#BBD5FF}
.cl-title{font-size:52px;font-weight:900;margin:14px 0 28px;letter-spacing:-1.5px;line-height:1.2}
.cl-list{list-style:none;display:flex;flex-direction:column;gap:14px}
.cl-list li{position:relative;font-size:22px;line-height:1.45;color:#EAF1FF;padding-left:32px;font-weight:600}
.cl-list li::before{content:"→";position:absolute;left:0;top:0;color:#fff;font-weight:900}
.cl-brand{margin-top:38px;font-size:17px;font-weight:800;color:#BBD5FF}

/* chrome */
#bar{position:fixed;top:0;left:0;height:4px;background:var(--blue);z-index:60;transition:width .3s ease}
#counter{position:fixed;right:18px;bottom:14px;color:#fff;font-size:13px;font-weight:800;
  background:rgba(25,31,40,.72);padding:6px 13px;border-radius:999px;z-index:50}
#hint{position:fixed;left:18px;bottom:14px;color:#E5E8EB;font-size:12.5px;font-weight:700;
  background:rgba(25,31,40,.62);padding:6px 13px;border-radius:999px;z-index:50}

@media print{
  @page{size:1280px 720px;margin:0}
  html,body{height:auto;overflow:visible;background:#fff}
  #scaler{position:static;display:block;inset:auto}
  #stage{transform:none!important;box-shadow:none;width:1280px;height:auto;overflow:visible}
  .slide{position:relative;opacity:1!important;visibility:visible!important;page-break-after:always;
    break-after:page;height:720px;inset:auto;transition:none}
  #bar,#counter,#hint{display:none!important}
}
"""

JS = r"""
const stage=document.getElementById('stage');
const slides=[...document.querySelectorAll('.slide')];
const bar=document.getElementById('bar');
const counter=document.getElementById('counter');
let i=0;
function fit(){const s=Math.min(window.innerWidth/1280,window.innerHeight/720);stage.style.transform='scale('+s+')';}
function show(n){i=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((s,k)=>s.classList.toggle('active',k===i));
  bar.style.width=((i+1)/slides.length*100)+'%';counter.textContent=(i+1)+' / '+slides.length;location.hash=i+1;}
function next(){show(i+1)} function prev(){show(i-1)}
window.addEventListener('resize',fit);
document.addEventListener('keydown',e=>{
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();next()}
  else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();prev()}
  else if(e.key==='Home'){show(0)} else if(e.key==='End'){show(slides.length-1)}
  else if(e.key==='f'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}});
stage.addEventListener('click',e=>{
  if(e.target.closest('button,a,pre')) return;
  if(window.getSelection && String(window.getSelection())) return;
  const r=stage.getBoundingClientRect();
  if(e.clientX < r.left + r.width/2) prev(); else next();
});
fit();show((parseInt((location.hash||'#1').slice(1))||1)-1);
"""

_slides_html = render_slides()
_count = _slides_html.count('class="slide')
HTML = f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI는 디자인을 더럽게 못합니다 | 하네스톤 #1 우승 회고</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>{CSS}</style></head><body>
<div id="bar"></div>
<div id="scaler"><div id="stage">
{_slides_html}
</div></div>
<div id="counter">1 / {_count}</div>
<div id="hint">← → 이동 · F 전체화면 · ⌘/Ctrl+P → PDF 저장</div>
<script>{JS}</script>
</body></html>"""

with open(OUT,"w",encoding="utf-8") as f:
    f.write(HTML)
print(f"OK  slides={_count}  ->  {OUT}")
