---
stepsCompleted: [1]
inputDocuments: []
session_topic: 'App cá nhân tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh quang học'
session_goals: 'Làm rõ workflow, config mục tiêu, công nghệ hiển thị ảnh và điều chỉnh khung, xử lý ảnh giao cắt GeoJSON, metadata ảnh, UI duyệt/chọn/chỉnh, xuất PowerPoint và TXT'
selected_approach: 'Progressive Technique Flow'
techniques_used: []
ideas_generated: []
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** Ongtu
**Date:** 2026-05-23

## Session Overview

**Topic:** App cá nhân tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh quang học, dựa trên cấu hình mục tiêu bằng GeoJSON và metadata ảnh.

**Goals:** Làm rõ workflow từ config mục tiêu -> lấy ảnh giao cắt -> nhóm theo mục tiêu -> duyệt/chọn/chỉnh khung -> xuất PowerPoint + TXT; xác định cấu trúc config mục tiêu; đề xuất công nghệ, đặc biệt cho hiển thị ảnh và điều chỉnh khung; nhận diện rủi ro GIS/ảnh/template.

### Session Setup

Người dùng chọn cách brainstorm `[4] Progressive Technique Flow`: bắt đầu rộng để mở các hướng giải pháp, sau đó thu hẹp thành mô hình sản phẩm, yêu cầu, và quyết định kỹ thuật.


## Technique Execution Results

**Phase 1 - First Principles Thinking:**

- Người dùng chọn hướng hiển thị/chỉnh khung `[D]`: kết hợp GIS mini để chỉnh chính xác với slide preview để kiểm tra kết quả xuất.
- Hàm ý kỹ thuật: app cần một workspace có trạng thái theo từng mục tiêu, không chỉ là script batch. Viewer phải xử lý tọa độ/CRS/extent/grid; preview phải mô phỏng khung slide/template.

- Quyết định tiếp theo: MVP ưu tiên Desktop App, không đi theo webapp local ở giai đoạn đầu.
- Lý do chính: truy cập file local/LAN, xử lý GeoTIFF lớn, cache phiên làm việc, và xuất PowerPoint/TXT đều tự nhiên hơn trong Python desktop.

- Người dùng chọn ưu tiên MVP `[B]`: GIS/editor mạnh hơn. MVP cần pan/zoom tốt, nhiều ảnh cùng mục tiêu, overlay chính xác, và grid tọa độ đẹp hơn mức tối thiểu.

- Với nhiều ảnh cho một mục tiêu, người dùng chọn `[C]`: chồng nhiều ảnh/layer, cho phép bật tắt và chọn vùng phù hợp. MVP không mặc định mosaic tự động và không ép mỗi ảnh thành một slide riêng.

- Metadata thời gian: người dùng chọn hiển thị dạng khoảng thời gian. Mỗi mục tiêu có chung ngày chụp; nếu nhiều ảnh/layer trong một mục tiêu thì hiển thị khoảng giờ-phút theo format ví dụ `09.30-10.25/13.05.26`.
- Cấu trúc trích xuất từ tên ảnh: ví dụ `PSScene_20260211_033928_97_252b_cloud_50.0.tif`; trường `20260211` là ngày dạng `YYYYMMDD`, trường `033928` là giờ dạng `hhMMss`. Có thể parse bằng pattern tương đương `^PSScene_(\d{8})_(\d{6})_.*_cloud_([0-9.]+)\.tif$`.
- Quy tắc tạo thời gian mục tiêu: lấy timestamp từ các image layer được chọn/bật cho target; nếu có một timestamp thì hiển thị một thời điểm, nếu nhiều timestamp cùng ngày thì hiển thị khoảng `HH.MM-HH.MM/DD.MM.YY` từ min đến max; cloud percent có thể lưu metadata phụ để hỗ trợ chọn ảnh.

- Nếu các layer của cùng một mục tiêu khác ngày chụp: app phải hiển thị thông báo/cảnh báo và tự tách thành nhiều slide theo từng ngày. Mỗi slide là một nhóm ảnh cùng target + cùng ngày; thời gian hiển thị của slide lấy từ min/max timestamp trong nhóm ngày đó.

- Khi một target tách thành nhiều slide theo ngày, người dùng chọn `[B]`: mỗi ngày có thể chỉnh khung riêng. Đơn vị chỉnh sửa/xuất slide nên là `target-day composition` thay vì chỉ `target`.

