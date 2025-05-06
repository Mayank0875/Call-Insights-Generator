separation_prompt_template = """
You are an expert at separating and analyzing transcripts of sales calls. It's very crucial for the company, so ensure the output is accurate.

Given the following call transcript, identify who is the **Sales Agent** and who is the **Customer**, and separate their dialogue accordingly.

Format:
Agent: <agent's dialogue>
Customer: <customer's dialogue>

Example Input:
Transcript: Hi, I’m calling to ask about your plans. Sure! I’d be happy to help you with that.

Output:
Customer: Hi, I’m calling to ask about your plans.
Agent: Sure! I’d be happy to help you with that.

Transcript: {transcript}
Separated dialogue:
"""


summary_prompt_template = """
You are highly skilled at summarizing and analyzing structured sales call dialogues. This task is important for understanding customer behavior, improving sales strategies, and capturing valuable insights.

Your job is to:
1. Identify key discussion points
2. Extract customer objections (if any)
3. Understand the customer’s needs or pain points
4. Note any product features discussed
5. Capture commitments made by the agent or the customer

Please provide your analysis in a clear and structured format.

Example:
Sales call:
Agent: Hello! Thanks for calling. How can I help you today?
Customer: I’ve been having trouble with my internet connection.
Agent: I’m sorry to hear that. Are you experiencing slow speeds or complete disconnections?
Customer: Mostly disconnections during video calls.
Agent: Understood. We have a new router model that stabilizes connectivity during high-usage periods. Would you like to try it out?
Customer: Yes, but I’m concerned about installation charges.
Agent: We’re offering free installation this week. Shall I schedule it for tomorrow?
Customer: That would be great.

Structured Analysis:
1. **Key Discussion Points**:
   - Internet connectivity issues
   - Product recommendation (new router)
   - Offer details (free installation)

2. **Customer Objections**:
   - Concern about installation charges

3. **Customer Needs/Pain Points**:
   - Frequent disconnections during video calls

4. **Product Features Discussed**:
   - Router improves stability during high-usage periods

5. **Commitments Made**:
   - Agent offers free installation
   - Customer agrees to schedule installation

Now, analyze the following structured dialogue:
Sales call:
{structured_dialogue}

Structured Analysis:
"""


performance_prompt_template = """
You are excellent at evaluating sales agent performance based on structured sales call dialogues. This evaluation is **crucial** for identifying strengths and improvement areas, ensuring sales effectiveness, and delivering training insights.

Your task is to assess the agent's performance across the following seven core dimensions:
- **Opening (1-10)**: How well did the agent establish rapport and set the agenda?
- **Discovery (1-10)**: How effectively did they uncover customer needs?
- **Presentation (1-10)**: How clearly did they articulate value propositions?
- **Objection handling (1-10)**: How well did they address concerns?
- **Closing (1-10)**: How effectively did they advance the sale?
- **Tone and rapport (1-10)**: How was their overall communication style?
- **Active listening (1-10)**: Did they understand and respond to customer needs?

For each dimension, provide:
1. A **numerical score** (1–10)
2. A **brief explanation** with specific examples from the dialogue
3. **One actionable improvement suggestion**

---

**Example**  
Sales call:  
Agent: Hi there! Thanks for reaching out to us—how can I assist you today?  
Customer: I’m considering switching to your service, but I need to understand the costs.  
Agent: Absolutely, I’d be happy to walk you through our pricing and plans. Can I ask what you're currently using and what you’re hoping to improve?  
Customer: My current provider charges a lot for poor service.  
Agent: That’s frustrating. Our standard plan is $49/month with 24/7 support and 99.9% uptime.  
Customer: Sounds good, but I’m not sure about switching right away.  
Agent: I understand. We also offer a 30-day money-back guarantee, so you can try risk-free. Would you like to get started?

**Sales Performance Evaluation**:  
- **Opening (8/10)**: Friendly tone and clear intent to help. Could have introduced themselves by name.  
  - *Improvement:* Start with a self-introduction to build more trust.

- **Discovery (7/10)**: Asked about current service and expectations.  
  - *Improvement:* Probe deeper into pain points (e.g., frequency or type of poor service).

- **Presentation (8/10)**: Explained value props like 24/7 support and uptime.  
  - *Improvement:* Mention more unique differentiators to stand out.

- **Objection handling (9/10)**: Proactively offered a risk-free trial.  
  - *Improvement:* Ask what’s holding the customer back to tailor the response better.

- **Closing (8/10)**: Tried to close with a clear call-to-action.  
  - *Improvement:* Use urgency or additional incentives to prompt faster decision.

- **Tone and rapport (9/10)**: Friendly, understanding, and professional throughout.  
  - *Improvement:* Use the customer’s name to create a more personal touch.

- **Active listening (8/10)**: Addressed customer's main concern, but didn’t explore all comments deeply.  
  - *Improvement:* Reflect back customer statements to show full understanding.

---

Now, assess the following sales call:  
Sales call:  
{structured_dialogue}

Sales Performance Evaluation:
"""
