# Cập nhật bộ lọc LI theo giao diện Aging

Áp dụng cho đúng project LI_APP_Without_CLI(1).zip đã gửi.

## Cài đặt
1. Đóng ứng dụng LI.
2. Giải nén gói này, chép các thư mục controllers, repositories, services, ui, workers và tests vào thư mục LI_APP đang dùng. Đồng ý ghi đè các file trùng tên; giữ các file khác.
3. Chép read.md và change log.txt vào gốc project nếu muốn lưu hướng dẫn.
4. Chạy main.py như trước. Không cần tạo lại hoặc xóa database, không thêm thư viện.

## File chỉnh sửa
- controllers/prime_controller.py: điều phối nạp lựa chọn bằng worker sau khởi tạo database và sau PRIME/CUM; dùng cùng vòng đời worker để không chồng tác vụ và đóng cửa sổ an toàn.
- ui/pages/prime_page.py: gắn bộ lọc Aging vào trang LI, nối hai nút import hiện có, lưu và phát điều kiện SEARCH. Có vùng cuộn khi cửa sổ nhỏ.
- tests/test_gui.py: cập nhật kiểm thử giao diện từ hai nút sang bộ lọc mới.

## File thêm
- ui/widgets/__init__.py
- ui/widgets/filter_panel.py: giao diện và hành vi bộ lọc lấy từ Aging, đổi Chamber thành SLOT, hiển thị cả hai nút import.
- repositories/filter_option_repository.py: truy vấn các giá trị phân biệt, không ghi dữ liệu.
- workers/filter_option_worker.py: nạp lựa chọn ngoài luồng giao diện.
- services/scrap_code_config.py: danh sách mã ưu tiên giống Aging.
- tests/test_filters.py: kiểm thử nguồn lựa chọn và thao tác bộ lọc.

## Quy tắc lựa chọn
| Trường | Nguồn / hành vi |
| --- | --- |
| From, To | Mặc định hôm nay, lịch popup, hiển thị yyyy-MM-dd; tự điều chỉnh để From không vượt To; điều kiện xuất ra yyyyMMdd. |
| EQP | DISTINCT EQP trong prime_data; chưa chọn nghĩa là không giới hạn máy. |
| SLOT | DISTINCT SLOT trong prime_data, sắp theo số; chưa chọn nghĩa là không giới hạn slot. Không sinh cứng danh sách 1–48. |
| Tier | TIER khác NULL từ prime_data và cum_data, giống Aging; checkbox và Select All, mặc định chọn tất cả. |
| Model | MODEL từ prime_data, giống Aging; checkbox và Select All, mặc định chọn tất cả. |
| Scrap Code | Mã 4 chữ số từ prime_data.SCRAPCODE và cum_scrap_detail.scrap_code; checkbox, Select All, mặc định chưa chọn. Mã 3212, 3308, 3329, 3346, 3382 được ưu tiên và tô đỏ khi có trong dữ liệu. |

Danh sách là toàn bộ lựa chọn hiện có, không phụ thuộc khoảng ngày hoặc EQP đang chọn, giống bộ lọc Aging. Sau import, danh sách được đọc lại và lựa chọn trở về mặc định giống Aging. Ngày From/To được giữ nguyên.

Tier NULL không xuất hiện trong danh sách, giống Aging. Nếu PRIME chưa được ghép Tier từ CUM, danh sách Tier có thể trống. Bản này không thay đổi cách tính Tier.

## Phạm vi SEARCH và bước phát triển tiếp
Project LI đầu vào mới có chức năng import, chưa có bảng Summary/Yield Slot hoặc biểu đồ. Bản cập nhật này hoàn thành giao diện, nạp lựa chọn thật từ database, kiểm soát lựa chọn và phát điều kiện khi bấm SEARCH; chưa tạo các màn hình phân tích hoặc truy vấn kết quả cho chúng.

SEARCH lưu FilterCriteria tại prime_page.current_criteria và phát prime_page.filter_applied(criteria). Các trường là date_from, date_to, selected_date=None, eqp, slot, tiers, models, scrap_codes. Dòng dưới bộ lọc xác nhận điều kiện vừa chọn; không phải thống kê kết quả trong database.

Giữ ý nghĩa Scrap Code của Aging: chọn chuỗi lỗi cho biểu đồ, không dùng để loại các dòng PASS khỏi mẫu số tính Yield. Khi nối màn hình phân tích ở bước sau, áp dụng From/To/EQP/SLOT/Tier/Model vào truy vấn; Tier hoặc Model bỏ chọn hết phải cho kết quả rỗng như Aging. Không nối vào dữ liệu alarm hoặc thay đổi thuật toán Yield trong bản này.

## Nạp dữ liệu và hiệu năng
Dùng một connection riêng và một read transaction trong worker để lấy snapshot nhất quán. Chỉ đọc danh sách lúc khởi tạo xong và sau import; không truy vấn database khi tick từng checkbox. Bản này dùng DISTINCT trực tiếp, chưa bổ sung bảng cache/migration như Aging. Database lớn có thể mất thời gian nạp nhưng UI không bị chặn bởi truy vấn.

## Kiểm tra
Đã chạy 7 kiểm thử bằng PyQt5 ở chế độ offscreen trên Linux: nguồn lựa chọn PRIME/CUM, lọc mã lỗi đúng 4 chữ số, không sửa dữ liệu khi đọc, ngày From/To, Select All và điều kiện SEARCH, startup, import/reimport, hủy lựa chọn, đóng cửa sổ. Đã mở và kiểm tra ảnh giao diện 1366×768. Chưa chạy trực tiếp trên Windows hoặc database sản xuất của bạn.

Chạy lại: python -m unittest discover -s tests -v


---

# [2026-09-13 22:24:28] CẬP NHẬT — CUM YIELD LI SUMMARY

Thời gian ghi: giờ Việt Nam (UTC+7). Áp dụng cho LI_APP(6).zip.
Nội dung phía trên là lịch sử được giữ nguyên. Phần cập nhật này thay thế mô tả cũ rằng SEARCH chưa có bảng/biểu đồ; riêng CUM Summary áp dụng phạm vi lọc dưới đây.

## [2026-09-13 22:24:28] Cài đặt

1. Đóng LI App.
2. Giải nén gói LI_APP_Summary_patch.zip và chép toàn bộ nội dung bên trong vào thư mục LI_APP có main.py; đồng ý ghi đè các file trùng tên.
3. Trong môi trường Python đang chạy LI, thực hiện `python -m pip install -r requirements.txt` để bổ sung Matplotlib.
4. Chạy `python main.py`, chọn From/To, Tier và Model rồi bấm SEARCH.
5. Không xóa hoặc tạo lại database. Gói chỉ chứa file thêm/sửa, không chứa database hay toàn bộ project.

File nhật ký mới có tên `changelog.txt` theo yêu cầu lần này. Toàn bộ lịch sử trong `change log.txt` cũ đã được chép nguyên vẹn vào đầu file này rồi nối thêm lần cập nhật mới. Từ lần này tiếp tục nối vào `changelog.txt`; file `change log.txt` cũ có thể lưu làm bản lịch sử, không cần dùng để ghi tiếp. Không tự đặt ngày giờ cho các mục cũ vì file nguồn không có thông tin đó.

## [2026-09-13 22:24:28] Giao diện và tính dữ liệu

- Tab Summary có tiêu đề Cum Yield LI Summary, bảng bên trái và biểu đồ bên phải.
- Bảng gồm EQPID, In Qty, Out Qty, Fail Qty, Fail PPM, Yield; dòng Total in đậm nền xám, tiêu đề cột xanh nhạt như Aging.
- Nguồn là cum_data, GROUP BY EQPID, ORDER BY EQPID.
- In Qty = SUM(INQTY); Out Qty = SUM(OUTQTY); Fail Qty = In Qty − Out Qty.
- Fail PPM = Fail Qty / In Qty × 1.000.000; Yield = Out Qty / In Qty × 100.
- Không dùng cột FAILQTY/YIELD đã lưu để tính Summary. Total tính lại tỷ lệ từ tổng In/Out, không lấy trung bình tỷ lệ từng máy.
- In Qty <= 0: bảng hiện dấu — cho PPM/Yield. Biểu đồ giữ cách xử lý Aging: giá trị không có tỷ lệ được vẽ bằng 0.
- Bảng hiển thị PPM không có số lẻ, Yield hai chữ số thập phân; biểu đồ dùng số liệu chưa làm tròn.
- Không có dữ liệu: bảng chỉ còn Total với Qty = 0, tỷ lệ = —; biểu đồ hiện thông báo rỗng, xóa cột/đường/chú thích cũ.
- Biểu đồ giữ mã vẽ của Aging: cột Fail PPM vàng, đường Yield xanh, hai trục Y, nhãn Yield, lưới và chú thích. Đổi tiêu đề Aging thành LI. Giữ kích thước 1300 × 536 của Aging; vùng Summary có thanh cuộn cho màn hình nhỏ.

## [2026-09-13 22:24:28] Quy tắc bộ lọc

| Trường | Tác động tới CUM Summary |
| --- | --- |
| From, To | DATE BETWEEN From AND To, gồm cả hai ngày đầu/cuối. |
| Tier | Chỉ lấy các TIER được chọn. Bỏ chọn hết: dữ liệu rỗng. |
| Model | Chỉ lấy các MODEL được chọn. Bỏ chọn hết: dữ liệu rỗng. |
| EQP, SLOT | Không giới hạn khối Summary toàn bộ máy, theo cách triển khai Aging. |
| Scrap Code | Không lọc Summary và không thay đổi mẫu số Yield, theo Aging. |

Nguồn lựa chọn Model vẫn là prime_data như bộ lọc hiện tại/Aging. Model chỉ có trong CUM mà chưa có trong PRIME chưa xuất hiện trong danh sách chọn; không thay đổi nguồn lựa chọn ở lần này.

## [2026-09-13 22:24:28] Tổ chức và hiệu năng

Luồng: SEARCH → PrimeController → SummaryWorker → SummaryRepository → cum_data → SummaryPage/CumEqpChart.
Repository chỉ đọc dữ liệu, tính tỷ lệ theo Aging. Worker mở/đóng kết nối trong luồng của nó. Controller dùng chung cơ chế điều phối tác vụ hiện có để không chạy chồng import và Summary; UI chỉ dựng bảng/biểu đồ trên luồng chính.

Chỉ truy vấn sau SEARCH; Matplotlib được nạp và chart được tạo ở SEARCH đầu tiên. Khi From/To/Tier/Model không đổi, giữ kết quả đã hiển thị, không query/vẽ lại. Đổi riêng EQP/SLOT/Scrap Code không làm mất cache Summary. Sau luồng import/khởi tạo và nạp lại bộ lọc, xóa cache và kết quả cũ; bấm SEARCH để lấy dữ liệu mới. Khi lỗi đọc/vẽ, hiện thông báo và cho phép thử lại. Khi đóng cửa sổ đang đọc, đợi worker kết thúc trước khi đóng.

## [2026-09-13 22:24:28] Danh sách file

File sửa:
- controllers/prime_controller.py: điều phối SEARCH, cache, lỗi và vòng đời worker.
- ui/pages/prime_page.py: bổ sung QTabWidget và trang Summary.
- requirements.txt: thêm Matplotlib.
- read.md: giữ nội dung cũ và nối hướng dẫn lần này.