- Thuật ngữ: dùng `composition` trong code/model; trong UI có thể hiển thị là `Phiên ảnh` hoặc `Slide mục tiêu`. Người dùng đồng ý với đề xuất này.
- Config mục tiêu lưu dạng JSON. Trường bắt buộc ban đầu: `id`, `name`, `alias`, `title`, `geojson_file`, `scale`, `grid`.

- Cấu trúc config chọn `[B]`: dùng object chi tiết, ví dụ `default_view: { scale, center, buffer_percent }` và `grid: { interval, label_format }`, không đặt `scale/grid` dạng phẳng ở root.

- Trạng thái chỉnh sửa chọn `[C]`: mỗi target-date/composition có một file JSON riêng trong workspace, thay vì một session.json lớn hoặc SQLite. Điều này giúp mỗi slide mục tiêu là một artifact độc lập, dễ inspect và dễ phục hồi.

- Khi bấm `Lấy dữ liệu`, người dùng chọn `[A]`: xóa sạch toàn bộ workspace/cache/compositions/renders của phiên trước rồi tạo lại từ dữ liệu mới. Cần có xác nhận trước khi xóa để tránh mất chỉnh sửa cũ ngoài ý muốn.

- Nếu một ảnh intersect nhiều target, người dùng chọn `[A]`: copy cùng ảnh vào từng folder target liên quan. Ưu tiên workspace độc lập, dễ quản lý từng target/composition, chấp nhận tốn dung lượng hơn.

- Thứ tự layer mặc định trong composition: người dùng chọn `[A]` ảnh mới nhất nằm trên cùng. UI phải cho người dùng thay đổi thứ tự layer trực tiếp; thứ tự này lưu vào `order` trong composition JSON.

- Chỉnh khung bản đồ trong editor: người dùng chọn `[A]` kéo/pan bản đồ bên dưới, khung slide/map frame đứng yên ở giữa. Zoom/scale thay đổi kích thước hiển thị bản đồ dưới khung; frame cố định đại diện vùng sẽ export.

- Scale UX: người dùng chỉnh bằng scroll con trỏ chuột hoặc slider `phóng to/thu nhỏ`; app tự quy đổi nội bộ. Config vẫn có scale mặc định để khởi tạo, UI không buộc người dùng nhập tỷ lệ bản đồ thủ công trong lúc chỉnh.

- Rotation: người dùng chọn `[C]` chưa cần hỗ trợ xoay trong MVP, nhưng data model để sẵn `rotation`. Mặc định `rotation = 0`, UI chưa expose điều khiển xoay, render/export bản đầu luôn north-up.

- Công nghệ viewer/editor MVP: người dùng chọn `[A]` PySide6 + QGraphicsView tự render. Không dùng PyQGIS ở MVP. Ưu tiên nhẹ hơn, tự kiểm soát UI, chấp nhận tự triển khai các hành vi GIS cần thiết.


**Phase 2 - Pattern Recognition / Mind Mapping:**

- Người dùng chọn `[G]`: đi tuần tự qua các cụm Target Config, Data Ingestion, Workspace/Composition Model, GIS Editor, Export, Validation & Warnings.

- Target Config: người dùng chọn `[B]` không dùng `default_settings` cấp file; mỗi target khai báo đầy đủ tất cả trường cần thiết. Ưu tiên rõ ràng, dễ kiểm tra thủ công, không có merge rule ẩn.

- Target Config bổ sung: người dùng chọn `[A]` thêm cả `enabled` và `sort_order` cho mỗi target.

- Data Ingestion: nếu ảnh không parse được tên theo pattern `PSScene_YYYYMMDD_hhMMss_..._cloud_X.tif`, người dùng chọn `[C]` cho phép sửa metadata thủ công trong UI. Ảnh vẫn có thể được đưa vào nếu intersect, nhưng phải đánh dấu cần sửa metadata và composition chưa ready cho export đến khi metadata hợp lệ.

- Data Ingestion/Metadata Edit: nếu người dùng sửa metadata ngày chụp khác với folder cache hiện tại, chọn `[C]` hỏi người dùng trước khi move file sang `cache/target_id/YYYYMMDD/` tương ứng.

- Cloud filter: người dùng chọn `[D]` không dùng cloud filter ở MVP. `cloud_percent` vẫn được parse/lưu/hiển thị như metadata, nhưng ingestion không bỏ qua hoặc tự ẩn ảnh theo cloud.

- Intersect criterion: người dùng chọn `[A]` chỉ cần ảnh GeoTIFF giao với target GeoJSON là lấy. MVP ưu tiên không bỏ sót ảnh; người dùng lọc/chọn bằng layer visible trong editor.

