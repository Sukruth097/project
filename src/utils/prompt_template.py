tables_summarizer_prompt = """
Table: {table_content}
Analyze the table provided and summarize its content comprehensively and concisely. 
Ensure the summary captures all key details, trends, and relationships within the data, 
providing a clear understanding of the context and insights. Avoid omitting any relevant 
information while maintaining precision in your response.Avoid bullet points.
"""

images_summarizer_prompt = """
You are an advanced assistant specializing in image summarization also avoid the bullet points.
Your task is to provide precise, accurate,
and concise descriptions of the image without any hallucination.
Do not exceed more than 2-3 snetences.
 
Summary:
"""
