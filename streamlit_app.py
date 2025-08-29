import streamlit as st
import uuid
from src.annotation import AnnotationManager
from datetime import datetime

def load_documents():
    """Load preprocessed documents (placeholder)."""
    return [
        "Document 1: Global temperatures have risen significantly according to NASA data...",
        "Document 2: Blog claims climate change is a hoax without providing evidence...",
        "Document 3: Research paper demonstrates correlation between emissions and warming..."
    ]

def main():
    st.title("TruthLens Annotation Interface")
    
    # Initialize annotation manager
    annotation_mgr = AnnotationManager()
    
    # Session state for document index
    if 'doc_index' not in st.session_state:
        st.session_state.doc_index = 0
    
    # Load documents
    documents = load_documents()
    
    if documents:
        # Display current document
        st.subheader("Document to Annotate:")
        st.text_area("Content", documents[st.session_state.doc_index], height=200)
        
        # Annotation options
        col1, col2 = st.columns(2)
        with col1:
            label = st.radio("Select Label:", ["Reliable", "Unreliable"])
        with col2:
            annotator = st.text_input("Annotator Name:", "")
        
        # Submit button
        if st.button("Submit Annotation"):
            if annotator:
                annotation = {
                    "id": str(uuid.uuid4()),
                    "text": documents[st.session_state.doc_index],
                    "label": label,
                    "annotator": annotator,
                    "timestamp": datetime.now().isoformat()
                }
                
                if annotation_mgr.save_annotation(annotation):
                    st.success("Annotation saved!")
                    # Move to next document
                    st.session_state.doc_index = (st.session_state.doc_index + 1) % len(documents)
                else:
                    st.error("Failed to save annotation")
            else:
                st.warning("Please enter annotator name")
        
        # Progress
        st.progress((st.session_state.doc_index + 1) / len(documents))
        st.text(f"Document {st.session_state.doc_index + 1} of {len(documents)}")

if __name__ == "__main__":
    main()
