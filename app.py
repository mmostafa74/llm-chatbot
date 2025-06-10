import random
import streamlit as st
import time
import json
from utils import generate_llm_response
from config import config

# UI Configuration
st.set_page_config(
    page_title=config.app.get("title", "AI Chatbot"),
    page_icon=config.app.get("page_icon", "🤖"),
    layout=config.ui.get("layout", "wide"),
    initial_sidebar_state=config.ui.get("initial_sidebar_state", "expanded"),
)


# Custom CSS for styling
st.markdown(f"<style>{config.styles.get('css')}</style>", unsafe_allow_html=True)

# Main Header
st.markdown(
    f"""
        <div class="main-header">
            <h1>{config.app.get("title", "LLM Assistant")}</h1>
            <p>{config.app.get("description", "Ask me anything about AI, coding, or beyond!")}</p>
        </div>
        """,
    unsafe_allow_html=True,
)

# Initialize chat messages and stats
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_count" not in st.session_state:
    st.session_state.user_count = 0
if "ai_count" not in st.session_state:
    st.session_state.ai_count = 0
if "response_times" not in st.session_state:
    st.session_state.response_times = []


# Enhanced Sidebar with Fixed Theme Toggle
with st.sidebar:
    # Chat Controls Section
    st.markdown(
        f"""
    <div class="sidebar-section">
        <h2 style="color: #667eea; margin-bottom: 20px;">{config.sidebar.get("chat_controls_title", "🎛️ Chat Controls").replace("## ", "")}</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Model Selection
    st.markdown("**🤖 AI Model**")
    selected_model = st.selectbox(
        "Choose a model:",
        config.api.get("available_models", [config.app.get("model")]),
        index=0,
        label_visibility="collapsed",
    )
    # Temperature Control
    st.markdown("**🌡️ Creativity Level**")
    temperature = st.slider(
        "Temperature:",
        0.0,
        1.5,
        config.api.get("temperature", 0.7),
        0.1,
        help="Higher values make responses more creative, lower values more focused",
        label_visibility="collapsed",
    )
    # Temperature indicator
    temp_emoji = (
        "🧊"
        if temperature < 0.3
        else "❄️"
        if temperature < 0.7
        else "🔥"
        if temperature > 1.2
        else "🌡️"
    )
    temp_desc = (
        "Very Focused"
        if temperature < 0.3
        else "Focused"
        if temperature < 0.7
        else "Very Creative"
        if temperature > 1.2
        else "Balanced"
    )
    st.markdown(
        f"<small>{temp_emoji} {temp_desc} ({temperature})</small>",
        unsafe_allow_html=True,
    )

    # Random starter button

    st.markdown("**🎲 Quick Start**")
    if st.button(
        "Get Random Question",
        use_container_width=True,
        help=config.sidebar.get(
            "random_button_tooltip", "Get a random conversation starter"
        ),
    ):
        random_prompt = random.choice(config.prompts.get("random_starters", ["Hello!"]))
        st.session_state.random_prompt = random_prompt

        st.rerun()

    # Divider
    st.markdown("---")

    # Enhanced Chat Statistics Section
    st.markdown(
        f"""
    <div class="sidebar-section">
        <h3 style="color: #667eea; margin-bottom: 20px;">{config.sidebar.get("chat_stats_title", "📊 Chat Statistics").replace("### ", "")}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Calculate statistics
    avg_time = (
        sum(st.session_state.response_times) / len(st.session_state.response_times)
        if st.session_state.response_times
        else 0
    )

    total_messages = st.session_state.user_count + st.session_state.ai_count

    # Enhanced stat cards with better styling
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
        <div class="enhanced-stat-card">
            <div class="stat-icon">👤</div>
            <div class="stat-number">{st.session_state.user_count}</div>
            <div class="stat-label">Your Messages</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="enhanced-stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-number">{avg_time:.1f}s</div>
            <div class="stat-label">Avg Response</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="enhanced-stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-number">{st.session_state.ai_count}</div>
            <div class="stat-label">AI Responses</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="enhanced-stat-card">
            <div class="stat-icon">💬</div>
            <div class="stat-number">{total_messages}</div>
            <div class="stat-label">Total Messages</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Response time indicator
    if avg_time > 0:
        speed_emoji = "🚀" if avg_time < 2 else "⚡" if avg_time < 5 else "🐌"
        speed_desc = (
            "Lightning Fast" if avg_time < 2 else "Fast" if avg_time < 5 else "Slow"
        )
        st.markdown(
            f"<div style='text-align: center; margin: 10px 0;'><small>{speed_emoji} {speed_desc}</small></div>",
            unsafe_allow_html=True,
        )

    # Divider
    st.markdown("---")

    # Enhanced Action Buttons Section
    st.markdown("**🛠️ Actions**")

    # Clear Chat Button with confirmation
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        if st.session_state.messages:
            st.session_state.show_clear_confirm = True
        else:
            st.info("Chat is already empty!")

    # Confirmation dialog for clear
    if (
        hasattr(st.session_state, "show_clear_confirm")
        and st.session_state.show_clear_confirm
    ):
        st.warning("⚠️ This will delete all messages!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", use_container_width=True):
                st.session_state.messages.clear()
                st.session_state.user_count = 0
                st.session_state.ai_count = 0
                st.session_state.response_times.clear()
                st.session_state.show_clear_confirm = False
                st.success("Chat cleared!")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_clear_confirm = False
                st.rerun()

    # Export Chat Button with options
    if st.session_state.messages:
        # Prepare export data
        export_data = {
            "chat_history": st.session_state.messages,
            "statistics": {
                "user_messages": st.session_state.user_count,
                "ai_responses": st.session_state.ai_count,
                "total_messages": total_messages,
                "average_response_time": f"{avg_time:.2f}s",
                "model_used": selected_model,
                "temperature": temperature,
            },
            "exported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "app_info": {
                "title": config.app.get("title", "AI Chatbot"),
                "version": "1.0",
            },
        }

        st.download_button(
            label="💾 Export Chat",
            data=json.dumps(export_data, indent=2, ensure_ascii=False),
            file_name=f"chat_export_{time.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            help="Download chat history with statistics",
        )

        # Additional export formats
        with st.expander("📄 More Export Options"):
            # Text format export
            text_export = f"""
                    {config.app.get("title", "AI Chatbot")} - Chat Export
                    Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
                    Model: {selected_model}
                    Temperature: {temperature}

                    Statistics:
                    - Your Messages: {st.session_state.user_count}
                    - AI Responses: {st.session_state.ai_count}
                    - Average Response Time: {avg_time:.2f}s

                    Chat History:
                    {"=" * 50}
                """
            for msg in st.session_state.messages:
                role = "You" if msg["role"] == "user" else "Assistant"
                timestamp = msg.get("timestamp", "")
                text_export += f"[{timestamp}] {role}: {msg['content']}\n\n"

            st.download_button(
                label="📝 Export as Text",
                data=text_export,
                file_name=f"chat_export_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.button(
            "💾 Export Chat",
            disabled=True,
            use_container_width=True,
            help="No messages to export",
        )

    # Divider
    st.markdown("---")

    # Footer with app info
    st.markdown(
        f"""
    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 20px;">
        <small style="color: #6c757d;">
            {config.messages.get("footer_text", "Built with ❤️ using Streamlit")}
        </small>
    </div>
    """,
        unsafe_allow_html=True,
    )