- Progress Data Ingestion: người dùng muốn progress chi tiết gồm số ảnh đã scan, số ảnh matched, số target có ảnh, warning count, đang scan mục tiêu nào, và bao nhiêu ảnh đã match cho mục tiêu đó.

- Workspace/Composition initial status: người dùng chọn `[B]` `reviewed=false`, `ready=false`, `include=false`. Composition mới mặc định không xuất; người dùng phải duyệt/chỉnh và bật include sau khi kiểm tra.

- Composition review workflow bằng phím/nút điều hướng: sau khi chỉnh layer/khung/grid/metadata, người dùng bấm mũi tên phải hoặc nút trên màn hình để đánh dấu đã duyệt, hợp lệ cho xuất báo cáo, và chuyển sang composition tiếp theo. Bấm mũi tên lên hoặc nút tương ứng để đánh dấu đã duyệt nhưng không hợp lệ/bỏ qua composition này. Bấm mũi tên trái để quay lại composition trước và đánh dấu lại composition đó là chưa duyệt/chưa hợp lệ để chỉnh lại.

- Composition status model: người dùng chọn `[C]` dùng `reviewed`, `ready`, `include`; không thêm `valid`. `ready` là trạng thái đủ điều kiện kỹ thuật; `include` thể hiện quyết định đưa vào báo cáo hay bỏ qua sau khi duyệt.

- Khi bấm mũi tên phải, app phải chạy validate kỹ thuật trước. Người dùng chọn `[A]`: nếu validate lỗi thì không cho chuyển tiếp, không set ready/include, và phải thông báo đầy đủ lỗi kèm cách khắc phục.

- Mũi tên trái/quay lại: người dùng chọn `[C]` nếu composition trước đã `ready=true` thì app phải hỏi trước khi reset trạng thái. Nếu người dùng xác nhận chỉnh lại, reset `reviewed=false`, `ready=false`, `include=false`; nếu không xác nhận thì chỉ quay lại xem hoặc không thay đổi trạng thái.

- GIS Editor layout: người dùng muốn chia 2 vùng có thể resize, mặc định vùng trái chiếm 1/4 màn hình. Vùng trái chia 3 phần cũng có thể resize: trên là target/composition list, giữa là layers, dưới là preview. Vùng phải là GIS editor chính.

- Slide preview trong panel trái: người dùng chọn `[A]` cập nhật realtime khi pan/zoom/layer/grid thay đổi. Cần thiết kế cache/downsample/render pipeline để realtime không làm lag với GeoTIFF lớn.

- Grid editor: mặc định lấy `grid.interval` từ config của từng target; trong editor người dùng có thể nhập custom interval cho composition hiện tại. Custom grid lưu vào composition JSON như override, không sửa config gốc.

- Custom grid interval: người dùng muốn nhập dạng độ/phút/giây. App cần parser DMS và quy đổi sang decimal degree nội bộ để render grid.

- Grid label format: người dùng chọn `[A]` DMS đầy đủ, ví dụ `16°03'00"N`.

- Correction D5: Grid label format không cố định `[A]`; người dùng sửa thành `[D]` cho config chọn, mặc định DMS đầy đủ (`dms_full`).
- Boundary GeoJSON: chỉ dùng để scan/check intersect ảnh trong Data Ingestion; sau đó không dùng trong editor/export, không cần hiển thị boundary layer trong GIS editor và không đưa lên slide.

- GIS Editor overlays: không thêm overlay khác ngoài ảnh và grid/frame ở MVP; không north arrow, không scale bar.
- Map frame background: cần cấu hình màu nền khung bản đồ theo mã RGB để dùng khi ảnh không phủ hết khung; không để mặc định nền trắng. Trường này nên nằm trong config target và/hoặc composition override.

- Map frame background RGB: người dùng chọn `[B]` chỉ lấy từ config, không cho chỉnh trong editor MVP.

- Export slide order: người dùng chọn `[C]` theo thứ tự người dùng duyệt trong editor. Khi bấm mũi tên phải hợp lệ, app nên gán/lưu `review_order` hoặc export sequence cho composition.

- TXT export format: người dùng chọn `[D]` do config/template quyết định. Nên có trường `txt_line_template` trong target export hoặc global export config; mỗi dòng TXT tương ứng một composition/slide đã include.

- PowerPoint template handling: app không cần bước `Analyze template` để đọc shape name/tọa độ trực tiếp từ PPTX. Bước phân tích template sẽ do một script riêng thực hiện trước, trích xuất thông tin template/placeholder cần thiết và cung cấp cho app. App chỉ dùng template metadata đã trích xuất để export.

