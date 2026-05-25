const FEATURE_STYLE = {
  color: "#f97316",
  weight: 2,
  opacity: 1,
  fillColor: "#f59e0b",
  fillOpacity: 0.28,
};

const DRAWN_STYLE = {
  color: "#176b87",
  weight: 2,
  opacity: 1,
  fillColor: "#25a18e",
  fillOpacity: 0.28,
};

const SELECTED_STYLE = {
  color: "#dc2626",
  weight: 4,
  opacity: 1,
  fillColor: "#f97316",
  fillOpacity: 0.38,
};

const BULK_SELECTED_STYLE = {
  color: "#2563eb",
  weight: 4,
  opacity: 1,
  fillColor: "#38bdf8",
  fillOpacity: 0.36,
};

const state = {
  map: null,
  drawing: false,
  editMode: false,
  bulkGroupMode: false,
  bulkSelectedFeatures: new Set(),
  currentPoints: [],
  currentPolyline: null,
  features: [],
  selectedFeature: null,
  tempMarkers: [],
  editMarkers: [],
  nextFeatureId: 1,
};

const elements = {
  editModeBtn: document.getElementById("editModeBtn"),
  bulkGroupModeBtn: document.getElementById("bulkGroupModeBtn"),
  drawBtn: document.getElementById("drawBtn"),
  finishBtn: document.getElementById("finishBtn"),
  undoPointBtn: document.getElementById("undoPointBtn"),
  deleteLastBtn: document.getElementById("deleteLastBtn"),
  clearBtn: document.getElementById("clearBtn"),
  downloadBtn: document.getElementById("downloadBtn"),
  uploadInput: document.getElementById("uploadInput"),
  featureEditor: document.getElementById("featureEditor"),
  featureAliasInput: document.getElementById("featureAliasInput"),
  featureGroupInput: document.getElementById("featureGroupInput"),
  selectedFeatureType: document.getElementById("selectedFeatureType"),
  saveFeaturePropsBtn: document.getElementById("saveFeaturePropsBtn"),
  deleteFeatureBtn: document.getElementById("deleteFeatureBtn"),
  bulkGroupEditor: document.getElementById("bulkGroupEditor"),
  bulkSelectedCount: document.getElementById("bulkSelectedCount"),
  bulkGroupInput: document.getElementById("bulkGroupInput"),
  applyBulkGroupBtn: document.getElementById("applyBulkGroupBtn"),
  clearBulkSelectionBtn: document.getElementById("clearBulkSelectionBtn"),
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

  setStatus(state.currentPoints.length >= 3 ? "Có thể bấm 'Hoàn tất vùng' để tạo feature mới." : "Thêm ít nhất 3 điểm để tạo một vùng.");
  updateUi();
}

function toggleEditMode() {
  state.editMode = !state.editMode;

  if (!state.editMode) {
    state.bulkGroupMode = false;
    stopDrawing();
    selectFeature(null);
    clearBulkSelection();
    setStatus("Đã tắt chế độ chỉnh sửa.");
  } else {
    setStatus("Đã bật chỉnh sửa: chọn feature để sửa alias, group, xóa hoặc kéo các đỉnh polygon.");
  }

  updateUi();
}

function toggleBulkGroupMode() {
  state.bulkGroupMode = !state.bulkGroupMode;

  if (state.bulkGroupMode) {
    state.editMode = true;
    stopDrawing();
    selectFeature(null);
    clearBulkSelection();
    setStatus("Đang sửa group nhiều feature: click các feature cần cập nhật group.");
  } else {
    clearBulkSelection();
    setStatus("Đã tắt sửa group nhiều feature.");
  }

  updateUi();
}

function startDrawing() {
  state.drawing = true;
  state.bulkGroupMode = false;
  state.currentPoints = [];
  clearCurrentSketch();
  selectFeature(null);
  clearBulkSelection();
  state.map.getContainer().classList.add("drawing");
  setStatus("Đang vẽ feature mới: click lên bản đồ để thêm các đỉnh polygon.");
  updateUi();
}

function stopDrawing() {
  state.drawing = false;
  state.currentPoints = [];
  clearCurrentSketch();
  state.map?.getContainer().classList.remove("drawing");
}

