# Visual Physics Reference — Shadow, Contrast, Color

Claude MUST understand these principles and apply them when building prompts.
This is NOT decoration — these are physical laws that determine what a camera captures.

---

## 1. Shadow Formation (그림자 원리)

### 1.1 Shadow Types
```
Form Shadow (명암 그림자)
  - 물체 자체에 생기는 그림자
  - 빛이 닿지 않는 면에 자연스러운 그라데이션으로 형성
  - 구의 경우: 밝은면 → 중간톤 → 코어 섀도(가장 어두운 선) → 반사광

Cast Shadow (투영 그림자)
  - 물체가 다른 표면에 드리우는 그림자
  - 물체와 접하는 부분(contact shadow)이 가장 어둡고 선명
  - 멀어질수록 흐려지고 밝아짐 (penumbra 확대)

Contact Shadow (접촉 그림자)
  - 물체가 표면에 닿는 바로 그 지점
  - 가장 어둡고 가장 선명
  - 이것이 없으면 물체가 "떠 보인다"
```

### 1.2 Light Source × Shadow Shape
```
광원 유형          그림자 특성
─────────────────────────────────────────
점광원 (전구)      선명한 경계, 한 방향, 강한 명암
면광원 (창문)      부드러운 경계, 그라데이션 전환
확산광 (흐린 날)    거의 그림자 없음, 균일, 입체감 약함
형광등 (천장)      편평, 바로 아래만 약한 그림자, 입체감 적음
역광              가장자리만 밝음 (림라이트), 정면 어둡고 실루엣
복수 광원          여러 방향 그림자, 각 그림자 강도 다름
```

### 1.3 Critical Rule: 그림자는 절대 순수한 검정이 아니다
```
현실에서 그림자는:
  - 주변 반사광(bounce light)을 받아 완전히 검지 않음
  - 환경의 색을 흡수함 (초록 잔디 위 그림자 → 약간 초록 tint)
  - 광원의 보색(complementary color) 경향을 가짐:
    · 따뜻한 햇빛 그림자 → 차가운 파랑/보라
    · 차가운 형광등 그림자 → 약간 따뜻한 톤
    · 노란 텅스텐 그림자 → 파란/남색
```

### 1.4 Prompt에서 그림자 묘사법
```
❌ 나쁜 예: "with shadows" (의미 없음)
❌ 나쁜 예: "dark shadows" (방향/질감 정보 없음)

✅ 좋은 예 (형광등 아래 햄스터):
  "overhead fluorescent casting flat even illumination,
   minimal cast shadow directly beneath the hamster's body,
   contact shadow where belly meets paper bedding is darkest,
   form shadows between fur strands remain warm golden,
   no dramatic shadow direction due to diffused overhead source"

✅ 좋은 예 (창가 카페 음식):
  "window light from left casting soft diagonal shadows to the right,
   shadow under the cup is short and soft-edged,
   contact shadow where cup meets saucer is crisp and dark,
   the shadow area on the right side of the tiramisu shows
   reflected warm light bouncing from the marble table"
```

---

## 2. Contrast & Tonal Range (명암과 대비)

### 2.1 Tonal Structure
```
하이라이트 (Highlights)
  │  가장 밝은 부분. 반사광, 직접 빛 반사
  │  광택 표면: 작고 날카로운 스펙큘러 하이라이트
  │  매트 표면: 넓고 부드러운 하이라이트
  ▼
미드톤 (Midtones)
  │  물체의 실제 색(local color)이 가장 잘 보이는 영역
  │  대부분의 디테일과 텍스처 정보가 여기에 있음
  ▼
그림자 (Shadows)
  │  빛이 적게 닿는 부분
  │  반사광에 의해 완전히 검지 않음
  │  환경색의 영향을 가장 많이 받음
  ▼
코어 섀도 (Core Shadow)
    물체의 form shadow 중 가장 어두운 선/영역
    밝은 면과 그림자 면의 전환점
```

### 2.2 Contrast by Lighting Condition
```
조건               대비      특성
───────────────────────────────────────────────
한낮 직사광       매우 높음   눈부신 하이라이트, 깊은 그림자, 선명한 경계
골든 아워        중간~높음   따뜻한 톤, 긴 그림자, 드라마틱하지만 부드러움
흐린 날          낮음       균일한 톤, 그림자 거의 없음, 색 자체가 잘 보임
형광등 실내      낮음~중간   편평한 조명, 약한 그림자, 색이 약간 탁해짐
캔들/단일 전구   높음       한쪽만 밝음, 반대쪽 어둠, 극적
네온             중간       색 대비가 주요, 명암보다 색상 차이가 큼
```

### 2.3 Material × Contrast
```
재질              하이라이트            미드톤              그림자
──────────────────────────────────────────────────────────────
유리/금속         작고 날카로운 반사점    어둡거나 투명       깊고 선명
매트 천/종이      넓고 부드러운 밝은면    고른 색상          부드러운 전환
피부              부드러운 광택          피부색 변화         붉은 반투명(SSS)
털/모피           털끝에 림라이트        풍부한 색감         털 사이 깊은 어둠
액체 (커피)       표면 반사 하이라이트    투명/반투명 층      바닥에 그림자
빵 껍질           기름기 반사 점         질감 풍부           기공 안쪽 어둠
```

