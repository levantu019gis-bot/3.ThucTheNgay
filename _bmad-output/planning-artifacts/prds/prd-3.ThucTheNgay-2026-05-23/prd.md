---
title: "PRD: App tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh"
status: draft
created: 2026-05-23
updated: 2026-05-23
---

# PRD: App tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh

## 0. Document Purpose

PRD này định nghĩa yêu cầu sản phẩm cho MVP desktop app tạo báo cáo PowerPoint/TXT từ ảnh vệ tinh quang học GeoTIFF theo danh sách mục tiêu cố định. Tài liệu dùng cho các bước UX design, architecture, epics/stories và implementation. Technical-how chi tiết được chuyển sang `addendum.md`; PRD này tập trung vào hành vi sản phẩm, workflow, functional requirements, success metrics, non-goals và open questions. Data model, rendering, template/export và epic-direction details nằm trong PRD Addendum các mục tương ứng.

## 1. Vision

Sản phẩm giúp người dùng biến một tập ảnh vệ tinh GeoTIFF rời rạc thành báo cáo PowerPoint/TXT có cấu trúc, đúng template và có kiểm soát trực quan. Thay vì tự tìm ảnh, căn slide, nhập thời gian và kiểm tra từng lỗi bằng tay, người dùng làm việc trong một desktop workflow thống nhất: lấy dữ liệu, duyệt/chỉnh từng phiên ảnh, rồi xuất báo cáo.

Điểm quan trọng là app không chỉ batch export. Mỗi composition cần được người dùng kiểm tra bằng mắt: ảnh nào bật, layer nào nằm trên, khung bản đồ nào được đưa vào slide, grid tọa độ có hợp lý không, metadata thời gian có đủ không, và template target có sẵn sàng không. MVP vì vậy ưu tiên editor GIS mini và validation rõ ràng hơn là automation hoàn toàn.

Sản phẩm thành công khi người dùng tạo được một báo cáo PPTX/TXT đáng tin cậy từ dữ liệu thật, giảm thao tác lặp, giảm lỗi căn khung/metadata/template, và vẫn giữ quyền quyết định slide nào được đưa vào báo cáo.

## 2. Target User

### 2.1 Primary Persona

**Operator báo cáo ảnh vệ tinh** là một cá nhân hoặc nhóm nhỏ thường xuyên lập báo cáo mục tiêu từ ảnh vệ tinh quang học. Họ quen với file ảnh, thư mục local/LAN, PowerPoint template và khái niệm tọa độ/grid, nhưng không muốn mỗi lần báo cáo phải thao tác thủ công qua nhiều công cụ GIS/PowerPoint riêng lẻ.

### 2.2 Jobs To Be Done

- Khi có bộ ảnh GeoTIFF mới, người dùng muốn nhanh chóng biết ảnh nào liên quan tới mục tiêu nào.
- Khi một mục tiêu có nhiều ảnh/layer, người dùng muốn bật/tắt, sắp xếp và chọn vùng hiển thị phù hợp cho slide.
- Khi metadata ảnh thiếu hoặc sai, người dùng muốn app chỉ rõ vấn đề và cho sửa trước khi export.
- Khi báo cáo sẵn sàng, người dùng muốn xuất một PPTX tổng hợp và một TXT đi kèm theo đúng thứ tự duyệt.
- Khi có lỗi kỹ thuật, người dùng muốn biết lỗi gì, ở target/composition/layer nào, và cách khắc phục.

### 2.3 Non-Users (v1)

- Người dùng cần một GIS đầy đủ với phân tích không gian nâng cao.
- Người dùng cần web app nhiều người dùng, phân quyền, đồng bộ cloud hoặc workflow phê duyệt.
- Người dùng cần tự động mosaic/orthorectify/ xử lý ảnh chuyên sâu trong MVP.

### 2.4 Key User Journeys

- **UJ-1. Operator báo cáo ảnh vệ tinh lấy dữ liệu từ một bộ ảnh mới.**  
  Operator báo cáo ảnh vệ tinh mở app ở mode Setup, chọn config JSON, thư mục ảnh GeoTIFF và workspace. Họ bấm `Lấy dữ liệu`, xác nhận xóa workspace cũ, theo dõi progress scan/matched/warnings. Khi hoàn tất, app tạo cache và composition theo từng target-date, rồi Operator chuyển sang Review/Edit.

