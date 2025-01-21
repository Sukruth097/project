tables_summarizer_prompt = """
Table: {table_content}
Analyze the table provided and summarize its content comprehensively and concisely. 
Ensure the summary captures all key details, trends, and relationships within the data, 
providing a clear understanding of the context and insights. Avoid omitting any relevant 
information while maintaining precision in your response.
"""

image_summarizer_prompt = """
Analyze the given image and provide a concise and comprehensive summary of its content. 
Clearly describe the key elements, context, and any significant details or patterns observed, 
ensuring no relevant information is omitted while maintaining precision in your response.
Image: {image_element}
Limit your description to 3-4 sentences, ensuring it's precise and informative
"""
