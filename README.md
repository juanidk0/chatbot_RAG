# ColumbusAI Chatbot RAG System

A sophisticated AI chatbot system built with LangChain and FastAPI that provides intelligent responses about ColumbusAI Solutions company data using Retrieval-Augmented Generation (RAG) architecture.

## 🚀 Features

- **RAG-powered responses**: Combines company knowledge with web search capabilities
- **Persistent conversation memory**: Maintains context across conversations
- **Dual interface**: Both REST API and Streamlit web interface
- **Company knowledge base**: Pre-loaded with company information, employee data, and product details
- **Web search integration**: Uses DuckDuckGo for external information retrieval
- **Vector database**: ChromaDB for efficient document storage and retrieval

## 🏗️ Architecture

The system consists of three main components:

### 1. Agent (`agent.py`)
- **LangChain Agent**: Core AI agent with OpenAI tools integration
- **RAG Chain**: Retrieval-Augmented Generation for company knowledge
- **Memory System**: Conversation buffer memory for context retention
- **Tools Integration**: 
  - CompanyKnowledge tool for internal data retrieval
  - WebSearch tool for external information
- **Vector Store**: ChromaDB with OpenAI embeddings

### 2. API Service (`api.py`)
- **FastAPI Server**: RESTful API with CORS middleware
- **Endpoints**:
  - `GET /`: Health check endpoint
  - `POST /chat`: Main chat endpoint accepting JSON queries
- **Response Format**: JSON with agent responses

### 3. Web Interface (`ui.py`)
- **Streamlit Application**: User-friendly chat interface
- **Features**:
  - Real-time chat with message history
  - ChatGPT-style message bubbles
  - Session state management
  - Responsive design with custom CSS styling

## 📋 Prerequisites
- Python 3.8+
- OpenAI API key
- Required Python packages (see Installation)
- *See requirements.txt for detailed package versions*

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/juanidk0/chatbot_RAG.git
   cd chatbot_RAG
   ```

2. **Install dependencies**:
   ```bash
    pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-5-nano  # or your preferred model
   CHROMA_PATH=company_db
   ```

## 🚀 Usage

### Option 1: FastAPI Server

1. **Start the API server**:
   ```bash
   uvicorn api:app --reload
   ```

2. **Test the API**:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "Tell me about ColumbusAI Solutions"}'
   ```

### Option 2: Streamlit Web Interface

1. **Launch the web interface**:
   ```bash
   streamlit run ui.py
   ```

2. **Access the interface**: Open your browser to `http://localhost:8501`

## 📊 Data Structure

The system uses a ChromaDB vector database located in the `company_db/` directory containing:

- **Company Information**: Business overview, history, and strategy
- **Employee Data**: Staff profiles and roles
- **Product Catalog**: Detailed product specifications and use cases

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-5-nano` |
| `CHROMA_PATH` | Path to ChromaDB database | `company_db` |

### Agent Configuration

The agent is configured with:
- **Max iterations**: 5
- **Verbose mode**: Enabled for debugging
- **Error handling**: Graceful parsing error management
- **Memory**: Conversation buffer with message history

## 🤖 Agent Capabilities

The ColumbusAI agent can:

1. **Answer company-specific questions** using internal knowledge base
2. **Perform web searches** for external information
3. **Maintain conversation context** across multiple interactions
4. **Handle complex queries** requiring both internal and external data
5. **Reset conversation history** with the 'reset' command

## 📝 API Reference

### POST /chat

**Request Body**:
```json
{
  "query": "Your question here"
}
```

**Response**:
```json
{
  "response": "Agent's response here"
}
```

### GET /

**Response**:
```json
{
  "status": "ok",
  "message": "LangChain Agent API ready 🚀"
}
```

## 🎯 Use Cases

- **Employee onboarding**: Get information about company structure and products
- **Customer support**: Answer questions about ColumbusAI's offerings
- **Internal knowledge sharing**: Quick access to company information
- **Strategic planning**: Combine internal data with market research

## 🔒 Security Considerations

- API keys should be stored securely in environment variables
- Consider implementing authentication for production use
- CORS settings should be restricted in production environments
- Vector database access should be properly secured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support or questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for troubleshooting tips

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Multi-language support
- [ ] Advanced analytics and conversation insights
- [ ] Integration with more external data sources
- [ ] Enhanced UI/UX improvements
- [ ] Docker containerization
- [ ] Production deployment guides