- **UJ-2. Operator báo cáo ảnh vệ tinh duyệt và chỉnh một composition.**  
  Operator báo cáo ảnh vệ tinh chọn một composition trong tree `target -> composition`. App load layer, hiển thị GIS editor và slide preview. Operator pan/zoom ảnh dưới map frame cố định, bật/tắt layer, đổi thứ tự layer, chỉnh grid interval nếu cần, xem warnings. Khi hợp lệ, họ bấm mũi tên phải để validate, set ready/include và chuyển sang composition tiếp theo.

- **UJ-3. Operator báo cáo ảnh vệ tinh xử lý metadata ảnh không parse được.**  
  Trong Review/Edit, Operator báo cáo ảnh vệ tinh thấy một composition hoặc layer có cảnh báo metadata. Operator mở layer metadata editor, nhập ngày/giờ chụp. Nếu ngày sửa khác folder cache hiện tại, app hỏi trước khi move file. Composition chỉ có thể ready/include sau khi metadata đủ để tạo time label.

- **UJ-4. Operator báo cáo ảnh vệ tinh xuất báo cáo.**  
  Operator báo cáo ảnh vệ tinh vào mode Export, chạy preflight. Nếu còn composition include nhưng chưa ready, app hỏi dừng toàn bộ hoặc bỏ qua composition lỗi. Khi export, app render PNG bản đồ theo từng composition, copy slide mẫu từ template riêng của target, thay ảnh/text, tạo PPTX tổng hợp và TXT. Sau export, app hiển thị summary và ghi log cạnh output.

## 3. Glossary

- **Target** — Mục tiêu cố định trong config JSON. Mỗi target có `id`, tên/alias/title, tọa độ target, scale, GeoJSON boundary để ingest, grid/export/template settings và metadata phụ.
- **GeoJSON boundary** — File GeoJSON của target, chỉ dùng để kiểm tra giao cắt khi ingest. Không hiển thị trong editor và không xuất lên slide ở MVP.
- **Image layer** — Một GeoTIFF đã được đưa vào workspace cho một target/date. Layer có visibility, order và metadata nghiệp vụ.
- **Composition** — Đơn vị trình bày `target + date`. Một composition tương ứng một slide nếu được `include=true`.
- **Workspace** — Thư mục làm việc chứa manifest, cache ảnh, composition JSON, renders và exports. Workspace là source of truth cho state.
- **Review order** — Thứ tự người dùng duyệt hợp lệ bằng mũi tên phải. Export sắp slide theo review order.
- **Template PPTX mapping** — cấu hình trong target export trỏ tới PPTX template một slide và ánh xạ các report fields tới PowerPoint element ids.
- **Map frame** — Vùng trên slide dùng để đặt ảnh bản đồ render final.
- **View state** — Trạng thái hiển thị bản đồ của composition gồm `center` `[lon, lat]`, `scale`, và `rotation=0`; đây là source-of-truth cho preview/final render. View ban đầu được khởi tạo từ tọa độ target và scale trong config. `scale` là mẫu số tỷ lệ bản đồ: `scale=50000` nghĩa là 1:50.000.
- **Issue** — Kết quả validation có `severity` là `info`, `warning`, hoặc `error`. `error` chặn ready/export.

## 4. Features

### 4.1 Project Setup and Data Ingestion

**Description:** Người dùng chọn config, imagery input folder và workspace, sau đó app quét GeoTIFF, parse metadata, kiểm tra giao cắt với target GeoJSON, copy ảnh vào cache và tạo composition theo target-date. Realizes UJ-1.

**Functional Requirements:**

#### FR-1: Load target config

Người dùng có thể chọn một config JSON mô tả danh sách target enabled, tọa độ target, scale mẫu số tỷ lệ bản đồ, settings grid/export/template và đường dẫn GeoJSON.

**Consequences:**
- App báo lỗi nếu config JSON không đọc được hoặc thiếu trường bắt buộc.
- App chỉ ingest target có `enabled=true`.
- App dùng `sort_order` để hiển thị target mặc định.

