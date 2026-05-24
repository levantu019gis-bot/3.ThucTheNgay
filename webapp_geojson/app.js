const state = {
  map: null,
  drawing: false,
  currentPoints: [],
  currentPolyline: null,
  polygons: [],
  tempMarkers: [],
};

const elements = {
  drawBtn: document.getElementById("drawBtn"),
  finishBtn: document.getElementById("finishBtn"),
  undoPointBtn: document.getElementById("undoPointBtn"),
  deleteLastBtn: document.getElementById("deleteLastBtn"),
  clearBtn: document.getElementById("clearBtn"),
  downloadBtn: document.getElementById("downloadBtn"),
  polygonCount: document.getElementById("polygonCount"),
  pointCount: document.getElementById("pointCount"),
  status: document.getElementById("status"),
};

function initMap() {
  state.map = L.map("map", {
    center: [16.047079, 108.20623],
    zoom: 6,
    preferCanvas: true,
  });

  L.tileLayer("https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", {
    maxZoom: 22,
    attribution: "Map tiles © Google",
  }).addTo(state.map);

  state.map.on("click", (event) => {
    if (!state.drawing) return;
    addPoint(event.latlng);
  });

  updateUi();
}

function addPoint(latLng) {
  state.currentPoints.push(latLng);

  const marker = L.circleMarker(latLng, {
    radius: 5,
    color: "#ffffff",
    weight: 2,
    fillColor: "#176b87",
    fillOpacity: 0.95,
    interactive: false,
  }).addTo(state.map);
  state.tempMarkers.push(marker);

  if (!state.currentPolyline) {
    state.currentPolyline = L.polyline(state.currentPoints, {
      color: "#176b87",
      weight: 3,
      opacity: 1,
      interactive: false,
    }).addTo(state.map);
  } else {
    state.currentPolyline.setLatLngs(state.currentPoints);
  }

  if (state.currentPoints.length >= 3) {
    setStatus("Có thể bấm 'Hoàn tất vùng' để tạo polygon.");
  } else {
    setStatus("Thêm ít nhất 3 điểm để tạo một vùng.");
  }
  updateUi();
}

function startDrawing() {
  state.drawing = true;
  state.currentPoints = [];
  clearCurrentSketch();
  state.map.getContainer().classList.add("drawing");
  setStatus("Đang vẽ: click lên bản đồ để thêm các đỉnh polygon.");
  updateUi();
}

function finishPolygon() {
  if (state.currentPoints.length < 3) {
    setStatus("Polygon cần ít nhất 3 điểm.", true);
    return;
  }

  const polygon = L.polygon(state.currentPoints, {
    color: "#176b87",
    weight: 2,
    opacity: 1,
    fillColor: "#25a18e",
    fillOpacity: 0.28,
  }).addTo(state.map);

  state.polygons.push(polygon);
  state.drawing = false;
  state.currentPoints = [];
  clearCurrentSketch();
  state.map.getContainer().classList.remove("drawing");
  fitToPolygons();
  setStatus("Đã tạo vùng. Bấm tải GeoJSON để xuất file.");
  updateUi();
}

function undoPoint() {
  if (!state.currentPoints.length) return;

  state.currentPoints.pop();
  const marker = state.tempMarkers.pop();
  marker?.remove();
  state.currentPolyline?.setLatLngs(state.currentPoints);

  setStatus(state.currentPoints.length ? "Đã lùi một điểm." : "Chưa có điểm nào trong vùng đang vẽ.");
  updateUi();
}

function deleteLastPolygon() {
  const polygon = state.polygons.pop();
  polygon?.remove();
  setStatus("Đã xóa vùng cuối.");
  updateUi();
}

function clearAll() {
  state.polygons.forEach((polygon) => polygon.remove());
  state.polygons = [];
  state.currentPoints = [];
  state.drawing = false;
  clearCurrentSketch();
  state.map.getContainer().classList.remove("drawing");
  setStatus("Đã xóa tất cả vùng.");
  updateUi();
}

function clearCurrentSketch() {
  state.currentPolyline?.remove();
  state.currentPolyline = null;
  state.tempMarkers.forEach((marker) => marker.remove());
  state.tempMarkers = [];
}

function polygonToCoordinates(polygon) {
  const latLngs = polygon.getLatLngs()[0] || [];
  const ring = latLngs.map((point) => [roundCoord(point.lng), roundCoord(point.lat)]);

  if (ring.length) {
    const first = ring[0];
    const last = ring[ring.length - 1];
    if (first[0] !== last[0] || first[1] !== last[1]) {
      ring.push([...first]);
    }
  }

  return [ring];
}

function buildGeoJson() {
  return {
    type: "FeatureCollection",
    features: state.polygons.map((polygon, index) => ({
      type: "Feature",
      properties: {
        id: index + 1,
      },
      geometry: {
        type: "Polygon",
        coordinates: polygonToCoordinates(polygon),
      },
    })),
  };
}

function downloadGeoJson() {
  if (!state.polygons.length) return;

  const geojson = buildGeoJson();
  const blob = new Blob([JSON.stringify(geojson, null, 2)], {
    type: "application/geo+json;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `drawn-polygons-${new Date().toISOString().slice(0, 19).replaceAll(":", "-")}.geojson`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function fitToPolygons() {
  if (!state.polygons.length) return;
  const group = L.featureGroup(state.polygons);
  state.map.fitBounds(group.getBounds(), { padding: [48, 48] });
}

function updateUi() {
  const canFinish = state.currentPoints.length >= 3;
  const hasCurrentPoints = state.currentPoints.length > 0;
  const hasPolygons = state.polygons.length > 0;

  elements.drawBtn.disabled = state.drawing;
  elements.finishBtn.disabled = !state.drawing || !canFinish;
  elements.undoPointBtn.disabled = !state.drawing || !hasCurrentPoints;
  elements.deleteLastBtn.disabled = !hasPolygons;
  elements.clearBtn.disabled = !hasPolygons && !hasCurrentPoints;
  elements.downloadBtn.disabled = !hasPolygons;
  elements.polygonCount.textContent = String(state.polygons.length);
  elements.pointCount.textContent = String(state.currentPoints.length);
}

function setStatus(message, isError = false) {
  elements.status.textContent = message;
  elements.status.style.color = isError ? "#b23a48" : "";
}

function roundCoord(value) {
  return Number(value.toFixed(7));
}

elements.drawBtn.addEventListener("click", startDrawing);
elements.finishBtn.addEventListener("click", finishPolygon);
elements.undoPointBtn.addEventListener("click", undoPoint);
elements.deleteLastBtn.addEventListener("click", deleteLastPolygon);
elements.clearBtn.addEventListener("click", clearAll);
elements.downloadBtn.addEventListener("click", downloadGeoJson);

initMap();
