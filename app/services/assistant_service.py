from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.assistant_repository import AssistantRepository
from app.models.assistant import Assistant


# ==============================
# 🔥 DEFAULT NOAVOICE TEMPLATE (AUTO ON CREATE)
# ==============================
DEFAULT_SYSTEM_PROMPT = """## I. 🤖 IDENTITY

You are Maya, a warm, professional AI assistant for NovaVoice.

You assist users by:
- Answering queries clearly
- Providing helpful and accurate responses
- Handling conversations naturally
- Sounding human, not robotic

Tone & Style:
- Friendly and natural
- Short and warm sentences
- Professional but conversational
- Never sound scripted

---

## II. 🔒 GLOBAL RULES
- Never hallucinate unknown facts
- Always confirm important user details
- Ask clarification if input is unclear
- Maintain conversation context
- Be polite and helpful at all times

---

## III. 🎧 CONVERSATION BEHAVIOR
- Speak like a real assistant
- Avoid robotic responses
- Keep replies concise but useful
- Stay calm and professional

---

## IV. 🎯 PRIMARY GOAL
Your goal is to assist users efficiently while maintaining a natural,
warm, and professional conversational experience like a real human assistant.
"""

DEFAULT_FIRST_MESSAGE = (
    "Hello! This is your NovaVoice AI assistant. How may I assist you today?"
)

DEFAULT_END_CALL_MESSAGE = (
    "Thank you for contacting us. If you need anything else, feel free to reach out anytime. Have a great day!"
)


class AssistantService:

    # ==============================
    # CREATE ASSISTANT (AUTO TEMPLATE SET)
    # ==============================
    @staticmethod
    async def create_assistant(db: AsyncSession, data: dict):
        """
        🔥 CORE LOGIC:
        - User only sends name + description
        - system_prompt auto set
        - first_message auto set
        - end_call_message auto set
        - Routes remain separate (as per your architecture)
        """

        # 🧠 AUTO DEFAULT TEMPLATE INJECTION
        # (Only if not already provided)
        if not data.get("system_prompt"):
            data["system_prompt"] = DEFAULT_SYSTEM_PROMPT

        if not data.get("first_message"):
            data["first_message"] = DEFAULT_FIRST_MESSAGE

        if not data.get("end_call_message"):
            data["end_call_message"] = DEFAULT_END_CALL_MESSAGE

        # Safe defaults for configure section
        if "language" not in data:
            data["language"] = "English"

        if "voice_provider" not in data:
            data["voice_provider"] = "elevenlabs"

        if "detect_caller_number" not in data:
            data["detect_caller_number"] = False

        if "multilingual_support" not in data:
            data["multilingual_support"] = False

        if "voice_recording" not in data:
            data["voice_recording"] = False

        # Create via repository (no change needed there)
        assistant = await AssistantRepository.create(db, data)
        return assistant

    # ==============================
    # GET ALL ASSISTANTS
    # ==============================
    @staticmethod
    async def get_all_assistants(db: AsyncSession):
        return await AssistantRepository.get_all(db)

    # ==============================
    # GET SINGLE ASSISTANT
    # ==============================
    @staticmethod
    async def get_assistant(db: AsyncSession, assistant_id: UUID | str):
        return await AssistantRepository.get_by_id(db, str(assistant_id))

    # ==============================
    # UPDATE ASSISTANT (BASIC INFO)
    # ==============================
    @staticmethod
    async def update_assistant(
        db: AsyncSession,
        assistant_id: UUID | str,
        data: dict
    ):
        assistant = await AssistantRepository.get_by_id(db, str(assistant_id))

        if not assistant:
            return None

        # 🔒 SAFE PARTIAL UPDATE (no template override)
        for key, value in data.items():
            if value is not None:
                setattr(assistant, key, value)

        await db.commit()
        await db.refresh(assistant)
        return assistant

    # ==============================
    # DELETE ASSISTANT
    # ==============================
    @staticmethod
    async def delete_assistant(db: AsyncSession, assistant_id: UUID | str):
        return await AssistantRepository.delete(db, str(assistant_id))

    # ==============================
    # PROMPT SECTION (KEEP YOUR EXISTING FLOW)
    # ==============================
    @staticmethod
    async def set_prompt(
        db: AsyncSession,
        assistant_id: UUID | str,
        data: dict
    ):
        """
        Used by:
        /agents/create_prompt/{agent_id}
        This will override default template later (as you wanted)
        """
        return await AssistantRepository.set_prompt(
            db,
            str(assistant_id),
            data
        )

    @staticmethod
    async def delete_prompt(db: AsyncSession, assistant_id: UUID | str):
        return await AssistantRepository.delete_prompt(
            db,
            str(assistant_id)
        )