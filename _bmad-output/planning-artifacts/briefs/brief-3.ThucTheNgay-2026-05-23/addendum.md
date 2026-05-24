# Product Brief Addendum

## Architecture Notes

MVP chọn layered architecture:

```text
app/
  config/
  ingestion/
  workspace/
  gis/
  editor/
  render/
  export/
  validation/
```

`workspace/` là source of truth cho manifest, composition JSON, cache references, render/export paths và status. `editor/` chỉ giữ UI state đang hiển thị; các thay đổi quan trọng đi qua workspace service. `validation/` trả issue, không tự mutate state.

## Composition Model Highlights

- `composition = target + date = one exported slide if included`.
- Status gồm `reviewed`, `ready`, `include`, `review_order`, `notes`.
- Composition lưu `validation_summary`, không lưu full issue list.
- Layer lưu metadata nghiệp vụ: path, visible, order, capture date/time, timestamp source, cloud percent, metadata status/notes.
- Raster technical metadata như CRS, bounds, transform, dimensions được đọc lại khi validate/render.
- View lưu `extent: [min_lon, min_lat, max_lon, max_lat]`; center/scale/zoom là derived.

## Template Decisions

- Mỗi target có `export.template_metadata_file`.
- Template metadata trỏ tới `template_pptx` riêng của target.
- Shape reference dùng `name` chính và `fallback_id` tùy chọn.
- Output vẫn là một PPTX tổng hợp, với constraint các target template dùng cùng base/theme/master tương thích.

## Validation Timing

- Validate khi chọn composition để cập nhật status/issue panel.
- Full validation khi bấm mũi tên phải để set ready/include.
- Export preflight validate lại composition `include=true`.
- Sau thay đổi view/layer/grid/metadata, UI đánh dấu `needs_revalidation` thay vì full validate liên tục.

## Suggested Vertical Slice Sequence

1. JSON schemas và sample fixtures cho 1-2 targets.
2. Config/workspace/composition services.
3. Ingestion tối thiểu: scan, parse filename, intersect GeoJSON, copy cache, create composition.
4. Final render PNG từ extent, visible layers, grid, background RGB.
5. Target-specific template metadata loading và one-slide PPTX export.
6. PySide6 Review/Edit shell trên dữ liệu thật.
7. Setup progress UI và Export preflight/summary.
8. Harden validation, warnings panel, metadata edit, two-stage preview cache.
