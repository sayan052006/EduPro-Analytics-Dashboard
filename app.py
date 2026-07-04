import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Instructor Performance and Course Quality Evaluation")
st.markdown("### EduPro Analytics Dashboard")

# -----------------------------
# Load Excel File
# -----------------------------
excel_file = "EduPro Online Platform.xlsx"

teachers = pd.read_excel(excel_file, sheet_name="Teachers")
courses = pd.read_excel(excel_file, sheet_name="Courses")
transactions = pd.read_excel(excel_file, sheet_name="Transactions")
users = pd.read_excel(excel_file, sheet_name="Users")

# -----------------------------
# Merge Data
# -----------------------------
teacher_transaction = pd.merge(
    teachers,
    transactions,
    on="TeacherID",
    how="inner"
)

final_df = pd.merge(
    teacher_transaction,
    courses,
    on="CourseID",
    how="inner"
)
# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")

expertise = st.sidebar.selectbox(
    "Select Expertise",
    ["All"] + sorted(final_df["Expertise"].unique())
)

category = st.sidebar.selectbox(
    "Select Course Category",
    ["All"] + sorted(final_df["CourseCategory"].unique())
)

level = st.sidebar.selectbox(
    "Select Course Level",
    ["All"] + sorted(final_df["CourseLevel"].unique())
)

filtered_df = final_df.copy()

if expertise != "All":
    filtered_df = filtered_df[filtered_df["Expertise"] == expertise]

if category != "All":
    filtered_df = filtered_df[filtered_df["CourseCategory"] == category]

if level != "All":
    filtered_df = filtered_df[filtered_df["CourseLevel"] == level]

# -----------------------------
# KPI Calculations
# -----------------------------
total_teachers = filtered_df["TeacherID"].nunique()
total_courses = filtered_df["CourseID"].nunique()
total_users = users["UserID"].nunique()
total_transactions = filtered_df["TransactionID"].nunique()

avg_teacher_rating = round(filtered_df["TeacherRating"].mean(), 2)
avg_course_rating = round(filtered_df["CourseRating"].mean(), 2)
# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("👨‍🏫 Total Teachers", total_teachers)
col2.metric("📚 Total Courses", total_courses)
col3.metric("👨‍🎓 Total Users", total_users)

col4, col5, col6 = st.columns(3)

col4.metric("💳 Transactions", total_transactions)
col5.metric("⭐ Avg Teacher Rating", avg_teacher_rating)
col6.metric("🌟 Avg Course Rating", avg_course_rating)

st.markdown("---")

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Merged Dataset Preview")

st.dataframe(filtered_df.head())

st.markdown("---")
st.subheader("📊 Teacher Rating Distribution")

fig = px.histogram(
    filtered_df,
    x="TeacherRating",
    nbins=10,
    color="TeacherRating",
    title="Distribution of Teacher Ratings"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Experience vs Teacher Rating")

fig = px.scatter(
    filtered_df,
    x="YearsOfExperience",
    y="TeacherRating",
    color="Expertise",
    hover_name="TeacherName",
    title="Experience vs Teacher Rating"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top 10 Teachers")

top_teachers = (
    filtered_df[["TeacherName", "TeacherRating"]]
    .drop_duplicates()
    .sort_values("TeacherRating", ascending=False)
    .head(10)
)

fig = px.bar(
    top_teachers,
    x="TeacherName",
    y="TeacherRating",
    color="TeacherRating",
    title="Top 10 Teachers"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📚 Average Course Rating by Category")

category_df = (
    filtered_df.groupby("CourseCategory")["CourseRating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    category_df,
    x="CourseCategory",
    y="CourseRating",
    color="CourseCategory",
    title="Course Category Performance"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📈 Experience vs Teacher Rating")

fig = px.scatter(
    filtered_df,
    x="YearsOfExperience",
    y="TeacherRating",
    color="Expertise",
    hover_name="TeacherName",
    title="Experience vs Teacher Rating"
)

st.plotly_chart(fig, use_container_width=True, key="exp_rating")

st.markdown("---")
st.subheader("📊 Course Rating Distribution")

fig = px.histogram(
    filtered_df,
    x="CourseRating",
    nbins=10,
    color="CourseRating",
    title="Course Rating Distribution"
)

st.plotly_chart(fig, use_container_width=True, key="course_rating")

st.markdown("---")
st.subheader("👨‍🏫 Teacher Expertise Performance")

expertise_df = (
    filtered_df.groupby("Expertise")["TeacherRating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    expertise_df,
    x="Expertise",
    y="TeacherRating",
    color="TeacherRating",
    title="Average Teacher Rating by Expertise"
)

st.plotly_chart(fig, use_container_width=True, key="expertise")

st.markdown("---")
st.subheader("🎓 Course Level Analysis")

level_df = (
    filtered_df.groupby("CourseLevel")["CourseRating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    level_df,
    x="CourseLevel",
    y="CourseRating",
    color="CourseLevel",
    title="Average Course Rating by Level"
)

st.plotly_chart(fig, use_container_width=True, key="level")

st.markdown("---")
st.subheader("🏆 Teacher Leaderboard")

leaderboard = (
    filtered_df.groupby(
        ["TeacherName", "Expertise"]
    )["TeacherRating"]
    .mean()
    .reset_index()
    .sort_values("TeacherRating", ascending=False)
)

st.dataframe(leaderboard, use_container_width=True)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
