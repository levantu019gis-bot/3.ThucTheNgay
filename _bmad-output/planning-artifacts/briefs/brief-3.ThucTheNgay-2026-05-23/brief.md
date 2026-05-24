---
title: "Product Brief: App tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh"
status: draft
created: 2026-05-23
updated: 2026-05-23
---

# Product Brief: App tạo PowerPoint báo cáo mục tiêu từ ảnh vệ tinh

## Executive Summary

Sản phẩm là một desktop app cá nhân giúp tạo báo cáo PowerPoint và TXT từ ảnh vệ tinh quang học GeoTIFF cho các mục tiêu cố định. Người dùng cấu hình danh sách mục tiêu bằng JSON và GeoJSON, app tự quét thư mục ảnh, tìm ảnh giao cắt từng mục tiêu, nhóm theo mục tiêu và ngày chụp, cho phép người dùng duyệt/chỉnh khung bản đồ, bật tắt layer ảnh, kiểm tra grid tọa độ, rồi xuất báo cáo.

Vấn đề chính không chỉ là xuất slide hàng loạt. Người dùng cần kiểm soát trực quan từng “phiên ảnh” trước khi đưa vào báo cáo: ảnh nào dùng, thứ tự layer, vùng bản đồ nào nằm trong frame slide, grid hiển thị ra sao, metadata thời gian có hợp lệ không, và template slide của từng mục tiêu có đúng không. Vì vậy MVP được định hướng là desktop workflow có editor GIS mini, không phải script batch hoặc web app.

## Problem

Quy trình hiện tại khi làm báo cáo mục tiêu từ ảnh vệ tinh thường tốn nhiều thao tác thủ công: tìm ảnh đúng vùng mục tiêu, kiểm tra ngày giờ chụp, căn vùng ảnh vào khung slide, thêm grid tọa độ, điền nhãn thời gian, rồi lặp lại cho nhiều mục tiêu/ngày. Khi nhiều ảnh giao cùng một mục tiêu hoặc một ảnh giao nhiều mục tiêu, rủi ro sai sót tăng: bỏ sót ảnh, dùng sai ngày, lệch khung, sai template, hoặc xuất slide không đúng thứ tự duyệt.

Các công cụ GIS đầy đủ có thể xử lý dữ liệu, nhưng không tối ưu cho workflow tạo báo cáo PowerPoint theo template mục tiêu. Ngược lại, thao tác trực tiếp trong PowerPoint không đủ năng lực GIS để xử lý GeoTIFF, CRS, extent, grid và giao cắt GeoJSON.

## Solution

App cung cấp một workflow ba bước: Setup, Review/Edit, Export.

Trong Setup, người dùng chọn config JSON, thư mục ảnh GeoTIFF và workspace. App quét ảnh, parse metadata từ tên file, kiểm tra giao cắt với GeoJSON mục tiêu, copy ảnh vào workspace và tạo các composition theo `target + date`.

Trong Review/Edit, người dùng duyệt từng composition. Mỗi composition tương ứng một slide nếu được include. Editor cho phép pan/zoom ảnh dưới một map frame cố định, bật tắt layer, đổi thứ tự layer, chỉnh grid interval, xem preview slide, và dùng phím/nút điều hướng để đánh dấu ready/include hoặc bỏ qua.

Trong Export, app chạy preflight validation, render PNG bản đồ theo template metadata riêng của từng target, copy slide mẫu tương ứng vào một PPTX báo cáo tổng hợp, thay ảnh/text placeholders, xuất TXT theo template dòng cấu hình, và ghi log/summary sau export.

## Who This Serves

Người dùng chính là cá nhân hoặc nhóm nhỏ thường xuyên lập báo cáo mục tiêu từ ảnh vệ tinh quang học, cần kết quả PowerPoint nhất quán nhưng vẫn muốn kiểm soát thủ công từng slide trước khi xuất.

Thành công với người dùng là: giảm thời gian lặp thao tác, giảm lỗi metadata/template/khung ảnh, vẫn giữ quyền quyết định ảnh nào đưa vào báo cáo, và tạo được PPTX/TXT có thể dùng ngay sau khi review.

## Product Principles

- Workspace JSON là source of truth, dễ inspect và phục hồi.
- Mỗi composition là một artifact độc lập và tương ứng một slide.
- Preview phải đủ gần final export để người dùng tin vào kết quả.
- Validation phải chặn lỗi kỹ thuật thật sự, nhưng warning không cản workflow.
- MVP ưu tiên vertical slice chạy thật từ ảnh đến PPTX hơn là hoàn thiện từng module cô lập.

## MVP Scope

Included in MVP:

- Desktop app PySide6/PyQt6.
- Target config JSON với target khai báo đầy đủ, không dùng default ngầm cấp file.
- Ingestion GeoTIFF theo giao cắt target GeoJSON.
- Parse metadata từ tên file PlanetScope-style, cho phép sửa metadata thủ công khi parse lỗi.
- Workspace gồm manifest, cache ảnh, composition JSON, renders, exports.
- Review/Edit với tree `target -> composition`, layer panel, slide preview, GIS editor.
- View source-of-truth bằng geographic extent.
- Grid DMS, background RGB từ config target, không boundary overlay trong editor/export.
- Renderer hybrid: preview cache/downsample, final render chất lượng cao.
- Mỗi target có template metadata và PPTX template riêng; output vẫn là một PPTX tổng hợp.
- Validation issue schema với `issue_id` tiếng Anh, message/remediation tiếng Việt.
- Export PPTX/TXT, summary và log cạnh output.

Explicitly out of MVP:

- PyQGIS integration.
- Web app/local web server.
- Auto mosaic ảnh.
- Cloud filter tự động.
- Rotation UI.
- North arrow, scale bar, boundary overlay trên slide.
- Analyze template trực tiếp trong app chính; template metadata do script riêng tạo trước.

## Success Criteria

- Từ một config nhỏ và bộ GeoTIFF mẫu, app tạo được workspace và composition đúng theo target/ngày.
- Người dùng duyệt được composition, chỉnh extent/layer/grid và lưu lại state JSON.
- App render được PNG bản đồ final khớp với preview về extent, layer order, grid và background.
- App xuất được một PPTX tổng hợp từ nhiều target template tương thích, đúng review order.
- App xuất TXT với một dòng cho mỗi composition included.
- Validation chặn các lỗi bắt buộc: thiếu layer visible, file ảnh mất, metadata ngày giờ thiếu, grid invalid, template metadata/placeholder thiếu, render lỗi.

## Key Risks

- Copy slide giữa nhiều PPTX bằng `python-pptx` có thể phức tạp do relationship, media và theme/master. MVP giảm rủi ro bằng yêu cầu tất cả target template được tạo từ cùng base/theme tương thích.
- GeoTIFF lớn có thể làm preview lag. MVP cần cache/downsample và two-stage render cho editor chính.
- Metadata filename có thể không ổn định. MVP cho phép sửa metadata thủ công và chặn ready/export khi metadata chưa hợp lệ.
- CRS/geotransform/grid rendering cần được test bằng dữ liệu thật sớm, vì sai lệch nhỏ có thể làm slide không đáng tin.

## Implementation Direction

Đi theo vertical slice sớm: config nhỏ -> ingest ảnh -> tạo composition -> render PNG -> export PPTX/TXT -> gắn UI Review/Edit tối thiểu. Sau khi luồng thật chạy được, mở rộng validation, metadata edit, multi-target/multi-date, preview realtime, warnings panel và export log.