File thêm:
- domain/summary.py: kiểu dữ liệu dòng/tổng Summary.
- repositories/data_filter.py: quy tắc Tier/Model lấy từ Aging.
- repositories/summary_repository.py: SQL tổng hợp và công thức.
- workers/summary_worker.py: đọc Summary bằng worker.
- ui/pages/summary_page.py: bảng và vùng biểu đồ.
- ui/charts/__init__.py, ui/charts/cum_eqp_chart.py: biểu đồ lấy từ Aging.
- tests/test_summary.py: kiểm thử tính toán và luồng Summary.
- changelog.txt: toàn bộ lịch sử cũ và mục mới có ngày giờ.

## [2026-09-13 22:24:28] Kiểm tra

Đã chạy 9 kiểm thử thành công: 7 kiểm thử hiện có và 2 kiểm thử Summary. Kiểm tra cộng gộp nhiều ngày, Total có trọng số, bỏ qua FAILQTY/YIELD lưu sẵn, lọc ngày/Tier/Model, In = 0, lựa chọn rỗng, số liệu bảng/biểu đồ, cache, làm mới sau luồng nạp bộ lọc, lỗi truy vấn và thử lại, xóa biểu đồ cũ, đóng cửa sổ khi worker chạy. Đã xem ảnh giao diện với dữ liệu giả lập ở 1920 × 900. Chưa chạy trực tiếp trên Windows hoặc dữ liệu sản xuất.

Chạy lại: `python -m unittest discover -s tests -v` tại gốc LI_APP.


---

# [2026-09-13 22:48:31] SỬA BỘ LỌC MODEL BỎ SÓT CUM (UTC+7)

Nguyên nhân: danh sách Model trước đây chỉ lấy từ prime_data, trong khi Summary truy vấn cum_data theo các Model đã chọn. Vì vậy Select All chỉ chọn các Model đang xuất hiện trong danh sách; các Model chỉ có ở CUM bị loại khỏi kết quả. Trong dữ liệu và ảnh đã gửi, Model đang chọn khác MZWL6/MZWLR của các dòng CUM.

Thay đổi: lấy hợp danh sách MODEL của prime_data và cum_data bằng UNION, loại trùng và sắp xếp. Nội dung này thay thế quy tắc nguồn Model chỉ từ PRIME trong các phần lịch sử phía trên. Giữ nguyên công thức CUM Summary và quy tắc bỏ chọn hết Model thì kết quả rỗng.

Cài đặt: đóng app, giải nén LI_Model_Filter_fix.zip, chép các file vào gốc LI_Tool có main.py và đồng ý ghi đè. Mở lại app để nạp danh sách Model mới; chọn khoảng ngày chứa dữ liệu, Select All ở Tier/Model rồi bấm SEARCH. Không cần import lại dữ liệu hoặc xóa database.

File sửa: repositories/filter_option_repository.py, tests/test_filters.py, read.md, changelog.txt. Chỉ file repository ảnh hưởng hành vi chạy; file test cập nhật kiểm tra nguồn lựa chọn và xác nhận CUM vẫn được thống kê khi PRIME rỗng.

Kiểm tra: 9 kiểm thử thành công trên môi trường Linux/offscreen; có kiểm tra Model riêng của CUM xuất hiện, được chọn mặc định và trả về Summary. Chưa chạy trực tiếp trên Windows hoặc database thực tế của bạn.


---

# [2026-09-13 22:56:57] SỬA ĐÓNG APP BẰNG MỘT LẦN CLICK (UTC+7)

Nguyên nhân: khi app rảnh, closeEvent bỏ qua sự kiện ban đầu rồi phát close_requested. Controller gọi finish_close ngay, nhưng finish_close gọi self.close() trong lúc closeEvent đầu tiên vẫn đang chạy. Qt bỏ qua yêu cầu đóng lồng nhau, khiến phải bấm lần hai.

Sửa ui/main_window.py: finish_close đánh dấu được phép đóng và dùng QTimer.singleShot(0, self.close) để đóng ở lượt xử lý sự kiện tiếp theo. Không gọi close lồng trong closeEvent. Khi app rảnh chỉ cần bấm Close một lần; khi đang có worker, controller vẫn hủy import nếu có và đợi worker kết thúc rồi tự đóng, không cần bấm thêm.

Cài đặt: đóng ứng dụng, giải nén LI_Close_Once_fix.zip, chép các file vào gốc LI_Tool chứa main.py và đồng ý ghi đè. Chạy lại app. Không cần cài thêm thư viện hay thay đổi database.

File trong gói: ui/main_window.py, tests/test_gui.py, read.md, changelog.txt. Đây là bản vá tiếp theo sau bản sửa Model; không chứa lại các file của bản vá Model.

Kiểm tra: đã tái hiện lỗi trên code cũ bằng kiểm thử một lần close khi app rảnh (thất bại trước sửa); sau sửa toàn bộ 10 kiểm thử thành công, gồm một lần close khi rảnh và đóng khi worker đang chạy. Kiểm tra trên Linux/offscreen, chưa chạy trực tiếp trên Windows. Nội dung tài liệu và nhật ký các lần trước được giữ nguyên.


---

# [2026-09-13 23:23:59] CẬP NHẬT — TỐI ƯU INDEX VÀ LOADING DIALOG (UTC+7)

Áp dụng tiếp trên project LI_Tool hiện tại. Không cần xóa database cũ. Khi mở app, database schema 2 đang dùng sẽ tự bổ sung các index còn thiếu bằng `CREATE INDEX IF NOT EXISTS`.

## Đánh giá index hiện tại

Các index cũ đã phù hợp cho những phần sau:

| Index cũ | Truy vấn được hỗ trợ | Đánh giá |
| --- | --- | --- |
| `idx_prime_date` | Xóa/thay PRIME theo `DATE`; cập nhật PRIME theo ngày khi đồng bộ Tier | Phù hợp |
| `idx_prime_eqp_date` | Lấy danh sách EQP; truy vấn PRIME theo EQP/ngày về sau | Phù hợp |
| `idx_prime_slot_time` | Truy vấn PRIME theo EQP + SLOT + DATE + TIME | Phù hợp nếu truy vấn có EQP |
| `idx_cum_date` | Xóa/thay CUM theo ngày | Phù hợp |
| `idx_cum_lot_date_tier` | Đồng bộ `prime_data.TIER` từ CUM theo `LOTID` và cửa sổ ngày | Rất cần, giữ nguyên |
| `idx_cum_eqp_date` | Truy vấn CUM theo EQP/ngày về sau | Phù hợp |
| `idx_cum_scrap_code` | Lấy/lọc mã scrap từ bảng chi tiết CUM | Phù hợp |

Các điểm còn thiếu:

| Truy vấn | Vấn đề cũ | Index bổ sung |
| --- | --- | --- |
| `SELECT DISTINCT SLOT FROM prime_data ORDER BY SLOT` | `idx_prime_slot_time` bắt đầu bằng EQP nên không tối ưu cho riêng SLOT | `idx_prime_slot` |
| `MODEL` từ `prime_data` | Chưa có index dẫn đầu bằng MODEL | `idx_prime_model` |
| `TIER` + `MODEL` trên PRIME | Chưa có index ghép cho bộ lọc Tier/Model | `idx_prime_tier_model` |
| `SCRAPCODE` từ PRIME | Chưa có index riêng cho mã lỗi PRIME | `idx_prime_scrapcode` |
| `MODEL` từ `cum_data` | Chưa có index dẫn đầu bằng MODEL | `idx_cum_model` |
| Summary CUM `WHERE TIER IN (...) AND MODEL IN (...) AND DATE BETWEEN ... GROUP BY EQPID` | Chỉ có `idx_cum_date`, chưa tận dụng tốt Tier/Model | `idx_cum_tier_model_date_eqp` |

Không thêm index cho tất cả tổ hợp EQP/SLOT/Scrap Code vì hiện tại Summary chưa dùng các trường này để lọc dữ liệu. Thêm quá nhiều index sẽ làm import PRIME/CUM chậm hơn do mỗi lần ghi phải cập nhật thêm index.

## Thay đổi giao diện loading

- SEARCH dùng `LoadingDialog` giống Aging, hiển thị hộp thoại `Please Wait / Loading ...` trong khi worker Summary chạy.
- Import PRIME và Import CUM cũng dùng cùng `LoadingDialog`, thay cho `QProgressDialog` cũ.
- Bỏ chữ `(đang tải...)` trong tiêu đề `Cum Yield LI Summary`; trạng thái loading chỉ hiển thị bằng dialog.
- Vẫn chạy tác vụ bằng worker/QThread, không khóa UI bằng truy vấn trực tiếp.

## File liên quan theo từng chức năng

| Chức năng | File liên quan | Trạng thái trong lần này |
| --- | --- | --- |
| Khởi tạo database và tối ưu index | `database/schema.py` | Sửa |
| Import PRIME | `controllers/prime_controller.py`, `ui/dialogs/import_dialogs.py`, `ui/widgets/loading_dialog.py`, `workers/prime_import_worker.py`, `repositories/prime_repository.py`, `services/prime_import_service.py`, `services/prime_log_reader.py`, `domain/prime.py` | Sửa controller/dialog; thêm loading dialog |
| Import CUM | `controllers/prime_controller.py`, `ui/dialogs/import_dialogs.py`, `ui/widgets/loading_dialog.py`, `workers/cum_import_worker.py`, `repositories/cum_repository.py`, `services/cum_import_service.py`, `services/cum_excel_reader.py`, `domain/cum.py` | Sửa controller/dialog; thêm loading dialog |
| SEARCH / CUM Summary | `controllers/prime_controller.py`, `workers/summary_worker.py`, `repositories/summary_repository.py`, `repositories/data_filter.py`, `ui/pages/summary_page.py`, `ui/charts/cum_eqp_chart.py`, `domain/summary.py`, `ui/widgets/loading_dialog.py` | Sửa controller/summary page; thêm loading dialog |
| Bộ lọc From/To/EQP/SLOT/Model/Scrap/Tier | `ui/widgets/filter_panel.py`, `ui/pages/prime_page.py`, `repositories/filter_option_repository.py`, `workers/filter_option_worker.py`, `services/scrap_code_config.py` | Không đổi logic lần này |
| Đóng app một lần click | `ui/main_window.py`, `controllers/prime_controller.py` | Không đổi lần này, giữ bản vá cũ |
| Kiểm thử | `tests/test_filters.py`, `tests/test_gui.py`, `tests/test_summary.py` | Sửa `tests/test_filters.py` để kiểm tra index |
| Tài liệu bàn giao | `read.md`, `changelog.txt` | Sửa |

## File sửa / thêm trong gói lần này

File sửa:
- `database/schema.py`
- `controllers/prime_controller.py`
- `ui/dialogs/import_dialogs.py`
- `ui/pages/summary_page.py`
- `tests/test_filters.py`
- `read.md`
- `changelog.txt`

File thêm:
- `ui/widgets/loading_dialog.py`

## Kiểm tra

Đã chạy `python -m unittest discover -s tests -v`: 11 kiểm thử thành công. Bổ sung kiểm thử xác nhận các index mới được tạo khi khởi tạo database. Chưa chạy trực tiếp trên Windows hoặc database sản xuất của bạn.

