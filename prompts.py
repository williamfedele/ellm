explainer = """
You are tasked with explaining a piece of code to someone who may not be familiar with its functionality or purpose. Your goal is to provide a clear, concise, and comprehensive explanation of the code's structure, purpose, and functionality.

Here is the code you need to explain:

<code>
{{CODE}}
</code>

To explain this code effectively, follow these steps:

1. First, identify the programming language used in the code. This will help set the context for your explanation.

2. Provide a brief overview of what the code does at a high level. What is its main purpose or function?

3. Break down the code into logical sections or components. This could be by functions, classes, or major code blocks.

4. For each section or component:
   a. Explain its purpose within the overall code.
   b. Describe how it works, including any important algorithms or data structures used.
   c. Highlight any notable programming techniques or patterns employed.

5. Identify and explain any important variables, functions, or classes and their roles in the code.

6. If there are any complex or unusual parts of the code, provide a more detailed explanation of how they work and why they're implemented that way.

7. Mention any external libraries or dependencies the code relies on and briefly explain their purpose.

8. If applicable, discuss the code's efficiency, potential improvements, or alternative approaches that could be used.

Remember to be thorough in your explanation, but also try to be concise and clear. Use simple language where possible, and explain any technical terms you need to use.

Present your explanation within <explanation> tags. You may use additional nested tags to structure your response, such as <overview>, <components>, <details>, and <summary> if you find them helpful in organizing your explanation.

Begin your explanation now.
"""

optimizer = """
You are tasked with optimizing a piece of code. Your goal is to improve its efficiency, readability, and overall performance without changing its core functionality. Here's the code you need to optimize:

<code>
{{CODE}}
</code>

To optimize this code, follow these steps:

1. Analyze the code:
   - Identify any inefficient algorithms or data structures
   - Look for redundant operations or unnecessary computations
   - Check for any potential performance bottlenecks

2. Consider the following optimization techniques:
   - Improve algorithm efficiency (e.g., use more efficient sorting or searching algorithms)
   - Optimize data structures (e.g., use more appropriate containers)
   - Reduce time complexity and space complexity where possible
   - Eliminate redundant computations or unnecessary operations
   - Improve memory usage and management
   - Enhance readability and maintainability

3. Implement the optimizations:
   - Make changes to the code based on your analysis
   - Ensure that the core functionality remains unchanged
   - Add comments to explain significant changes or complex optimizations

4. Provide the optimized code:
   - Present the optimized version of the code

5. Explain the optimizations:
   - Describe the changes you made and why
   - Highlight the expected improvements in performance or efficiency

Format your response as follows:

<optimized_code>
[Insert the optimized code here]
</optimized_code>

<optimization_explanation>
[Provide a detailed explanation of the optimizations made, including:
- What changes were implemented
- Why these changes improve the code
- Expected benefits in terms of performance, readability, or efficiency]
</optimization_explanation>

Remember to maintain the original functionality of the code while improving its efficiency and readability. If you believe the original code is already optimal or if there are no significant optimizations possible, explain why in the optimization explanation.
"""
