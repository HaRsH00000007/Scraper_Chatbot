# Scraper_Chatbot

Web Scraper Chatbot Platform

Overview

This project is a web scraper chatbot platform inspired by Elephant.ai. It allows users to input a website link, scrape data from the provided website, and interact with the scraped content using a chatbot. The chatbot leverages the Mixtral-8x7b-32768 model to provide coherent and contextually relevant responses.

Features

-> Web Scraping: Extracts raw data from dynamic and static websites.

-> Data Preprocessing: Cleans and structures the scraped data to ensure accuracy and relevancy.

-> Text Embeddings: Converts preprocessed data into semantic embeddings using Hugging Face models.

-> Vector Database Storage: Stores embeddings in a vector store (Pinecone/FAISS) for efficient retrieval.

-> LLM-Powered Chatbot: Uses Mixtral-8x7b-32768 to generate responses based on user queries and the retrieved data.

-> Embeddable Widget: Provides an integration code snippet for embedding the chatbot on any website.

Workflow

-> Scrape Data: Collect raw data from the provided web links.

-> Preprocess Data: Clean, structure, and prepare the data for embedding.

-> Convert to Embeddings: Generate semantic vector representations of the data using Hugging Face models.

-> Store in Vector Database: Save embeddings in a vector database like Pinecone or FAISS.

-> Use Llama for Responses: Retrieve relevant embeddings and generate chatbot responses with Mixtral-8x7b-32768.


Model Details

Name: Mixtral-8x7b-32768

Capabilities: Advanced text generation and context-based responses.

Usage: Integrated for generating chatbot responses based on retrieved embeddings.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

Contact

Author: Harsh Singh

Email: harshsingh26603@gmail.com

GitHub: HaRsH00000007