# Cập nhật LI — Cum/Prime Yield Daily theo Scrap Code (PPM)

Áp dụng cho đúng bản nguồn `LI_App_v1.1-master.zip` đã gửi trong cuộc trao đổi này. Đối chiếu cách tính và hiển thị với `Aging_Tool_v1.0.21-master(8).zip`.

## Cài cập nhật

1. Đóng LI, giải nén gói cập nhật.
2. Chép các thư mục bên trong vào thư mục project chứa `main.py`, ghi đè các file trùng tên. Các file mới phải giữ đúng đường dẫn.
3. Chạy `python main.py`. Nếu đang dùng EXE, cần build lại từ mã nguồn đã cập nhật.
4. Giữ database LI schema 2 hiện tại. App tự bổ sung index còn thiếu trong worker khởi tạo sau khi cửa sổ hiển thị. Không xóa database, không import lại chỉ để dùng tính năng này.

Gói chỉ gồm file thêm/sửa và tài liệu, không phải toàn bộ project. Thư mục tests phục vụ kiểm thử, không cần gọi khi chạy app thông thường. Không bổ sung thư viện ứng dụng ngoài requirements đang có.

## Sử dụng

Chọn From/To, một EQP, Tier, Model; tick Scrap Code và bấm SEARCH. Cuộn xuống bên dưới Cum Yield LI Summary để xem lần lượt:

- Cum Yield LI Daily: bảng theo ngày và biểu đồ ngay dưới.
- Prime Yield LI Daily: bảng theo ngày và biểu đồ ngay dưới.

Giống Aging, Daily là thống kê **toàn máy EQP**, không phụ thuộc SLOT. CUM dùng `EQPID`, PRIME dùng `EQP` để khớp EQP đã chọn. Không chọn EQP thì xóa kết quả Daily cũ và nhắc chọn EQP; bảng Summary theo các máy vẫn hoạt động.

Bảng Daily hiển thị toàn bộ mã lỗi phát sinh theo EQP/Date/Tier/Model. Scrap Code được tick chỉ quyết định cột chồng trên biểu đồ, không lọc mẫu số hay thay đổi In/Pass/Fail/Yield. Không chọn Tier hoặc Model thì không có dữ liệu, đúng bộ lọc hiện tại. Không chọn mã lỗi hoặc mã chọn không phát sinh thì hiện thông báo thay biểu đồ, đúng Aging.

## Dữ liệu và công thức

| Nội dung | CUM | PRIME |
| --- | --- | --- |
| Ngày thống kê | DATE trong cum_data | DATE trong prime_data |
| In Qty | SUM(INQTY) | SUM(QTY) |
| Pass | SUM(OUTQTY) | SUM(QTY) với RESULT='PASS' |
| Fail Qty | In Qty − Pass; không lấy cột FAILQTY có sẵn | In Qty − Pass |
| Fail PPM | Fail Qty / In Qty × 1.000.000 | Cùng công thức |
| Yield | Pass / In Qty × 100 | Cùng công thức |
| Số lượng từng mã lỗi | SUM(cum_scrap_detail.qty), join bằng cum_data_id | SUM(QTY), chỉ RESULT='FAIL' và SCRAPCODE không rỗng |
| PPM từng mã lỗi | Số lượng mã lỗi / In Qty của ngày × 1.000.000 | Cùng công thức |

Có đủ mọi ngày từ From đến To, kể cả hai đầu. Ngày không có dữ liệu có In/Pass/Fail bằng 0; PPM/Yield để trống. Ô Scrap Code không phát sinh để trống. PPM làm tròn số nguyên khi hiển thị, Yield hai chữ số thập phân. Không lấy trung bình Yield hay cộng PPM giữa các ngày. Fail không có Scrap Code vẫn được tính vào Fail Qty/Fail PPM, vì vậy tổng các cột Scrap PPM không nhất thiết bằng Fail PPM.

## Bảng và biểu đồ

Tái sử dụng các phương thức bảng Daily và lớp `CumDailyStackedChart` từ Aging, đổi tên hiển thị thành LI: header xanh nhạt, dòng xen kẽ, cao dòng 24 px, các cột Date/In Qty/Pass/Fail Qty/Fail PPM/Yield rồi đến mã lỗi. Bảng co theo nội dung, cuộn theo trang Summary.

Biểu đồ giữ thiết kế Aging: rộng 1550 px, cột chồng từng mã lỗi trên trục Scrap PPM bên trái; đường Yield, marker và nhãn trên trục phần trăm bên phải; chú giải phía dưới. Màn hình hẹp sử dụng thanh cuộn ngang của trang.

## Index và tải thư viện

- Giữ `idx_cum_eqp_date(EQPID, DATE)` và `idx_prime_eqp_date(EQP, DATE)` cho tra cứu một máy theo khoảng ngày; không tạo thêm index trùng tiền tố chỉ để đổi tên.
- CUM join chi tiết tận dụng unique index sẵn có `(cum_data_id, scrap_code)`; giữ các index phục vụ Summary, filter và import.
- Thêm `idx_prime_daily_fail(EQP, DATE, TIER, MODEL, SCRAPCODE, QTY)` với điều kiện `RESULT='FAIL' AND COALESCE(SCRAPCODE, '') <> ''`. Đây là partial index dành cho truy vấn mã lỗi PRIME, nhỏ hơn index tương tự trên toàn bộ bản ghi khi PASS chiếm đa số.
- Kiểm tra EXPLAIN QUERY PLAN trên dữ liệu kiểm thử xác nhận truy vấn mã lỗi PRIME dùng index mới. Chưa đo tốc độ trên database sản xuất hoặc ổ mạng của bạn; thời gian tạo index lần đầu phụ thuộc lượng dữ liệu.
- SQL GROUP BY thực hiện trong worker; UI chỉ nhận kết quả đã tổng hợp. Summary và hai Daily dùng cùng một connection và read transaction để dữ liệu nhất quán trong một lần SEARCH. Kết thúc đọc thì đóng connection trước khi nạp thư viện vẽ.
- Cache theo From/To/Tier/Model/EQP. Đổi mã lỗi chỉ vẽ lại từ cache khi bấm SEARCH. Import/refresh xóa cache; đổi EQP hoặc các điều kiện dữ liệu sẽ truy vấn lại.
- Matplotlib và backend Qt được import trong SummaryWorker khi SEARCH lần đầu, sau khi cửa sổ đã mở. Canvas chỉ được tạo trên luồng UI. Loading dialog giữ đến khi đã gắn kết quả vào giao diện.
- Không preload thư viện nặng trong main hoặc constructor cửa sổ. Cơ chế import pandas/openpyxl khi cần import CUM được giữ nguyên. Đã kiểm tra trước show: matplotlib, numpy, pandas, openpyxl đều chưa nằm trong sys.modules.

## File liên quan theo chức năng

| Chức năng | File thêm | File sửa | File liên quan giữ nguyên |
| --- | --- | --- | --- |
| Tính Cum/Prime Daily | domain/daily_summary.py; repositories/daily_summary_repository.py | domain/summary.py; workers/summary_worker.py; repositories/summary_repository.py | repositories/data_filter.py; database/connection.py |
| Bảng Daily | ui/widgets/daily_summary_widget.py | ui/pages/summary_page.py | ui/pages/prime_page.py |
| Biểu đồ PPM/Yield | ui/charts/cum_daily_chart.py | workers/summary_worker.py; ui/pages/summary_page.py | ui/charts/cum_eqp_chart.py |
| SEARCH/cache/loading | ui/widgets/daily_summary_widget.py | controllers/prime_controller.py; workers/summary_worker.py | ui/widgets/filter_panel.py; ui/dialogs/import_dialogs.py; ui/widgets/loading_dialog.py |
| Index tự bổ sung vào DB cũ | — | database/schema.py | workers/database_init_worker.py; database/connection.py |
| Trì hoãn thư viện nặng | — | workers/summary_worker.py | main.py; workers/cum_import_worker.py; services/cum_excel_reader.py |
| Kiểm thử | tests/test_daily_summary.py; tests/test_daily_gui.py | tests/test_summary.py | tests/test_filters.py; tests/test_gui.py |

## Danh sách file trong bản vá

| Thao tác | Đường dẫn |
| --- | --- |
| Sửa | controllers/prime_controller.py |
| Sửa | database/schema.py |
| Thêm | domain/daily_summary.py |
| Sửa | domain/summary.py |
| Thêm | repositories/daily_summary_repository.py |
| Sửa | repositories/summary_repository.py |
| Thêm | tests/test_daily_gui.py |
| Thêm | tests/test_daily_summary.py |
| Sửa | tests/test_summary.py |
| Thêm | ui/charts/cum_daily_chart.py |
| Sửa | ui/pages/summary_page.py |
| Thêm | ui/widgets/daily_summary_widget.py |
| Sửa | workers/summary_worker.py |

## Kiểm chứng

Đã chạy 15 kiểm thử thành công, gồm tính CUM/PRIME, ngày rỗng, lọc dữ liệu, upgrade index không mất dữ liệu, SEARCH/cache, hai biểu đồ, đổi/bỏ EQP, import lại và đóng app. Đã render và kiểm tra hình hai khối Daily bằng Qt offscreen với dữ liệu mẫu. Chưa kiểm thử EXE trên Windows hoặc kết nối database sản xuất.

Chạy lại từ thư mục chứa main.py:

```bash
python -m unittest discover -s tests -v
```


---

## [2026-09-14 14:14:42 UTC+7] Cập nhật Prime Yield LI Daily — chỉ tính TEST_COUNT = 1

Mục này bổ sung và thay thế phạm vi lấy dữ liệu PRIME Daily mô tả ở các mục trước: chỉ các dòng có `TEST_COUNT = 1` được dùng để tính thống kê. Toàn bộ lịch sử tài liệu phía trên được giữ nguyên.

- Thêm `AND TEST_COUNT = 1` vào cả hai truy vấn của `get_prime_daily_summary`: truy vấn In/Pass và truy vấn số lỗi theo Scrap Code.
- In Qty, Pass, Fail Qty, Fail PPM, Yield và PPM từng Scrap Code đều tính trên tập bản ghi test lần 1. Biểu đồ Prime Daily dùng cùng kết quả với bảng nên áp dụng điều kiện này tự động.
- Các dòng có TEST_COUNT khác 1 không tham gia kết quả. Ngày chỉ có các dòng này vẫn hiển thị trong khoảng ngày chọn với In/Pass/Fail bằng 0, PPM/Yield để trống.
- CUM Daily, CUM Summary, cơ chế import, cache và nạp thư viện giữ nguyên. Không xóa bản ghi test lại trong database, không sửa schema/index, không cần import lại.

### File liên quan đến chức năng lần này

| Vai trò | File | Trạng thái |
| --- | --- | --- |
| Lọc TEST_COUNT trong hai truy vấn PRIME Daily | repositories/daily_summary_repository.py | Sửa |
| Nhận kết quả truy vấn và đưa lên UI | workers/summary_worker.py | Liên quan, không sửa |
| Hiển thị bảng và chuyển dữ liệu sang biểu đồ | ui/widgets/daily_summary_widget.py | Liên quan, không sửa |
| Vẽ biểu đồ Prime Daily | ui/charts/cum_daily_chart.py | Liên quan, không sửa |
| Hướng dẫn cập nhật | read.md | Nối nội dung mới vào cuối |
| Lịch sử thay đổi có ngày giờ Việt Nam | changelog.txt | Nối nội dung mới vào cuối |