- Correction E1 - Template metadata location: mỗi target có template slide riêng. Đường dẫn template metadata được khai báo trong config của từng target, ví dụ `target.export.template_metadata_file`. App chính đọc template metadata theo target/composition đang export, không dùng một template metadata chung cấp project cho tất cả mục tiêu.

- PowerPoint export generation: người dùng chọn `[A]` copy slide mẫu một lần cho mỗi composition rồi thay ảnh/text theo template metadata. Cách này giữ style/bố cục của template tốt nhất cho MVP.

- Validation & Warnings UI: người dùng chọn `[D]` kết hợp icon cảnh báo/lỗi trực tiếp trên target/composition list và một panel tổng hợp `Warnings` trong app.

- Issue severity: người dùng chọn `[B]` gồm `info`, `warning`, `error`. `error` chặn ready/export; `warning` không chặn nhưng cần chú ý; `info` là thông tin/trạng thái.

- Export preflight: nếu còn composition `include=true` nhưng `ready=false`, người dùng chọn `[C]` app hỏi người dùng: chặn export toàn bộ hay bỏ qua composition lỗi và export phần còn lại.

- Export completion report: người dùng chọn `[D]` hiển thị summary sau export gồm số slide, số target, số skipped, warnings; đồng thời xuất thêm file log JSON/TXT cạnh PPTX.


## Resume State - End of Current Working Session

**Stop point:** Ended after completing Phase 2 Pattern Recognition / Mind Mapping. Next session should start with **Phase 3 - Idea Development / Solution Matrix** to turn the decisions into MVP architecture, data model, modules, and implementation roadmap.

### Product Concept

Personal desktop app that generates PowerPoint reports from optical satellite GeoTIFF imagery for fixed targets. Each slide presents one target occurrence, with image layers placed in a map frame with coordinate grid labels. The app also exports a TXT file with one line per exported slide.

### Core Terms

- `target`: fixed configured objective/area, defined in target config JSON.
- `composition`: code/model term for one target-date presentation unit; exactly one exported slide if included.
- UI label for composition: `Phiên ảnh` or `Slide mục tiêu`.
- `1 composition = 1 slide`.

### Chosen Technology Direction

- App type: Desktop app.
- UI: PySide6 / PyQt6.
- GIS editor/viewer MVP: `PySide6 + QGraphicsView` self-rendered; no PyQGIS for MVP.
- GIS/raster processing: `rasterio`, `GDAL`, `shapely`, `pyproj`, `numpy`, `Pillow`.
- PowerPoint export: `python-pptx`.
- Config/state: JSON.

### Target Config Decisions

- Config file is JSON.
- No file-level `default_settings`; every target declares all needed fields explicitly.
- Each target includes:
  - `id`
  - `enabled`
  - `sort_order`
  - `name`
  - `alias`
  - `title`
  - `geojson_file`
  - `default_view`
  - `grid`
  - `export`
  - `image_rules`
  - `metadata`
  - `map_frame.background_rgb`
- `scale/grid` use detailed objects, not flat root fields.
- Boundary GeoJSON is used only for ingestion/intersect; not displayed in editor and not exported.

Example target config shape:

```json
{
  "id": "target_001",
  "enabled": true,
  "sort_order": 1,
  "name": "ten_muc_tieu",
  "alias": "MT-001",
  "title": "Tên hiển thị trên slide",
  "geojson_file": "targets/target_001.geojson",
  "default_view": {
    "scale": 25000,
    "center": null,
    "buffer_percent": 15
  },
  "grid": {
    "enabled": true,
    "interval": {
      "degrees": 0,
      "minutes": 30,
      "seconds": 0
    },
    "label_format": "dms_full"
  },
  "export": {
    "slide_layout": "default_target",
    "template_metadata_file": "templates/target_001.template.json",
    "title_template": "{alias} - {title}",
    "time_template": "{time_range}/{date}",
    "txt_line_template": "{alias} | {title} | {time_label}"
  },
  "image_rules": {
    "same_day_split": true,
    "multi_layer_mode": "stack"
  },
  "map_frame": {
    "background_rgb": [32, 32, 32]
  },
  "metadata": {
    "category": null,
    "priority": null,
    "notes": null
  }
}
```

### Data Ingestion Decisions

- User selects config JSON, imagery input folder local/LAN, and workspace folder.
- On `Lấy dữ liệu`, app warns and then clears the old workspace completely.
- Scan imagery recursively for GeoTIFF.
- Filename pattern:
  - Example: `PSScene_20260211_033928_97_252b_cloud_50.0.tif`
  - `20260211` = `YYYYMMDD`
  - `033928` = `hhMMss`
  - cloud percent from `_cloud_50.0`
  - Suggested regex: `^PSScene_(\d{8})_(\d{6})_.*_cloud_([0-9.]+)\.tif$`
