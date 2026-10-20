# 26D1DAT60900201_Group15

# Dynamic Rebate Recommendation Framework (DRRF)

**Môn:** Phân tích dữ liệu – UEH · **Nhóm 15:** Đoàn Thị Thanh Tân, Trần Hạnh Thảo, Trần Lê Minh Trung

> **Lưu ý về dữ liệu:** Bộ dữ liệu 240 nhà phân phối (NPP) xi măng trong repo là **dữ liệu mô phỏng** phục vụ mục đích học tập, không phải số liệu thật của doanh nghiệp.

---

## 1. Giới thiệu dự án

Dự án xây dựng **Dynamic Rebate Recommendation Framework (DRRF)** để hỗ trợ doanh nghiệp phân bổ lại ngân sách rebate cho hệ thống NPP dựa trên dữ liệu. Lĩnh vực áp dụng hiện tại là ngành xi măng.

Chính sách hiện tại chủ yếu phân bổ rebate theo quy mô doanh số, nên dễ gặp hai vấn đề:

- NPP lớn tiếp tục nhận rebate cao dù hiệu quả hỗ trợ tăng thêm không còn nhiều.
- NPP có biên lợi nhuận thấp, cạnh tranh cao hoặc còn tiềm năng tăng trưởng chưa được hỗ trợ tương xứng.

DRRF kết hợp phân cụm, chấm điểm đa tiêu chí và hồi quy để đề xuất mức rebate phù hợp hơn cho từng NPP.

---

## 2. Mục tiêu dự án

1. Phân tích hiện trạng phân bổ rebate và xác định các điểm bất hợp lý.
2. Phân khúc NPP theo đặc điểm kinh doanh và nhu cầu hỗ trợ.
3. Xây dựng điểm rebate dựa trên nhiều tiêu chí thay vì chỉ dựa vào doanh số.
4. Đề xuất mức rebate chính thức bằng Weighted Scoring/AHP.
5. Dùng Ridge Regression để kiểm tra tính nhất quán và hỗ trợ chấm điểm nhanh.
6. Đánh giá tác động của phương án rebate bằng dữ liệu panel và phương pháp Difference-in-Differences.
7. Kiểm soát hiệu quả tài chính, ngân sách và rủi ro thua lỗ ở cấp từng NPP.

---

## 3. Nguyên tắc mô hình

### 3.1. Tầng 1 – Phân cụm K-Means

NPP được chia thành **k = 2 cụm** (chọn theo Silhouette và Davies–Bouldin). Mỗi cụm có khung rebate Min–Max riêng.

### 3.2. Weighted Scoring/AHP – phương án rebate chính thức

Trọng số 7 tiêu chí được tổng hợp từ ma trận so sánh cặp (thang Saaty 1–9) của 3 người đánh giá, gộp bằng trung bình nhân:

| Tiêu chí | Trọng số |
|---|---|
| Profitability Gap | 0,310 |
| Tiềm năng tăng trưởng | 0,176 |
| Cường độ cạnh tranh | 0,162 |
| Share of Wallet | 0,162 |
| Quy mô doanh số | 0,092 |
| Price Index | 0,050 |
| Tỷ lệ công nợ quá hạn | 0,050 |

Chỉ số nhất quán: λmax = 7,022; CR = 0,0028 (< 0,10). Điểm rebate tổng hợp được quy đổi thành VNĐ/tấn trong khung Min–Max của từng cụm.

### 3.3. Ridge Regression – kiểm tra nhất quán

Ridge **không** tự động quyết định mức rebate cuối cùng. Vai trò của Ridge:

- Kiểm tra tính nhất quán với rebate AHP.
- Phát hiện NPP có chênh lệch bất thường giữa AHP và kết quả hồi quy.
- Hỗ trợ chấm điểm nhanh khi dữ liệu được cập nhật ở các kỳ sau.
- Hỗ trợ phân tích kịch bản và kiểm tra độ ổn định của quy tắc phân bổ.

