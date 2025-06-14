  document.getElementById('close_Map').addEventListener('click', function(){
            document.getElementById('map').style.display = 'none';
            document.getElementById('close_Map').style.display = 'none';

            document.querySelectorAll('.show_Col').forEach(function(element) {
                element.style.display = 'block';
            });
        })
// Khởi tạo bản đồ
        const map = new ol.Map({
            target: 'map-container',
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                })
            ],
            view: new ol.View({
                center: ol.proj.fromLonLat([105.8542, 21.0285]),
                zoom: 12
            })
        });
document.querySelector('.navbar').classList.add('map-visible');
        setTimeout(() => {
            const overlayContainer = document.querySelector('.ol-overlaycontainer-stopevent');
            if (overlayContainer) {
                // Thêm thuộc tính style
                overlayContainer.style.display = 'none';
            } else {
                console.error('Không tìm thấy .ol-overlaycontainer-stopevent');
            }
        }, 0);

        // Tạo layer cho marker
        const marker = new ol.Feature();
        const vectorSource = new ol.source.Vector({
            features: [marker]
        });
        const vectorLayer = new ol.layer.Vector({
            source: vectorSource
        });
        map.addLayer(vectorLayer);

        // Hàm cập nhật marker và trung tâm bản đồ
        function updateMap(lon, lat) {
            const point = new ol.geom.Point(ol.proj.fromLonLat([lon, lat]));
            marker.setGeometry(point);
            map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
            map.getView().setZoom(15);
        }

        // Hàm lấy địa chỉ từ tọa độ bằng Nominatim
        async function getAddress(lon, lat) {
            try {
                const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lon=${lon}&lat=${lat}`);
                const data = await response.json();
                return data.display_name || 'Không tìm thấy địa chỉ';
            } catch (error) {
                console.error('Lỗi khi lấy địa chỉ:', error);
                return 'Không tìm thấy địa chỉ';
            }
        }

        document.querySelectorAll('.btn-location').forEach(button => {
            button.addEventListener('click', () => {
                console.log("Đã click vào .btn-location");
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        async (position) => {
                            const lon = position.coords.longitude;
                            const lat = position.coords.latitude;
                            updateMap(lon, lat);

                            // Thêm ký hiệu (marker) tại vị trí chính xác
                            const point = new ol.geom.Point(ol.proj.fromLonLat([lon, lat]));
                            marker.setGeometry(point);

                            // Tùy chỉnh style cho marker
                            marker.setStyle(new ol.style.Style({
                                image: new ol.style.Icon({
                                    src: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRHdFjb7tFfO1poVEbtcFJXvFsMHV2B4EwnQ&s',
                                    scale: 0.1
                                })
                            }));

                            // Lấy địa chỉ và cập nhật cả hai input
                            const address = await getAddress(lon, lat);
                            document.getElementById('map-service-input').value = address;
                            document.getElementById('email').value = address;
                        },
                        (error) => {
                            console.error('Lỗi khi lấy vị trí:', error);
                            alert('Không thể lấy vị trí. Vui lòng cho phép truy cập vị trí hoặc thử lại.');
                        }
                    );
                } else {
                    alert('Trình duyệt không hỗ trợ lấy vị trí.');
                }
            });
        });

        // Xử lý sự kiện đóng bản đồ và xóa class map-visible
        document.getElementById('close_Map').addEventListener('click', function(){
            document.getElementById('map').style.display = 'none';
            document.getElementById('close_Map').style.display = 'none';
            document.querySelectorAll('.show_Col').forEach(function(element) {
                element.style.display = 'block';
            });
            document.querySelector('.navbar').classList.remove('map-visible');
        });
