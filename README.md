# Cost-Optimized Multi-Modal Enterprise RAG Platform

## Overview
A production-oriented **Multi-Modal AI Knowledge Platform** that ingests **PDFs, audio, and video**, converts them into searchable knowledge, and delivers **semantic retrieval + intelligent AI answers** through a cost-optimized routing system.

This platform evolved from a traditional document RAG system into a **multi-modal enterprise intelligence architecture** supporting:
- Multi-PDF semantic enterprise search
- Audio/video ingestion with Whisper
- Timestamp-aware transcript intelligence
- FAISS-based vector retrieval
- Multi-model query routing (cost + complexity aware)
- Persistent knowledge storage
- Media-aware retrieval prioritization

---

# Core Features

## Document Intelligence
- PDF upload + parsing
- Context-aware chunking
- Heading-aware chunking
- Multi-document indexing
- Persistent FAISS vector store

## Multi-Modal Intelligence
- MP3 / WAV / M4A / MP4 ingestion
- Whisper transcription
- Audio extraction from video
- Timestamp-aware transcript generation
- Transcript archival (.txt)
- Media-aware retrieval routing

## AI Optimization Layer
- OpenAI API integration
- 3-tier model router:
  - `gpt-4o-mini` → Simple queries
  - `gpt-4o` → Moderate queries
  - `gpt-4.1` → Complex queries
- Cost optimization
- Latency + metrics logging

---

# System Architecture

```text
PDF / Audio / Video Upload
          ↓
Parsing / Whisper Transcription
          ↓
Context + Heading-Aware Chunking
          ↓
Embeddings (Sentence Transformers)
          ↓
FAISS Vector Storage
          ↓
Source-Aware Retrieval
          ↓
Query Complexity Router
          ↓
Optimized LLM Response


Project Structure
app/
 ┣ routes/
 ┃ ┣ upload.py
 ┃ ┣ upload_media.py
 ┃ ┗ chat.py
 ┣ services/
 ┃ ┣ retrieval_service.py
 ┃ ┣ llm_service.py
 ┃ ┗ router_service.py
 ┣ utils/
 ┃ ┣ pdf_parser.py
 ┃ ┣ media_parser.py
 ┃ ┗ chunker.py

data/
 ┣ faiss_index.bin
 ┣ document_metadata.json
 ┗ query_logs.json

transcripts/
uploads/

sample queries
{"query": "What are the pre-check steps?"}
{"query": "What does the video discuss?"}
{"query": "When does the speaker mention sustainable development?"}

Future Roadmap
Speaker diarization
YouTube ingestion
/summarize-media endpoint
Cloud deployment
Dashboard UI
Advanced vector indexing (HNSW / IVF)