#### FR-2: Select input and workspace folders

Người dùng có thể chọn imagery input folder local/LAN và workspace folder.

**Consequences:**
- App hiển thị rõ đường dẫn đã chọn trước khi ingest.
- Khi bấm `Lấy dữ liệu`, nếu workspace cũ tồn tại, app yêu cầu xác nhận trước khi xóa workspace/cache/compositions/renders/exports cũ.

#### FR-3: Scan and match GeoTIFF imagery

App scan GeoTIFF recursively, parse metadata filename theo pattern PlanetScope-style, và kiểm tra giao cắt giữa ảnh và GeoJSON boundary của từng target.

**Consequences:**
- Ảnh intersect target nào thì được copy vào cache của target đó.
- Một ảnh intersect nhiều target được copy vào từng folder target liên quan.
- Cloud percent được parse/lưu/hiển thị nhưng không dùng để lọc ảnh trong MVP.
- Ảnh không parse được metadata vẫn có thể vào workspace nếu intersect, nhưng layer bị đánh dấu cần sửa metadata.

#### FR-4: Create target-date compositions

App tạo một composition JSON cho mỗi cặp target-date có ảnh matched.

**Consequences:**
- Nếu target có ảnh ở nhiều ngày, app tạo nhiều composition và hiển thị warning/info phù hợp.
- Composition mới mặc định `reviewed=false`, `ready=false`, `include=false`.
- Layer mặc định sắp ảnh mới nhất ở trên cùng.

#### FR-5: Show ingestion progress and warnings

Setup mode hiển thị progress ingest.

**Consequences:**
- Progress gồm scanned image count, matched image count, targets with images, warning count, current target đang xử lý và matched count cho target hiện tại.
- Warnings ingest được đưa vào Warnings panel hoặc summary sau ingest.

### 4.2 Workspace and Composition State

**Description:** App quản lý state trong workspace bằng JSON artifact độc lập để người dùng có thể inspect, backup và phục hồi. Realizes UJ-1, UJ-2, UJ-4.

**Functional Requirements:**

#### FR-6: Maintain workspace structure

Workspace chứa `manifest.json`, `cache/`, `compositions/`, `renders/` và `exports/`.

**Consequences:**
- Composition JSON nằm ở `compositions/target_id__YYYYMMDD.json` hoặc scheme tương đương ổn định.
- Workspace service là source of truth cho read/write composition, status, review order và validation summary.

#### FR-7: Persist composition status

App lưu status của mỗi composition gồm `reviewed`, `ready`, `include`, `review_order`, `notes`.

**Consequences:**
- Mũi tên phải chỉ set `reviewed=true`, `ready=true`, `include=true` sau full validation pass.
- Mũi tên lên set `reviewed=true`, `ready=false`, `include=false` và chuyển tiếp.
- Mũi tên trái quay lại composition trước; nếu composition trước đang `ready=true`, app hỏi trước khi reset state để chỉnh lại.

#### FR-8: Persist validation summary only

Composition lưu validation summary thay vì full issue list.

**Consequences:**
- Summary gồm last validated time và count theo severity.
- Issue chi tiết được tính lại khi chọn composition, khi duyệt và khi export preflight.
- Sau thay đổi layer/view/grid/metadata, app đánh dấu composition cần revalidate.

### 4.3 Review/Edit Workspace

**Description:** Review/Edit mode là màn hình chính để người dùng duyệt composition, điều chỉnh layer/view/grid và quyết định slide nào đưa vào báo cáo. Realizes UJ-2, UJ-3.

**Functional Requirements:**

#### FR-9: Provide target-composition navigation

Review/Edit hiển thị tree `target -> composition` kèm queue filters.

**Consequences:**
- Tree hiển thị status/icon issue ở cả target và composition.
- Filters tối thiểu gồm `Tất cả`, `Chưa duyệt`, `Ready`, `Include`, `Có warning`, `Có error`.
- Target node aggregate số composition chưa duyệt, ready/include và issue counts.

#### FR-10: Show and edit layer stack

Người dùng có thể xem layers của composition, bật/tắt visibility và đổi order.

