---
project_name: '3.ThucTheNgay'
user_name: 'Ongtu'
date: '2026-05-25'
sections_completed:
  - technology_stack
  - language_rules
  - framework_rules
  - testing_rules
  - quality_rules
  - autonomous_execution_rules
  - workflow_rules
  - anti_patterns
status: 'complete'
rule_count: 37
optimized_for_llm: true
---

# Project Context for AI Agents

_File này chứa các quy tắc bắt buộc AI agents phải đọc trước khi code, fix bug, hoặc thêm module trong dự án 3.ThucTheNgay._

---

## Technology Stack & Versions

- Python baseline: `>=3.11,<3.12`; môi trường chuẩn của dự án là conda env tên `ttn-env`.
- Conda channel chuẩn: `conda-forge`.
- Runtime chính: `PySide6>=6.7`, `pydantic>=2.7`, `rasterio>=1.3`, `shapely>=2.0`, `pyproj>=3.6`, `gdal>=3.7`, `numpy>=1.26`, `Pillow`, `python-pptx>=1.0`, `lxml>=6.1`.
- Dev tools: `pytest>=8.0`, `ruff>=0.4`, `uv`.
- App type: desktop Python/PySide6 Qt Widgets, không phải web app và không dùng PyQGIS.
- Source package: `src/thucthengay/`.
- Test root: `tests/`; default test command lấy từ `pyproject.toml`.

## Critical Implementation Rules

### Environment Rules

- Luôn ưu tiên chạy lệnh trong conda env `ttn-env`.
- Nếu shell chưa có `conda` trong PATH, dùng `/home/ongtu/miniconda3/bin/conda`.
- Với fallback conda, không chạy `uv sync` để tránh thay native GIS packages của conda-forge bằng PyPI wheels.
- Dùng mẫu:

```bash
/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync pytest
/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync ruff check .
/home/ongtu/miniconda3/bin/conda run -n ttn-env env UV_PROJECT_ENVIRONMENT=/home/ongtu/miniconda3/envs/ttn-env uv run --no-sync python -m thucthengay
```

### Research & Analysis Mandate

- Trước khi code, fix bug, hoặc thêm module mới: phải đọc artifact/story/architecture liên quan và khảo sát code hiện có.
- Không được sửa theo phỏng đoán khi chưa truy vết nguyên nhân hoặc chưa hiểu boundary của module bị chạm.
- Với bug: ghi rõ quan sát, giả thuyết, nguyên nhân đã xác nhận, và cách verify trong story/dev record hoặc implementation artifact nếu thay đổi không tầm thường.
- Với feature/module mới: xác định owner module, input/output contract, dependency được phép, và tests trước khi patch.
- Nếu phát hiện thông tin mâu thuẫn giữa PRD, architecture, story và code hiện tại: dừng lại ở kết luận thận trọng, ghi rõ nguồn mâu thuẫn, rồi chọn hướng ít phá vỡ nhất hoặc hỏi người dùng.

### Module Ownership Rules

- `models/`: Pydantic schemas/enums shared across config, workspace, validation, render, export.
- `config/`: load/validate config files, resolve config-relative paths; không sở hữu workspace state.
- `workspace/`: nguồn sự thật duy nhất cho manifest/composition JSON; atomic writes thuộc module này.
- `ingestion/`: scan GeoTIFF, parse metadata, match target GeoJSON, build cache/compositions.
- `gis/`: CRS, geometry, raster window, grid/DMS math; không import UI.
- `render/`: preview/final render; không phụ thuộc Qt widgets.
- `validation/`: trả về `Issue`; không mutate workspace trực tiếp.
- `export/`: PPTX/TXT/log generation; không phụ thuộc UI.
- `jobs/`: progress/cancellation wrappers for long-running work.
- `editor/`: PySide6 widgets/models/delegates only; UI không đọc/ghi JSON trực tiếp.
- `utils/`: helper nhỏ, không được biến thành nơi chứa business logic.

### Isolation & Coupling Rules

- Khi code/fix/thêm module, chỉ chạm file đúng ownership; tránh refactor lan rộng nếu không cần cho acceptance criteria.
- Module mới phải có contract rõ: model/result type, public function/class, và tests.
- Core modules không được import `PySide6` hoặc `thucthengay.editor`.
- UI có thể import services/models; services/models không import UI.
- Không tạo vòng phụ thuộc giữa các domain modules.
- Không duplicate model/dataclass nếu đã có Pydantic model trong `models/`.
- Không đưa business logic vào `app.py` hoặc package `editor/`.

### Data & State Rules

