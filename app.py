import streamlit as st
import time

# --- Rule-Based Inference Engine ---
# This class contains the logic for both forward and backward chaining.
# It's the core of our chatbot's reasoning.
class InferenceEngine:
    def __init__(self, rules):
        self.rules = rules
        self.facts = set()
        self.conclusions = set()

    # Forward Chaining (Data-Driven)
    # Starts with known facts and infers new conclusions.
    def forward_chain(self, new_facts):
        self.facts.update(new_facts)
        
        st.subheader("Forward Chaining in Action")
        st.info(f"Starting with facts: {list(new_facts)}")
        
        inferred_new = True
        while inferred_new:
            inferred_new = False
            for conclusion, premises in self.rules.items():
                # If a rule's premises are all known facts...
                if set(premises).issubset(self.facts) and conclusion not in self.conclusions:
                    st.success(f"Rule fired: Since we know {list(premises)}, we can conclude '{conclusion}'.")
                    self.conclusions.add(conclusion)
                    self.facts.add(conclusion) # The new conclusion becomes a new fact
                    inferred_new = True
                    # Add a brief pause for the animation effect
                    time.sleep(0.5)

    # Backward Chaining (Goal-Driven)
    # Starts with a goal and works backward to find supporting facts.
    def backward_chain(self, goal, context, questions_to_ask, answers):
        
        st.subheader("Backward Chaining in Action")
        st.info(f"Checking if the goal '{goal}' can be proved...")

        if goal in self.facts:
            st.success(f"Goal '{goal}' is a known fact!")
            return True

        if goal in answers and answers[goal]:
            st.success(f"Goal '{goal}' is supported by a user's answer.")
            return True

        # Check if the goal can be concluded by any rule
        for conclusion, premises in self.rules.items():
            if conclusion == goal:
                all_premises_true = True
                premise_list_for_display = []
                for premise in premises:
                    # Recursively check each premise
                    st.write(f"-> To prove '{goal}', we need to prove '{premise}'.")
                    time.sleep(0.2)
                    if not self.backward_chain(premise, context, questions_to_ask, answers):
                        all_premises_true = False
                        break
                if all_premises_true:
                    st.success(f"Goal '{goal}' is proved!")
                    return True
        
        # If the goal cannot be proved by any rule, it must be a user question
        if goal not in questions_to_ask[context]:
            st.warning(f"Goal '{goal}' is a new premise. Let's ask the user.")
            questions_to_ask[context].append(goal)
            time.sleep(0.2)

        return False

# --- Streamlit UI and State Management ---

if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'questions_to_ask' not in st.session_state:
    st.session_state.questions_to_ask = { 'mental': [] }
if 'answers' not in st.session_state:
    st.session_state.answers = { 'mental': {} }
if 'mental_health_facts' not in st.session_state:
    st.session_state.mental_health_facts = set()

# --- Sidebar Navigation ---
st.sidebar.title("AI Lab Chaining Demos")
st.session_state.page = st.sidebar.radio("Go to", ["Home", "Mental Health Chatbot"])

# --- Home Page ---
if st.session_state.page == "Home":
    st.title("Forward and Backward Chaining Demo")
    st.markdown("""
    Welcome to this interactive application demonstrating two core AI reasoning techniques:
    **Forward Chaining** and **Backward Chaining**.

    - **Forward Chaining (Data-Driven):** Starts with known facts and applies rules to deduce new conclusions.
    - **Backward Chaining (Goal-Driven):** Starts with a specific goal and works backward to find the facts needed to prove it.

    Navigate to the **Mental Health Chatbot** to see these algorithms in action!
    """)
    st.image("https://placehold.co/800x400/228B22/FFFFFF?text=AI+Reasoning+Illustration", use_column_width=True)


