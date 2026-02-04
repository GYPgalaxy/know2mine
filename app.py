import streamlit as st
import pandas as pd
from database import get_db
from services.note_service import NoteService
from services.ai_service import AIService
from config import Config
import time
import os

# Try to setup RQ
try:
    from redis import Redis
    from rq import Queue
    redis_conn = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, password=Config.REDIS_PASSWORD)
    q = Queue(connection=redis_conn)
    USE_RQ = True
except (ImportError, Exception) as e:
    print(f"RQ/Redis not available: {e}")
    USE_RQ = False

# Page Config
st.set_page_config(page_title="Smart Knowledge Hub", layout="wide", page_icon="🧠")

# Initialize Services
db = next(get_db())
note_service = NoteService(db)
ai_service = AIService()

# Sidebar
st.sidebar.title("🧠 Knowledge Hub")

# AI Configuration Section
st.sidebar.subheader("⚙️ Settings")
ai_provider = st.sidebar.selectbox(
    "AI Provider", 
    ["openai", "gemini", "claude"], 
    index=["openai", "gemini", "claude"].index(Config.AI_PROVIDER) if Config.AI_PROVIDER in ["openai", "gemini", "claude"] else 0
)

# Update config if changed (Note: This is per session/rerun, doesn't persist to .env)
# In a real app, you might want to reload the AIService or update a singleton config
if ai_provider != Config.AI_PROVIDER:
    Config.AI_PROVIDER = ai_provider
    # Re-initialize AI service
    ai_service = AIService()

page = st.sidebar.radio("Navigate", ["Knowledge Base", "Recycle Bin"])

st.sidebar.markdown("---")
st.sidebar.caption("System Status")
if USE_RQ:
    st.sidebar.success("Async Worker: Active")
else:
    st.sidebar.warning("Async Worker: Inactive (Sync Mode)")

# Simple Auto-cleanup trigger check
if st.sidebar.button("Run Auto-Cleanup"):
    note_service.cleanup_old_deleted_notes()
    st.sidebar.success("Cleanup executed.")