- If filename metadata cannot be parsed:
  - still check intersect;
  - if intersect, copy and mark metadata as needing manual edit;
  - composition is not ready until metadata is fixed.
- If manual metadata date differs from current cache folder, app asks before moving file.
- Cloud filter is not used in MVP; `cloud_percent` is parsed/stored/displayed only.
- Intersect criterion: any GeoTIFF/target GeoJSON intersection is enough.
- If one image intersects multiple targets, copy it into each target folder.
- Ingestion progress UI must show:
  - scanned image count;
  - matched image count;
  - targets with images;
  - warning count;
  - current target being scanned/processed;
  - matched image count for current target.

### Workspace / Composition Decisions

Workspace shape:

```text
workspace/
├── manifest.json
├── cache/
│   └── target_id/YYYYMMDD/*.tif
├── compositions/
│   └── target_id__YYYYMMDD.json
├── renders/
└── exports/
```

- Each target-date has one composition JSON file.
- If a target has images on multiple dates, app shows a warning and automatically creates one composition/slide per date.
- Each date/composition can have its own frame/view/grid adjustments.
- New composition initial status:

```json
"status": {
  "reviewed": false,
  "ready": false,
  "include": false,
  "notes": null
}
```

- Status meanings:
  - `reviewed`: user has reviewed the composition.
  - `ready`: technically valid for export.
  - `include`: include in PPTX/TXT export.
- No `valid` field.
- Review keyboard workflow:
  - Right arrow / screen button: validate technically; if pass set `reviewed=true`, `ready=true`, `include=true`, assign `review_order`, then move to next composition.
  - If right-arrow validation fails: do not move; show full errors and remediation steps.
  - Up arrow / screen button: mark reviewed but skipped: `reviewed=true`, `ready=false`, `include=false`, then move to next composition.
  - Left arrow: go back to previous composition. If previous composition is `ready=true`, ask before resetting. If user confirms edit, reset `reviewed=false`, `ready=false`, `include=false` and remove/reassign review order as appropriate.

### Layer / Time Decisions

- Multiple images for one composition are handled as stackable layers, not auto-mosaic.
- Default layer order: newest image on top.
- User can change layer order directly in UI; save to `layers[].order`.
- User can toggle layer visibility.
- If layers share same date, time label uses min/max time among included/visible selected layers.
- Time label format example: `09.30-10.25/13.05.26`.
- If only one timestamp, example: `03.39/11.02.26`.

### GIS Editor Decisions

Layout:

```text
QMainWindow
└── horizontal QSplitter
    ├── left panel, default 25%, resizable
    │   └── vertical QSplitter
    │       ├── target/composition list
    │       ├── layers panel
    │       └── slide preview
    └── right panel, default 75%
        └── GIS editor
```

- Slide preview updates realtime when pan/zoom/layers/grid/metadata change.
- Need cache/downsample/render strategy so realtime preview remains responsive with large GeoTIFFs.
- Map frame is fixed; user pans/zooms map/image underneath the frame.
- Zoom/scale UX:
  - mouse wheel under cursor;
  - zoom slider `phóng to/thu nhỏ`;
  - app converts internally.
- Config has scale default, but UI does not require manual map scale input.
- Internal view may store `meters_per_pixel` or equivalent.
- Rotation: keep `rotation` in data model, default `0`, but no rotation UI in MVP; render/export north-up.
- Grid:
  - default interval from target config;
  - user can enter custom grid interval per composition;
  - custom interval input is degree/minute/second fields;
  - app converts DMS interval to decimal degrees internally;
  - grid label format is config-selectable, default `dms_full`.
- No boundary overlay in editor/export.
- No north arrow, no scale bar in MVP.
- Map frame background color comes from target config RGB; not editable in editor MVP.

### Export Decisions

- PowerPoint template analysis is out of scope for the app. A separate script will extract template metadata/placeholders from PPTX and provide metadata to the app.
- Each target declares its own template metadata path in target config, e.g. `target.export.template_metadata_file`.
- App exports PPTX by copying the target-specific sample slide once per included composition, then replacing/inserting image/text according to that target's template metadata.
- Slide order is the order the user reviewed compositions in editor, saved as `review_order`.
- TXT format is config/template driven, using `txt_line_template`.
- Export includes compositions where `reviewed=true`, `ready=true`, `include=true`, sorted by `review_order`.
- If export preflight finds `include=true` but `ready=false`, app asks whether to stop export or skip invalid compositions and export the rest.
- After export, app shows summary and writes log JSON/TXT next to PPTX/TXT.