Không thêm file mã nguồn. Gói bàn giao lần này chỉ gồm ba file có thay đổi: `repositories/daily_summary_repository.py`, `read.md`, `changelog.txt`.

### Áp dụng và kiểm chứng

Đóng app, chép đè ba file theo đúng đường dẫn vào project chứa `main.py`, mở lại và bấm SEARCH. Nếu sử dụng EXE thì build lại từ mã nguồn đã cập nhật.

Đã kiểm tra dữ liệu mẫu trộn TEST_COUNT 1, 2, 3, 5: các lần test lại không làm tăng In/Pass/Fail và Scrap PPM; mã lỗi chỉ xuất hiện ở lần test lại không vào kết quả; ngày chỉ có test lại trở thành ngày không có dữ liệu lần 1. Đã xác nhận CUM không đổi và không mất bản ghi database. Chưa kiểm thử EXE trên Windows.


[2026-09-14 14:37:40 UTC+7] Prime Yield by Slot — tab Yield Slot
Sử dụng và phạm vi thống kê
Chọn From/To, một EQP, Tier và Model; mở tab Yield Slot rồi bấm SEARCH.
Bảng có 48 cột slot (1–48), cuộn ngang để xem các cột còn lại; bên dưới là biểu đồ 48 cột đỏ Prime FAIL có nhãn số lượng.
Tiêu đề hiển thị khoảng ngày và EQP đã truy vấn.
Chỉ lấy `prime_data.TEST_COUNT = 1`; các lần test khác vẫn lưu trong database nhưng không tham gia thống kê.
Lọc theo `DATE BETWEEN From AND To` (bao gồm hai ngày biên), EQP, Tier và Model giống Summary/Daily.
In = SUM(QTY); PASS = SUM(QTY của RESULT='PASS'); Prime FAIL = In − PASS.
Prime Yield = PASS / In × 100; Fail PPM = Prime FAIL / In × 1.000.000.
Tính tỷ lệ từ tổng số lượng toàn khoảng ngày, không lấy trung bình tỷ lệ từng ngày.
Slot không có dữ liệu lần test đầu: In/PASS/FAIL = 0; Yield và PPM để trống.
Chưa chọn EQP: yêu cầu chọn máy, không cộng gộp nhiều máy.
Không chọn Tier hoặc Model: không trả dữ liệu, theo quy tắc bộ lọc hiện có.
SLOT và Scrap Code không thu hẹp chức năng này: luôn thống kê đủ 48 slot và toàn bộ Prime FAIL.
Yield hiển thị 2 số thập phân; PPM làm tròn để hiển thị số nguyên, biểu đồ lấy số FAIL nguyên từ cùng kết quả bảng.
Màu Yield: xanh từ 99,8%; vàng từ 95% đến dưới 99,8%; đỏ dưới 95%. Đây là màu hiển thị, không thay đổi phép tính.
Luồng chạy và tối ưu
SEARCH → controller xác định tab đang mở → worker riêng → repository SQL GROUP BY SLOT → trả tối đa 48 dòng → cập nhật bảng → vẽ biểu đồ.
Summary chỉ chạy khi đang mở Summary; Yield Slot chỉ chạy khi đang mở Yield Slot. Chuyển tab đơn thuần không query; bấm SEARCH để áp dụng bộ lọc cho tab đó.
Cache riêng mỗi tab theo From/To/Tier/Model/EQP. Search lại cùng điều kiện dùng kết quả đã hiển thị; thay riêng SLOT/Scrap Code không query Yield Slot lại.
Sau import/refresh filter, xóa cache và kết quả của cả hai tab để lần SEARCH tiếp theo lấy dữ liệu mới.
SQL chạy trên QThread với kết nối SQLite riêng; không đưa log thô lên UI, không dùng pandas cho thống kê slot.
Matplotlib chỉ import trong worker khi SEARCH sau khi cửa sổ đã mở; canvas tạo ở UI thread khi có kết quả. Khởi tạo cửa sổ không nạp matplotlib/pandas/numpy/openpyxl.
Dùng LoadingDialog hiện có, giữ đến khi cập nhật kết quả; khóa chuyển tab trong lúc worker chạy để kết quả không vẽ vào tab vừa bị ẩn. Khi lỗi, đóng loading và cho phép SEARCH lại.
Bổ sung index `idx_prime_first_slot`:
```sql
CREATE INDEX IF NOT EXISTS idx_prime_first_slot
ON prime_data(EQP, DATE, TIER, MODEL, SLOT, RESULT, QTY)
WHERE TEST_COUNT = 1;
```
EQP trước DATE phục vụ điều kiện máy bằng giá trị và khoảng ngày; các cột còn lại phục vụ lọc/tổng hợp. Partial index chỉ chứa test đầu, tránh đưa test lại vào index này.
SQLite có thể dùng bảng tạm nhỏ để GROUP BY SLOT; không ép INDEXED BY. Đã kiểm tra EXPLAIN QUERY PLAN chọn index mới trên dữ liệu kiểm thử.
Database schema 2 cũ được tự bổ sung index trong DatabaseInitWorker; database mới có sẵn index. Không xóa bảng, không yêu cầu import lại. Lần đầu mở database lớn có thể cần thêm thời gian tạo index ở worker nền.
File liên quan lần cập nhật này
Chức năng	File	Thay đổi
Cấu trúc kết quả slot	domain/slot_summary.py	Thêm
Truy vấn tổng hợp slot	repositories/slot_summary_repository.py	Thêm
Worker nền, nạp thư viện chart	workers/slot_summary_worker.py	Thêm
Bảng 48 slot và vùng biểu đồ	ui/pages/yield_slot_page.py	Thêm
Biểu đồ số lượng Prime Fail	ui/charts/slot_fail_chart.py	Thêm
Thêm tab Yield Slot	ui/pages/prime_page.py	Sửa
Search tab hiện tại, cache, loading	controllers/prime_controller.py	Sửa
Index cho database cũ/mới	database/schema.py	Sửa
Kiểm thử dữ liệu/index	tests/test_slot_summary.py	Thêm
Kiểm thử UI/cache/tab/lỗi	tests/test_slot_gui.py	Thêm
Tài liệu	read.md	Nối thêm, giữ nguyên toàn bộ nội dung cũ
Nhật ký có ngày giờ Việt Nam	changelog.txt	Nối thêm, giữ nguyên toàn bộ nội dung cũ
Giữ tên `changelog.txt` đúng theo project gốc (không tạo thêm file trùng nội dung tên `changlog.txt`).
Áp dụng
Đóng app, giải nén gói cập nhật và chép các file/thư mục vào thư mục chứa main.py, chấp nhận ghi đè file cùng tên. Không xóa database. Nếu dùng EXE, build lại sau khi cập nhật mã nguồn.
Gói chỉ chứa 12 file mới/sửa nêu trên, không chứa toàn bộ project hoặc database.
Kiểm chứng
4 kiểm thử mới đều đạt: công thức và 48 slot; loại TEST_COUNT 2/3/5; lọc ngày biên/EQP/Tier/Model; slot 48; dữ liệu rỗng; tạo lại index không đổi dữ liệu; query plan; Search không query tab ẩn; cache; reset sau refresh; lỗi truy vấn và thử lại; bảng/biểu đồ dùng cùng số FAIL.
Đã chạy kiểm thử hồi quy hiện có: có một lỗi cũ `test_ui_criteria_and_select_all` về thứ tự Scrap Code (mong 3212, thực tế 9999), tái hiện trên bản gốc chưa chỉnh sửa. Không sửa logic bộ lọc ngoài phạm vi yêu cầu.
Đã xem ảnh render Qt offscreen và kiểm tra không nạp thư viện nặng khi tạo cửa sổ. Chưa kiểm thử EXE Windows hoặc hiệu năng trên database sản xuất/ổ mạng thực tế.

[2026-09-14 17:17:24 UTC+7] Chỉnh giao diện Yield Slot và tự tải khi chuyển tab
Nội dung thay đổi
Biểu đồ Slot Fail Prime có lưới ngang/dọc màu xám nhạt và khung bốn cạnh giống phong cách biểu đồ CUM. Bỏ vạch tick bên trái và phía dưới, giữ số nhãn trục.
Giới hạn trên trục Y bằng đúng số Prime FAIL lớn nhất, không nhân thêm 1,2. Ví dụ lớn nhất bằng 1 thì trục Y dừng ở 1. Nếu toàn bộ bằng 0, dùng thang 0–1 để trục hợp lệ.
Nhãn số lượng trên đỉnh cột vẫn hiển thị kể cả khi cột chạm khung trên. Với số lượng tối đa nhỏ (0–2), thêm lưới ngang phụ để nền vẫn có các ô; nhãn số lượng trục Y vẫn là số nguyên.
Bỏ dòng “Áp dụng From/To...” phía trên bảng.
Ô góc trên In có nhãn Slot, nền xanh cùng tiêu đề bảng; cố định khi cuộn ngang.
Thu hẹp cột theo kích thước chữ thực tế, đủ cho PPM `1000000` và Yield `100.00%`; khoảng 59 px với font trong môi trường kiểm thử, tự mở rộng nếu số lượng có nhiều chữ số hơn. Không cắt giá trị hoặc giảm độ chính xác thống kê.
Chuyển tab và bộ lọc
Mục này cập nhật hành vi mô tả ở phần trước: chuyển tab sẽ tự áp dụng bộ lọc hiện tại, không cần bấm SEARCH ở tab mới.
`QTabWidget.currentChanged` → `PrimePage._on_tab_changed` → đọc `FilterPanel.get_filter_criteria()` → phát filter_applied → controller chọn worker của tab đang mở.
Đọc trực tiếp From/To, EQP, SLOT, Tier, Model và Scrap Code từ các điều khiển, bao gồm thay đổi chưa bấm SEARCH. Mỗi tab vẫn áp dụng các trường thuộc phạm vi thống kê của nó.
Chỉ query/render tab mới hiện ra; không tải đồng thời tab ẩn. Dùng cache riêng từng tab theo cơ chế đang có.
Điều kiện không đổi thì dùng cache; thay riêng Scrap Code vẫn vẽ lại Summary theo logic hiện có mà không query lại số lượng.
Tab chuyển trong lúc khởi tạo/chưa sẵn sàng không khởi chạy truy vấn. Trong lúc worker chạy vẫn khóa tab và dùng LoadingDialog hiện có.
Bấm SEARCH vẫn áp dụng bộ lọc cho tab hiện tại như trước. Thay từng điều khiển khi đang ở một tab chưa tự query ngay; query diễn ra khi SEARCH hoặc chuyển tab.
Không thay đổi SQL, index, công thức, điều kiện `TEST_COUNT = 1`, import hoặc dữ liệu database. Matplotlib vẫn chỉ nạp sau khi giao diện mở, khi lần đầu thực sự tải biểu đồ (SEARCH hoặc chuyển tab).
Các file liên quan
Chức năng	File	Trạng thái
Lưới, khung, tick và giới hạn trục Y	ui/charts/slot_fail_chart.py	Sửa
Nhãn Slot, bỏ chú thích, co cột bảng	ui/pages/yield_slot_page.py	Sửa
Tự áp dụng bộ lọc khi chuyển tab	ui/pages/prime_page.py	Sửa
Đọc bộ lọc hiện tại dùng chung với SEARCH	ui/widgets/filter_panel.py	Sửa
Kiểm thử chuyển tab, cache, bảng và chart	tests/test_slot_tab_refresh.py	Thêm
Hướng dẫn	read.md	Nối thêm
Nhật ký có ngày giờ Việt Nam	changelog.txt	Nối thêm
Controller/worker/repository/schema liên quan được giữ nguyên. Giữ tên `changelog.txt` đang có trong project, không tạo thêm file `changlog.txt` trùng nội dung.
Áp dụng và kiểm chứng
Gói cập nhật chỉ chứa 7 file mới/sửa ở trên. Đóng app, chép file theo đúng đường dẫn vào thư mục chứa main.py, chấp nhận ghi đè. Không xóa database. Nếu dùng EXE thì build lại.
Đã kiểm tra trực quan Qt offscreen: lưới/khung, Slot nền xanh, bỏ chú thích, PPM không bị cắt và nhãn trên đỉnh cột. 5 kiểm thử nhóm Slot và 2 kiểm thử Summary đều đạt, bao gồm thay ngày không SEARCH rồi chuyển tab, cả hai hướng chuyển tab, không query tab ẩn, cache và bỏ chọn EQP. Kiểm tra riêng giới hạn Y với cực đại 0/1/2/7/37 đều đạt; tạo cửa sổ không import Matplotlib. Chưa kiểm thử EXE trên Windows.