- JSON persisted fields dùng `snake_case`.
- Workspace-relative paths được ưu tiên trong workspace JSON.
- Config paths resolve relative to config file, nhưng path existence check không nằm trong model contract nếu story chỉ yêu cầu schema.
- Composition id format: `target_id__YYYYMMDD`.
- `scale` là mẫu số tỷ lệ bản đồ: `50000` nghĩa là `1:50,000`.
- View state source-of-truth là `view.center` `[lon, lat]` và `view.scale`; không quay lại bbox extent trừ khi story yêu cầu migration rõ ràng.
- Composition mới mặc định: `reviewed=false`, `ready=false`, `include=false`; state đổi sau edit phải dẫn tới `needs_revalidation`.
- User-facing validation/workflow issue phải dùng shared `Issue` model với message/remediation tiếng Việt.

### Testing Rules

- Mọi thay đổi core logic phải có unit tests focused trong `tests/unit/`.
- Tests không được yêu cầu network, real GeoTIFF, real PPTX, LAN paths, hoặc Qt GUI event loop trừ khi story nói rõ.
- Sau mỗi story/fix: chạy `pytest`, `ruff check .`, và `python -m thucthengay` bằng env `ttn-env`.
- Import-boundary tests phải luôn pass; không bypass bằng dynamic imports.
- Khi thêm schema/model: test cả valid round-trip và invalid field locations từ Pydantic `ValidationError.errors()`.

### Code Quality & Style Rules

- Dùng `ruff` rules hiện tại: `E`, `F`, `I`, `UP`, `B`; line length `100`; target `py311`.
- Package/module/file/function/variable dùng `snake_case`; class dùng `PascalCase`; constant dùng `UPPER_SNAKE_CASE`.
- Pydantic v2: dùng `BaseModel`, `Field`, validators; ưu tiên `ConfigDict(extra="forbid")` cho persisted schemas.
- Comments chỉ dùng khi giải thích logic không hiển nhiên; không thêm comment mô tả lại dòng code.
- Code phải nhỏ và phân tách rõ module/function/file; một function chỉ nên có một trách nhiệm chính.
- Không thêm abstraction nếu chưa giảm được complexity thật hoặc chưa khớp pattern đã có.

### Autonomous Epic Execution Mandate

- Khi người dùng giao nhiệm vụ tiếp tục xây dựng dự án theo BMad story plan, Codex phải tự động thực hiện trọn vòng `code -> check -> fix -> review -> update artifacts` cho từng story theo thứ tự trong sprint status.
- Codex không dừng ở bước review hoặc chờ chỉ đạo giữa các story nếu còn story thuộc cùng epic có thể triển khai an toàn; chỉ dừng khi epic hiện tại hoàn thành, gặp blocker cần quyết định của người dùng, hoặc có rủi ro phá dữ liệu/thiết kế vượt ngoài story.
- Sau khi hoàn thành một story và cập nhật trạng thái/story artifact, Codex phải compact cuộc trò chuyện bằng cơ chế compact của môi trường hiện hành (ví dụ `/compact` trong Codex CLI) trước khi bắt đầu story tiếp theo.

### BMad Workflow Rules

- Làm theo sprint status trong `_bmad-output/implementation-artifacts/sprint-status.yaml`.
- Story lifecycle: `backlog -> ready-for-dev -> in-progress -> review -> done`.
- Chỉ mark `done` sau khi code review findings được xử lý và quality gates pass.
- Khi cập nhật story file, chỉ sửa các vùng được workflow cho phép: task checkboxes, Dev Agent Record, File List, Change Log, Status.
- Planning artifacts trong `_bmad-output/planning-artifacts/` là nguồn context chính; không tự ý rewrite chúng khi đang dev story.

### Critical Don't-Miss Rules

- Không implement Story 1.3+ trong Story 1.2; giữ scope đúng story.
- Không kiểm tra file existence trong Pydantic schema nếu requirement thuộc config loader/service.
- Không để UI hoặc job layer trở thành source of truth cho workspace state.
- Không silent-drop GIS dependencies vì GDAL/rasterio packaging khó; ghi rõ fallback hoặc failure.
- Không tạo workflow tự động include/export mà bỏ qua validation/review state.
- Không dùng màu làm tín hiệu trạng thái duy nhất trong UI; status cần icon/text/tooltip khi tới UI stories.
- Không thay đổi workspace/cache/compositions/renders/exports mà thiếu explicit confirmation trong các story có destructive behavior.
- Nếu đang sửa bug, luôn verify bằng test hoặc command tái hiện được; nếu chưa verify được, ghi rõ giới hạn.

---

## Usage Guidelines

**For AI Agents:**

- Đọc file này trước khi implement hoặc review code.
- Tuân thủ tất cả mandate ở trên; khi nghi ngờ, chọn hướng hẹp hơn và ít ảnh hưởng hơn.
- Nếu rule mới phát sinh từ review/bug, cập nhật file này hoặc đề xuất cập nhật.

**For Humans:**

- Giữ file này ngắn, ưu tiên rule mà AI dễ quên.
- Cập nhật khi stack, workflow, hoặc module ownership thay đổi.
- Xóa rule đã lỗi thời để tránh làm nhiễu context.

Last Updated: 2026-05-25
