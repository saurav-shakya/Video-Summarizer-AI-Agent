import streamlit as st 
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import random
import math
from time import sleep

load_dotenv()
import os
API_KEY=os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def process_with_retry(processed_video, max_attempts=3):
    for _ in range(max_attempts):
        try:
            result = get_file(processed_video.name)
            if result:
                return result
        except Exception as e:
            if "RATE_LIMIT_EXCEEDED" in str(e):
                time.sleep(5)
                continue
            raise e
    raise Exception("Max retry attempts reached")

st.set_page_config(
    page_title="Video Summizer AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern UI CSS with improved colors and effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base Theme */
    .main {
        background: linear-gradient(135deg, #0f1729, #1e1b4b, #0f1729);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Header Layout */
    .header-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        margin-bottom: 2rem;
    }
    
    .logo-container {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
    }
    
    .header-text {
        flex-grow: 1;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    /* Enhanced Container Styles */
    .neo-container {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            inset 0 0 0 1px rgba(255, 255, 255, 0.05);
        padding: 2rem;
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .neo-container:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.3),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    
    /* Upload Zone with Better Visual Feedback */
    .upload-zone {
        border: 2px dashed rgba(59, 130, 246, 0.3);
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        background: radial-gradient(circle at center, rgba(59, 130, 246, 0.05) 0%, transparent 70%);
    }
    
    .upload-zone:hover {
        border-color: #3b82f6;
        background: radial-gradient(circle at center, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    }
    
    /* Modern Button Style */
    .neo-button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .neo-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Update Header Text with Version
st.markdown("""
    <div class="header-container">
        <div class="logo-container">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                <path d="M12 2a10 10 0 1 0 10 10H12V2z"/>
                <path d="M12 2a10 10 0 1 1-10 10h10V2z"/>
                <circle cx="12" cy="12" r="3"/>
            </svg>
        </div>
        <div class="header-text">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <h1 class="main-title">Video Summarizer AI Agent</h1>
                <span style="
                    background: rgba(59, 130, 246, 0.1);
                    color: #3b82f6;
                    padding: 0.2rem 0.8rem;
                    border-radius: 12px;
                    font-size: 0.9rem;
                    border: 1px solid rgba(59, 130, 246, 0.2);
                ">Beta v1.0</span>
            </div>
            <p style="color: rgba(255,255,255,0.7); margin: 0;">Powered by Gemini 2.0 flash</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Upload Section
with st.container():
    st.markdown("""
        <div class="neo-container upload-zone">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <h2 style="color: white; margin: 1rem 0;">Upload Your Video</h2>
            <p style="color: rgba(255,255,255,0.7);">Drag & drop your video file here</p>
            <p style="color: #3b82f6; font-size: 0.875rem;">MP4, MOV, AVI • Max 200MB</p>
        </div>
    """, unsafe_allow_html=True)
    
    video_file = st.file_uploader(
        label="Upload Video File",
        type=['mp4', 'mov', 'avi'],
    )

@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )
## Initialize the agent
multimodal_Agent=initialize_agent()

if video_file:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name
        
        st.video(video_path, format="video/mp4", start_time=0)
        
        # Chat/Query Section
        st.markdown("""
            <div class="neo-container">
                <h3 style="color: white; margin-bottom: 1rem;">🤖 Chat with Video AI</h3>
                <p style="color: rgba(255,255,255,0.7);">Ask any question about the video content</p>
            </div>
        """, unsafe_allow_html=True)
        
        user_query = st.text_area(
            label="Enter your video query",
            value="",
            placeholder="Example: What is the main topic of this video? What are the key points discussed?",
            help="Be specific with your questions for better insights",
        )
        
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            if not user_query:
                st.warning("Please enter your question first!")
            else:
                with st.spinner("🎥 Processing video and analyzing..."):
                    try:
                        # Process video
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)

                        # Generate and run analysis
                        analysis_prompt = f"""
                        Based on the video content:
                        {user_query}
                        
                        Provide a clear, detailed response that directly addresses the question.
                        Include specific references from the video where relevant.
                        """
                        
                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
                        
                        # Display results
                        st.markdown("""
                            <div class="neo-container" style="border-left: 4px solid #3b82f6;">
                                <h3 style="color: #3b82f6; margin-bottom: 1rem;">💡 Analysis Results</h3>
                                <div style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                                    {}
                                </div>
                            </div>
                        """.format(response.content), unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Analysis error: {str(e)}")
                        if "RATE_LIMIT_EXCEEDED" in str(e):
                            st.info("💡 Please wait a moment and try again")
                
    finally:
        # Cleanup temporary files
        if 'video_path' in locals():
            Path(video_path).unlink(missing_ok=True)

    # Options Section
    st.markdown("""
        <div class="neo-container">
            <h3 style="color: white; margin-bottom: 1rem;">Summarization Options</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div class="neo-card">
                    <h4 style="color: #f9d423;">📝 Text Summary</h4>
                    <p style="color: rgba(255,255,255,0.7);">Detailed text analysis</p>
                </div>
                <div class="neo-card">
                    <h4 style="color: #f9d423;">📊 Key Timelines</h4>
                    <p style="color: rgba(255,255,255,0.7);">Important moments</p>
                </div>
                <div class="neo-card">
                    <h4 style="color: #f9d423;">🔍 Bullet Points</h4>
                    <p style="color: rgba(255,255,255,0.7);">Quick overview</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.6); padding: 3rem;">
            <div class="floating">
                ⬆️
            </div>
            <p style="margin-top: 1rem;">Upload a video to begin your AI-powered analysis journey</p>
        </div>
    """, unsafe_allow_html=True)

# Update the Footer
st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.5);">
        <p>Crafted with ❤️ by <a href="https://x.com/sauravv_x" target="_blank" style="color: #3b82f6; text-decoration: none; transition: color 0.3s ease;">Saurav</a></p>
    </div>
""", unsafe_allow_html=True)