**Consequences:**
- Layer order được lưu vào composition JSON.
- Time label tính từ các layer visible/selected hợp lệ trong composition.
- Nếu không có layer visible, validation trả `error`.

#### FR-11: Edit composition view through GIS editor

Người dùng pan/zoom bản đồ bên dưới map frame cố định.

**Consequences:**
- Source-of-truth lưu lại là `view.center` `[lon, lat]` và `view.scale`; view ban đầu của composition lấy từ tọa độ target và scale trong config. `view.scale` lưu mẫu số tỷ lệ bản đồ, ví dụ `50000` cho tỷ lệ 1:50.000.
- Grid interval ban đầu lấy từ target grid config để vẽ overlay trên view này; override per composition thuộc FR-12.
- Rotation lưu mặc định `0` nhưng không có UI xoay trong MVP.
- UI có mouse wheel zoom và slider phóng to/thu nhỏ; scale được cập nhật từ thao tác zoom nhưng không bắt người dùng nhập scale thủ công.

#### FR-12: Configure grid override per composition

Người dùng có thể chỉnh grid interval cho composition hiện tại bằng DMS fields.

**Consequences:**
- Grid default lấy từ target config.
- Custom grid lưu trong composition override, không sửa config gốc.
- Label format lấy từ config, default `dms_full`.

#### FR-13: Show slide preview

Panel trái hiển thị slide preview cập nhật khi view/layer/grid/metadata thay đổi.

**Consequences:**
- Preview dùng debounce hoặc cache để không làm lag editor.
- Preview phải đủ gần final export về tâm/scale view, layer order, grid và background.

#### FR-14: Support manual metadata correction

Người dùng có thể sửa metadata ngày/giờ của layer không parse được hoặc sai.

**Consequences:**
- Layer lưu `metadata_status` và metadata source.
- Nếu sửa date khác folder cache hiện tại, app hỏi trước khi move file.
- Composition không thể ready nếu metadata không đủ để tạo time label.

### 4.4 Rendering

**Description:** Renderer tạo preview nhanh trong editor và PNG final chất lượng cao để chèn vào PPTX. Realizes UJ-2, UJ-4.

**Functional Requirements:**

#### FR-15: Render map output from composition state

Renderer nhận composition, target config, PPTX map-frame bounds và output size để tạo map image.

**Consequences:**
- Render dùng `view.center`, `view.scale`, visible layer order, grid settings, background RGB và map frame aspect ratio; geographic read window được suy ra từ center, mẫu số scale, và kích thước vật lý của map frame trong PPTX template.
- Final render output size được lấy từ template map frame metadata hoặc export settings; MVP phải ghi rõ pixel width/height dùng cho PNG final trong render log.
- Boundary GeoJSON không được render trong editor/export ở MVP.
- Không render north arrow hoặc scale bar trong MVP.

#### FR-16: Provide hybrid preview/final pipeline

Renderer có preview path tối ưu tốc độ và final path tối ưu chất lượng.

**Consequences:**
- GIS editor chính dùng two-stage render: interactive thô khi kéo/zoom, settle sắc nét khi dừng.
- Final render đọc raster ở chất lượng phù hợp output size chính thức từ PPTX map-frame bounds/export settings.
- Render job cũ bị cancel hoặc ignore nếu state mới hơn xuất hiện.
- Acceptance for first vertical slice: preview and final render must use the same `view.center`, `view.scale`, visible layer order and grid interval; any remaining pixel-level tolerance is measured against sample fixtures after real imagery is available.

### 4.5 Validation and Warnings

**Description:** App phát hiện lỗi kỹ thuật, cảnh báo rủi ro và hướng dẫn khắc phục trước khi ready/export. Realizes UJ-2, UJ-3, UJ-4.

**Functional Requirements:**

#### FR-17: Produce structured issues

Validation trả issue có `issue_id`, `severity`, `scope`, target/composition/layer reference, message, remediation và blocking flag.

**Consequences:**
- `issue_id` dùng tiếng Anh ổn định cho code/test/log.
- `message` và `remediation` dùng tiếng Việt cho UI/log.
- Severity gồm `info`, `warning`, `error`; `error` chặn ready/export.

#### FR-18: Validate at key workflow points

