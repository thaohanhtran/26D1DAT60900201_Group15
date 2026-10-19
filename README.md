# 26D1DAT60900201_Group15

# Dynamic Rebate Recommendation Framework

## 1. Giới thiệu dự án

Dự án xây dựng **Dynamic Rebate Recommendation Framework, DRRF**, nhằm hỗ trợ doanh nghiệp phân bổ lại ngân sách rebate cho hệ thống nhà phân phối, NPP, dựa trên dữ liệu.
(Lĩnh vực áp dụng hiện tại thuộc ngành xi măng).

Chính sách hiện tại chủ yếu phân bổ rebate theo quy mô doanh số. Cách tiếp cận này có thể dẫn đến hai vấn đề:

- NPP có quy mô lớn tiếp tục nhận rebate cao dù hiệu quả hỗ trợ tăng thêm không còn nhiều.
- NPP có biên lợi nhuận thấp, cạnh tranh cao hoặc còn tiềm năng tăng trưởng chưa được hỗ trợ tương xứng.

DRRF kết hợp phân tích dữ liệu, phân cụm, chấm điểm đa tiêu chí và hồi quy để đề xuất mức rebate phù hợp hơn cho từng NPP.

---

## 2. Mục tiêu dự án

Dự án hướng đến các mục tiêu chính:

1. Phân tích hiện trạng phân bổ rebate và xác định các bất hợp lý.
2. Phân khúc NPP theo đặc điểm kinh doanh và nhu cầu hỗ trợ.
3. Xây dựng điểm rebate dựa trên nhiều tiêu chí thay vì chỉ dựa vào doanh số.
4. Đề xuất mức rebate chính thức bằng Weighted Scoring/AHP.
5. Sử dụng Ridge Regression để kiểm tra tính nhất quán và hỗ trợ chấm điểm nhanh.
6. Đánh giá tác động của phương án rebate bằng dữ liệu panel và phương pháp Difference-in-Differences.
7. Kiểm soát hiệu quả tài chính, ngân sách và rủi ro thua lỗ ở cấp từng NPP.

---

## 3. Nguyên tắc mô hình

### 3.1. Weighted Scoring/AHP

Weighted Scoring/AHP được sử dụng để tạo **phương án rebate đề xuất chính thức**.

Mức rebate AHP được xác định dựa trên các nhóm tiêu chí:

- Profitability Gap.
- Tiềm năng tăng trưởng.
- Cường độ cạnh tranh.
- Share of Wallet.
- Quy mô doanh số.
- Price Index.
- Tỷ lệ công nợ quá hạn.

Trọng số AHP giúp chuyển các tiêu chí nghiệp vụ thành một điểm rebate tổng hợp, sau đó quy đổi thành mức rebate trong khoảng Min-Max của từng cụm NPP.

### 3.2. Ridge Regression

Ridge Regression không được sử dụng để tự động quyết định mức rebate cuối cùng.

Vai trò của Ridge gồm:

- Kiểm tra tính nhất quán với rebate AHP.
- Phát hiện các NPP có chênh lệch bất thường giữa AHP và kết quả hồi quy.
- Hỗ trợ chấm điểm nhanh khi dữ liệu được cập nhật ở các kỳ tiếp theo.
- Hỗ trợ phân tích kịch bản và kiểm tra độ ổn định của quy tắc phân bổ.

Quy trình đề xuất cuối cùng:

```text
Dữ liệu NPP
→ Phân cụm K-Means
→ Chấm điểm Weighted Scoring/AHP
→ Đề xuất rebate AHP
→ Ridge kiểm tra tính nhất quán
→ Sales và Finance rà soát
→ Phê duyệt rebate cuối cùng
```

### Cấu trúc thư mục
├── eda_stats_chart/
│   └── Các biểu đồ phân tích khám phá dữ liệu và thống kê mô tả
│
├── outputs_Q3_2026/
│   └── Các file kết quả đánh giá giả lập Q3/2026
│
├── 06_eda_thong_ke_mo_ta.ipynb
│   └── Phân tích khám phá dữ liệu và thống kê mô tả
│
├── DRRF_Muc5_Colab.ipynb
│   └── Xây dựng framework, phân cụm NPP, AHP và mô hình học máy
│
├── DRRF_Q3_2026_Danh_gia_hieu_qua_mo_hinh.ipynb
│   └── Đánh giá hiệu quả phương án rebate AHP trong Q3/2026
│
├── rebate_recommendation_output_need.csv
│   └── Dữ liệu đầu ra đề xuất rebate cấp NPP
│
└── README.md
    └── Tài liệu hướng dẫn dự án
