import streamlit as st
import time

# --- Aesthetically Pleasing UI and Animations ---
def add_mood_elements():
    """Adds positive, mood-elevating elements to the app."""
    st.markdown(
        """
        <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 24px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .st-emotion-cache-1629p8f.e1y5o3x0 {
            background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(200,240,255,1) 100%);
        }
        .st-emotion-cache-1j43d5x h1 {
            color: #333366;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.snow()

# --- Simplified Rule-Based Engine for Demonstration ---
class SimpleEngine:
    def __init__(self, rules):
        self.rules = rules
        self.facts = set()

# --- Functions for Each Page ---

def home_page():
    st.title("AI Chaining Playground ✨")
    st.header("Welcome to the World of AI Reasoning!")
    add_mood_elements()
    st.image("https://placehold.co/800x400/FFD700/000000?text=AI+Thinking+Illustration", use_column_width=True)
    st.markdown("""
        Have you ever wondered how a chatbot or an expert system makes a decision? 🤖
        They often use a process called **"chaining"** to figure things out! It's like a detective solving a mystery.

        We'll explore two main types of chaining:
        1.  **Forward Chaining (The "What's happening?" Approach):** Starts with clues to find a conclusion.
        2.  **Backward Chaining (The "What do I need?" Approach):** Starts with a goal and works backward to find the clues.

        Navigate using the sidebar to see them in action!
        """)

def forward_chaining_page():
    st.title("🚀 Forward Chaining: The Clue Collector")
    st.header("How It Works ")
    st.markdown("""
    Imagine you're a detective. You start with all the clues you have, and you see what you can figure out.
    When a rule's clues are all found, you can make a new conclusion! You keep doing this until you can't figure out anything else.

    **It's like this:**
    - **Clues (Facts):** You know a dog barked and you heard it. 🐕
    - **Rules:** "IF a dog barks AND you hear it, THEN you know a dog is nearby."
    - **Conclusion:** You conclude "a dog is nearby."

    Let's try it with a simple mental health scenario!
    """)
    
    add_mood_elements()
    
    mental_rules = {
        'needs_a_break': ['feeling_tired'],
        'needs_a_hug': ['feeling_sad'],
        'needs_calm_space': ['feeling_overwhelmed'],
        'feeling_unwell': ['needs_a_break', 'needs_a_hug']
    }

    initial_facts = []
    
    st.markdown("---")
    st.subheader("What clues do we have?")
    
    if st.checkbox("I feel tired. 😴", key='tired_fact'):
        initial_facts.append('feeling_tired')
    if st.checkbox("I feel sad. 😢", key='sad_fact'):
        initial_facts.append('feeling_sad')
    if st.checkbox("I feel overwhelmed. 🤯", key='overwhelmed_fact'):
        initial_facts.append('feeling_overwhelmed')

    if st.button("Start the Deduction!", key='start_forward'):
        engine = SimpleEngine(mental_rules)
        engine.facts.update(initial_facts)
        
        st.write("---")
        st.subheader("🕵️ The Deduction Process:")

        inferred_new = True
        while inferred_new:
            inferred_new = False
            for conclusion, premises in mental_rules.items():
                if set(premises).issubset(engine.facts) and conclusion not in engine.facts:
                    st.success(f"**Clue Found!** We know: {', '.join(premises)}. So, we conclude: **{conclusion.replace('_', ' ')}** 🎉")
                    engine.facts.add(conclusion)
                    inferred_new = True
                    time.sleep(0.5)
        
        st.markdown("---")
        st.success(f"**Final Conclusions:** {', '.join(engine.facts - set(initial_facts))}")

def backward_chaining_page():
    st.title("🎯 Backward Chaining: The Goal Hunter")
    st.header("How It Works ")
    st.markdown("""
    Imagine you have a specific goal, like "I want to eat a delicious pizza." 🍕
    You ask, "What do I need to make a pizza?"
    - **Goal:** "Eat pizza."
    - **Rule:** "IF you have dough, sauce, cheese, THEN you can make pizza."
    - **New Goal:** "Do I have dough? Do I have sauce? Do I have cheese?"
    You keep working backward until you find a question you can answer!

    Let's try it with a mental health support goal.
    """)
    
    add_mood_elements()

    mental_rules = {
        'suggest_therapy': ['feeling_sad', 'feeling_anxious'],
        'suggest_mindfulness': ['feeling_overwhelmed'],
        'suggest_break': ['feeling_tired']
    }

    mental_goals = ['suggest_therapy', 'suggest_mindfulness', 'suggest_break']

    st.markdown("---")
    st.subheader("What's our goal?")
    goal_to_prove = st.selectbox("I want to figure out if I should...", mental_goals)
    
    st.markdown("---")
    st.subheader("Now, let's hunt for clues!")

    # State for tracking questions and answers
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = {}
    if 'backward_run' not in st.session_state:
        st.session_state.backward_run = False

    def backward_chain_demo(goal, facts, indent=""):
        if goal in facts:
            st.write(f"{indent}✅ We already know '{goal}' is true!")
            return True

        if goal in st.session_state.questions_asked:
             st.write(f"{indent}🤔 We already asked about '{goal}'. Skipping.")
             return st.session_state.questions_asked[goal]

        for conclusion, premises in mental_rules.items():
            if conclusion == goal:
                st.write(f"{indent}🔍 To prove **{goal.replace('_', ' ')}**, we need to find clues for: {', '.join(premises)}")
                time.sleep(0.5)
                all_premises_true = True
                for premise in premises:
                    if not backward_chain_demo(premise, facts, indent + "    "):
                        all_premises_true = False
                        break
                if all_premises_true:
                    st.success(f"{indent}🎉 Goal '{goal.replace('_', ' ')}' is proven! The recommendation is: **{goal.replace('_', ' ')}**")
                    return True
        
        # If we reach here, the goal is a question for the user
        st.write(f"{indent}❓ We need to ask a question to find out about: **{goal.replace('_', ' ')}**")
        st.session_state.questions_asked[goal] = st.checkbox(f"Are you **{goal.replace('_', ' ')}**?", key=f'question_{goal}')
        time.sleep(0.5)
        return st.session_state.questions_asked[goal]


    if st.button("Start the Goal Hunt!", key='start_backward'):
        st.write("---")
        st.session_state.questions_asked = {} # Reset questions
        st.session_state.backward_run = True # Set the flag to true
        st.subheader("🎯 Hunting for the Goal...")
        
        backward_chain_demo(goal_to_prove, set())
        
        st.markdown("---")
        
        if any(st.session_state.questions_asked.values()):
            st.success("The goal was either proven or you provided the necessary clues!")
        else:
            st.warning("The goal could not be proven based on the provided clues.")

# --- Main App Logic ---
st.sidebar.title("AI Chaining App")
page = st.sidebar.radio("Choose a Page", ["Home", "Forward Chaining", "Backward Chaining"])

if page == "Home":
    home_page()
elif page == "Forward Chaining":
    forward_chaining_page()
elif page == "Backward Chaining":
    backward_chaining_page()