App validate khi chọn composition, khi duyệt bằng mũi tên phải và khi export preflight.

**Consequences:**
- Khi chọn composition, app cập nhật issue panel/list status.
- Khi mũi tên phải có error, app không set ready/include và không chuyển tiếp.
- Export preflight validate lại composition `include=true` để tránh stale state.

#### FR-19: Surface issues in UI

UI hiển thị issue ở tree và Warnings panel.

**Consequences:**
- Target/composition tree có icon hoặc indicator theo severity cao nhất.
- Warnings panel cho phép xem issue aggregate và điều hướng tới target/composition/layer liên quan.

### 4.6 PowerPoint and TXT Export

**Description:** Export mode tạo một PPTX báo cáo tổng hợp và TXT đi kèm từ các composition included, theo review order. Realizes UJ-4.

**Functional Requirements:**

#### FR-20: Load target-specific one-slide PowerPoint template

Mỗi target khai báo trực tiếp `export.template_pptx_file`; PPTX template riêng của target phải có đúng một slide dùng làm slide mẫu.

**Consequences:**
- Target export config chứa mapping giữa report fields và PowerPoint element ids đã biết trong PPTX.
- Placeholder lookup dùng PowerPoint element id là cơ chế chính; shape name chỉ dùng làm thông tin chẩn đoán nếu cần.
- Validation báo lỗi nếu template PPTX thiếu, không đúng một slide, hoặc thiếu required element ids.
- Minimum compatibility checks for MVP: template PPTX exists, exactly one slide resolves, required element ids resolve, map frame dimensions are positive, and image/text replacement can be completed on a dry-run copy; failure is an `error` blocking export.

#### FR-21: Export one combined PPTX

App xuất một PPTX tổng hợp gồm các composition `reviewed=true`, `ready=true`, `include=true`, sorted by `review_order`.

**Consequences:**
- Mỗi exported composition copy one-slide target-specific template.
- Các target template trong MVP phải dùng cùng base/theme/master tương thích.
- App thay map image và text placeholders theo PowerPoint element-id mapping trong target export config.

#### FR-22: Export TXT using configured template

App xuất TXT với một dòng cho mỗi composition included.

**Consequences:**
- Dòng TXT dùng `txt_line_template` từ target config hoặc export config của target.
- Time label có format một timestamp hoặc khoảng thời gian theo layer visible hợp lệ.
- Missing required template fields or unresolved placeholders in `txt_line_template` are validation `error`; optional fields may render as empty only when explicitly marked optional in config.

#### FR-23: Show export summary and write logs

Sau export, app hiển thị summary và ghi log cạnh output.

**Consequences:**
- Summary gồm số slide, số target, số skipped, warnings và output paths.
- Log JSON/TXT ghi composition exported/skipped và issue summary.

## 5. Non-Goals (Explicit)

- Không xây GIS đầy đủ hoặc thay thế QGIS/ArcGIS.
- Không làm web app, multi-user, auth, cloud sync hoặc permission system trong MVP.
- Không auto mosaic hoặc tự động chọn ảnh tốt nhất.
- Không cloud filter tự động; cloud percent chỉ parse/lưu/hiển thị.
- Không hỗ trợ rotation UI trong MVP.
- Không render boundary, north arrow hoặc scale bar lên slide trong MVP.
- Không yêu cầu metadata JSON trung gian cho template PowerPoint trong MVP; app dùng PPTX template một slide và mapping element id khai báo trong config.

## 6. MVP Scope

### 6.1 In Scope

- Desktop app PySide6/PyQt6.
- Target config JSON đầy đủ per target.
- Ingestion GeoTIFF theo target GeoJSON intersection.
- Workspace/cache/composition JSON.
- Review/Edit với tree + filters, layer panel, slide preview, GIS editor.
- Manual metadata correction cho layer cần sửa.
- Grid DMS và custom grid interval per composition.
- Hybrid renderer và final PNG export.
- Target-specific one-slide PPTX template and element-id replacement mapping.
- One combined PPTX output và TXT output.
- Validation issues, Warnings panel, export preflight và export logs.

### 6.2 Out of Scope for MVP