### 2.4 Prompt에서 대비 묘사법
```
❌ 나쁜 예: "high contrast" (무의미한 키워드)

✅ 좋은 예 (형광등 아래 햄스터):
  "low contrast flat lighting typical of fluorescent,
   fur midtones dominate with rich golden hue,
   subtle highlight along the top of the fur where light hits,
   shadows between strands are soft and warm not black,
   paper bedding shows minimal shadow variation"

✅ 좋은 예 (창가 카페 라떼):
  "medium contrast from directional window light,
   sharp specular highlight on glass surface of iced latte,
   ice cubes catching light as bright white points,
   the shadow side of the glass shows coffee color through transparency,
   tiramisu has soft tonal range with cocoa powder as darkest value"
```

---

## 3. Color Science (색채 원리)

### 3.1 Color Temperature of Light Sources
```
광원                색온도 (K)     색감
──────────────────────────────────────────────
촛불               1,800K         깊은 오렌지
백열등/텅스텐       2,700K         따뜻한 노랑
일출/일몰          3,000K         골든 오렌지
할로겐             3,200K         따뜻한 흰색
형광등 (cool)      4,000K         약간 녹색 끼 흰색
정오 햇빛          5,500K         중립 백색
흐린 하늘          6,500K         차가운 흰색
그늘               7,500K         파란 끼 있는 빛
푸른 하늘 (직접)   10,000K+       매우 차가운 파랑
```

### 3.2 Mixed Lighting = Color Conflict
```
현실에서는 단일 광원이 거의 없다:

카페 실내:
  창문 (5,500K 자연광) + 실내등 (3,000K 텅스텐)
  → 창쪽은 차갑고 실내쪽은 따뜻 → 피사체에 두 색이 섞임

케이지 속 햄스터:
  형광등 (4,000K) + 주변 벽 반사
  → 전체적으로 약간 녹색/청백색, 그림자는 약간 따뜻

야간 거리:
  네온 (다양한 색) + 가로등 (주황 2,700K) + 간판 (차가운 LED 6,500K)
  → 피사체에 여러 색 빛이 동시에 영향
```

### 3.3 Shadow Color Rule (핵심!)
```
그림자의 색 = 광원 보색 방향 + 환경 반사색

따뜻한 광원 (햇빛/텅스텐):
  → 그림자는 차가운 톤 (파랑, 보라, 청록)
  → 예: 석양의 그림자는 보라빛

차가운 광원 (형광등/흐린날):
  → 그림자는 약간 따뜻한 톤 (갈색, 따뜻한 회색)
  → 예: 형광등 아래 그림자는 회갈색

반사 환경색:
  → 초록 잔디 위 → 그림자에 녹색 반사
  → 붉은 벽 옆 → 그림자에 붉은 기운
  → 흰 종이 위 → 그림자가 비교적 중립
```

### 3.4 Material Color Behavior
```
같은 빨간 사과도 조명에 따라 색이 달라진다:

  햇빛 아래:    선명한 빨강, 하이라이트 흰색, 그림자 짙은 빨강+보라
  형광등 아래:  약간 탁한 빨강, 하이라이트에 녹색끼, 전체 채도 저하
  텅스텐 아래:  따뜻한 오렌지-빨강, 더 풍부해 보임, 그림자 짙은 갈색
  흐린날:       가장 정확한 실제 색, 하이라이트 약함, 채도 중립

금색 햄스터 털:
  형광등:   털 끝 차가운 흰색 하이라이트, 전체적으로 약간 차가워진 금색,
           깊은 부분은 따뜻한 갈색 유지, 채도 약간 낮음
  햇빛:    빛나는 따뜻한 금색, 하이라이트 노랑/흰색, 그림자 갈색+보라
  저녁:    오렌지빛 금색, 전체 따뜻, 그림자 깊은 앰버
```

### 3.5 Prompt에서 색채 묘사법
```
❌ 나쁜 예: "vibrant colors" (현실을 반영하지 않음)
❌ 나쁜 예: "golden fur" (어떤 조명에서의 금색인지 불명)

✅ 좋은 예 (형광등 아래 금색 햄스터):
  "golden fur appears slightly desaturated and cooler under fluorescent,
   fur tips catch cool-white highlights,
   deeper layers of fur retain warm amber-gold,
   overall color shifted slightly toward yellow-green
   compared to how it would look in warm sunlight"

✅ 좋은 예 (창가 카페 아이스 라떼):
  "coffee appears warm brown with amber highlights where window light passes through,
   milk swirls are creamy off-white not pure white,
   ice cubes reflect blue-white window light on top surfaces,
   shadow side of glass shows deeper coffee tone,
   marble table reflects subtle warm light back up onto the glass bottom"
```

---

## 4. Quick Reference Checklist

프롬프트 작성 시 반드시 확인:

```
□ 그림자 방향이 광원 위치와 일치하는가?
□ 그림자 경계가 광원 유형에 맞는가? (점=선명, 면=부드러움, 확산=없음)
□ 그림자 색이 순수한 검정이 아닌 환경+보색 반영인가?
□ 접촉 그림자(contact shadow)가 묘사되었는가?
□ 재질별 하이라이트가 정확한가? (유리=날카로운, 천=넓은, 털=림)
□ 광원 색온도가 피사체 색에 미치는 영향이 반영되었는가?
□ 혼합 광원이 있다면 색 충돌이 묘사되었는가?
□ 대비 수준이 조명 조건에 맞는가? (형광등=낮음, 직사광=높음)
```