function finishPolygon() {
  if (state.currentPoints.length < 3) {
    setStatus("Polygon cần ít nhất 3 điểm.", true);
    return;
  }

  const polygon = L.polygon(state.currentPoints, DRAWN_STYLE).addTo(state.map);
  const feature = addFeatureLayer(polygon, { alias: "", group: "" }, DRAWN_STYLE);

  stopDrawing();
  fitToFeatures();
  selectFeature(feature);
  setStatus("Đã tạo feature mới. Có thể nhập alias/group hoặc tiếp tục chỉnh sửa.");
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

function deleteLastFeature() {
  const feature = state.features.at(-1);
  if (!feature) return;
  deleteFeature(feature);
  setStatus("Đã xóa feature cuối.");
}

function clearAll() {
  clearBulkSelection();
  state.features.forEach((feature) => feature.layer.remove());
  state.features = [];
  stopDrawing();
  selectFeature(null);
  setStatus("Đã xóa tất cả feature GeoJSON.");
  updateUi();
}

function clearCurrentSketch() {
  state.currentPolyline?.remove();
  state.currentPolyline = null;
  state.tempMarkers.forEach((marker) => marker.remove());
  state.tempMarkers = [];
}

function addFeatureLayer(layer, properties = {}, style = FEATURE_STYLE) {
  const feature = {
    id: state.nextFeatureId,
    layer,
    properties: { ...properties },
    style,
  };
  state.nextFeatureId += 1;
  state.features.push(feature);
  makeFeatureSelectable(feature);
  return feature;
}

function makeFeatureSelectable(feature) {
  feature.layer.on("click", (event) => {
    if (!state.editMode) return;
    if (event.originalEvent) L.DomEvent.stop(event.originalEvent);

    if (state.bulkGroupMode) {
      toggleBulkFeatureSelection(feature);
      return;
    }

    selectFeature(feature);
  });
}

function selectFeature(feature) {
  if (state.selectedFeature && state.selectedFeature !== feature) {
    setFeatureBaseStyle(state.selectedFeature);
  }

  clearEditMarkers();
  state.selectedFeature = feature;

  if (!feature) {
    elements.featureEditor.hidden = true;
    updateUi();
    return;
  }

  setLayerStyle(feature.layer, SELECTED_STYLE);
  const geojson = layerToFeature(feature);
  elements.selectedFeatureType.textContent = geojson.geometry?.type || "Feature";
  elements.featureAliasInput.value = feature.properties.alias || feature.properties.name || "";
  elements.featureGroupInput.value = feature.properties.group ?? "";
  elements.featureEditor.hidden = false;
  createEditMarkers(feature);
  setStatus("Đã chọn feature. Kéo đỉnh polygon để sửa hình hoặc nhập alias/group rồi lưu.");
  updateUi();
}

function setFeatureBaseStyle(feature) {
  setLayerStyle(
    feature.layer,
    state.bulkSelectedFeatures.has(feature) ? BULK_SELECTED_STYLE : feature.style
  );
}

function toggleBulkFeatureSelection(feature) {
  if (state.bulkSelectedFeatures.has(feature)) {
    state.bulkSelectedFeatures.delete(feature);
    setLayerStyle(feature.layer, feature.style);
  } else {
    state.bulkSelectedFeatures.add(feature);
    setLayerStyle(feature.layer, BULK_SELECTED_STYLE);
  }

  updateBulkEditor();
  updateUi();
}

function clearBulkSelection() {
  state.bulkSelectedFeatures.forEach((feature) => setLayerStyle(feature.layer, feature.style));
  state.bulkSelectedFeatures.clear();
  updateBulkEditor();
}

function updateBulkEditor() {
  elements.bulkSelectedCount.textContent = String(state.bulkSelectedFeatures.size);
  elements.bulkGroupEditor.hidden = !state.bulkGroupMode;
}

function parseGroupValue(value) {
  const trimmed = value.trim();
  const numberValue = Number(trimmed);

  if (trimmed && Number.isFinite(numberValue)) return numberValue;
  return trimmed;
}

function applyBulkGroup() {
  if (!state.bulkSelectedFeatures.size) {
    setStatus("Chưa chọn feature nào để cập nhật group.", true);
    return;
  }

  const rawValue = elements.bulkGroupInput.value.trim();
  if (!rawValue) {
    setStatus("Nhập giá trị group trước khi cập nhật.", true);
    return;
  }

  const groupValue = parseGroupValue(rawValue);
  state.bulkSelectedFeatures.forEach((feature) => {
    feature.properties.group = groupValue;
  });

  setStatus(`Đã cập nhật group cho ${state.bulkSelectedFeatures.size} feature.`);
}

function setLayerStyle(layer, style) {
  if (typeof layer.setStyle === "function") {
    layer.setStyle(style);
  }

  if (typeof layer.eachLayer === "function") {
    layer.eachLayer((child) => setLayerStyle(child, style));
  }
}

function createEditMarkers(feature) {
  const polygon = findEditablePolygon(feature.layer);
  const ring = getEditableRing(polygon);

  if (!ring) {
    setStatus("Feature này có thể sửa alias/group hoặc xóa; chỉnh đỉnh chỉ hỗ trợ Polygon đơn.");
    return;
  }

  ring.forEach((latLng, index) => {
    const marker = L.marker(latLng, {
      draggable: true,
      icon: createVertexIcon(),
    }).addTo(state.map);

    marker.on("drag", () => {
      ring[index] = marker.getLatLng();
      polygon.setLatLngs([ring]);
    });
    marker.on("dragend", () => {
      ring[index] = marker.getLatLng();
      polygon.setLatLngs([ring]);
    });
    state.editMarkers.push(marker);
  });
}

function clearEditMarkers() {
  state.editMarkers.forEach((marker) => marker.remove());
  state.editMarkers = [];
}

function createVertexIcon() {
  return L.divIcon({
    className: "vertex-marker",
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
}

function findEditablePolygon(layer) {
  if (layer instanceof L.Polygon && !(layer instanceof L.Rectangle)) return layer;

  if (typeof layer.eachLayer === "function") {
    let found = null;
    layer.eachLayer((child) => {
      if (!found) found = findEditablePolygon(child);
    });
    return found;
  }

  return null;
}

function getEditableRing(polygon) {
  if (!polygon) return null;

  const latLngs = polygon.getLatLngs();
  const ring = latLngs[0];

  if (!Array.isArray(ring) || !ring.length || !ring[0].lat) return null;
  return ring;
}

function saveSelectedFeatureProperties() {
  if (!state.selectedFeature) return;

  const alias = elements.featureAliasInput.value.trim();
  const group = elements.featureGroupInput.value.trim();

  if (alias) {
    state.selectedFeature.properties.alias = alias;
  } else {
    delete state.selectedFeature.properties.alias;
  }

  if (group) {
    state.selectedFeature.properties.group = parseGroupValue(group);
  } else {
    delete state.selectedFeature.properties.group;
  }

  setStatus("Đã lưu alias và group cho feature đang chọn.");
}

function deleteSelectedFeature() {
  if (!state.selectedFeature) return;
  deleteFeature(state.selectedFeature);
  setStatus("Đã xóa feature đang chọn.");
}

function deleteFeature(feature) {
  feature.layer.remove();
  state.features = state.features.filter((item) => item !== feature);
  state.bulkSelectedFeatures.delete(feature);

  if (state.selectedFeature === feature) {
    state.selectedFeature = null;
    elements.featureEditor.hidden = true;
    clearEditMarkers();
  }

  updateUi();
}

function uploadGeoJson(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    try {
      const geojson = JSON.parse(String(reader.result));
      const features = normalizeGeoJsonFeatures(geojson);

      if (!features.length) {
        setStatus("File GeoJSON không có feature hợp lệ.", true);
        return;
      }

      features.forEach((featureGeoJson) => addUploadedFeature(featureGeoJson));
      fitToFeatures();
      setStatus(`Đã upload và hiển thị ${features.length} feature từ ${file.name}.`);
      updateUi();
    } catch (error) {
      setStatus("Không đọc được file GeoJSON. Kiểm tra lại định dạng JSON.", true);
    } finally {
      elements.uploadInput.value = "";
    }
  };
  reader.readAsText(file);
}

function addUploadedFeature(featureGeoJson) {
  const group = L.geoJSON(featureGeoJson, {
    style: FEATURE_STYLE,
    pointToLayer: (_feature, latLng) =>
      L.circleMarker(latLng, {
        radius: 6,
        color: "#ffffff",
        weight: 2,
        fillColor: "#f97316",
        fillOpacity: 0.95,
      }),
  }).addTo(state.map);

  addFeatureLayer(group, featureGeoJson.properties || {}, FEATURE_STYLE);
}

function normalizeGeoJsonFeatures(geojson) {
  if (geojson?.type === "FeatureCollection") {
    return (geojson.features || []).filter((feature) => feature?.geometry);
  }

  if (geojson?.type === "Feature" && geojson.geometry) return [geojson];
  if (geojson?.type && geojson.coordinates) {
    return [{ type: "Feature", properties: {}, geometry: geojson }];
  }

  return [];
}

function buildGeoJson() {
  return {
    type: "FeatureCollection",
    features: state.features.map((feature, index) => ({
      ...layerToFeature(feature),
      properties: {
        id: index + 1,
        ...feature.properties,
      },
    })),
  };
}

function layerToFeature(feature) {
  const geojson = feature.layer.toGeoJSON();

  if (geojson.type === "FeatureCollection") {
    const first = geojson.features[0] || {
      type: "Feature",
      properties: {},
      geometry: null,
    };
    return {
      ...first,
      properties: { ...feature.properties },
    };
  }

  return {
    ...geojson,
    properties: { ...feature.properties },
  };
}

function downloadGeoJson() {
  if (!state.features.length) return;
  downloadJson(buildGeoJson(), `geojson-features-${timestamp()}.geojson`);
}

function downloadJson(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/geo+json;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function fitToFeatures() {
  if (!state.features.length) return;
  const group = L.featureGroup(state.features.map((feature) => feature.layer));
  const bounds = group.getBounds();

  if (bounds.isValid()) {
    state.map.fitBounds(bounds, { padding: [48, 48] });
  }
}

function updateUi() {
  const canFinish = state.currentPoints.length >= 3;
  const hasCurrentPoints = state.currentPoints.length > 0;
  const hasFeatures = state.features.length > 0;

  elements.editModeBtn.textContent = state.editMode ? "Tắt chỉnh sửa" : "Bật chỉnh sửa";
  elements.editModeBtn.classList.toggle("active", state.editMode);
  elements.drawBtn.disabled = state.drawing;
  elements.finishBtn.disabled = !state.drawing || !canFinish;
  elements.undoPointBtn.disabled = !state.drawing || !hasCurrentPoints;
  elements.deleteLastBtn.disabled = !hasFeatures;
  elements.clearBtn.disabled = !hasFeatures && !hasCurrentPoints;
  elements.downloadBtn.disabled = !hasFeatures;
  elements.bulkGroupModeBtn.textContent = state.bulkGroupMode ? "Tắt sửa group" : "Sửa group nhiều feature";
  elements.bulkGroupModeBtn.classList.toggle("active", state.bulkGroupMode);
  elements.applyBulkGroupBtn.disabled = !state.bulkSelectedFeatures.size;
  elements.clearBulkSelectionBtn.disabled = !state.bulkSelectedFeatures.size;
  elements.polygonCount.textContent = String(state.features.length);
  elements.pointCount.textContent = String(state.currentPoints.length);
}

function setStatus(message, isError = false) {
  elements.status.textContent = message;
  elements.status.style.color = isError ? "#b23a48" : "";
}

function timestamp() {
  return new Date().toISOString().slice(0, 19).replaceAll(":", "-");
}

elements.editModeBtn.addEventListener("click", toggleEditMode);
elements.bulkGroupModeBtn.addEventListener("click", toggleBulkGroupMode);
elements.drawBtn.addEventListener("click", startDrawing);
elements.finishBtn.addEventListener("click", finishPolygon);
elements.undoPointBtn.addEventListener("click", undoPoint);
elements.deleteLastBtn.addEventListener("click", deleteLastFeature);
elements.clearBtn.addEventListener("click", clearAll);
elements.downloadBtn.addEventListener("click", downloadGeoJson);
elements.uploadInput.addEventListener("change", uploadGeoJson);
elements.saveFeaturePropsBtn.addEventListener("click", saveSelectedFeatureProperties);
elements.deleteFeatureBtn.addEventListener("click", deleteSelectedFeature);
elements.applyBulkGroupBtn.addEventListener("click", applyBulkGroup);
elements.clearBulkSelectionBtn.addEventListener("click", clearBulkSelection);

initMap();
