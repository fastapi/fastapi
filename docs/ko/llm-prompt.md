### Target language

Translate to Korean (한국어).

Language code: ko.

### Grammar and tone

- Use polite, instructional Korean (e.g. 합니다/하세요 style).
- Keep the tone consistent with the existing Korean FastAPI docs.
- Do not translate “You” literally as “당신”. Use “여러분” where appropriate, or omit the subject if it sounds more natural in Korean.

### Headings

- Follow existing Korean heading style (short, action-oriented headings like “확인하기”).
- Do not add trailing punctuation to headings.

### Quotes

- Keep quote style consistent with the existing Korean docs.
- Never change quotes inside inline code, code blocks, URLs, or file paths.

### Ellipsis

- Keep ellipsis style consistent with existing Korean docs (often `...`).
- Never change `...` in code, URLs, or CLI examples.

### Preferred translations / glossary

Use the following preferred translations when they apply in documentation prose:

- request (HTTP): 요청
- response (HTTP): 응답
- path operation: 경로 처리
- path operation function: 경로 처리 함수
- app: 애플리케이션
- command: 명령어
- burger: 햄버거 (NOT 버거)

### `///` admonitions

1) Keep the admonition keyword in English (do not translate `note`, `tip`, etc.).
2) If a title is present, prefer these canonical titles:

- `/// note | 참고`
- `/// tip | 팁`
- `/// warning | 경고`
- `/// info | 정보`
- `/// danger | 위험`
- `/// note Technical Details | 기술 세부사항`
- `/// check | 확인`
Notes:

- `details` blocks exist in Korean docs; keep `/// details` as-is and translate only the title after `|`.
- Example canonical title used: `/// details | 상세 설명`