- PyQGIS integration.
- Web/local web server implementation.
- Multi-user collaboration.
- Auto mosaic, auto image ranking, cloud filtering.
- Rotation controls.
- Advanced cartographic decorations beyond grid.
- Template analyzer inside main app.

## 7. Cross-Cutting NFRs

- **Performance:** Editor interactions should remain responsive with large GeoTIFFs by using cache/downsample and two-stage render. [ASSUMPTION: exact acceptable latency targets will be defined after testing with real imagery.]
- **Reliability:** Workspace writes should avoid corrupting composition JSON; failed writes should not leave partial invalid JSON.
- **Recoverability:** Workspace artifacts should be inspectable and recoverable manually where possible.
- **Traceability:** Export log must make it clear which composition created which slide/TXT line and why any composition was skipped.
- **Data locality:** App works with local/LAN files and does not require network access for MVP.
- **Usability:** Critical validation errors must include remediation text in Vietnamese.

## 8. Constraints and Guardrails

- MVP technology direction is desktop PySide6/PyQt6 with self-rendered QGraphicsView, not PyQGIS.
- Raster/GIS processing uses Python ecosystem libraries such as rasterio/GDAL/shapely/pyproj/numpy/Pillow.
- PowerPoint export uses `python-pptx` plus any necessary controlled XML/media handling.
- Target templates may be separate PPTX files, but must be created from a compatible base/theme/master for MVP.
- Workspace cleanup on `Lấy dữ liệu` must require explicit confirmation.

## 9. Risks and Mitigations

- **R-1: PPTX slide copying across templates may be unstable.** Mitigation: require same base/theme/master, validate template compatibility, and prove export in the first vertical slice.
- **R-2: Large GeoTIFF preview may lag.** Mitigation: implement downsample/overview cache and two-stage render before expanding UI polish.
- **R-3: CRS/grid rendering may be subtly wrong.** Mitigation: test render output with known fixtures and inspect grid labels early.
- **R-4: Filename metadata pattern may not cover all imagery.** Mitigation: allow manual metadata edit and block ready/export until fixed.
- **R-5: Clearing workspace may destroy useful edits.** Mitigation: require confirmation and make behavior explicit in Setup.

## 10. Success Metrics

**Primary**

- **SM-1:** End-to-end vertical slice succeeds on sample data: ingest -> composition -> review/edit -> render -> PPTX/TXT export. Validates FR-1 through FR-23.
- **SM-2:** Exported PPTX has correct slide count, review order, map image placement and target-specific text for all included compositions. Validates FR-20, FR-21, FR-23.
- **SM-3:** Validation blocks all known error cases in test fixtures: no visible layer, missing image file, missing capture time, invalid grid, missing template placeholder. Validates FR-17, FR-18.

**Secondary**

- **SM-4:** User can recover or inspect state from workspace JSON without opening the app. Validates FR-6, FR-7, FR-8.
- **SM-5:** Preview and final render match in center, scale, visible layer order, grid interval and map frame aspect ratio; final PNG size is recorded from PPTX map-frame bounds/export settings. Pixel-level tolerance is calibrated with real sample imagery. Validates FR-13, FR-15, FR-16.

**Counter-metrics**

- **SM-C1:** Do not optimize for fully automatic export at the cost of review control. Manual review is intentionally part of the workflow.
- **SM-C2:** Do not optimize for adding GIS features beyond the report workflow before the vertical slice is proven.

## 11. Open Questions

1. **Architecture blocker:** What is the real target output resolution/DPI required for map images in PPTX?
2. **Architecture blocker:** What exact target export mapping schema will store PPTX element ids for map image and text/image placeholders?
3. **Architecture blocker:** What real GeoTIFF CRS patterns must MVP support beyond the initial sample set?
4. **Can defer to implementation hardening:** Should manual metadata edits be stored only in composition JSON, or also in a separate metadata overrides file for reuse across re-ingest?
5. **UX/performance blocker before UI polish:** What is the acceptable UI latency for pan/zoom and settle render on representative large GeoTIFFs?
6. **Architecture/UX blocker:** How should review_order be reassigned if a previously ready composition is reset and reviewed again?

## 12. Assumptions Index

- §7 Performance — acceptable latency targets will be defined after testing with real imagery.
