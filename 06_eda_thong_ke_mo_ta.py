# -*- coding: utf-8 -*-
"""
06_eda_thong_ke_mo_ta.py
------------------------------------------------------------
PHÂN TÍCH THỐNG KÊ MÔ TẢ (Descriptive Statistics) + PHÁT HIỆN OUTLIER
+ TRỰC QUAN HÓA cho dataset_cement_cust.xlsx (240 NPP, 21 biến, KHÔNG có
cột nhãn mục tiêu "Rebate đề xuất" — đúng dữ liệu khách hàng cung cấp).

(Đã gộp thêm phần phân tích "nhóm cạnh tranh" và toàn bộ các CSV xuất chi
tiết từ 00_eda_business_combined.py — file 00 có thể xóa, mọi nội dung
không trùng lặp của nó đã được đưa vào đây.)

Gồm:
  1. Thống kê mô tả đầy đủ: mean, median, mode, std, min, max, range,
     skewness, kurtosis, hệ số biến thiên (CV) cho biến định lượng;
     bảng tần suất cho biến định tính (kèm xuất CSV riêng từng biến).
  2. Phát hiện outlier bằng 2 phương pháp: IQR (1.5x) và Z-score (|z|>3),
     liệt kê cụ thể NPP nào là outlier ở từng biến quan trọng (kèm xuất
     CSV chi tiết riêng từng biến).
  3. Trực quan hóa: histogram, boxplot, ma trận tương quan (kèm xuất CSV),
     scatter, so sánh nhóm Vùng miền/Loại NPP, và so sánh nhóm theo
     Cường độ cạnh tranh (bảng + biểu đồ "nghịch lý" Rebate vs Profit Gap).

Chạy: python 06_eda_thong_ke_mo_ta.py
Kết quả: các file PNG và CSV trong eda_stats_charts/, và bảng số liệu in ra
console (được dùng để đưa vào báo cáo Word).
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"
OUT_DIR = "eda_stats_charts"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_excel("dataset_cement_cust.xlsx")
print(f"Đã nạp {df.shape[0]} NPP, {df.shape[1]} biến (không có cột nhãn mục tiêu)")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
print(f"\nBiến định lượng ({len(numeric_cols)}): {numeric_cols}")
print(f"Biến định tính ({len(categorical_cols)}): {categorical_cols}")

# ==================================================================
# 1. THỐNG KÊ MÔ TẢ — BIẾN ĐỊNH LƯỢNG
# ==================================================================
print("\n" + "=" * 72)
print("1. THỐNG KÊ MÔ TẢ — BIẾN ĐỊNH LƯỢNG")
print("=" * 72)

desc_rows = []
for col in numeric_cols:
    s = df[col].dropna()
    mode_val = s.mode().iloc[0] if not s.mode().empty else np.nan
    cv = (s.std() / s.mean() * 100) if s.mean() != 0 else np.nan
    desc_rows.append({
        "Bien": col,
        "N": s.count(),
        "Mean": s.mean(),
        "Median": s.median(),
        "Mode": mode_val,
        "Std": s.std(),
        "Min": s.min(),
        "Max": s.max(),
        "Range": s.max() - s.min(),
        "Skewness": stats.skew(s),
        "Kurtosis": stats.kurtosis(s),
        "CV_pct": cv,
    })
desc_df = pd.DataFrame(desc_rows).round(2)
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)
print(desc_df.to_string(index=False))
desc_df.to_csv(f"{OUT_DIR}/descriptive_stats.csv", index=False, encoding="utf-8-sig") # => Xuất csv



# ==================================================================
# 2. THỐNG KÊ MÔ TẢ — BIẾN ĐỊNH TÍNH (bảng tần suất)
# ==================================================================
print("\n" + "=" * 72)
print("2. BẢNG TẦN SUẤT — BIẾN ĐỊNH TÍNH")
print("=" * 72)
for col in categorical_cols:
    if col == "NPP_ID":
        continue

    print(f"\n--- {col} ---")
    vc = df[col].value_counts()
    vc_pct = (df[col].value_counts(normalize=True) * 100).round(1)

    freq_df = pd.DataFrame({
        "So_luong": vc,
        "Ty_le_pct": vc_pct
    })

    print(freq_df.head(15).to_string())

    # Xuất từng bảng tần suất thành một file CSV riêng
    safe_col_name = (
        col.replace("/", "_")
           .replace("\\", "_")
           .replace(" ", "_")
    )
    freq_df.to_csv(
        f"{OUT_DIR}/frequency_{safe_col_name}.csv",
        encoding="utf-8-sig"
    )

    print(f"Đã lưu {OUT_DIR}/frequency_{safe_col_name}.csv")



# ==================================================================
# 3. PHÁT HIỆN OUTLIER — PHƯƠNG PHÁP IQR (1.5x) VÀ Z-SCORE (|z|>3)
# ==================================================================
print("\n" + "=" * 72)
print("3. PHÁT HIỆN OUTLIER")
print("=" * 72)

key_vars = ["Doanh_so_12_thang_tan", "Muc_rebate_hien_tai_VND_tan",
            "Profitability_Gap_pct", "Bien_loi_nhuan_gop_NPP_pct",
            "Ty_le_cong_no_qua_han_pct", "Price_Index", "Vong_quay_ton_kho_ngay",
            "Share_of_Wallet_pct", "So_diem_ban"]

outlier_summary = []
outlier_detail = {}
for col in key_vars:
    s = df[col]
    Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    iqr_mask = (s < lower) | (s > upper)

    z = np.abs(stats.zscore(s))
    z_mask = z > 3

    outlier_summary.append({
        "Bien": col,
        "So_outlier_IQR": iqr_mask.sum(),
        "Ty_le_IQR_pct": round(iqr_mask.sum() / len(s) * 100, 1),
        "Nguong_duoi_IQR": round(lower, 2),
        "Nguong_tren_IQR": round(upper, 2),
        "So_outlier_Zscore": z_mask.sum(),
    })
    if iqr_mask.sum() > 0:
        detail = df.loc[iqr_mask, ["NPP_ID", "Tinh_Thanh", col]].sort_values(col)
        outlier_detail[col] = detail

outlier_df = pd.DataFrame(outlier_summary)
print(outlier_df.to_string(index=False))
outlier_df.to_csv(f"{OUT_DIR}/outlier_summary.csv", index=False, encoding="utf-8-sig") # => Xuất csv

print("\n--- Chi tiết NPP là outlier (phương pháp IQR) cho từng biến ---")
for col, detail in outlier_detail.items():
    print(f"\n{col} — {len(detail)} outlier(s):")
    print(detail.to_string(index=False))

    # Xuất chi tiết outlier từng biến ra CSV riêng
    safe_col_name = col.replace("/", "_").replace("\\", "_").replace(" ", "_")
    detail.to_csv(f"{OUT_DIR}/outlier_detail_{safe_col_name}.csv", index=False, encoding="utf-8-sig")
print(f"Đã lưu chi tiết outlier từng biến vào {OUT_DIR}/outlier_detail_*.csv")

# ==================================================================
# 4. TRỰC QUAN HÓA — HISTOGRAM PHÂN PHỐI (biến chính)
# ==================================================================
hist_vars = ["Doanh_so_12_thang_tan", "Muc_rebate_hien_tai_VND_tan",
             "Profitability_Gap_pct", "Cuong_do_canh_tranh_1_5",
             "Share_of_Wallet_pct", "Ty_le_cong_no_qua_han_pct"]
fig, axes = plt.subplots(2, 3, figsize=(17, 9))
fig.suptitle("Phân phối các biến chính (Histogram + đường Mean/Median)",
             fontsize=14, fontweight="bold")
for ax, col in zip(axes.flat, hist_vars):
    s = df[col]
    sns.histplot(s, bins=25, color="#2E74B5", ax=ax, kde=True)
    ax.axvline(s.mean(), color="#C00000", linestyle="-", linewidth=1.5, label=f"Mean={s.mean():.1f}")
    ax.axvline(s.median(), color="#548235", linestyle="--", linewidth=1.5, label=f"Median={s.median():.1f}")
    ax.set_title(col, fontsize=10)
    ax.legend(fontsize=7)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/01_histograms.png", dpi=150, bbox_inches="tight")
print(f"\nĐã lưu {OUT_DIR}/01_histograms.png") # => Xuất PNG.

# ==================================================================
# 5. TRỰC QUAN HÓA — BOXPLOT PHÁT HIỆN OUTLIER
# ==================================================================
fig, axes = plt.subplots(2, 3, figsize=(17, 9))
fig.suptitle("Boxplot phát hiện Outlier (điểm ngoài râu = outlier theo IQR)",
             fontsize=14, fontweight="bold")
box_vars = ["Doanh_so_12_thang_tan", "Muc_rebate_hien_tai_VND_tan",
            "Profitability_Gap_pct", "Ty_le_cong_no_qua_han_pct",
            "Price_Index", "Vong_quay_ton_kho_ngay"]
for ax, col in zip(axes.flat, box_vars):
    sns.boxplot(y=df[col], ax=ax, color="#8FAADC",
                flierprops={"markerfacecolor": "#C00000", "markeredgecolor": "#C00000", "markersize": 6})
    ax.set_title(col, fontsize=10)
    ax.set_ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/02_boxplots.png", dpi=150, bbox_inches="tight")
print(f"Đã lưu {OUT_DIR}/02_boxplots.png")

# ==================================================================
# 6. TRỰC QUAN HÓA — MA TRẬN TƯƠNG QUAN
# ==================================================================
corr_vars = [c for c in numeric_cols]
corr_matrix = df[corr_vars].corr().round(2)
corr_matrix.to_csv(f"{OUT_DIR}/correlation_matrix.csv", encoding="utf-8-sig")  # => Xuất csv
print(f"Đã lưu {OUT_DIR}/correlation_matrix.csv")
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, square=True, linewidths=0.5, annot_kws={"size": 7},
            cbar_kws={"shrink": 0.8})
plt.title("Ma trận tương quan toàn bộ biến định lượng", fontsize=13, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/03_correlation_heatmap.png", dpi=150, bbox_inches="tight")
print(f"Đã lưu {OUT_DIR}/03_correlation_heatmap.png") # => Xuất PNG.

# ==================================================================
# 7. TRỰC QUAN HÓA — BOXPLOT SO SÁNH THEO NHÓM (Vùng miền, Loại NPP)
# ==================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(data=df, x="Vung_Mien", y="Muc_rebate_hien_tai_VND_tan",
            hue="Vung_Mien", palette=["#2E74B5", "#70AD47"], legend=False, ax=axes[0])
axes[0].set_title("Rebate hiện tại theo Vùng miền")
axes[0].set_xlabel("")

sns.boxplot(data=df, x="Loai_NPP", y="Profitability_Gap_pct",
            hue="Loai_NPP", palette=["#BF8F00", "#C00000"], legend=False, ax=axes[1])
axes[1].axhline(0, color="grey", linestyle="--", linewidth=1)
axes[1].set_title("Profitability Gap theo Loại NPP")
axes[1].set_xlabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/04_group_comparison.png", dpi=150, bbox_inches="tight")
print(f"Đã lưu {OUT_DIR}/04_group_comparison.png")

# ==================================================================
# 8. SO SÁNH NHÓM THEO CƯỜNG ĐỘ CẠNH TRANH — NGHỊCH LÝ RÌO HIỆN TẠI
# ==================================================================
print("\n" + "=" * 72)
print("8. SO SÁNH NHÓM THEO CƯỜNG ĐỘ CẠNH TRANH")
print("=" * 72)

df["Nhom_canh_tranh"] = pd.cut(
    df["Cuong_do_canh_tranh_1_5"], bins=[0, 2.5, 5],
    labels=["Cạnh tranh thấp (≤2.5)", "Cạnh tranh cao (>2.5)"]
)
group_stats = df.groupby("Nhom_canh_tranh", observed=True).agg(
    So_luong=("NPP_ID", "count"),
    Profit_Gap_TB=("Profitability_Gap_pct", "mean"),
    Rebate_hien_tai_TB=("Muc_rebate_hien_tai_VND_tan", "mean"),
).round(2)
print(group_stats.to_string())
group_stats.to_csv(f"{OUT_DIR}/business_group_stats.csv", encoding="utf-8-sig")  # => Xuất csv
print(f"Đã lưu {OUT_DIR}/business_group_stats.csv")

# Tương quan tổng hợp với Rebate hiện tại (in rõ ràng để đối chiếu với bảng trên)
corr_size = df["Doanh_so_12_thang_tan"].corr(df["Muc_rebate_hien_tai_VND_tan"])
corr_profit = df["Profitability_Gap_pct"].corr(df["Muc_rebate_hien_tai_VND_tan"])
corr_comp = df["Cuong_do_canh_tranh_1_5"].corr(df["Muc_rebate_hien_tai_VND_tan"])
print("\n--- Tương quan với Rebate hiện tại ---")
print(f"Doanh số:             {corr_size:+.3f}")
print(f"Profitability Gap:    {corr_profit:+.3f}")
print(f"Cường độ cạnh tranh:  {corr_comp:+.3f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(data=df, x="Nhom_canh_tranh", y="Profitability_Gap_pct",
            hue="Nhom_canh_tranh", palette=["#70AD47", "#C00000"], legend=False, ax=axes[0])
axes[0].axhline(0, color="grey", linestyle="--", linewidth=1)
axes[0].set_title("Profitability Gap theo nhóm cạnh tranh")
axes[0].set_xlabel("")

x = np.arange(len(group_stats))
width = 0.35
ax2 = axes[1].twinx()
bar1 = axes[1].bar(x - width/2, group_stats["Rebate_hien_tai_TB"], width,
                    label="Rebate TB (VNĐ/tấn)", color="#2E74B5")
bar2 = ax2.bar(x + width/2, group_stats["Profit_Gap_TB"], width,
               label="Profit Gap TB (%)", color="#C00000")
axes[1].set_xticks(x)
axes[1].set_xticklabels(group_stats.index, rotation=10)
axes[1].set_title("Nghịch lý: Rebate hiện tại vs Profitability Gap TB")
lines = [bar1, bar2]
axes[1].legend(lines, [l.get_label() for l in lines], loc="upper right", fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/06_nghich_ly_canh_tranh.png", dpi=150, bbox_inches="tight")
print(f"Đã lưu {OUT_DIR}/06_nghich_ly_canh_tranh.png")

# ==================================================================
# 9. SCATTER: Rebate hiện tại vs các yếu tố chính (kèm hệ số tương quan)
# ==================================================================
fig, axes = plt.subplots(1, 3, figsize=(17, 5))
pairs = [
    ("Doanh_so_12_thang_tan", "Muc_rebate_hien_tai_VND_tan", "#2E74B5"),
    ("Profitability_Gap_pct", "Muc_rebate_hien_tai_VND_tan", "#548235"),
    ("Cuong_do_canh_tranh_1_5", "Muc_rebate_hien_tai_VND_tan", "#BF8F00"),
]
for ax, (x, y, color) in zip(axes, pairs):
    r = df[x].corr(df[y])
    sns.regplot(data=df, x=x, y=y, scatter_kws={"alpha": 0.4, "s": 18, "color": color},
                line_kws={"color": "#C00000"}, ax=ax)
    ax.set_title(f"{x}\nvs Rebate hiện tại (r={r:+.3f})", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/05_scatter_rebate_drivers.png", dpi=150, bbox_inches="tight")
print(f"Đã lưu {OUT_DIR}/05_scatter_rebate_drivers.png")

print("\nHOÀN TẤT PHÂN TÍCH.")