[2026-09-14 18:06:07 UTC+07:00] Daily Prime Yield by Slot
Chức năng và cách dùng
Chọn From/To, một EQP, một SLOT, Tier và Model; mở tab Yield Slot hoặc bấm SEARCH.
Khối mới nằm dưới biểu đồ Slot Fail Prime: bảng bên trái, biểu đồ bên phải (1300 × 536 px giống Cum Yield LI Summary). Trang dùng thanh cuộn chung.
Bảng gồm Day, Input, Output, Prime Fail, Prime Yield; một dòng cho từng ngày trong khoảng được chọn, cuối bảng là Total.
Input = SUM(QTY), Output = SUM(QTY của RESULT='PASS'), Prime Fail = Input - Output. Chỉ lấy TEST_COUNT = 1.
Yield ngày = Output / Input × 100. Total cộng số lượng tất cả ngày; Total Yield = tổng Output / tổng Input × 100, không trung bình Yield ngày.
Ngày không có dữ liệu: số lượng 0, Yield “—”, đường Yield ngắt tại ngày đó. Total Input=0 thì Total Yield “—”.
Biểu đồ cột đỏ Prime Fail, đường xanh Prime Yield, không vẽ Total. Có lưới/khung, bỏ vạch tick; trục Fail kết thúc đúng giá trị lớn nhất (dùng 1 nếu toàn 0). Trục Yield 0–120% theo mẫu.
Dùng ngưỡng màu Yield hiện có của Yield Slot: >=99.8% xanh, >=95% vàng, còn lại đỏ; Total nền xanh nhạt.
Chưa chọn SLOT chỉ xóa khối Daily; bảng/biểu đồ tổng hợp 48 slot vẫn hoạt động. Scrapcode không lọc mẫu số yield, giống thống kê slot hiện có.
Triển khai và tối ưu
SQL GROUP BY DATE trực tiếp trong SQLite, chỉ trả dữ liệu tổng hợp theo ngày; không tải từng bản ghi và không cần pandas.
Thêm partial index idx_prime_first_slot_daily trên (EQP, SLOT, DATE, TIER, MODEL, RESULT, QTY) WHERE TEST_COUNT = 1. Hai khóa EQP/SLOT đứng trước khoảng ngày; query plan đã xác nhận dùng index, không cần TEMP B-TREE cho GROUP BY/ORDER BY ngày.
Index tự bổ sung khi mở database hiện có; không xóa hoặc tạo lại database, không đổi schema version.
Tiếp tục dùng SlotSummaryWorker/QThread, connection riêng, dialog loading, cache tab và cơ chế làm mới sau import. SLOT được thêm vào khóa cache Yield Slot, Summary không bị ảnh hưởng.
Mỗi lần khóa cache đổi, worker tổng hợp 48 slot và (nếu chọn SLOT) query thêm thống kê ngày. Cache trùng thì không query lại.
Widget tạo nhẹ khi mở app; canvas chỉ tạo khi có kết quả, Matplotlib vẫn được nạp muộn trong worker hiện có. Bảng và biểu đồ dùng chung một kết quả.
Nhãn ngày/nhãn phần trăm được giảm mật độ khi trên 31 ngày; dữ liệu các ngày vẫn giữ đầy đủ.
File liên quan
Sửa domain/slot_summary.py: DTO cho dòng ngày và Total, kết quả Daily tùy chọn.
Sửa repositories/slot_summary_repository.py: query ngày và tính tổng có trọng số.
Sửa database/schema.py: bổ sung index cho DB mới và hiện có.
Sửa controllers/prime_controller.py: khóa cache có SLOT.
Sửa ui/pages/yield_slot_page.py: tích hợp khối mới dưới chart Slot Fail.
Thêm ui/widgets/slot_daily_widget.py: bảng ngày, Total, bố cục ngang và lazy canvas.
Thêm ui/charts/slot_daily_chart.py: chart Prime Fail/Prime Yield theo ngày.
Thêm tests/test_slot_daily.py; sửa tests/test_slot_gui.py: kiểm thử số liệu, index và thay đổi SLOT/cache.
Nối thêm read.md và changelog.txt, giữ nguyên toàn bộ nội dung cũ.
Kiểm tra và cài đặt
Đạt 7 kiểm thử liên quan slot: retest, ngày trống, tổng có trọng số, EQP/SLOT/Tier/Model, index DB hiện có, cache, chuyển tab, xử lý lỗi và phục hồi.
Đã kiểm tra UI Qt offscreen; chưa chạy trên Windows/database mạng thực tế.
Giải nén gói cập nhật và chép các thư mục/file vào thư mục project chứa main.py, thay thế file trùng tên; khởi động lại app. Gói chỉ chứa file thêm/sửa, không chứa database, build hoặc toàn project.

2026-09-15 09:31:00 (UTC+07:00) — Cum Yield by Model
Vị trí và sử dụng
Thêm khối Cum Yield by Model trong tab Summary, ngay dưới khối Cum Yield LI Summary và trước các bảng Daily hiện có.
Chọn bộ lọc rồi bấm SEARCH. Khi quay lại Summary, khối này tự áp dụng bộ lọc hiện tại theo cơ chế chuyển tab của project.
Bảng phía trên gồm Model, In, Out, Fail, Yield và toàn bộ scrapcode phát sinh trong dữ liệu CUM thỏa bộ lọc Date/EQP/Tier/Model. Không giới hạn bằng danh sách mã ưu tiên và không lọc bảng theo lựa chọn Scrap Code.
Dòng cuối gộp 5 ô đầu thành Total; mỗi cột scrap là tổng số lượng mã đó của tất cả Model trong bảng. Không đưa Total lên biểu đồ.
Ô scrap không phát sinh để trống. In = 0 hiển thị Yield là “—” và không vẽ điểm Yield giả bằng 0.
Bấm Copy All, Ctrl+C khi bảng có focus hoặc chuột phải → Copy All để sao chép toàn bộ header, các Model, mọi cột scrap và Total, kể cả phần đang khuất do cuộn. Clipboard là TSV, dán trực tiếp được vào Excel. Ctrl+C ở bảng này luôn copy toàn bộ bảng.
Biểu đồ nằm ngay dưới bảng: cột chồng số lượng scrap theo Model, đường Yield và nhãn phần trăm trên trục phải. Có nền gạch chéo, lưới và khung; không có vạch tick nhô ra ở trục.
Chọn một/nhiều Scrap Code rồi SEARCH: chỉ vẽ các mã được chọn. Mã được chọn nhưng không phát sinh trong kết quả có cột bằng 0. Không chọn mã nào: hiện lời nhắc chọn mã; bảng vẫn giữ đầy đủ.
Quy tắc bộ lọc
Bộ lọc	Bảng Cum theo Model	Biểu đồ bên dưới
From / To	Có, bao gồm cả hai ngày	Dùng cùng kết quả
EQP	Có; bỏ chọn EQP thì tổng hợp tất cả máy	Dùng cùng kết quả
Tier / Model	Có; không chọn Tier hoặc Model thì không trả dữ liệu	Dùng cùng kết quả
SLOT	Không áp dụng: cum_data không có cột SLOT	Không áp dụng
Scrap Code	Không áp dụng	Chỉ vẽ mã được chọn
Công thức và dữ liệu nguồn
In = SUM(cum_data.INQTY), Out = SUM(cum_data.OUTQTY), GROUP BY MODEL.
Fail = In - Out, đồng nhất với các bảng CUM trước đó. Không lấy tổng FAILQTY có thể khác công thức đang dùng.
Yield = Out / In × 100 từ tổng sản lượng, không trung bình cộng YIELD của từng dòng.
Số lượng scrap = SUM(cum_scrap_detail.qty), JOIN cum_data bằng cum_data_id = id và GROUP BY MODEL, scrap_code. Đây là số lượng, không phải PPM hoặc số bản ghi.
cum_scrap_detail được importer hiện có cập nhật từ cum_data.SCRAP. Không phân tích lại chuỗi SCRAP lúc SEARCH; nếu sửa SCRAP thủ công ngoài app thì cần cập nhật detail tương ứng hoặc import lại CUM qua app.
Tổng scrap không bị ép bằng Fail: giữ nguyên số lượng từng mã nguồn, không suy diễn các mã chưa có dữ liệu.
Tối ưu kỹ thuật
Chỉ thêm 2 truy vấn tổng hợp cho khối Model: sản lượng và scrap. Không query từng Model, từng mã hoặc từng ô.
Tách truy vấn sản lượng khỏi JOIN scrap để không nhân In/Out khi một dòng CUM có nhiều mã lỗi.
Các câu SELECT dùng chung connection và transaction đọc BEGIN của SummaryWorker với các bảng Summary/Daily, giúp dữ liệu đồng nhất trong một lần tải. Worker có connection riêng, không truyền connection SQLite sang GUI.
Tái sử dụng index idx_cum_tier_model_date_eqp(TIER, MODEL, DATE, EQPID) để lọc và UNIQUE index (cum_data_id, scrap_code) để JOIN detail. EXPLAIN QUERY PLAN trên fixture xác nhận cả hai được sử dụng; không thêm index trùng, không thay schema và không cần xóa database. Tốc độ thực tế còn phụ thuộc dung lượng dữ liệu và mạng.
Cache dùng key Summary hiện có: From, To, Tier, Model, EQP. SLOT và Scrap Code không nằm trong key. Khi chỉ đổi scrapcode, vẽ lại từ kết quả đã có; không query lại, không reset bảng Model.
Import PRIME/CUM hoặc refresh bộ lọc xóa cache và kết quả Model cùng các bảng Summary. Lỗi tải không giữ số liệu/biểu đồ cũ gây nhầm lẫn.
Bảng dùng QTableView + QAbstractTableModel: không tạo QTableWidgetItem cho từng ô; một lần beginResetModel/endResetModel khi nhận kết quả mới. Chiều cao giới hạn 440px, chiều rộng giới hạn 1300px, có thanh cuộn khi vượt giới hạn. Copy All vẫn chứa toàn bộ dữ liệu.
Matplotlib chỉ import sau khi SEARCH trong worker như cơ chế trước; CumModelChart chỉ được import/tạo khi nhận kết quả. Khởi tạo MainWindow không load pandas/Matplotlib.
Tái sử dụng canvas và hai trục, xóa artist/legend cũ và draw_idle; số cột legend/chiều cao thích ứng số mã, xoay tên Model khi nhiều Model. Không áp giới hạn cố định số scrapcode được thống kê.
File liên quan trong gói cập nhật
File	Loại	Chức năng
domain/model_summary.py	Thêm	Kiểu dữ liệu Model, số lượng scrap và Total
repositories/model_summary_repository.py	Thêm	Hai truy vấn tổng hợp theo Model với bộ lọc chung
ui/widgets/model_summary_widget.py	Thêm	Bảng động, Total, Copy All và cache biểu đồ
ui/charts/cum_model_chart.py	Thêm	Biểu đồ cột chồng scrap và đường Yield
domain/summary.py	Sửa	Bổ sung cum_model vào kết quả Summary
workers/summary_worker.py	Sửa	Nạp thống kê Model trong transaction Summary hiện có
ui/pages/summary_page.py	Sửa	Gắn khối mới, nhận kết quả, reset và cập nhật scrap
tests/test_model_summary.py	Thêm	Kiểm thử dữ liệu, query plan, UI/cache/copy và chuyển tab
read.md	Nối tiếp	Hướng dẫn và mô tả kỹ thuật lần cập nhật này
changelog.txt	Nối tiếp	Nhật ký thay đổi có ngày giờ
Kiểm tra và phạm vi xác minh
4 kiểm thử mới: tổng hợp/filters/mã động; index qua EXPLAIN QUERY PLAN; SEARCH qua worker, clipboard và đổi scrap từ cache; quay lại Summary lấy ngày vừa sửa không cần SEARCH.
3 kiểm thử hồi quy Summary và Daily GUI chạy thành công cùng 4 kiểm thử mới (7/7).
Kiểm tra riêng startup: MainWindow chưa import pandas hoặc Matplotlib.
Đã dựng và xem ảnh UI bằng Qt offscreen với 8 Model/4 scrapcode theo mẫu. Đây là dữ liệu minh họa; các số sản lượng thực lấy theo database, không hardcode bảng mẫu.
Kiểm thử cũ test_slot_tab_refresh thất bại ở yêu cầu độ rộng cột <64 (thực tế 80) trên cả ZIP gốc và bản sửa; không phải lỗi phát sinh từ cập nhật Model. Giữ nguyên file/chức năng Yield Slot ngoài phạm vi yêu cầu. Luồng chuyển tab của khối Model được kiểm tra riêng và đạt.
Kiểm thử chạy trên Linux/Qt offscreen, chưa chạy EXE Windows hoặc đo tốc độ trên database mạng thực tế của người dùng.
Cài cập nhật
Đóng app, giải nén gói vào thư mục gốc LI_App_v1.3-master (cạnh main.py), chép đè các file cùng đường dẫn và thêm các file mới. Gói chỉ chứa file thêm/sửa, không có database hoặc toàn bộ project. read.md và changelog.txt đã giữ nguyên nội dung cũ và nối thêm mục này ở cuối. Mở main.py như trước; không cần cài thêm dependency so với requirements.txt hiện có và không cần tạo lại database.