# --- Mental Health Chatbot Page ---
elif st.session_state.page == "Mental Health Chatbot":
    st.title("Mental Health Support Chatbot")
    st.markdown("""
    This bot uses rule-based AI to provide support. You'll see both **forward** and **backward chaining**
    at work, with a visual breakdown of how the reasoning happens.
    
    _Disclaimer: This is a demonstration. For real mental health support, please consult a professional._
    """)

    st.markdown("---")
    
    # Define rules and goals for the mental health bot
    mental_rules = {
        'suggest_therapy': ['feeling_sad', 'feeling_anxious'],
        'suggest_mindfulness': ['feeling_overwhelmed'],
        'suggest_break': ['feeling_tired', 'feeling_stressed'],
        'feeling_distressed': ['feeling_sad', 'feeling_anxious', 'feeling_overwhelmed']
    }
    
    mental_goals = ['suggest_therapy', 'suggest_mindfulness', 'suggest_break']
    
    # Initialize the inference engine
    engine = InferenceEngine(mental_rules)

    # --- Forward Chaining Section ---
    st.header("Step 1: Forward Chaining")
    st.markdown("Let's start by gathering some initial facts (symptoms) from you.")
    
    initial_facts = []
    
    st.markdown("""
    **Tell us what you're feeling:**
    """)

    if st.checkbox("Feeling sad?", key='sad_fact'):
        initial_facts.append('feeling_sad')
    if st.checkbox("Feeling anxious?", key='anxious_fact'):
        initial_facts.append('feeling_anxious')
    if st.checkbox("Feeling overwhelmed?", key='overwhelmed_fact'):
        initial_facts.append('feeling_overwhelmed')
    if st.checkbox("Feeling tired?", key='tired_fact'):
        initial_facts.append('feeling_tired')
    if st.checkbox("Feeling stressed?", key='stressed_fact'):
        initial_facts.append('feeling_stressed')

    if st.button("Start Forward Chaining", key='start_forward'):
        st.session_state.mental_health_facts.update(initial_facts)
        
        with st.expander("Show Chaining Process", expanded=True):
            engine.forward_chain(st.session_state.mental_health_facts)
        
        st.success(f"Forward chaining concluded with: {list(engine.conclusions)}")
        st.session_state.mental_health_facts.update(engine.conclusions)
        st.session_state.page = "Mental Health Chatbot_Backward" # Transition to backward chaining page

elif st.session_state.page == "Mental Health Chatbot_Backward":
    st.title("Mental Health Support Chatbot")
    st.markdown("""
    **Step 2: Backward Chaining**
    Now, the bot will use backward chaining to recommend a specific course of action based on the facts we've gathered.
    """)
    st.markdown("---")
    
    mental_rules = {
        'suggest_therapy': ['feeling_sad', 'feeling_anxious'],
        'suggest_mindfulness': ['feeling_overwhelmed'],
        'suggest_break': ['feeling_tired', 'feeling_stressed'],
        'feeling_distressed': ['feeling_sad', 'feeling_anxious', 'feeling_overwhelmed']
    }
    
    mental_goals = ['suggest_therapy', 'suggest_mindfulness', 'suggest_break']
    
    engine = InferenceEngine(mental_rules)
    engine.facts.update(st.session_state.mental_health_facts)

    found_recommendation = False
    with st.expander("Show Chaining Process", expanded=True):
        st.subheader("Backward Chaining in Action")
        for goal in mental_goals:
            # Check if the goal is supported by the facts we already have
            if engine.backward_chain(goal, 'mental', st.session_state.questions_to_ask, st.session_state.answers['mental']):
                if goal == 'suggest_therapy':
                    st.success("Recommendation: Based on your feelings, we recommend considering **therapy**.")
                elif goal == 'suggest_mindfulness':
                    st.success("Recommendation: It sounds like **mindfulness exercises** could be helpful.")
                elif goal == 'suggest_break':
                    st.success("Recommendation: Taking a short **break** can be very beneficial.")
                found_recommendation = True
                break

    if not found_recommendation:
        st.info("Based on the initial facts, no specific recommendation could be made yet.")

    # --- UI elements for a better visual experience ---
    st.markdown("---")
    st.subheader("Your Personal Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Known Facts", len(st.session_state.mental_health_facts))
    with col2:
        st.metric("Total Rules", len(mental_rules))
        
    st.snow()
    
    if st.button("Start Over", key='start_over_backward'):
        st.session_state.clear()
        st.experimental_rerun()