# Main Content
if page == "Knowledge Base":
    st.title("📚 Knowledge Base")

    # 1. Input Section
    with st.container():
        st.subheader("Capture Thought")
        with st.form(key='note_form', clear_on_submit=True):
            content_input = st.text_area("What's on your mind?", height=100, placeholder="Type your note here...")
            col_submit, col_empty = st.columns([1, 5])
            submit_button = col_submit.form_submit_button(label='Save Note')
            
            if submit_button and content_input:
                # 1. Save basic note
                note = note_service.create_note(content=content_input)
                
                # 2. AI Processing
                if USE_RQ:
                    try:
                        from worker import process_note_ai
                        q.enqueue(process_note_ai, note.id)
                        st.success("Note saved! AI processing running in background.")
                    except Exception as e:
                        st.error(f"Failed to enqueue task: {e}")
                else:
                    with st.spinner('AI Processing (Classifying & Embedding)...'):
                        ai_data = ai_service.classify_and_tag(content_input)
                        embedding = ai_service.generate_embedding(content_input)
                        
                        note_service.update_note_ai_data(
                            note_id=note.id,
                            category=ai_data.get("category"),
                            tags=ai_data.get("tags"),
                            embedding=embedding
                        )
                        note_service.update_note_status(note.id, "completed")
                    st.success("Note saved and processed!")
                
                time.sleep(1)
                st.rerun()

    st.markdown("---")

    # 2. Search & Filter Section
    col_search, col_view = st.columns([3, 1])
    search_query = col_search.text_input("🔍 Semantic Search", placeholder="Search by meaning...")
    view_mode = col_view.radio("View Mode", ["Cards", "Table"], horizontal=True)

    # 3. Data Retrieval
    if search_query:
        active_notes = note_service.get_active_notes()
        notes = ai_service.search_similar(search_query, active_notes)
        st.caption(f"Found {len(notes)} relevant results.")
    else:
        notes = note_service.get_active_notes()
        st.caption(f"Showing all {len(notes)} notes.")

    # 4. Display Section
    if not notes:
        st.info("No notes found. Start by adding one above!")
    else:
        if view_mode == "Cards":
            cols = st.columns(3)
            for i, note in enumerate(notes):
                with cols[i % 3]:
                    with st.container(border=True):
                        # Status Badge
                        if hasattr(note, 'status'):
                            if note.status == 'processing':
                                st.caption("⏳ Processing AI...")
                            elif note.status == 'failed':
                                st.caption("❌ AI Failed")
                        
                        st.markdown(f"**{note.category or 'Uncategorized'}**")
                        st.caption(note.created_at.strftime("%Y-%m-%d %H:%M"))
                        st.text(note.content[:150] + ("..." if len(note.content) > 150 else ""))
                        if note.tags:
                            st.markdown(" ".join([f"`#{tag}`" for tag in note.tags]))
                        
                        if st.button("🗑️", key=f"del_{note.id}", help="Move to Recycle Bin"):
                            note_service.soft_delete_notes([note.id])
                            st.rerun()

        elif view_mode == "Table":
            data = []
            for note in notes:
                status = getattr(note, 'status', 'unknown')
                data.append({
                    "Select": False,
                    "ID": note.id,
                    "Content": note.content,
                    "Category": note.category,
                    "Tags": str(note.tags),
                    "Status": status,
                    "Created At": note.created_at
                })
            
            df = pd.DataFrame(data)
            
            edited_df = st.data_editor(
                df,
                column_config={
                    "Select": st.column_config.CheckboxColumn("Select", default=False),
                    "ID": st.column_config.NumberColumn("ID", disabled=True),
                    "Content": st.column_config.TextColumn("Content", disabled=True),
                    "Category": st.column_config.TextColumn("Category", disabled=True),
                    "Tags": st.column_config.TextColumn("Tags", disabled=True),
                    "Status": st.column_config.TextColumn("Status", disabled=True),
                    "Created At": st.column_config.DatetimeColumn("Created At", disabled=True),
                },
                hide_index=True,
                use_container_width=True,
                key="editor_active"
            )
            
            selected_indices = edited_df[edited_df["Select"]].index
            if not selected_indices.empty:
                st.warning(f"Selected {len(selected_indices)} notes.")
                if st.button("🗑️ Batch Delete"):
                    selected_ids = edited_df[edited_df["Select"]]["ID"].tolist()
                    note_service.soft_delete_notes(selected_ids)
                    st.success(f"Moved {len(selected_ids)} notes to Recycle Bin.")
                    time.sleep(1)
                    st.rerun()

elif page == "Recycle Bin":
    st.title("♻️ Recycle Bin")
    st.caption("Items here are deleted automatically after 30 days.")

    col_empty_bin, _ = st.columns([1, 5])
    if col_empty_bin.button("🔥 Empty Recycle Bin"):
        note_service.empty_recycle_bin()
        st.success("Recycle Bin emptied.")
        st.rerun()

    deleted_notes = note_service.get_deleted_notes()

    if not deleted_notes:
        st.info("Recycle Bin is empty.")
    else:
        data = []
        for note in deleted_notes:
            data.append({
                "Select": False,
                "ID": note.id,
                "Content": note.content,
                "Deleted At": note.deleted_at,
                "Original Category": note.category
            })
        
        df = pd.DataFrame(data)

        edited_df = st.data_editor(
            df,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select", default=False),
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "Content": st.column_config.TextColumn("Content", disabled=True),
                "Deleted At": st.column_config.DatetimeColumn("Deleted At", disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            key="editor_deleted"
        )

        selected_rows = edited_df[edited_df["Select"]]
        
        if not selected_rows.empty:
            col_restore, col_hard_delete = st.columns(2)
            selected_ids = selected_rows["ID"].tolist()
            
            with col_restore:
                if st.button(f"♻️ Restore ({len(selected_ids)})"):
                    note_service.restore_notes(selected_ids)
                    st.success("Notes restored.")
                    time.sleep(1)
                    st.rerun()
            
            with col_hard_delete:
                if st.button(f"❌ Permanently Delete ({len(selected_ids)})"):
                    note_service.hard_delete_notes(selected_ids)
                    st.success("Notes permanently deleted.")
                    time.sleep(1)
                    st.rerun()

db.close()