### Validation / Warnings Decisions

- Severity levels: `info`, `warning`, `error`.
- `error` blocks ready/export.
- `warning` does not block export.
- `info` is status/context.
- UI shows issues in both:
  - icons directly in target/composition tree;
  - aggregated Warnings panel.
- Technical validation on right-arrow should check things such as:
  - at least one visible layer;
  - layer files exist;
  - visible GeoTIFFs readable;
  - CRS/geotransform valid;
  - date/time metadata complete;
  - time label can be generated;
  - view center/zoom valid;
  - grid interval valid;
  - render output can be produced;
  - target-specific template metadata file exists and is readable;
  - template/title/time data available.

### Next Recommended Step

Start next session by reading this file and continuing with:

**Phase 3 - Idea Development / Solution Matrix**

Suggested work for Phase 3:

1. Convert decisions into MVP architecture modules.
2. Define data models for target config, composition JSON, layer metadata, template metadata, export log.
3. Define renderer pipeline for QGraphicsView preview vs final PNG export.
4. Define UI components/screens.
5. Define validation rules and issue schema.
6. Produce a concise product brief or PRD after architecture options are shaped.

## Phase 3 - Idea Development / Solution Matrix

### Architecture Direction

- Người dùng chọn `[A] Layered rõ ràng` cho MVP architecture.
- App sẽ tách module theo trách nhiệm rõ ràng thay vì trộn logic vào UI desktop.
- Lý do: dự án có nhiều phần có thể test/validate độc lập: config, ingestion, workspace state, GIS math, rendering, export, validation. Tách module sớm giúp PRD/architecture và story implementation rõ hơn, giảm rủi ro khi UI/editor phát triển phức tạp.

Initial module boundary:

```text
app/
  config/          # đọc/validate target config
  ingestion/       # scan GeoTIFF, parse metadata, intersect GeoJSON, build workspace
  workspace/       # manifest, cache, composition JSON
  gis/             # raster loading, CRS, transforms, grid math
  editor/          # PySide6 UI + QGraphicsView interaction
  render/          # preview render + final PNG render
  export/          # PPTX/TXT export theo target template metadata
  validation/      # issue schema + validation rules
```

### Workspace State Ownership

- Người dùng chọn `[A] workspace/ là source of truth`.
- `workspace/` module chịu trách nhiệm đọc/ghi `manifest.json`, composition JSON, cache references, render/export paths, và status fields.
- `editor/` không giữ source-of-truth riêng; UI state sống chỉ là bản đang hiển thị/chỉnh, mọi thay đổi quan trọng được lưu qua workspace service.
- `validation/` không sở hữu state transition; validation nhận composition/config/layer context và trả danh sách issue. `editor/` hoặc workflow action quyết định gọi validation trước khi cập nhật status qua workspace service.
- Lợi ích: composition JSON vẫn là artifact độc lập, dễ inspect/backup/phục hồi; export và validation có thể chạy không phụ thuộc UI.

### Composition Validation Persistence

- Người dùng chọn `[C] lưu summary thôi` cho validation trong composition JSON.
- Composition không lưu toàn bộ `issues` chi tiết để tránh stale khi file ảnh/config/template thay đổi ngoài app.
- Composition lưu `validation_summary`, ví dụ `last_validated_at`, `error_count`, `warning_count`, `info_count`, `ready_at_validation`.
- Khi mở composition, bấm mũi tên phải, hoặc export preflight, app chạy lại validation để lấy issue chi tiết hiện thời.
- UI có thể dùng summary để hiển thị trạng thái nhanh trong list, sau đó refresh chi tiết khi composition được chọn hoặc khi user mở Warnings panel.

### Layer Metadata Persistence

- Người dùng chọn `[B] lưu metadata nghiệp vụ, metadata kỹ thuật đọc lại`.
- Mỗi layer trong composition lưu các trường cần cho workflow/editor/export: `layer_id`, `source_path` hoặc `workspace_path`, `visible`, `order`, `capture_date`, `capture_time`, `timestamp_source`, `cloud_percent`, `metadata_status`, `metadata_notes`.
- Các metadata kỹ thuật như CRS, raster bounds, transform, dimensions, nodata, overviews không là source-of-truth trong composition; validation/render sẽ đọc lại từ GeoTIFF khi cần.
- Lý do: hỗ trợ sửa metadata thủ công và tạo time label ổn định, trong khi tránh stale kỹ thuật nếu file ảnh thay đổi.