**Thiết kế kiểm định:** chia 80/20 (huấn luyện/kiểm tra). Trên tập huấn luyện dùng Repeated Stratified 5-fold CV (lặp 10 lần) để tinh chỉnh và so sánh Ridge, Random Forest, Gradient Boosting. Chọn mô hình theo quy tắc one-SE. Notebook đối chứng chia 60/20/20 lặp 200 seed cho thấy chia một lần làm kết quả dao động mạnh, nên nhóm dùng CV.

### 3.4. Quy trình đề xuất

```text
Dữ liệu NPP
→ Phân cụm K-Means (k = 2)
→ Chấm điểm Weighted Scoring/AHP
→ Đề xuất rebate AHP
→ Ridge kiểm tra tính nhất quán
→ Sales và Finance rà soát
→ Phê duyệt rebate cuối cùng
```

---

## 4. Kết quả chính

| Chỉ tiêu | Kết quả |
|---|---|
| Ridge – RMSE CV (5×10) | 2.859 ± 229 VNĐ/tấn (R² CV = 0,937) |
| Ridge – tập kiểm tra | RMSE 3.080 (CI 95%: 2.002–4.254); MAE 2.072; R² 0,915 |
| Tương quan Ridge – AHP | r = 0,971 |
| Tổng ngân sách | AHP 283,00 tỷ; Ridge 283,06 tỷ; giảm 7,16% so với hiện tại |

Theo tiêu chí đã đặt trước, Ridge chưa đủ điều kiện thay thế AHP. Vì vậy **phương án chính thức là rebate AHP**, còn Ridge dùng để kiểm tra chéo.

---

## 5. Cấu trúc thư mục

```text
.
├── eda_stats_chart/                       # Biểu đồ EDA và thống kê mô tả
├── figures_chuong5/                       # Hình 5.1–5.6 trong báo cáo (Chương 5)
├── outputs_Q3_2026/                       # Kết quả đánh giá giả lập Q3/2026
├── 06_eda_thong_ke_mo_ta.ipynb            # Phân tích khám phá dữ liệu, thống kê mô tả
├── DRRF_Muc5_Colab.ipynb                  # Notebook chính: phân cụm, AHP, 3 mô hình ML, ngân sách
├── DRRF_Muc5_DoiChung_60_20_20.ipynb      # Đối chứng: chia 60/20/20 lặp 200 seed so với 80/20 + CV
├── DRRF_Q3_2026_Danh gia hieu qua mo hinh.ipynb   # Đánh giá hiệu quả phương án rebate AHP trong Q3/2026
├── DRRF_Q3_2026_full_KPI_simulated_monthly_AHP.csv  # Dữ liệu panel giả lập theo tháng dùng để đánh giá
├── dataset_cement_cust.xlsx               # Dữ liệu đầu vào: 240 NPP × 21 cột (mô phỏng)
├── rebate_recommendation_output_need.csv  # Kết quả đề xuất rebate cấp NPP
└── README.md
```

---

## 6. Cách chạy lại

**Môi trường:** Python 3.10+ với `pandas`, `numpy`, `scikit-learn`, `scipy`, `matplotlib`, `openpyxl`.

```bash
pip install pandas numpy scikit-learn scipy matplotlib openpyxl
```

**Thứ tự chạy:**

1. `06_eda_thong_ke_mo_ta.ipynb`: EDA.
2. `DRRF_Muc5_Colab.ipynb`: chạy `Run all`. Để `dataset_cement_cust.xlsx` cùng thư mục với notebook; trên Google Colab, notebook sẽ yêu cầu tải file lên. Mất khoảng 5–8 phút. `random_state = 42` nên kết quả trùng với báo cáo. Notebook lưu 6 hình vào thư mục `hinh_anh_muc5_need/`; trên repo, thư mục này đã được đổi tên thành `figures_chuong5/`.
3. `DRRF_Muc5_DoiChung_60_20_20.ipynb`: kiểm tra đối chứng cách chia dữ liệu.
4. `DRRF_Q3_2026_Danh gia hieu qua mo hinh.ipynb`: đánh giá hiệu quả trên dữ liệu panel Q3/2026.