# Chat Messages Section - Custom Implementation with Full Control
st.markdown("### 💬 Conversation")

# Create a scrollable chat container
if st.session_state.messages:
    # Chat container with custom styling
    st.markdown(
        """
    <div class="custom-chat-container">
    """,
        unsafe_allow_html=True,
    )

    for i, message in enumerate(st.session_state.messages):
        timestamp = message.get("timestamp", "")
        content = message["content"]

        if message["role"] == "user":
            st.markdown(
                f"""
            <div class="message-row user-row">
                <div class="user-bubble">
                    <div class="message-header">
                        <span class="role-label">👤 You</span>
                        <span class="timestamp">🕐 {timestamp}</span>
                    </div>
                    <div class="message-content">{content}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="message-row ai-row">
                <div class="ai-bubble">
                    <div class="message-header">
                        <span class="role-label">🤖 Assistant</span>
                        <span class="timestamp">🕐 {timestamp}</span>
                    </div>
                    <div class="message-content">{content}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Interactive welcome with clickable suggestions

    st.markdown(
        f"""
    <div class="welcome-container">
        <div class="welcome-content">
            <div class="welcome-icon">🤖✨</div>
            <h2>{config.messages.get("welcome_title", "Welcome to AI Chat!")}</h2>
            <p>{config.messages.get("welcome_subtitle", "Start a conversation by typing a message below.")}</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🚀 Quick Start - Click to try:")
    # Create interactive suggestion buttons
    suggestions = [
        ("💡", "Explain concepts", "Explain quantum computing in simple terms"),
        ("📚", "Book recommendations", "Recommend a good science fiction book"),
        (
            "⚡",
            "Productivity tips",
            "How can I be more productive while working from home?",
        ),
        (
            "🔬",
            "Science questions",
            "What's the most fascinating recent scientific discovery?",
        ),
    ]

    cols = st.columns(len(suggestions))

    for i, (emoji, label, prompt) in enumerate(suggestions):
        with cols[i]:
            if st.button(
                f"{emoji} {label}", use_container_width=True, key=f"suggestion_{i}"
            ):
                # Set the prompt to be processed
                st.session_state.suggestion_prompt = prompt
                st.rerun()


# Handle random prompt if set
if hasattr(st.session_state, "random_prompt"):
    prompt = st.session_state.random_prompt
    del st.session_state.random_prompt
else:
    # Handle suggestion prompt if set
    suggestion_prompt = None
    if hasattr(st.session_state, "suggestion_prompt"):
        suggestion_prompt = st.session_state.suggestion_prompt
        del st.session_state.suggestion_prompt

    # Text input for new message

    user_input = st.chat_input(
        config.sidebar.get("input_placeholder", "Type your message here...")
    )

    # Process user input (either from chat input or suggestion)
    prompt = suggestion_prompt or user_input

# Process user input
if prompt:
    timestamp = time.strftime(config.chat.get("timestamp_format", "%H:%M"))

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "timestamp": timestamp}
    )
    st.session_state.user_count += 1

    # Show thinking indicator
    with st.spinner(config.messages.get("thinking", "🤔 Thinking...")):
        start_time = time.time()
        response = generate_llm_response(
            prompt, model=selected_model, temperature=temperature
        )
        elapsed = time.time() - start_time

    # Add AI response
    timestamp = time.strftime(config.chat.get("timestamp_format", "%H:%M"))
    st.session_state.messages.append(
        {"role": "assistant", "content": response, "timestamp": timestamp}
    )
    st.session_state.ai_count += 1
    st.session_state.response_times.append(elapsed)

    # Auto-scroll delay
    time.sleep(config.chat.get("auto_scroll_delay", 100) / 1000)
    st.rerun()