### Composition View Source of Truth

- Người dùng chọn `[A] lưu theo geographic extent`.
- Composition view lưu vùng bản đồ export bằng extent địa lý, ví dụ `[min_lon, min_lat, max_lon, max_lat]`, làm source-of-truth cho preview/final render.
- UI vẫn có thể cho người dùng pan/zoom bằng chuột và slider; khi lưu, app quy đổi trạng thái viewport thành `view.extent`.
- `center`, `scale`, `meters_per_pixel`, hoặc zoom factor chỉ là derived values phục vụ UI/debug, không phải source-of-truth trong composition.
- Lý do: extent dễ inspect trong JSON, ít mơ hồ khi render final PNG/PPTX, và ổn định hơn khi kích thước preview khác kích thước export.

### Renderer Pipeline Direction

- Người dùng chọn `[C] Hybrid` cho renderer pipeline.
- Core render math dùng chung cho preview và final export: `view.extent`, layer order/visibility, target map frame ratio, grid interval/labels, background RGB.
- Preview pipeline dùng cache/downsample/overview để cập nhật nhanh trong editor và slide preview realtime.
- Final pipeline đọc raster ở chất lượng cao hơn theo output size chính thức của template metadata, tạo PNG đủ chất lượng để chèn vào PowerPoint.
- Mục tiêu: preview gần giống final về bố cục/toạ độ/grid, nhưng không đánh đổi hiệu năng UI với GeoTIFF lớn.

### Realtime Preview Strategy

- Người dùng chọn `[C] Two-stage render`.
- GIS editor chính dùng render hai giai đoạn:
  - interactive stage: khi người dùng đang pan/zoom/drag, dùng ảnh cache/downsample rất nhanh để phản hồi tức thì;
  - settle stage: khi thao tác dừng, render lại sắc nét hơn theo extent hiện tại.
- Slide preview bên trái có thể dùng debounced render để tránh render quá nhiều lần khi người dùng đang kéo/zoom liên tục.
- Render job cũ nên có khả năng bị cancel/ignore nếu composition/view/layer state đã thay đổi trước khi job hoàn tất.
- Mục tiêu UX: thao tác editor không lag, nhưng preview cuối vẫn đủ gần final export để người dùng tin vào kết quả.

### Target Template Metadata Shape References

- Người dùng chọn `[C] cả name + fallback id`.
- Template metadata của từng target tham chiếu placeholder/shape bằng `name` là chính, kèm `fallback_id` tùy chọn để hỗ trợ debug hoặc fallback khi cần.
- Người thiết kế/analyze template cần đảm bảo shape names ổn định cho các placeholder quan trọng như map frame, title, time label, alias, notes/text fields.
- Export validation phải kiểm tra shape name trước; nếu không tìm thấy thì có thể thử fallback id nhưng vẫn tạo warning/error rõ ràng tùy mức độ placeholder bắt buộc.
- Cách này giữ metadata dễ đọc thủ công, đồng thời giảm rủi ro khi template bị chỉnh nhẹ.

### Target Template File Strategy

- Người dùng chọn `[A] mỗi target có PPTX template riêng`.
- Mỗi target config có `export.template_metadata_file`; metadata file đó trỏ tới `template_pptx` riêng của target.
- Export dùng PPTX template của target tương ứng với composition đang xuất, copy sample slide từ template đó, rồi thay map image/text theo metadata.
- Cách này ưu tiên rõ ràng và an toàn cho MVP: mỗi mục tiêu có layout/style riêng, tránh sửa nhầm slide trong một PPTX chung nhiều target.
- Có thể mở rộng sau này để nhiều target trỏ cùng một `template_pptx`, nhưng MVP không cần tối ưu theo hướng đó.

### Multi-Template PowerPoint Export Strategy

- Người dùng chọn `[C] MVP giới hạn: tất cả target template dùng chung theme/master tương thích, app copy slide XML/media có kiểm soát vào một output PPTX`.
- Sản phẩm vẫn xuất một file PPTX báo cáo tổng hợp gồm tất cả composition được include, sắp theo `review_order`.
- Mỗi composition dùng template PPTX riêng của target, nhưng các target template phải được tạo từ cùng một base PPTX/theme/master tương thích để giảm rủi ro khi copy slide giữa file.
- Export module cần validate compatibility ở mức tối thiểu: template file tồn tại, slide_index hợp lệ, required placeholders tồn tại, media/relationship có thể copy.
- Nếu sau này copy slide giữa nhiều PPTX bằng `python-pptx` không ổn định, có thể bổ sung helper XML-level hoặc bước prebuild base report template, nhưng MVP vẫn giữ mục tiêu một PPTX output.

