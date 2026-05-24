# GeoJSON Drawer

Webapp static dùng Leaflet với nền ảnh vệ tinh từ tile URL:

```text
https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}
```

App cho phép vẽ nhiều polygon và tải xuống file GeoJSON. Không cần Google Maps API key.

## Chạy nhanh

Mở trực tiếp `index.html`, hoặc chạy local server:

```bash
cd webapp_geojson
python3 -m http.server 8080
```

Sau đó mở:

```text
http://localhost:8080/
```

## Cách dùng

1. Bấm **Bắt đầu vẽ**.
2. Click trên bản đồ để thêm các đỉnh polygon.
3. Bấm **Hoàn tất vùng** khi có ít nhất 3 điểm.
4. Bấm **Tải GeoJSON** để tải `FeatureCollection`.

GeoJSON xuất ra dùng hệ tọa độ WGS84 với thứ tự tọa độ chuẩn `[longitude, latitude]`.