2026-09-15 10:11:45 (UTC+07:00) — Chuyển Cum theo Model sang Yield Slot, sửa legend và bố cục
Mục này thay thế hướng dẫn vị trí/bố cục của Cum Yield by Model trong lần cập nhật trước.
Thay đổi sử dụng
Cum Yield by Model nằm cuối tab Yield Slot, dưới toàn bộ bảng và biểu đồ Slot Daily. Bảng Model ở trên, biểu đồ Model ngay bên dưới; không còn xuất hiện trong Summary.
Legend chỉ hiển thị scrapcode vừa được chọn vừa có số lượng > 0 trong dữ liệu CUM hiện tại. Không tạo cột/legend cho mã không phát sinh và không tạo Rectangle cho ô số lượng bằng 0.
Nếu tất cả mã đang chọn đều không phát sinh: xóa biểu đồ/legend cũ và hiện thông báo. Không chọn Scrap Code: hiện hướng dẫn chọn mã. Bảng vẫn có tất cả scrapcode và Copy All hoạt động như trước.
Biểu đồ lấy trực tiếp bảng màu CODE_COLORS của CumDailyStackedChart; màu mỗi mã theo thứ tự mã trong kết quả đầy đủ, giữ ổn định khi chỉ đổi lựa chọn scrap. Đường Yield dùng #4472C4.
Legend giống cấu hình Cum Daily LI: tối đa 15 mục/hàng (bao gồm Yield), fontsize=8, handlelength=1.8, columnspacing=1.2, nằm giữa dưới biểu đồ. Khoảng đáy tính theo số hàng legend như Daily.
Canvas 1550 × 550 px giống Cum Daily LI; tiêu đề biểu đồ không in đậm. Giữ cách tính số lượng scrap, Yield, nền và lưới của biểu đồ Model.
Khung bảng giãn hết chiều ngang khả dụng của tab, bỏ giới hạn chiều rộng 1300px. Mỗi cột co theo chữ/số thực tế cộng 14px khoảng đệm; cột scrap vừa mã lỗi hoặc số lượng Total nếu số đó dài hơn. Không kéo giãn cột scrap khi ít mã; phần ngang còn dư của khung để trống. Có cuộn ngang nếu nhiều mã; Copy All vẫn chứa mọi dòng/cột.
Bộ lọc, worker và cache
Giữ bộ lọc CUM theo From/To, Tier, Model, EQP. SLOT không áp dụng cho CUM; Scrap Code chỉ áp dụng biểu đồ.
Khi chưa chọn EQP, phần PRIME Slot phía trên yêu cầu chọn máy như trước; phần CUM Model cuối tab vẫn tổng hợp tất cả máy.
SlotSummaryWorker tải cả kết quả Slot và CUM Model; SummaryWorker không query CUM Model nữa. ModelSummaryRepository vẫn dùng hai câu tổng hợp và index sẵn có, không thay dữ liệu hoặc schema.
Cache CUM theo 5 thành phần From/To/Tier/Model/EQP. Chỉ đổi SLOT: Slot worker tái sử dụng đối tượng kết quả CUM đã có, không query lại CUM. Chỉ đổi Scrap Code: không khởi động worker/query, chỉ cập nhật biểu đồ.
Chuyển sang Yield Slot tự áp dụng các giá trị bộ lọc hiện tại; import hoặc refresh filter vẫn xóa cả cache lẫn kết quả. Giữ dialog loading và lazy import Matplotlib sau khi giao diện đã mở.
Truy vấn CUM dùng transaction đọc riêng của ModelSummaryRepository trong Slot worker; truy vấn PRIME Slot giữ cơ chế kết nối hiện có. Không thay đổi cơ chế import/ghi dữ liệu.
File chỉnh sửa
File	Nội dung
controllers/prime_controller.py	Chuyển lựa chọn Scrap Code cho Yield Slot, cache CUM khi chỉ đổi SLOT, cho phép tải CUM khi không chọn EQP
domain/slot_summary.py	Thêm cum_model vào kết quả Slot
domain/summary.py	Bỏ cum_model khỏi kết quả Summary
workers/slot_summary_worker.py	Tải hoặc tái sử dụng CUM Model cùng tác vụ Slot
workers/summary_worker.py	Bỏ truy vấn CUM Model ở Summary
ui/pages/summary_page.py	Bỏ khối Model khỏi Summary
ui/pages/yield_slot_page.py	Đặt khối Model cuối tab, nhận dữ liệu/scrap và xóa cache khi refresh
ui/widgets/model_summary_widget.py	Khung bảng toàn chiều ngang, cột gọn theo nội dung, canh trái biểu đồ
ui/charts/cum_model_chart.py	Legend thực phát sinh, màu/số mục/chiều rộng giống Daily, title không đậm
tests/test_model_summary.py	Cập nhật kiểm thử vị trí mới và thêm kiểm tra legend/cache SLOT
read.md	Nối tiếp hướng dẫn lần này
changelog.txt	Nối tiếp nhật ký có ngày giờ
Xác minh và cài đặt
8/8 kiểm thử liên quan đạt: tổng hợp/filters/index, copy/cache, chuyển tab, legend/chiều rộng/title/cache khi đổi SLOT và hồi quy Summary/Daily.
Startup được kiểm tra riêng: tạo MainWindow chưa import pandas hoặc Matplotlib.
Đã dựng và xem giao diện Qt offscreen. Chưa chạy bản EXE Windows hoặc database mạng thực tế.
Đóng app, giải nén gói cập nhật vào thư mục cạnh main.py, chép đè đúng đường dẫn. Chỉ có file sửa so với LIApp (6).zip. Không cần xóa/tạo lại database. Nội dung read.md và changelog.txt cũ được giữ nguyên phía trước mục mới này.

2026-09-15 10:54:25 (UTC+07:00) — Cum Yield by Model chỉ lọc From / To / Tier
Mục này thay thế quy tắc EQP/Model và cache của Cum Yield by Model ở các mục trước. Khối vẫn ở cuối tab Yield Slot.
Bộ lọc	Bảng Cum Yield by Model	Biểu đồ Cum Yield by Model
From / To	Có, gồm cả hai ngày	Dùng cùng dữ liệu bảng
Tier	Có; không chọn Tier thì bảng rỗng	Dùng cùng dữ liệu bảng
EQP	Không; luôn tổng hợp mọi EQP	Không
Model	Không; luôn thống kê mọi Model trong khoảng ngày/Tier, kể cả khi bỏ chọn toàn bộ Model	Không
SLOT	Không	Không
Scrap Code	Không; bảng vẫn chứa tất cả mã phát sinh	Chỉ vẽ mã được chọn có số lượng > 0
Triển khai
ModelSummaryRepository.load chỉ nhận From, To, Tier và connection tùy chọn; không nhận EQP/Model. WHERE của cả hai truy vấn chỉ có DATE BETWEEN và TIER IN, không gọi bộ lọc chung build_data_filter vốn yêu cầu Model.
Giữ nguyên SUM(INQTY), SUM(OUTQTY), Fail = In - Out, Yield = Out/In × 100; scrap lấy SUM(qty) từ cum_scrap_detail. Dòng Total và Copy All không đổi.
SlotSummaryWorker chỉ chuyển 3 giá trị From/To/Tier cho repository CUM. Phần PRIME Slot vẫn nhận đầy đủ bộ lọc cũ.
Cache CUM so sánh 3 giá trị From/To/Tier. Đổi EQP, Model hoặc SLOT chỉ làm tải lại phần Slot theo cơ chế cũ, tái sử dụng dữ liệu CUM đã có; không query lại CUM. Đổi Scrap Code vẫn chỉ vẽ lại biểu đồ.
Đổi ngày/Tier hoặc import/refresh sẽ tải lại CUM. Chuyển tab tự áp dụng bộ lọc như trước. Không thay bộ lọc hay cách tính của Summary, Daily hoặc PRIME Slot.
Thêm index idx_cum_tier_date_model(TIER, DATE, MODEL) cho database mới và database hiện có qua ensure_performance_indexes. Không đổi schema version, không xóa dữ liệu, không cần tạo lại database. Giữ index cũ vì các chức năng khác vẫn cần lọc Model.
EXPLAIN QUERY PLAN trên fixture xác nhận truy vấn sản lượng dùng index Tier/Date mới; truy vấn scrap dùng index CUM và UNIQUE index detail để JOIN. SQLite tự chọn index theo từng truy vấn, không ép INDEXED BY.
File chỉnh sửa
File	Nội dung
repositories/model_summary_repository.py	Chỉ lọc ngày và Tier, bỏ phụ thuộc EQP/Model
workers/slot_summary_worker.py	Chỉ chuyển From/To/Tier vào truy vấn CUM
controllers/prime_controller.py	Cache CUM độc lập EQP/Model/SLOT
database/schema.py	Tự bổ sung index Tier/Date/Model cho DB mới và đang dùng
tests/test_model_summary.py	Kiểm tra mọi Model/máy, cache khi đổi EQP/Model/SLOT, đổi Tier/ngày và bổ sung index không mất dữ liệu
read.md	Nối tiếp hướng dẫn này
changelog.txt	Nối tiếp nhật ký có ngày giờ
Xác minh và cài đặt
8/8 kiểm thử liên quan đạt trên Qt offscreen: tổng hợp, index, cập nhật index lặp lại trên database có dữ liệu, bộ lọc/cache, copy/legend/chuyển tab và hồi quy Summary/Daily. Chưa chạy EXE Windows hoặc database mạng thực tế.
Đóng app, giải nén gói vào thư mục cạnh main.py và chép đè đúng đường dẫn. Gói chỉ gồm file sửa so với LIApp (7).zip; không chứa database. Khi mở app, index mới được bổ sung tự động. read.md và changelog.txt giữ nguyên nội dung cũ và nối mục mới này ở cuối.