### UI Workflow Structure

- Người dùng chọn `[C] ba mode rõ ràng: Setup, Review/Edit, Export`.
- App vẫn là một desktop main window, nhưng workflow được chia thành 3 mode/tab chính:
  - `Setup`: chọn config JSON, imagery input folder, workspace folder, chạy `Lấy dữ liệu`, xem progress/warnings ingest.
  - `Review/Edit`: duyệt composition, chỉnh layer/view/grid, realtime preview, dùng phím/nút điều hướng để set reviewed/ready/include.
  - `Export`: preflight, chọn output path, xuất PPTX/TXT, xem summary và log.
- Lý do: workflow tự nhiên đi từ lấy dữ liệu -> duyệt/chỉnh -> xuất báo cáo; tách mode giúp giảm nhầm lẫn và dễ validate trạng thái trước khi chuyển bước.

### Review/Edit Navigation Model

- Người dùng chọn `[C] Tree + queue filter`.
- Panel trái trong Review/Edit dùng tree theo `target -> composition`, vì một target có thể tách nhiều composition theo ngày.
- Tree hiển thị status/icon issue ở cả target và composition; target có thể aggregate số composition chưa duyệt, ready/include, warning/error.
- Bổ sung filter/queue như `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, `Có error`, giúp duyệt nhanh khi số lượng target/composition lớn.
- Review order vẫn được gán theo thứ tự người dùng bấm mũi tên phải hợp lệ, không nhất thiết trùng thứ tự tree.

### Validation Issue Language and Schema

- Người dùng chọn `[B] code tiếng Anh + message tiếng Việt`.
- `issue_id` dùng tiếng Anh dạng stable machine-readable, ví dụ `layer.file_missing`, `template.placeholder_missing`, `metadata.capture_time_missing`.
- `message` và `remediation` hiển thị tiếng Việt trong UI/log để phù hợp người dùng chính.
- Issue schema dự kiến gồm: `issue_id`, `severity`, `scope`, `target_id`, `composition_id`, `layer_id` optional, `message`, `remediation`, `blocking`.
- Severity vẫn gồm `info`, `warning`, `error`; `error` chặn ready/export, `warning` không chặn, `info` cung cấp ngữ cảnh/trạng thái.

### Validation Timing

- Người dùng chọn `[B] khi mở/chọn composition + khi duyệt/export`.
- Khi user chọn composition trong Review/Edit, app chạy validation để cập nhật issue panel/list status. Có thể tối ưu bằng lightweight checks và cache summary.
- Khi user bấm mũi tên phải để mark ready/include, app chạy full technical validation; nếu có error thì không set `reviewed/ready/include` và không chuyển tiếp.
- Khi export, app chạy preflight validation lại trên tất cả composition `include=true` để tránh xuất dữ liệu stale.
- Không chạy full realtime validation sau mọi thay đổi để tránh lag với GeoTIFF/template checks; UI chỉ đánh dấu trạng thái cần revalidate khi có thay đổi quan trọng.

### MVP Implementation Roadmap Direction

- Người dùng chọn `[B] Vertical slice sớm`.
- Roadmap MVP ưu tiên chứng minh một luồng end-to-end thật càng sớm càng tốt: config nhỏ -> ingest ảnh -> tạo composition -> editor chỉnh extent/layer/grid cơ bản -> render PNG -> export PPTX/TXT.
- Sau vertical slice đầu tiên, mở rộng theo module: validation đầy đủ hơn, metadata edit, multi-target/multi-date, preview realtime tối ưu, template compatibility, export logs.
- Lý do: dự án có nhiều tích hợp rủi ro giữa GIS/raster/render/PPTX/template; vertical slice giúp phát hiện sớm vấn đề thực tế thay vì hoàn thiện từng module cô lập quá lâu.

Suggested implementation sequence:

1. Define JSON schemas and sample fixtures for 1-2 targets.
2. Implement config/workspace/composition read-write services.
3. Implement ingestion minimal: scan GeoTIFF, parse filename metadata, intersect target GeoJSON, copy to workspace, create composition JSON.
4. Implement render final PNG for one composition from `view.extent`, visible layers, grid, background RGB.
5. Implement target-specific template metadata loading and one-slide PPTX export.
6. Build PySide6 Review/Edit shell around real composition data.
7. Add Setup mode progress UI and Export mode preflight/summary.
8. Harden validation, warnings panel, metadata edit, two-stage preview cache.
