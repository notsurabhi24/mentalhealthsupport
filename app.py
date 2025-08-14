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
        .st-emotion-cache-1j43d5x h1, .st-emotion-cache-1j43d5x h2, .st-emotion-cache-1j43d5x h3 {
            color: #333366;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
    st.title("AI Reasoning: An Exploration of Chaining 💡")
    st.header("Welcome to the Inference Engine Demo")
    add_mood_elements()
    st.image("https://placehold.co/800x400/FFD700/000000?text=AI+Inference+Illustration", use_column_width=True)
    st.markdown("""
        This application provides an interactive platform to understand and apply two fundamental AI reasoning techniques: **Forward Chaining** and **Backward Chaining**. These methods form the basis of rule-based expert systems and are crucial for developing intelligent agents.

        - **Forward Chaining:** A data-driven approach that infers new conclusions from a set of known facts.
        - **Backward Chaining:** A goal-driven approach that works backward from a desired conclusion to find the necessary facts.

        Use the sidebar to explore the dedicated pages for each concept and interact with the demonstration applications.
        """)

def forward_chaining_page():
    st.title("🚀 Forward Chaining: The Deductive Process")
    st.header("A Data-Driven Approach")
    st.markdown("""
    Forward chaining begins with an initial set of facts and iteratively applies rules to deduce new facts until a desired conclusion is reached or no new facts can be inferred. This is a **bottom-up** approach, starting from the known data.

    **Structure of a Rule-Based System:**
    - **Facts:** Known pieces of information.
    - **Rules:** Logical statements in the form `IF [Premise] THEN [Conclusion]`.
    - **Inference Engine:** The mechanism that applies rules to facts.

    Let's demonstrate with a basic mental health inference scenario.
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
    st.subheader("Initial Facts (Symptoms):")
    
    if st.checkbox("I feel tired. 😴", key='tired_fact'):
        initial_facts.append('feeling_tired')
    if st.checkbox("I feel sad. 😢", key='sad_fact'):
        initial_facts.append('feeling_sad')
    if st.checkbox("I feel overwhelmed. 🤯", key='overwhelmed_fact'):
        initial_facts.append('feeling_overwhelmed')

    if st.button("Start Inference", key='start_forward'):
        engine = SimpleEngine(mental_rules)
        engine.facts.update(initial_facts)
        
        st.write("---")
        st.subheader("🕵️ Forward Chaining Execution:")

        inferred_new = True
        while inferred_new:
            inferred_new = False
            for conclusion, premises in mental_rules.items():
                if set(premises).issubset(engine.facts) and conclusion not in engine.facts:
                    st.success(f"**Rule Fired!** Premise(s) {', '.join(premises)} satisfied. New conclusion inferred: **{conclusion.replace('_', ' ')}** 🎉")
                    engine.facts.add(conclusion)
                    inferred_new = True
                    time.sleep(0.5)
        
        st.markdown("---")
        st.success(f"**Final Inferences:** {', '.join(engine.facts - set(initial_facts))}")

def backward_chaining_page():
    st.title("🎯 Backward Chaining: The Goal-Driven Process")
    st.header("A Top-Down Approach")
    st.markdown("""
    Backward chaining starts with a specific goal and attempts to prove it by working backward through a set of rules. This **top-down** approach breaks down the main goal into sub-goals, recursively checking if these sub-goals can be proven by facts or other rules.

    **Algorithm Flow:**
    1.  Start with a Goal.
    2.  Find a rule whose conclusion matches the Goal.
    3.  Treat the rule's premises as new Sub-goals.
    4.  Recursively attempt to prove each Sub-goal.
    5.  If a Sub-goal is a known fact, it is proven.
    6.  If a Sub-goal cannot be proven by rules or facts, query the user for the information.

    Let's test this with a mental health recommendation system.
    """)
    
    add_mood_elements()

    mental_rules = {
        'suggest_therapy': ['feeling_sad', 'feeling_anxious'],
        'suggest_mindfulness': ['feeling_overwhelmed'],
        'suggest_break': ['feeling_tired']
    }

    mental_goals = ['suggest_therapy', 'suggest_mindfulness', 'suggest_break']

    st.markdown("---")
    st.subheader("Select a Goal to Prove:")
    goal_to_prove = st.selectbox("Hypothesis:", mental_goals)
    
    st.markdown("---")
    st.subheader("Premise Evaluation:")

    # State for tracking questions and answers
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = {}
    if 'backward_run' not in st.session_state:
        st.session_state.backward_run = False

    def backward_chain_demo(goal, facts, indent=""):
        if goal in facts:
            st.write(f"{indent}✅ **Known Fact:** '{goal}' is true.")
            return True

        if goal in st.session_state.questions_asked:
             st.write(f"{indent}🤔 **Cached:** Premise '{goal}' has already been evaluated.")
             return st.session_state.questions_asked[goal]

        for conclusion, premises in mental_rules.items():
            if conclusion == goal:
                st.write(f"{indent}🔍 **Evaluating Rule:** To prove `{goal.replace('_', ' ')}`, we need to prove premises: {', '.join(premises)}")
                time.sleep(0.5)
                all_premises_true = True
                for premise in premises:
                    if not backward_chain_demo(premise, facts, indent + "    "):
                        all_premises_true = False
                        break
                if all_premises_true:
                    st.success(f"{indent}🎉 **Goal Proven!** All premises for `{goal.replace('_', ' ')}` were satisfied. Final recommendation: **{goal.replace('_', ' ')}**")
                    return True
        
        # If we reach here, the goal is a question for the user
        st.write(f"{indent}❓ **Querying User:** Premise `{goal}` is not in our knowledge base. We must ask the user.")
        st.session_state.questions_asked[goal] = st.checkbox(f"Are you **{goal.replace('_', ' ')}**?", key=f'question_{goal}')
        time.sleep(0.5)
        return st.session_state.questions_asked[goal]


    if st.button("Start Goal Evaluation", key='start_backward'):
        st.write("---")
        st.session_state.questions_asked = {} # Reset questions
        st.session_state.backward_run = True # Set the flag to true
        st.subheader("🎯 Goal Evaluation Process:")
        
        backward_chain_demo(goal_to_prove, set())
        
        st.markdown("---")
        
        if any(st.session_state.questions_asked.values()):
            st.success("The goal was either proven by known facts or supported by your response.")
        else:
            st.warning("The goal could not be proven based on the provided information.")

def chatbot_page():
    st.title("Mental Health Chatbot 💬")
    st.header("An Interactive Conversational Agent")
    add_mood_elements()
    st.markdown("""
        This chatbot uses **backward chaining** in a conversational context. Its goal is to make a recommendation, and it will ask you questions to gather the necessary facts to achieve that goal.
    """)
    st.markdown("---")

    # Define mental health rules for the chatbot
    mental_rules = {
        'suggest_therapy': ['feeling_sad', 'feeling_anxious'],
        'suggest_mindfulness': ['feeling_overwhelmed'],
        'suggest_break': ['feeling_tired']
    }

    # Initialize chat history and state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm here to listen. How are you feeling today?"}]
    if "current_goal" not in st.session_state:
        st.session_state.current_goal = None
    if "known_facts" not in st.session_state:
        st.session_state.known_facts = set()

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Main chatbot logic using backward chaining
    def run_chatbot_logic(rules, facts, goal):
        for conclusion, premises in rules.items():
            if conclusion == goal:
                # Check if all premises are in our known facts
                missing_premises = [p for p in premises if p not in facts]
                if not missing_premises:
                    st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Success!** Based on your input, I've concluded you {goal.replace('_', ' ')}."})
                    return True, goal
                else:
                    # Ask the first missing premise as a question
                    question = f"Are you feeling **{missing_premises[0].replace('feeling_', '')}**?"
                    st.session_state.messages.append({"role": "assistant", "content": question})
                    st.session_state.current_goal = (goal, missing_premises[0]) # Store the current state
                    return False, None
        return False, None

    # Get user input
    if prompt := st.chat_input("I am feeling..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Check if we were expecting an answer
        if st.session_state.current_goal:
            goal, question_premise = st.session_state.current_goal
            # Assume a positive response for simplicity
            if "yes" in prompt.lower() or "i am" in prompt.lower() or "feeling" in prompt.lower():
                st.session_state.known_facts.add(question_premise)
                st.session_state.messages.append({"role": "assistant", "content": f"Okay, I've noted that you are '{question_premise.replace('_', ' ')}'."})
            
            # Reset goal and continue logic
            st.session_state.current_goal = None
        
        # Start a new chaining process
        is_proven = False
        for goal in mental_rules.keys():
            is_proven, recommendation = run_chatbot_logic(mental_rules, st.session_state.known_facts, goal)
            if is_proven:
                break
        
        # If no recommendation was found, provide a default response
        if st.session_state.current_goal is None and not is_proven:
            st.session_state.messages.append({"role": "assistant", "content": "Thank you for sharing. How else are you feeling?"})

def flow_diagram_page():
    st.title("Chaining Logic: A Visual Guide 🧠")
    st.header("Visualizing the Inference Process")
    add_mood_elements()
    st.markdown("""
        Understanding the flow of a reasoning engine is key to developing robust AI systems. Here's a structured visualization of the algorithms.
        """)
    
    st.subheader("Forward Chaining Flow")
    st.markdown("""
    Forward chaining is a **data-driven** process. We start with a set of facts and fire rules to deduce new facts.
    """)
    st.info("""
    **[ Start ]**
    
    _↓ Initial Facts_
    
    **[ Loop ]**
    
    _↓ Check all rules_
    
    **[ Rule Match? ]**
    
    _↓ If a rule's premises are all known facts_
    
    **[ Fire Rule ]**
    
    _↓ Infer a new conclusion and add it to facts_
    
    **[ New Fact? ]**
    
    _↓ If a new fact was inferred, repeat the loop_
    
    **[ End ]**
    
    _↓ No new facts can be inferred_
    
    **[ Final Conclusions ]**
    """)
    
    st.subheader("Backward Chaining Flow")
    st.markdown("""
    Backward chaining is a **goal-driven** process. We start with a goal and work backwards to find evidence.
    """)
    st.success("""
    **[ Start ]**
    
    _↓ Initial Goal_
    
    **[ Find Rule ]**
    
    _↓ Find a rule with the Goal as its conclusion_
    
    **[ Premise Check ]**
    
    _↓ Treat the rule's premises as new Sub-goals_
    
    **[ Sub-goal Evaluation ]**
    
    _↓ Recursively prove each Sub-goal_
    
    **[ Is it a Fact? ]**
    
    _↓ If yes, Sub-goal is proven_
    
    **[ Is it a New Sub-goal? ]**
    
    _↓ If yes, recursively check for rules_
    
    **[ Ask User ]**
    
    _↓ If no, query the user for the fact_
    
    **[ End ]**
    
    _↓ All premises for the initial Goal are proven_
    
    **[ Goal Proven ]**
    """)


# --- Main App Logic ---
st.sidebar.title("AI Chaining App")
page = st.sidebar.radio("Choose a Page", ["Home", "Forward Chaining", "Backward Chaining", "Chaining Flow Diagram", "Mental Health Chatbot"])

if page == "Home":
    home_page()
elif page == "Forward Chaining":
    forward_chaining_page()
elif page == "Backward Chaining":
    backward_chaining_page()
elif page == "Chaining Flow Diagram":
    flow_diagram_page()
elif page == "Mental Health Chatbot":
    chatbot_page()