[2026-09-15 11:10:24 (UTC+07:00)] File Management giống Aging
Cài đặt bản cập nhật
Giải nén gói cập nhật vào đúng thư mục LIApp đang chứa main.py và chép đè theo đường dẫn tương đối bên dưới. Không chép vào thư mục `New folder` trong project.
Gói chỉ gồm file thêm/sửa và tài liệu nối tiếp; không chứa database hay toàn bộ project.
Không cần xóa database. App bổ sung bảng cấu hình `auto_import_scheduler` với id=1; mặc định Auto Import tắt, giờ 03:00, thư mục trống. Schema dữ liệu LI vẫn là phiên bản 2.
Không cần thêm thư viện: dùng PyQt5 và openpyxl đã có trong requirements.txt.
Hành vi và giao diện
Bố cục: Prime Data List bên trái, Cum Data List ở giữa, Auto Import Prime Log bên phải. Hai bảng cùng chiều rộng; khối cấu hình rộng 440 px, căn trên; hàng cao 30 px, nền xen kẽ và khung giống Aging.
Bộ lọc thống kê chung được ẩn ở tab này. Danh sách không phụ thuộc From/To/EQP/SLOT/Model/Tier/Scrap Code.
Mỗi DATE thực tế chỉ hiển thị một dòng, sắp xếp giảm dần; Month lấy 6 ký tự đầu DATE. Load time lấy `data_import_status.imported_at`, chuyển UTC sang giờ máy và hiển thị `yyyy-MM-dd HH:mm:ss`. Ngày cũ thiếu metadata hiện dấu —, không tự tạo thời gian giả.
Filter Month/Filter Date độc lập cho từng bảng. Date chỉ liệt kê các ngày thuộc Month đang chọn. Đổi Month mặc định chọn tất cả Date của tháng đó; các ô chọn xuất được bỏ tích khi lọc hoặc tải lại như Aging.
PRIME có Select All và checkbox từng ngày. Select All chỉ tác động các dòng đang hiển thị. CUM không có checkbox hoặc Export.
Export Prime xuất tất cả cột và tất cả dòng của ngày được tích, bao gồm TEST_COUNT khác 1 và TIER trống. Không áp dụng bộ lọc thống kê.
Export chạy QThread, đọc batch 10.000 dòng, openpyxl write-only, tối đa 1.048.575 dòng dữ liệu/sheet. Ghi file tạm rồi thay file đích sau khi hoàn tất.
Tải danh sách và Export dùng loading dialog. Tab tạo lần đầu sau khi DB sẵn sàng, không tải openpyxl khi khởi động; tải lại khi quay lại tab để thấy dữ liệu do auto import/người khác cập nhật. Đóng cửa sổ đợi worker hoàn tất, không cần bấm Close lần hai.
Dùng index DATE hiện có; metadata có khóa chính (data_type, DATE), không tạo index trùng.
Auto Import và Task Scheduler
Enable, Import Time (HH:mm), Select Folder và Save giống Aging. Save chỉ lưu cấu hình trong DB; không tự tạo Windows Task Scheduler và không tạo bộ hẹn giờ trong GUI.
`auto_import_main.py` là tác vụ chạy độc lập giống entry point của Aging, cần thiết để chạy khi GUI đã đóng. Tác vụ chỉ import ngày hôm trước sau giờ cấu hình, bỏ qua khi tắt hoặc ngày đó đã auto import thành công.
Dùng đúng PrimeImportService của LI: parser LI, staging, khóa import dùng chung, thay dữ liệu theo các ngày thực tế trong staging, đồng bộ TIER. Không dùng parser/chamber của Aging. Không thay cơ chế import thủ công.
Chỉ ghi last_import_date sau khi service thành công; khi lỗi giữ mốc cũ để lần chạy sau thử lại. Thời điểm chạy theo đồng hồ Windows. Log nối tiếp ở `log/auto_import_log.txt` cạnh project/EXE.
Cấu hình Task Scheduler trên một máy phụ trách: Program là đường dẫn đầy đủ python.exe; Arguments là `"D:\LIApp\auto_import_main.py" --database "D:\LIApp\database\li_app.db"`; Start in là `D:\LIApp`. Thay các đường dẫn ví dụ bằng đường dẫn thực tế; --database phải trỏ cùng DB mà GUI dùng.
Đặt trigger lặp mỗi 5 phút, thời hạn Indefinitely; chọn “Do not start a new instance”. Script tự kiểm tra Import Time và ngày đã hoàn thành. Tài khoản chạy task cần đọc được folder log và ghi được database. Chưa tạo task hoặc chạy thử trên máy Windows của người dùng.
Nếu không truyền --database: dùng LI_DB_PATH nếu có, nếu không dùng DATABASE_PATH trong config/paths.py. Không thêm JSON cấu hình startup.
File liên quan
File	Thao tác	Chức năng
`auto_import_main.py`	Thêm	Entry point cho Task Scheduler: đọc cấu hình, import log hôm qua, ghi log và đánh dấu thành công.
`controllers/prime_controller.py`	Sửa	Tải tab sau khởi tạo DB; làm mới sau import; đợi worker khi đóng cửa sổ.
`database/connection.py`	Sửa	Bổ sung hàm tạo kết nối cho các repository/worker; giữ timeout và PRAGMA của LI.
`database/schema.py`	Sửa	Tạo bổ sung auto_import_scheduler cho DB LI mới/cũ, giữ nguyên dữ liệu schema 2.
`repositories/auto_import_scheduler_repository.py`	Thêm	Đọc/lưu Enable, Import Time, Log Folder và last_import_date.
`repositories/database_management_repository.py`	Thêm	Danh sách DATE thực tế qua index và LEFT JOIN metadata import LI.
`services/prime_export_service.py`	Thêm	Xuất toàn bộ cột PRIME bằng fetchmany và openpyxl write-only, chia sheet.
`tests/test_file_management.py`	Thêm	Kiểm thử database cũ, export, scheduler và vòng đời GUI.
`ui/filter_value_dialog.py`	Thêm	Popup lọc tháng/ngày có Search, Select All, OK/Cancel giống Aging.
`ui/pages/file_management_page.py`	Thêm	Hai bảng ngày, lọc độc lập, chọn PRIME, export và loading dialog.
`ui/pages/prime_page.py`	Sửa	Thêm tab File Management, ẩn bộ lọc thống kê khi mở tab, lazy-create UI.
`ui/widgets/auto_import_scheduler_panel.py`	Thêm	Khối Auto Import Prime Log bên phải giống Aging.
`workers/database_management_worker.py`	Thêm	Worker tải danh sách và xuất Excel ngoài UI thread.
`read.md`	Sửa, nối tiếp	Hướng dẫn chức năng, file liên quan, cài đặt và kiểm thử.
`changelog.txt`	Sửa, nối tiếp	Lịch sử thay đổi có ngày giờ.
Kiểm thử và giới hạn xác nhận
4 kiểm thử File Management đạt: bổ sung cấu hình trên DB đã có dữ liệu và chạy lặp; danh sách/metadata; Excel chọn ngày và chia sheet vẫn giữ TEST_COUNT; scheduler tắt/thành công/lỗi/chạy lặp; tải tab, lọc/chọn, export QThread và đóng cửa sổ lúc worker đang chạy. Chạy: `python -m unittest discover -s tests -p "test_file_management.py" -v`.
5 kiểm thử GUI có sẵn đạt: import/re-import, hủy chọn, ngày, đóng một lần, đóng khi đang chạy tác vụ.
Hai kiểm tra cũ không đạt ở cả bản ZIP gốc và bản cập nhật trong môi trường Qt offscreen: số QPushButton thực tế 4 thay vì 3; chiều rộng cột Slot 80 thay vì <64. Không sửa các kiểm tra hay giao diện thống kê không liên quan.
Đã kiểm tra ảnh giao diện Qt offscreen; font/emoji thực tế có thể khác theo Windows và DPI. Chưa kiểm thử trực tiếp UNC/Task Scheduler trên máy sản xuất.

[2026-09-15 11:20:49 (UTC+07:00)] Sửa File Management ẩn bộ lọc
Bỏ logic ẩn filter_panel/filter_status và đổi lề về 0 khi mở File Management. Bộ lọc và lề 24 px được giữ như các tab khác; File Management nằm trong vùng tab bên dưới.
Nội dung cập nhật này thay thế mô tả “Bộ lọc thống kê chung được ẩn ở tab này” trong lần bàn giao trước.
Giữ nguyên truy vấn, export, cấu hình Auto Import và bộ lọc Month/Date riêng của File Management.
File sửa: `ui/pages/prime_page.py` (bố cục khi chuyển tab); `tests/test_file_management.py` (đổi kiểm tra sang yêu cầu bộ lọc vẫn hiển thị); `read.md` và `changelog.txt` (nối tiếp).
Chép đè các file theo đúng thư mục trong gói vào thư mục LIApp chứa main.py rồi mở lại app. Không cần thay đổi database.
Đã chạy 4 kiểm thử File Management thành công, gồm kiểm tra bộ lọc hiển thị khi mở tab bằng Qt offscreen.

