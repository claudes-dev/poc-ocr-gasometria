# Copilot / AI Agent Instructions

This repo is a small Python proof-of-concept for OCR extraction of arterial blood gas results.
Follow these concise, actionable rules to be immediately productive.

**Project Purpose**: extract numeric gasometria parameters from images and return a JSON result.

**Key files**
- [main.py](main.py): core pipeline — image preprocessing (`preprocessar_imagem`), OCR call, value extraction (`extrair_valores`), and validation (`validar_valores`).
- [testar_ocr.py](testar_ocr.py): simple CLI test runner for a single image.
- [testar_interativo.py](testar_interativo.py): interactive tester that guides users to run and save JSON output.

Quick facts
- Python version: 3.14 (see README). Dependencies: `opencv-python`, `pytesseract`, `numpy`.
- Tesseract must be installed separately (UB-Mannheim recommended). Paths are configured directly in `main.py` via `pytesseract.pytesseract.tesseract_cmd` and `os.environ['TESSDATA_PREFIX']`.
- OCR uses language `por` with fallback to `eng` in `processar_foto`.

What to look for / modify
- To change Tesseract installation path, edit the two lines near the top of `main.py` (tesseract_cmd and TESSDATA_PREFIX).
- To tune image processing, update `preprocessar_imagem` (resizing, denoising, CLAHE, adaptive thresholding and morphology).
- All extraction heuristics live in `extrair_valores` — regex patterns and a set of OCR-correction substitutions. When adding a parameter or improving accuracy, update patterns here and corresponding validation in `RANGES_GASOMETRIA`.
- Validation ranges are defined in `RANGES_GASOMETRIA` (top of `main.py`). Keep them in-sync with domain expectations when changing parameter names.

Conventions & patterns specific to this repo
- The main API returns a JSON string from `processar_foto(imagem_bytes, validar=True, debug=False)` — tests and scripts parse/display this JSON.
- The code aggressively normalizes common OCR misreads (e.g., `OB` -> 98, `AG` -> 4.4, `LA` -> 1.2). These mappings are encoded in `extrair_valores` and are intentional; change them only with supporting test images.
- Regex patterns prioritize robustness over strictness: expect many alternates and fallback groups. Add unit-test images when you add or change patterns.

Developer workflows (discoverable in repo)
- Run a single-file test: `python testar_ocr.py <image_path>` or `python testar_interativo.py` for interactive mode.
- Run quick end-to-end from `main.py`: `py main.py` (the script contains example usage and a default path to an image).

Testing guidance for agents
- When changing regex or substitution mappings, provide 1–3 sample images (or synthetic text snippets) demonstrating the before/after behavior and update README or add a small `tests/` helper for regression checks.
- Use the `debug=True` flag when calling `processar_foto` to include `texto_ocr` in output for diagnosis.

Error handling expectations
- If OCR fails to decode an image, `processar_foto` returns `{"sucesso": false, "erro": <msg>}` — follow this return shape for downstream code.

Do NOT assume
- No external API or database integrations exist — this is a local POC. Do not scaffold remote services unless the user asks.

Examples (copyable)
- Programmatic call:

```python
from main import processar_foto
with open('gasometria.png','rb') as f:
    out = processar_foto(f.read(), validar=True, debug=True)
    print(out)
```

- CLI test:

```bash
python testar_ocr.py gasometria.png
```

If anything here is unclear or you'd like deeper conventions (unit-test patterns, CI commands, or preferred branching/commit messages), tell me which area to expand. 
