import streamlit as st
import urllib.parse
import json
import requests
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="WEB CHẤM BÀI",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
    }
    
    h1, h2, h3 {
        color: #2d5a2d !important;
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #45a049) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #45a049, #4CAF50) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fff8 0%, #e8f5e8 100%) !important;
        border-right: 3px solid #4CAF50 !important;
    }
    
    .analysis-card {
        background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%);
        border-left: 4px solid #4CAF50;
        padding: 20px;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);
        border: 1px solid #d4edda;
    }
    
    .problem-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        border-left: 4px solid #28a745;
        padding: 20px;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.1);
        border: 1px solid #c3e6cb;
    }
    
    .test-case-detail {
        background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
        border: 2px solid #d4edda;
        padding: 20px;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 2px solid #28a745 !important;
        border-radius: 8px !important;
        color: #155724 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border: 2px solid #dc3545 !important;
        border-radius: 8px !important;
        color: #721c24 !important;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #d4edda !important;
        border-radius: 8px !important;
        background: #f8fff8 !important;
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #d4edda !important;
        border-radius: 8px !important;
        background: #f8fff8 !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid #c3e6cb !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #45a049) !important;
        border-radius: 10px !important;
    }
    
    .stCodeBlock {
        background: #f8fff8 !important;
        border: 2px solid #d4edda !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-474836e4c7b6462d8a9a24ed964b0251")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def load_users_from_excel():
    try:
        if os.path.exists('users.xlsx'):
            df = pd.read_excel('users.xlsx', engine='openpyxl')
            return df.to_dict('records')
        else:
            st.error("❌ File users.xlsx không tồn tại!")
            return []
    except Exception as e:
        st.error(f"Lỗi đọc file users: {str(e)}")
        return []

def authenticate_user(username, password):
    users = load_users_from_excel()
    
    for user in users:
        if (user['username'] == username and 
            user['password'] == password and 
            user.get('is_active', True)):
            return user
    return None

def login_page():
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>LẬP TRÌNH VUI VẺ</h1>
        <h3>YÊU CODE</h3>
        <p style="color: #4CAF50; font-size: 16px;">code không lỗi đời không nể</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("👤 Tên đăng nhập", placeholder="Nhập username...")
                password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Nhập password...")
                submit_button = st.form_submit_button("🚀 Đăng nhập", type="primary")
                
                if submit_button:
                    if not username or not password:
                        st.error("❌ Vui lòng nhập đầy đủ thông tin!")
                        return False
                    
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.logged_in = True
                        st.success(f"✅ Đăng nhập thành công! Chào mừng {user['full_name']}")
                        st.rerun()
                    else:
                        st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng!")
                        return False
                
    
    return False

def show_statistics_page():
    st.title("📊 Thống kê hệ thống")
    
    submissions_df = pd.read_excel('submissions.xlsx', engine='openpyxl') if os.path.exists('submissions.xlsx') else pd.DataFrame()
    problems_df = pd.read_excel('problems.xlsx', engine='openpyxl')
    users_df = pd.read_excel('users.xlsx', engine='openpyxl')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Tổng bài tập", len(problems_df))
    with col2:
        st.metric("Tổng user", len(users_df))
    with col3:
        st.metric("Tổng bài làm", len(submissions_df))
    with col4:
        if len(submissions_df) > 0:
            success_rate = len(submissions_df[submissions_df['status'] == 'AC']) / len(submissions_df) * 100
            st.metric("✅ Tỷ lệ thành công", f"{success_rate:.1f}%")
        else:
            st.metric("✅ Tỷ lệ thành công", "0%")
    
    if len(submissions_df) > 0:
        st.subheader("📈")
        submissions_df['timestamp'] = pd.to_datetime(submissions_df['timestamp'])
        submissions_df['date'] = submissions_df['timestamp'].dt.date
        
        daily_submissions = submissions_df.groupby('date').size()
        st.line_chart(daily_submissions)
    
    if st.button("← Quay lại"):
        st.session_state.show_stats = False
        st.rerun()

def show_user_management_page():
    st.title("Quản lý tài khoản")
    
    users_df = pd.read_excel('users.xlsx', engine='openpyxl')
    
    st.subheader("📋 Danh sách tài khoản")
    
    display_df = users_df.copy()
    display_df['password'] = '***' 
    
    st.dataframe(display_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Admin", len(users_df[users_df['role'] == 'admin']))
    with col2:
        st.metric("👨‍🎓 học sinh", len(users_df[users_df['role'] == 'student']))
    
    if st.button("← Quay lại"):
        st.session_state.show_user_management = False
        st.rerun()

def show_leaderboard_page():
    st.title("🏆 Bảng xếp hạng học sinh")
    
    try:
        submissions_df = pd.read_excel('submissions.xlsx', engine='openpyxl') if os.path.exists('submissions.xlsx') else pd.DataFrame()
        users_df = pd.read_excel('users.xlsx', engine='openpyxl')
        problems_df = pd.read_excel('problems.xlsx', engine='openpyxl')
        
        if len(submissions_df) == 0:
            st.info("📝 Chưa có bài gửi nào để tính xếp hạng!")
            if st.button("← Quay lại"):
                st.session_state.show_leaderboard = False
                st.rerun()
            return

        successful_submissions = submissions_df[submissions_df['status'] == 'AC']
        
        student_users = users_df[users_df['role'] == 'student']
        
        leaderboard_data = []
        total_problems = len(problems_df)
        
        for _, user in student_users.iterrows():
            username = user['username']
            full_name = user['full_name']
            if len(successful_submissions) > 0 and 'username' in successful_submissions.columns: #số bài mà học sinh làm đc
                user_submissions = successful_submissions[successful_submissions['username'] == username]
                completed_count = len(user_submissions)
            else:
                # nếu không có ai làm đc
                completed_count = 0
            
            leaderboard_data.append({
                'username': username,
                'full_name': full_name,
                'completed_problems': completed_count,
                'total_problems': total_problems
            })
        
        leaderboard_data.sort(key=lambda x: x['completed_problems'], reverse=True)
        
        leaderboard_df = pd.DataFrame(leaderboard_data)
        
        # biểu đồ cột cho đơn giản chứ mấy cái khc k bic làm
        if len(leaderboard_df) > 0:
            st.subheader("📊 Biểu đồ xếp hạng")
            
            # Chuẩn bị dữ liệu cho biểu đồ
            chart_data = leaderboard_df[['full_name', 'completed_problems']].copy()
            chart_data.columns = ['Học sinh', 'Số bài hoàn thành']
            
            # Hiển thị biểu đồ cột
            st.bar_chart(chart_data.set_index('Học sinh'))
            
            # Bảng xếp hạng đơn giản
            st.subheader("🏆 Bảng xếp hạng")
            
            # Thêm cột xếp hạng
            leaderboard_df['rank'] = range(1, len(leaderboard_df) + 1)
            
            # Hiển thị bảng đơn giản
            for idx, row in leaderboard_df.iterrows():
                rank = row['rank']
                full_name = row['full_name']
                completed = row['completed_problems']
                total = row['total_problems']
                
                # Hiển thị huy chương
                if rank == 1:
                    medal = "🥇"
                elif rank == 2:
                    medal = "🥈"
                elif rank == 3:
                    medal = "🥉"
                else:
                    medal = f"#{rank}"
                
                st.markdown(f"**{medal} {full_name}** - {completed}/{total} bài tập")
            
            if len(successful_submissions) == 0 or 'username' not in successful_submissions.columns:
                st.info("ℹ️ Chưa có submissions hoặc submissions không có thông tin username.")
        else:
            st.info("📝 Chưa có dữ liệu học sinh!")
        
    except Exception as e:
        st.error(f"Lỗi khi tải ô noooo :(({str(e)}")
    
    # Quay lại
    if st.button("← Quay lại"):
        st.session_state.show_leaderboard = False
        st.rerun()

def load_problems_from_excel():
    try:
        if os.path.exists('problems.xlsx'):
            df = pd.read_excel('problems.xlsx', engine='openpyxl')
            return df.to_dict('records')
        else:
            st.error("❌ File problems.xlsx không tồn tại!")
            return []
    # except ImportError:
    #     st.error("❌ Lỗi: Thiếu thư viện openpyxl. Vui lòng cài đặt bằng lệnh: pip install openpyxl")
    #     st.info("💡 Hướng dẫn cài đặt:")
    #     st.code("pip install openpyxl")
    #     return []
    except Exception as e:
        st.error(f"Lỗi đọc file Excel: {str(e)}")
        return []

def load_test_cases(problem_id):
    try:
        if os.path.exists('testcases.xlsx'):
            df = pd.read_excel('testcases.xlsx', engine='openpyxl')
            test_cases = df[df['problem_id'] == problem_id]
            return test_cases.to_dict('records')
        else:
            st.error("❌ File testcases.xlsx không tồn tại!")
            return []
    except Exception as e:
        st.error(f"Lỗi đọc test cases: {str(e)}")
        return []

def run_all_test_cases(code, problem_id):
    test_cases = load_test_cases(problem_id)
    if not test_cases:
        return []
    
    results = []
    for test_case in test_cases:
        is_correct, actual_output = run_test_case(
            code, 
            test_case['input'], 
            test_case['expected_output']
        )
        results.append({
            'test_id': test_case['test_id'],
            'input': test_case['input'],
            'expected': test_case['expected_output'],
            'actual': actual_output,
            'is_correct': is_correct,
            'description': test_case.get('description', ''),
            'is_hidden': test_case.get('is_hidden', False)
        })
    
    return results

def run_test_case(code, input_data, expected_output):
    try:
        # tạo mt ảo
        import subprocess
        import sys
        
        temp_file = "temp_code.py"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        result = subprocess.run(
            [sys.executable, temp_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if result.returncode == 0:
            actual_output = result.stdout.strip()
            
            # phần quan trọng bị lỗi nhìu lần ở đây 
            if isinstance(expected_output, (int, float)):
                expected_output_clean = str(expected_output)
            else:
                expected_output_clean = str(expected_output).strip()
            
            # So sánh kq
            is_correct = actual_output == expected_output_clean
            
            return is_correct, actual_output
        else:
            return False, f"Lỗi: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "Timeout - Code chạy quá lâu"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"

def analyze_code_with_deepseek(code, problem_title=""):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        code_preview = code[:2000] + "..." if len(code) > 2000 else code
        
        prompt = f"""
        Phân tích code Python sau đây cho bài tập "{problem_title}":

        Code:
        {code_preview}

        Hãy đánh giá:
        1. Độ chính xác của thuật toán
        2. Hiệu quả và độ phức tạp
        3. Cách viết code và style
        4. Gợi ý cải thiện
        5. Lời động viên cho người học

        Trả lời bằng tiếng Việt một cách tự nhiên.
        """
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 800
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return content
        else:
            st.error(f"Lỗi API: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏰ Lỗi timeout - API mất quá nhiều thời gian để phản hồi.")
        return None
    except Exception as e:
        st.error(f"Lỗi kết nối API: {str(e)}")
        return None

def create_pythontutor_url(code, raw_inputs=None):
    if len(code) > 5000:
        st.warning("⚠️ Code quá dài! PythonTutor chỉ hỗ trợ code dưới 5600 bytes.")
        return None
    
    encoded_code = urllib.parse.quote(code)
    
    raw_input_json = json.dumps(raw_inputs) if raw_inputs else "[]"
    encoded_raw_input = urllib.parse.quote(raw_input_json)
    
    url = f"https://pythontutor.com/iframe-embed.html#code={encoded_code}&py=3&cumulative=true&curInstr=0&rawInputLstJSON={encoded_raw_input}"
    return url

def save_submission(problem_id, code, analysis, status, test_results, username=None):
    """Lưu submission vào Excel"""
    try:
        submission_data = {
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'problem_id': [problem_id],
            'username': [username] if username else [st.session_state.user['username']],
            'code': [code],
            'analysis': [analysis],
            'status': [status],
            'test_results': [json.dumps(test_results)]
        }
        
        df = pd.DataFrame(submission_data)
        
        if os.path.exists('submissions.xlsx'):
            existing_df = pd.read_excel('submissions.xlsx', engine='openpyxl')
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel('submissions.xlsx', index=False, engine='openpyxl')
        return True
    except ImportError:
        st.error("❌ Lỗi: Thiếu thư viện openpyxl. Vui lòng cài đặt: pip install openpyxl")
        return False
    except Exception as e:
        st.error(f"Lỗi lưu submission: {str(e)}")
        return False

def display_test_case_detail(input_data, expected_output, actual_output, is_correct):
    """Hiển thị chi tiết test case"""
    st.markdown('<div class="test-case-detail">', unsafe_allow_html=True)
    st.markdown("**🧪 Chi tiết Test Case:**")
    
    st.markdown("**📥 Input:**")
    st.code(input_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Output:**")
        st.code(expected_output)
    
    with col2:
        st.markdown("**🎯 Output:**")
        if is_correct:
            st.code(actual_output)
        else:
            st.error(actual_output)
    
    # So sánh
    if not is_correct:
        st.markdown("**🔍 So sánh:**")
        st.markdown(f"- **kết quả:** `{expected_output}`")
        st.markdown(f"- **kết quả:** `{actual_output}`")
        
        # Phân tích sự khác biệt
        expected_str = str(expected_output)
        actual_str = str(actual_output)
        
        if expected_str.isdigit() and actual_str.isdigit():
            expected_num = int(expected_str)
            actual_num = int(actual_str)
            if actual_num > expected_num:
                st.warning("⚠️ Kết quả lớn hơn - có thể có lỗi logic")
            elif actual_num < expected_num:
                st.warning("⚠️ Kết quả nhỏ hơn - có thể thiếu tính toán")
        elif expected_str != actual_str:
            st.warning("⚠️ Kết quả không khớp - kiểm tra lại logic")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # phần 9 cực k quan trokn
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'selected_problem' not in st.session_state:
        st.session_state.selected_problem = None
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'show_simulation' not in st.session_state:
        st.session_state.show_simulation = False
    if 'simulation_url' not in st.session_state:
        st.session_state.simulation_url = None
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    if 'ai_analysis_pending' not in st.session_state:
        st.session_state.ai_analysis_pending = False
    
    # p kết n
    if not st.session_state.logged_in:
        login_page()
        return
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("DEMO WEB CHẤM BÀI")
    with col2:
        st.markdown(f"**👤 {st.session_state.user['full_name']}**")
        st.markdown(f"**🎭 {st.session_state.user['role'].title()}**")
    with col3:
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    problems = load_problems_from_excel()
    
    with st.sidebar:
        st.header("🌿 DEMO WEB CHẤM BÀI")
        
        # Phân quyền theo
        user_role = st.session_state.user['role']
        
        if user_role == 'admin':
            st.success("🔧 Quyền Admin - Có thể xem tất cả")
        elif user_role == 'student':
            st.info("👨‍🎓 Quyền học sinh - Chỉ có thể làm bài")
        
        st.markdown("### 🔍 Tìm kiếm bài tập")
        search_term = st.text_input("Nhập từ khóa tìm kiếm:", placeholder="Tên bài tập, độ khó...")
        
        filtered_problems = problems
        if search_term:
            search_term = search_term.lower()
            filtered_problems = [
                p for p in problems 
                if (search_term in p['title'].lower() or 
                    search_term in p['difficulty'].lower() or
                    search_term in p['description'].lower())
            ]
        
        if search_term:
            st.info(f"🔍 Tìm thấy {len(filtered_problems)} bài tập phù hợp")
        
        st.markdown("### Danh sách bài tập")
        for problem in filtered_problems:
            if st.button(f"{problem['id']}. {problem['title']} ({problem['difficulty']})"):
                st.session_state.selected_problem = problem
                st.session_state.show_analysis = False
                st.session_state.show_simulation = False
                st.session_state.test_results = []
                st.session_state.ai_analysis_pending = False
        
        if user_role == 'admin':
            st.markdown("---")
            st.header("⚙️ Quản lý")
            
            if st.button("📊 Xem thống kê"):
                st.session_state.show_stats = True
            
            if st.button("👥 Quản lý tài khoản"):
                st.session_state.show_user_management = True
            
            if st.button("🏆 Bảng xếp hạng"):
                st.session_state.show_leaderboard = True
    

    if hasattr(st.session_state, 'show_stats') and st.session_state.show_stats:
        show_statistics_page()
        return
    
    if hasattr(st.session_state, 'show_user_management') and st.session_state.show_user_management:
        show_user_management_page()
        return
    
    if hasattr(st.session_state, 'show_leaderboard') and st.session_state.show_leaderboard:
        show_leaderboard_page()
        return
    
    if st.session_state.selected_problem:
        problem = st.session_state.selected_problem
        
        st.markdown(f"<div class='problem-card'>", unsafe_allow_html=True)
        st.markdown(f"**📝 Bài {problem['id']}: {problem['title']}**")
        st.markdown(f"**🎯 Độ khó:** {problem['difficulty']}")
        st.markdown(f"**📖 Mô tả:** {problem['description']}")
        st.markdown(f"**📥 Input:** {problem['input_format']}")
        st.markdown(f"**📤 Output:** {problem['output_format']}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### 💻 Viết code")
        code = st.text_area(
            "Nhập code Python của bạn:",
            value="",
            height=300,
            placeholder="Viết code giải bài tập ở đây..."
        )
        
        test_cases = load_test_cases(problem['id'])
        visible_test_cases = [tc for tc in test_cases if not tc.get('is_hidden', False)]
        
        if visible_test_cases:
            st.markdown("### 🧪 Test cases (Preview)")
            for i, test_case in enumerate(visible_test_cases[:2], 1):
                st.markdown(f"**Test Case {i}:**")
                st.markdown("**Input:**")
                st.code(test_case['input'])
                st.markdown("**Expected Output:**")
                st.code(test_case['expected_output'])
                if test_case.get('description'):
                    st.markdown(f"*{test_case['description']}*")
                st.markdown("---")
        else:
            st.warning("⚠️ Không có test cases hiển thị cho bài tập này!")
        
        if st.button("🚀 Submit bài", type="primary"):
            if not code.strip():
                st.error("❌ Vui lòng nhập code!")
                return
            
            if len(code.strip()) < 10:
                st.warning("⚠️ Code quá ngắn! Vui lòng viết code đầy đủ.")
                return
            
            st.session_state.show_analysis = False
            st.session_state.show_simulation = False
            st.session_state.test_results = []
            
            st.info("🧪 Đang chạy tất cả test cases...")
            all_results = run_all_test_cases(code, problem['id'])
            
            if not all_results:
                st.error("❌ Không tìm thấy test cases cho bài tập này!")
                return
            
            st.session_state.test_results = all_results
            
            total_tests = len(all_results)
            passed_tests = sum(1 for result in all_results if result['is_correct'])
            failed_tests = total_tests - passed_tests
            
            if failed_tests == 0:
                st.success(f"🎉 Tất cả {total_tests} test cases PASSED!")
            else:
                st.error(f"❌ {failed_tests}/{total_tests} test cases FAILED!")
            
            st.markdown("### 📊 Chi tiết kết quả")
            for result in all_results:
                if result['is_correct']:
                    st.markdown(f"✅ **Test Case {result['test_id']}:** PASSED")
                    if result.get('description'):
                        st.markdown(f"   *{result['description']}*")
                else:
                    st.markdown(f"❌ **Test Case {result['test_id']}:** FAILED")
                    if result.get('description'):
                        st.markdown(f"   *{result['description']}*")
                    
                    with st.expander(f"Chi tiết Test Case {result['test_id']}"):
                        display_test_case_detail(
                            result['input'], 
                            result['expected'], 
                            result['actual'], 
                            result['is_correct']
                        )
            
            st.session_state.show_simulation = True
            try:
                if all_results:
                    first_test_case = all_results[0]
                    raw_inputs = first_test_case['input'].split('\n')
                    iframe_url = create_pythontutor_url(code, raw_inputs)
                    if iframe_url:
                        st.session_state.simulation_url = iframe_url
            except Exception as e:
                st.error(f"❌ Lỗi mô phỏng: {str(e)}")
            
            status = "AC" if failed_tests == 0 else "WA"
            save_submission(problem['id'], code, None, status, all_results, st.session_state.user['username'])
            
            st.session_state.ai_analysis_pending = True
            st.session_state.analysis_result = None
        
        if st.session_state.show_simulation and st.session_state.simulation_url:
            st.markdown("### 🎬 Mô phỏng thực thi")
            st.markdown("""
            <div style="position: relative; overflow: hidden; border-radius: 8px; border: 1px solid #ddd;">
                <iframe src="{}" width="100%" height="600" frameborder="0" style="border: none; margin: 0; padding: 0;"></iframe>
            </div>
            """.format(st.session_state.simulation_url), unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'ai_analysis_pending') and st.session_state.ai_analysis_pending:
            if not hasattr(st.session_state, 'analysis_result') or st.session_state.analysis_result is None:
                st.info("🤖 AI đang phân tích code...")
                with st.spinner("Đang phân tích..."):
                    analysis = analyze_code_with_deepseek(code, problem['title'])
                    if analysis:
                        st.session_state.analysis_result = analysis
                        st.session_state.show_analysis = True
                        st.session_state.ai_analysis_pending = False
                        st.rerun()
        
        if st.session_state.show_analysis and st.session_state.analysis_result:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("**🤖 Đánh giá AI:**")
            st.markdown(st.session_state.analysis_result)
            st.markdown('</div>', unsafe_allow_html=True)
    

if __name__ == "__main__":
    main() 