[2026-09-15 12:47:53 (UTC+07:00)] Auto Import bỏ qua ngày chưa có file
Khi `PrimeImportService` trả đúng lỗi `Không tìm thấy file .txt trong các folder ngày được chọn`, `auto_import_main.py` ghi một dòng `SKIPPED` rồi kết thúc với mã `0`. Vì vậy Task Scheduler không còn nhận trạng thái lỗi và log không có `ERROR` hoặc `TRACEBACK` cho trường hợp này.
Không cập nhật `last_import_date` khi chưa có file. Nếu Task Scheduler chạy lặp, lần chạy sau vẫn kiểm tra lại ngày hôm trước và sẽ import khi file xuất hiện.
Chỉ trường hợp không có file được bỏ qua. Folder không truy cập được, file sai cấu trúc, file rỗng/không có sản phẩm hợp lệ, dữ liệu sai hoặc lỗi database vẫn được chuyển tới `main()` để ghi `ERROR` và `TRACEBACK` như trước.
Import PRIME thủ công không thay đổi: khi người dùng chọn ngày không có file, giao diện vẫn có thể báo không tìm thấy file để người dùng biết lựa chọn không có dữ liệu.
File sửa: `auto_import_main.py`; `tests/test_file_management.py`; `read.md`; `changelog.txt`.
Đã kiểm tra: ngày không có file trả mã `0`, ghi `SKIPPED`, giữ `last_import_date` rỗng; file `.txt` sai nội dung vẫn phát sinh `ValidationError`.

[2026-09-15 13:12:28 (UTC+07:00)] Auto Import PRIME ngày hiện tại
Cơ chế hoạt động
Thêm entry point `auto_import_today_main.py` dành riêng cho Task Scheduler. Mỗi lần được gọi, file lấy ngày hiện tại theo đồng hồ Windows và truyền ngày đó vào chính `PrimeImportService` mà nút Import PRIME đang dùng.
Cơ chế ghi đè không được viết lại riêng: service đọc và kiểm tra toàn bộ file vào SQLite staging trước; khi staging hợp lệ, `PrimeRepository.replace_from_staging()` mở transaction, xóa dữ liệu PRIME của ngày trong staging, ghi toàn bộ bản mới, đồng bộ TIER rồi commit. Nếu đọc/kiểm tra lỗi, dữ liệu đang có không bị xóa.
Không kiểm tra và không cập nhật `last_import_date`. Vì vậy Task Scheduler có thể gọi nhiều lần trong ngày và lần nào cũng thay lại dữ liệu hôm nay. File `auto_import_main.py` vẫn có thể import chốt ngày hôm qua vào ngày kế tiếp.
Dùng chung `Enable Auto Import Prime Log`, `Import Time` và `Log Folder` đã lưu tại tab File Management. Nếu Auto Import tắt hoặc chưa đến Import Time thì ghi `SKIPPED` và kết thúc bình thường.
Nếu hôm nay chưa có file `.txt`, ghi `SKIPPED`, không ghi `ERROR/TRACEBACK`, không xóa dữ liệu đang có và chờ lần chạy sau. Các lỗi truy cập folder, cấu trúc log, dữ liệu và database vẫn ghi `ERROR/TRACEBACK`.
Tất cả trạng thái INFO/SUCCESS/SKIPPED/ERROR được nối vào cùng file `log/auto_import_log.txt` mà `auto_import_main.py` đang sử dụng. Nội dung log có chữ `TODAY` để phân biệt hai tác vụ.
Dùng khóa import chung của LI. Nếu Import PRIME/CUM hoặc một auto task khác đang ghi database, tác vụ không chạy chồng lên transaction hiện tại.
Cài Task Scheduler cho Today
Program/script: đường dẫn đầy đủ tới `python.exe` đang chạy LI App.
Add arguments: `"D:\LIApp\auto_import_today_main.py" --database "D:\LIApp\database\li_app.db"`.
Start in: `D:\LIApp` (thư mục chứa `main.py` và `auto_import_today_main.py`). Thay đường dẫn ví dụ bằng đường dẫn thực tế; database phải giống `DATABASE_PATH` của GUI.
Trigger đề xuất: chạy mỗi 1 giờ trong ngày. Chọn `Do not start a new instance` cho task Today. Nên tránh đặt task Today và task Yesterday chạy đúng cùng phút vì hai tác vụ dùng chung khóa import.
Nếu đóng gói thành EXE riêng, dùng `auto_import_today_main.py` làm entry point và đặt EXE cùng thư mục ứng dụng; Task Scheduler gọi EXE với `--database` tương tự.
File bàn giao và kiểm thử
`auto_import_today_main.py`: file mới để import/ghi đè log hôm nay.
`tests/test_auto_import_today.py`: kiểm tra chạy lại thay dữ liệu và thiếu file không xóa dữ liệu cũ.
`read.md`, `changelog.txt`: nối tiếp nội dung hiện tại.
Đã chạy `python -m unittest tests.test_auto_import_today -v`: 2/2 kiểm thử đạt. Kết quả xác nhận lần chạy thứ hai xóa một bản ghi cũ, chỉ giữ bản ghi mới; `last_import_date` không đổi; ngày chưa có file trả `SKIPPED` và giữ dữ liệu cũ.

[2026-09-15 14:47:10 (UTC+07:00)] Tab Send Mail theo giao diện Aging
Phạm vi chức năng
Sender: Add/Delete, User ID và Name bắt buộc, không trùng User ID; che mật khẩu trên bảng; Enable tối đa một Sender. Đổi Enable chạy trong transaction BEGIN IMMEDIATE và có unique index bảo vệ.
Receiver / CC: Add/Delete; đổi Receiver/CC/None ngay tại bảng. Tải lại cả danh sách và bảng sau khi đổi loại để thứ tự dòng và ID xóa luôn khớp nhau.
Auto Send Mail: giữ giao diện Enable Auto Send Mail, Send Time HH:mm và Save như Aging. Chỉ lưu cấu hình SQLite; KHÔNG tạo Task Scheduler, không chạy timer gửi mail, không gửi tự động dù Enable đã được lưu.
Test Login: kiểm tra Sender đang Enable qua cùng endpoint đăng nhập của Aging. Chạy QThread, chỉ nạp requests trong worker khi bấm nút. Luôn đóng session, xử lý lỗi và dọn thread. Đóng app khi đang đăng nhập sẽ chờ worker kết thúc, không cần bấm Close lần thứ hai.
Customize Email: vẫn hiển thị tại vị trí cũ nhưng tạm vô hiệu hóa. Chưa đưa luồng tạo nội dung hoặc gửi email vào LI. Nút gửi thủ công không hiển thị như bản Aging nguồn/ảnh mẫu.
MAIL HISTORY: giữ 8 cột ID, Alarm Date, Send Time, Sender, Receiver, CC, Result, Detail. Hiển thị tối đa 500 lịch sử mới nhất; click để xem snapshot HTML và thông tin mail. Database mới chưa có mail nên bảng trống, không tạo lịch sử giả.
Tab và hộp thoại giữ bố cục, màu, kích thước cột, hàng và các điều khiển của Aging. Giữ bộ lọc chung của LI ở trên tab theo bố cục hiện tại; dữ liệu mail độc lập mọi bộ lọc thống kê.
Database và tích hợp
Khởi tạo tự bổ sung mail_sender, mail_recipient, auto_send_mail_scheduler và mail_send_history cho database mới hoặc LI schema 2 hiện tại; không cần xóa/tạo lại database.
Bổ sung schema theo savepoint để lỗi có thể rollback toàn bộ phần tạo bảng mail. Giữ schema 2 và toàn bộ dữ liệu PRIME/CUM, File Management, lịch sử cấu hình đã lưu. Chưa tạo bảng Slot Fail hay lịch sử slot đã gửi.
Tái sử dụng kết nối LI: journal_mode DELETE, busy_timeout 60 giây, kết nối riêng cho tác vụ. Giao diện tạo tab lần đầu sau khi database sẵn sàng và nạp lại khi quay về tab.
Test Login dùng URL của Aging: http://107.11.192.45/DATA/Ajax_UserLoginGet.asp. Cần chạy trong mạng nội bộ có thể truy cập hệ thống này.
Mật khẩu được lưu theo cơ chế database của Aging; ký tự che chỉ áp dụng trên giao diện.
File thêm/sửa theo chức năng
File	Loại	Vai trò
ui/pages/prime_page.py	Sửa	Thêm tab Send Mail và tín hiệu mở tab, nạp giao diện khi cần.
controllers/prime_controller.py	Sửa	Mở tab sau khi DB sẵn sàng, Search độc lập bộ lọc, chờ login khi đóng app.
database/schema.py	Sửa	Gọi bổ sung schema mail khi mở database.
database/mail_schema.py	Thêm	Bốn bảng mail và index; khởi tạo lại không ghi đè cấu hình.
ui/pages/send_mail_page.py	Thêm	Giao diện Send Mail, thao tác cấu hình, lịch sử, Test Login.
ui/mail_party_dialogs.py	Thêm	Form Add Sender và Add Receiver/CC.
ui/mail_history_dialog.py	Thêm	Xem nội dung mail và thông tin lịch sử.
ui/widgets/auto_send_mail_scheduler_panel.py	Thêm	Checkbox, giờ gửi và Save.
repositories/mail_configuration_repository.py	Thêm	Đọc/ghi Sender và người nhận; transaction và kiểm tra dữ liệu.
repositories/auto_send_mail_scheduler_repository.py	Thêm	Đọc/ghi và kiểm tra cấu hình giờ gửi.
repositories/mail_send_repository.py	Thêm	Chỉ đọc danh sách/chi tiết lịch sử; không gửi mail.
services/mail_service.py	Thêm	Chỉ đăng nhập hệ thống mail và đóng session.
workers/mail_login_worker.py	Thêm	Chạy login ngoài UI thread, trả kết quả/lỗi và tín hiệu hoàn tất.
requirements.txt	Sửa	Bổ sung requests cho Test Login.
read.md, changelog.txt	Sửa	Nối tiếp mô tả triển khai và lịch sử thay đổi.
Cách áp dụng
Đóng ứng dụng LI.
Giải nén gói và chép các file theo đúng đường dẫn tương đối vào thư mục LIApp đang chứa main.py. Chấp nhận ghi đè các file cùng tên. Gói không chứa database, không chứa toàn bộ project.
Chạy `python -m pip install -r requirements.txt` bằng môi trường Python dùng để chạy LI.
Mở lại app, vào tab Send Mail, Add Sender và Receiver/CC. Chọn một Sender Enable rồi bấm Test Login.
Customize Email và gửi mail sẽ triển khai sau khi có chức năng Slot Fail. Việc lưu Auto Send Mail hiện tại chưa làm phát sinh email.
Kiểm tra đã thực hiện
Kiểm tra cú pháp Python của project; chạy GUI Qt offscreen và kiểm tra ảnh tab Send Mail.
Tạo DB mới, mở lại nhiều lần; bổ sung bảng trên bản sao database đính kèm và đối chiếu toàn bộ dòng PRIME/CUM trước/sau không đổi.
Thêm Sender trùng bị từ chối và rollback, chỉ một Sender được Enable; thêm/xóa người nhận, đổi loại làm thay thứ tự rồi xóa vẫn đúng ID.
Lưu cấu hình và giữ nguyên khi khởi tạo lại; từ chối giờ sai; hiển thị lịch sử và đọc snapshot HTML.
Xác nhận requests chưa được nạp khi chỉ mở tab; Test Login success/failure với phản hồi mô phỏng; Customize Email vẫn khóa; đóng app một lần khi login đang chạy.
