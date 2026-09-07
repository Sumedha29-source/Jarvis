# JARVIS - Multimodal AI Desktop Assistant

JARVIS is an AI-powered desktop assistant capable of understanding natural language and performing actions directly on a user's computer.

## Vision

Unlike traditional AI chatbots that only provide answers, JARVIS is designed to perceive context and take actions across applications, files, the browser, and the operating system.

## Planned Features

- Voice interaction
- Natural language command understanding
- Desktop application control
- File and folder management
- Browser automation
- System monitoring
- Screen understanding
- Hand gesture recognition
- Contextual memory
- AI task planning
- Custom productivity routines
- Email and calendar integration

## Current Status

### v0.1

- FastAPI backend
- Health/status endpoint
- Initial desktop tool architecture
- Application launching support

## Tech Stack

- Python
- FastAPI
- React / Electron
- OpenCV
- MediaPipe
- LLM APIs
- Speech-to-Text
- Text-to-Speech

## Architecture

```text
Voice ────────┐
Gestures ─────┤
Screen ───────┤
Files ────────┼──> JARVIS Brain ───> Actions
Calendar ─────┤
Memory ───────┘